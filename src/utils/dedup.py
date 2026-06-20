"""URL deduplication utility for the Knowledge Extractor.

Provides URL normalization and visited-URL tracking to ensure the same content
reached through multiple link paths is processed only once (Requirement 1.6).
"""

from urllib.parse import urlparse, urlunparse, parse_qs, urlencode


def normalize_url(url: str) -> str:
    """Normalize a URL for consistent deduplication comparison.

    Normalization steps:
    - Lowercase scheme and host
    - Remove URL fragments (#...)
    - Sort query parameters alphabetically
    - Remove trailing slashes from path
    - Strip default ports (80 for http, 443 for https)

    Args:
        url: The URL string to normalize.

    Returns:
        The normalized URL string.
    """
    parsed = urlparse(url)

    # Lowercase scheme and host
    scheme = parsed.scheme.lower()
    hostname = parsed.hostname or ""
    hostname = hostname.lower()

    # Strip default ports
    port = parsed.port
    if port == 80 and scheme == "http":
        port = None
    elif port == 443 and scheme == "https":
        port = None

    # Reconstruct netloc with optional port
    if port:
        netloc = f"{hostname}:{port}"
    else:
        netloc = hostname

    # Remove trailing slashes from path (but keep root "/" as empty for urlunparse)
    path = parsed.path.rstrip("/")
    if not path:
        path = ""

    # Sort query parameters alphabetically
    query_params = parse_qs(parsed.query, keep_blank_values=True)
    sorted_params = sorted(query_params.items())
    # Flatten multi-value params into sorted individual key=value pairs
    flat_params: list[tuple[str, str]] = []
    for key, values in sorted_params:
        for value in sorted(values):
            flat_params.append((key, value))
    query = urlencode(flat_params)

    # Remove fragment entirely
    fragment = ""

    normalized = urlunparse((scheme, netloc, path, parsed.params, query, fragment))
    return normalized


class URLTracker:
    """Tracks visited URLs using normalized forms to avoid processing duplicates.

    Used by the KnowledgeExtractor to ensure that the same content reachable
    through multiple link paths is processed only once (Requirement 1.6).
    """

    def __init__(self) -> None:
        """Initialize with an empty set of visited URLs."""
        self._visited: set[str] = set()

    def has_visited(self, url: str) -> bool:
        """Check if a URL (after normalization) has already been visited.

        Args:
            url: The URL to check.

        Returns:
            True if the normalized URL was already marked as visited.
        """
        return normalize_url(url) in self._visited

    def mark_visited(self, url: str) -> None:
        """Mark a URL as visited by storing its normalized form.

        Args:
            url: The URL to mark as visited.
        """
        self._visited.add(normalize_url(url))

    def get_visited(self) -> set[str]:
        """Return all visited URLs in their normalized form.

        Returns:
            A set of all normalized visited URL strings.
        """
        return set(self._visited)
