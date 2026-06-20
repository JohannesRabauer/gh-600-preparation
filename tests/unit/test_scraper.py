"""Unit tests for the HTTP scraper utility.

Tests cover rate limiting behavior, retry logic, error logging,
and HTML parsing helpers.
"""

from __future__ import annotations

import asyncio
import time

import httpx
import pytest

from src.utils.scraper import Scraper, extract_links, extract_text


# === Scraper Context Manager Tests ===


@pytest.mark.asyncio
async def test_scraper_context_manager():
    """Scraper opens and closes httpx client properly."""
    async with Scraper() as scraper:
        assert scraper._client is not None
    assert scraper._client is None


@pytest.mark.asyncio
async def test_scraper_raises_without_context_manager():
    """Scraper raises RuntimeError if used without async with."""
    scraper = Scraper()
    with pytest.raises(RuntimeError, match="async context manager"):
        await scraper.fetch("https://example.com")


# === Successful Fetch Tests ===


@pytest.mark.asyncio
async def test_fetch_success(httpx_mock):
    """Successful fetch returns content and no error."""
    httpx_mock.add_response(
        url="https://learn.microsoft.com/page1",
        text="<html><body>Hello</body></html>",
    )

    async with Scraper() as scraper:
        content, error = await scraper.fetch("https://learn.microsoft.com/page1")

    assert error is None
    assert "Hello" in content
    assert scraper.error_log == []


# === Error Handling Tests ===


@pytest.mark.asyncio
async def test_fetch_http_404_logs_error(httpx_mock):
    """HTTP 404 is logged with URL, error, and referrer."""
    httpx_mock.add_response(
        url="https://learn.microsoft.com/missing",
        status_code=404,
    )

    async with Scraper() as scraper:
        content, error = await scraper.fetch(
            "https://learn.microsoft.com/missing",
            referrer="https://learn.microsoft.com/parent",
        )

    assert content == ""
    assert error == "HTTP 404"
    assert len(scraper.error_log) == 1
    assert scraper.error_log[0] == {
        "url": "https://learn.microsoft.com/missing",
        "error": "HTTP 404",
        "referrer": "https://learn.microsoft.com/parent",
    }


@pytest.mark.asyncio
async def test_fetch_http_500_logs_error(httpx_mock):
    """HTTP 500 is logged as error."""
    httpx_mock.add_response(
        url="https://docs.github.com/error",
        status_code=500,
    )

    async with Scraper() as scraper:
        content, error = await scraper.fetch(
            "https://docs.github.com/error",
            referrer="https://docs.github.com/home",
        )

    assert content == ""
    assert error == "HTTP 500"
    assert len(scraper.error_log) == 1


@pytest.mark.asyncio
async def test_fetch_connection_error_logs_error(httpx_mock):
    """Connection errors are caught and logged."""
    httpx_mock.add_exception(
        httpx.ConnectError("Connection refused"),
        url="https://learn.microsoft.com/down",
    )

    async with Scraper() as scraper:
        content, error = await scraper.fetch(
            "https://learn.microsoft.com/down",
            referrer="https://learn.microsoft.com/root",
        )

    assert content == ""
    assert "ConnectError" in error
    assert len(scraper.error_log) == 1
    assert scraper.error_log[0]["referrer"] == "https://learn.microsoft.com/root"


# === Timeout and Retry Tests ===


@pytest.mark.asyncio
async def test_fetch_timeout_retries_once(httpx_mock):
    """On timeout, retries once then logs error."""
    httpx_mock.add_exception(
        httpx.ReadTimeout("Read timed out"),
        url="https://learn.microsoft.com/slow",
    )
    httpx_mock.add_exception(
        httpx.ReadTimeout("Read timed out"),
        url="https://learn.microsoft.com/slow",
    )

    async with Scraper(timeout_seconds=0.1, delay_seconds=0.01) as scraper:
        content, error = await scraper.fetch(
            "https://learn.microsoft.com/slow",
            referrer="https://learn.microsoft.com/parent",
        )

    assert content == ""
    assert "Timeout" in error
    assert "2 attempts" in error
    assert len(scraper.error_log) == 1


