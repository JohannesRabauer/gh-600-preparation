"""HTTP scraper utility with rate limiting, retry logic, and error handling.

Provides an async HTTP client for fetching web pages from Microsoft Learn
and GitHub documentation domains, with concurrency control, per-domain
rate limiting, and structured error logging.
"""

from __future__ import annotations

import asyncio
import time
from urllib.parse import urlparse

import httpx
from bs4 import BeautifulSoup

from src.config import (
    MAX_CONCURRENT_REQUESTS,
    MAX_RETRIES,
    REQUEST_DELAY_SECONDS,
    REQUEST_TIMEOUT_SECONDS,
)


class Scraper:
    """Async HTTP scraper with rate limiting and retry logic.

    Supports async context manager usage:
        async with Scraper() as scraper:
            content, error = await scraper.fetch(url)

    Features:
    - Limits concurrent requests via asyncio.Semaphore (default: 5)
    - Per-domain rate limiting: minimum 1s between requests to same domain
    - Retry on timeout: 1 retry with the configured timeout
    - Exponential backoff on HTTP 429 (Too Many Requests)
    - Structured error logging with URL, error message, and referrer
    """

    def __init__(
        self,
        max_concurrent: int = MAX_CONCURRENT_REQUESTS,
        delay_seconds: float = REQUEST_DELAY_SECONDS,
        timeout_seconds: float = REQUEST_TIMEOUT_SECONDS,
        max_retries: int = MAX_RETRIES,
    ) -> None:
        self._max_concurrent = max_concurrent
        self._delay_seconds = delay_seconds
        self._timeout_seconds = timeout_seconds
        self._max_retries = max_retries

        self._semaphore = asyncio.Semaphore(max_concurrent)
        self._domain_last_request: dict[str, float] = {}
        self._domain_locks: dict[str, asyncio.Lock] = {}
        self._error_log: list[dict[str, str]] = []
        self._client: httpx.AsyncClient | None = None

    @property
    def error_log(self) -> list[dict[str, str]]:
        """Access the accumulated error log entries."""
        return self._error_log

    async def __aenter__(self) -> Scraper:
        self._client = httpx.AsyncClient(
            timeout=httpx.Timeout(self._timeout_seconds),
            follow_redirects=True,
            headers={
                "User-Agent": "GH600-ExamPrep/1.0 (educational scraper)",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            },
        )
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:  # noqa: ANN001
        if self._client:
            await self._client.aclose()
            self._client = None

    def _get_domain(self, url: str) -> str:
        """Extract domain from URL."""
        return urlparse(url).netloc.lower()

    def _get_domain_lock(self, domain: str) -> asyncio.Lock:
        """Get or create a lock for the given domain."""
        if domain not in self._domain_locks:
            self._domain_locks[domain] = asyncio.Lock()
        return self._domain_locks[domain]

    async def _enforce_rate_limit(self, domain: str) -> None:
        """Enforce per-domain rate limiting (minimum delay between requests)."""
        lock = self._get_domain_lock(domain)
        async with lock:
            now = time.monotonic()
            last_request = self._domain_last_request.get(domain, 0.0)
            elapsed = now - last_request
            if elapsed < self._delay_seconds:
                await asyncio.sleep(self._delay_seconds - elapsed)
            self._domain_last_request[domain] = time.monotonic()

    def _log_error(self, url: str, error: str, referrer: str) -> None:
        """Log an inaccessible resource."""
        self._error_log.append({
            "url": url,
            "error": error,
            "referrer": referrer,
        })

    async def fetch(self, url: str, referrer: str = "") -> tuple[str, str | None]:
        """Fetch a URL and return its content.

        Args:
            url: The URL to fetch.
            referrer: The referring URL (for error logging).

        Returns:
            A tuple of (html_content, error). On success, error is None.
            On failure, content is empty string and error contains the message.
        """
        if not self._client:
            raise RuntimeError(
                "Scraper must be used as async context manager: "
                "async with Scraper() as scraper:"
            )

        domain = self._get_domain(url)

        async with self._semaphore:
            return await self._fetch_with_retry(url, domain, referrer)

    async def _fetch_with_retry(
        self, url: str, domain: str, referrer: str
    ) -> tuple[str, str | None]:
        """Fetch with retry on timeout and exponential backoff on 429."""
        attempts = 0
        max_attempts = 1 + self._max_retries  # Initial attempt + retries

        while attempts < max_attempts:
            await self._enforce_rate_limit(domain)

            try:
                response = await self._client.get(url)  # type: ignore[union-attr]

                if response.status_code == 429:
                    # Exponential backoff for rate limiting
                    backoff = 2**attempts * self._delay_seconds
                    await asyncio.sleep(backoff)
                    attempts += 1
                    continue

                if response.status_code >= 400:
                    error_msg = f"HTTP {response.status_code}"
                    self._log_error(url, error_msg, referrer)
                    return "", error_msg

                return response.text, None

            except httpx.TimeoutException:
                attempts += 1
                if attempts >= max_attempts:
                    error_msg = f"Timeout after {self._timeout_seconds}s ({attempts} attempts)"
                    self._log_error(url, error_msg, referrer)
                    return "", error_msg
                # Retry on timeout - loop continues

            except httpx.HTTPError as exc:
                error_msg = f"{type(exc).__name__}: {exc}"
                self._log_error(url, error_msg, referrer)
                return "", error_msg

        # Should not reach here, but handle edge case
        error_msg = f"Max retries ({self._max_retries}) exceeded"
        self._log_error(url, error_msg, referrer)
        return "", error_msg


def extract_text(html: str) -> str:
    """Extract readable text content from HTML.

    Strips navigation, scripts, styles, and other non-content elements.

    Args:
        html: Raw HTML string.

    Returns:
        Cleaned text content.
    """
    soup = BeautifulSoup(html, "html.parser")

    # Remove non-content elements
    for tag in soup(["script", "style", "nav", "header", "footer", "aside"]):
        tag.decompose()

    # Get text with whitespace normalization
    text = soup.get_text(separator="\n", strip=True)
    # Collapse multiple blank lines
    lines = [line.strip() for line in text.splitlines()]
    return "\n".join(line for line in lines if line)


def extract_links(html: str, base_url: str) -> list[str]:
    """Extract absolute URLs from HTML anchor tags.

    Resolves relative URLs against the base URL. Filters out
    fragment-only links and non-HTTP schemes.

    Args:
        html: Raw HTML string.
        base_url: The URL the HTML was fetched from (for resolving relative links).

    Returns:
        List of absolute URLs found in the document.
    """
    from urllib.parse import urljoin

    soup = BeautifulSoup(html, "html.parser")
    links: list[str] = []

    for anchor in soup.find_all("a", href=True):
        href = anchor["href"].strip()

        # Skip empty, fragment-only, and javascript links
        if not href or href.startswith("#") or href.startswith("javascript:"):
            continue

        # Resolve relative URLs
        absolute_url = urljoin(base_url, href)

        # Only include HTTP(S) links
        parsed = urlparse(absolute_url)
        if parsed.scheme in ("http", "https"):
            # Strip fragments from the URL
            clean_url = f"{parsed.scheme}://{parsed.netloc}{parsed.path}"
            if parsed.query:
                clean_url += f"?{parsed.query}"
            links.append(clean_url)

    return links