@pytest.mark.asyncio
async def test_fetch_timeout_then_success(httpx_mock):
    """On first timeout, retry succeeds."""
    httpx_mock.add_exception(
        httpx.ReadTimeout("Read timed out"),
        url="https://learn.microsoft.com/slow",
    )
    httpx_mock.add_response(
        url="https://learn.microsoft.com/slow",
        text="<html>Success after retry</html>",
    )

    async with Scraper(timeout_seconds=0.1, delay_seconds=0.01) as scraper:
        content, error = await scraper.fetch("https://learn.microsoft.com/slow")

    assert error is None
    assert "Success after retry" in content
    assert scraper.error_log == []


# === HTTP 429 Exponential Backoff Tests ===


@pytest.mark.asyncio
async def test_fetch_429_retries_with_backoff(httpx_mock):
    """HTTP 429 triggers exponential backoff and retry."""
    httpx_mock.add_response(
        url="https://learn.microsoft.com/rate-limited",
        status_code=429,
    )
    httpx_mock.add_response(
        url="https://learn.microsoft.com/rate-limited",
        text="<html>OK</html>",
        status_code=200,
    )

    async with Scraper(delay_seconds=0.01) as scraper:
        content, error = await scraper.fetch(
            "https://learn.microsoft.com/rate-limited"
        )

    assert error is None
    assert "OK" in content


@pytest.mark.asyncio
async def test_fetch_429_exhausts_retries(httpx_mock):
    """HTTP 429 on all attempts exhausts retries and logs error."""
    # With max_retries=1, we get 2 total attempts
    httpx_mock.add_response(
        url="https://learn.microsoft.com/always-429",
        status_code=429,
    )
    httpx_mock.add_response(
        url="https://learn.microsoft.com/always-429",
        status_code=429,
    )

    async with Scraper(delay_seconds=0.01, max_retries=1) as scraper:
        content, error = await scraper.fetch(
            "https://learn.microsoft.com/always-429",
            referrer="https://learn.microsoft.com/home",
        )

    assert content == ""
    assert error is not None
    assert len(scraper.error_log) == 1


# === Rate Limiting Tests ===


@pytest.mark.asyncio
async def test_per_domain_rate_limiting(httpx_mock):
    """Requests to the same domain are delayed by at least delay_seconds."""
    httpx_mock.add_response(
        url="https://learn.microsoft.com/page1",
        text="Page 1",
    )
    httpx_mock.add_response(
        url="https://learn.microsoft.com/page2",
        text="Page 2",
    )

    delay = 0.1  # Use 100ms for testability
    async with Scraper(delay_seconds=delay) as scraper:
        start = time.monotonic()
        await scraper.fetch("https://learn.microsoft.com/page1")
        await scraper.fetch("https://learn.microsoft.com/page2")
        elapsed = time.monotonic() - start

    # Should take at least one delay interval between the two requests
    assert elapsed >= delay


@pytest.mark.asyncio
async def test_different_domains_not_rate_limited(httpx_mock):
    """Requests to different domains are not mutually delayed."""
    httpx_mock.add_response(
        url="https://learn.microsoft.com/page",
        text="MS Page",
    )
    httpx_mock.add_response(
        url="https://docs.github.com/page",
        text="GH Page",
    )

    delay = 0.2
    async with Scraper(delay_seconds=delay) as scraper:
        start = time.monotonic()
        # Fetch from two different domains concurrently
        results = await asyncio.gather(
            scraper.fetch("https://learn.microsoft.com/page"),
            scraper.fetch("https://docs.github.com/page"),
        )
        elapsed = time.monotonic() - start

    # Both should succeed
    assert results[0][1] is None
    assert results[1][1] is None
    # Should be faster than 2x the delay (since different domains)
    assert elapsed < 2 * delay


@pytest.mark.asyncio
async def test_concurrency_limited_to_max():
    """No more than max_concurrent requests run simultaneously."""
    concurrent_count = 0
    max_observed = 0

    async def tracked_get(url, **kwargs):
        nonlocal concurrent_count, max_observed
        concurrent_count += 1
        max_observed = max(max_observed, concurrent_count)
        await asyncio.sleep(0.05)  # Simulate network delay
        concurrent_count -= 1
        return httpx.Response(200, text="OK")

    max_concurrent = 3
    async with Scraper(max_concurrent=max_concurrent, delay_seconds=0.0) as scraper:
        # Override the client.get to track concurrency
        import unittest.mock

        with unittest.mock.patch.object(
            scraper._client, "get", side_effect=tracked_get
        ):
            tasks = [
                scraper.fetch(f"https://learn.microsoft.com/page{i}")
                for i in range(10)
            ]
            await asyncio.gather(*tasks)

    assert max_observed <= max_concurrent


# === HTML Parsing Tests ===


class TestExtractText:
    """Tests for the extract_text helper function."""

    def test_basic_text_extraction(self):
        """Extracts visible text from HTML."""
        html = "<html><body><h1>Title</h1><p>Hello world.</p></body></html>"
        text = extract_text(html)
        assert "Title" in text
        assert "Hello world." in text

    def test_strips_scripts_and_styles(self):
        """Removes script and style content."""
        html = """
        <html><body>
            <script>var x = 1;</script>
            <style>.foo { color: red; }</style>
            <p>Content here</p>
        </body></html>
        """
        text = extract_text(html)
        assert "var x" not in text
        assert ".foo" not in text
        assert "Content here" in text

    def test_strips_nav_header_footer(self):
        """Removes navigation, header, and footer elements."""
        html = """
        <html><body>
            <nav><a href="/">Home</a></nav>
            <header><h1>Site Header</h1></header>
            <main><p>Main content</p></main>
            <footer><p>Footer info</p></footer>
        </body></html>
        """
        text = extract_text(html)
        assert "Home" not in text
        assert "Site Header" not in text
        assert "Footer info" not in text
        assert "Main content" in text

    def test_empty_html(self):
        """Handles empty HTML gracefully."""
        assert extract_text("") == ""
        assert extract_text("<html></html>") == ""


class TestExtractLinks:
    """Tests for the extract_links helper function."""

    def test_extracts_absolute_links(self):
        """Extracts absolute http/https URLs."""
        html = '<a href="https://learn.microsoft.com/docs">Link</a>'
        links = extract_links(html, "https://example.com/page")
        assert "https://learn.microsoft.com/docs" in links

    def test_resolves_relative_links(self):
        """Resolves relative URLs against base URL."""
        html = '<a href="/en-us/training">Training</a>'
        links = extract_links(html, "https://learn.microsoft.com/page")
        assert "https://learn.microsoft.com/en-us/training" in links

    def test_skips_fragment_only_links(self):
        """Fragment-only links are skipped."""
        html = '<a href="#section">Jump</a>'
        links = extract_links(html, "https://example.com/page")
        assert links == []

    def test_skips_javascript_links(self):
        """JavaScript pseudo-links are skipped."""
        html = '<a href="javascript:void(0)">Click</a>'
        links = extract_links(html, "https://example.com")
        assert links == []

    def test_strips_fragments_from_links(self):
        """Fragments are stripped from extracted URLs."""
        html = '<a href="https://learn.microsoft.com/page#section">Link</a>'
        links = extract_links(html, "https://example.com")
        assert "https://learn.microsoft.com/page" in links
        assert "#section" not in links[0]

    def test_preserves_query_params(self):
        """Query parameters are preserved."""
        html = '<a href="https://learn.microsoft.com/search?q=test">Search</a>'
        links = extract_links(html, "https://example.com")
        assert "https://learn.microsoft.com/search?q=test" in links

    def test_skips_non_http_schemes(self):
        """Non-HTTP schemes (mailto, ftp) are excluded."""
        html = """
        <a href="mailto:test@example.com">Email</a>
        <a href="ftp://files.example.com">FTP</a>
        <a href="https://real.example.com">Real</a>
        """
        links = extract_links(html, "https://example.com")
        assert len(links) == 1
        assert "https://real.example.com" in links

    def test_handles_empty_html(self):
        """Empty HTML returns empty list."""
        assert extract_links("", "https://example.com") == []
