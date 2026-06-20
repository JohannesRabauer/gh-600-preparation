"""Property-based tests for Phase 1: Knowledge Extractor.

Tests correctness properties 1 and 2 from the design document:
- Property 1: Link Traversal Depth and Breadth Constraints
- Property 2: URL Deduplication

**Validates: Requirements 1.2, 1.6**
"""

from __future__ import annotations

import asyncio
from unittest.mock import AsyncMock, patch
from urllib.parse import urljoin

import pytest
from hypothesis import given, settings, HealthCheck
from hypothesis import strategies as st

from src.phases.phase01_extractor import ExtractorConfig, KnowledgeExtractor
from src.utils.dedup import URLTracker, normalize_url


# === Strategies ===


def _url_path_segment() -> st.SearchStrategy[str]:
    """Generate a valid URL path segment."""
    return st.from_regex(r"[a-z][a-z0-9\-]{1,20}", fullmatch=True)


def _allowed_url() -> st.SearchStrategy[str]:
    """Generate a URL within allowed domains."""
    domain = st.sampled_from(["learn.microsoft.com", "docs.github.com"])
    path = st.lists(_url_path_segment(), min_size=1, max_size=4).map(
        lambda parts: "/" + "/".join(parts)
    )
    return st.tuples(domain, path).map(
        lambda t: f"https://{t[0]}{t[1]}"
    )


def _link_count_per_page() -> st.SearchStrategy[int]:
    """Generate the number of links a page can contain (0 to 120)."""
    return st.integers(min_value=0, max_value=120)


def _url_with_variations() -> st.SearchStrategy[str]:
    """Generate URLs that may have fragments, different query orders, or case differences."""
    base_url = _allowed_url()
    fragment = st.sampled_from(["", "#section1", "#top", "#details"])
    query_params = st.sampled_from([
        "",
        "?a=1&b=2",
        "?b=2&a=1",
        "?view=all",
        "?A=1&B=2",
    ])
    casing = st.sampled_from(["lower", "upper_host", "mixed"])

    def combine(parts: tuple) -> str:
        url, frag, query, case_style = parts
        result = url
        if query:
            result += query
        if frag:
            result += frag
        if case_style == "upper_host":
            result = result.replace("learn.microsoft.com", "LEARN.MICROSOFT.COM")
            result = result.replace("docs.github.com", "DOCS.GITHUB.COM")
        elif case_style == "mixed":
            result = result.replace("https://", "HTTPS://")
        return result

    return st.tuples(base_url, fragment, query_params, casing).map(combine)


# === Helpers ===


def _make_html_with_links(links: list[str]) -> str:
    """Create a minimal HTML page with the given list of links."""
    anchor_tags = "\n".join(f'<a href="{url}">Link</a>' for url in links)
    return f"""<html>
<head><title>Test Page</title></head>
<body>
<h1>Test Document</h1>
<p>This is a test document with enough words to form a meaningful paragraph that
the extractor should consider as content worth processing into knowledge points
for the exam preparation generator system.</p>
{anchor_tags}
</body>
</html>"""


# === Property 1: Link Traversal Depth and Breadth Constraints ===


# Feature: gh-600-exam-prep, Property 1: Link Traversal Depth and Breadth Constraints
class TestLinkTraversalDepthAndBreadth:
    """The extractor never fetches more than MAX_LINKS_PER_LEVEL links per depth level,
    and never traverses deeper than MAX_LINK_DEPTH.

    **Validates: Requirements 1.2**
    """

    @given(
        max_links_per_level=st.integers(min_value=1, max_value=10),
        num_links_depth0=st.integers(min_value=1, max_value=30),
        num_links_depth1=st.integers(min_value=0, max_value=30),
    )
    @settings(
        max_examples=100,
        deadline=10000,
        suppress_health_check=[HealthCheck.too_slow],
    )
    @pytest.mark.asyncio
    async def test_breadth_constraint_per_level(
        self,
        max_links_per_level: int,
        num_links_depth0: int,
        num_links_depth1: int,
    ) -> None:
        """The total documents processed at each depth level never exceeds max_links_per_level."""
        # Generate distinct URLs for links at depth 0 and depth 1
        base = "https://learn.microsoft.com"
        source_url = f"{base}/source"
        depth1_links = [f"{base}/d1-page-{i}" for i in range(num_links_depth0)]
        depth2_links = [f"{base}/d2-page-{i}" for i in range(num_links_depth1)]

        # Create mock pages: source page has depth1_links, each depth1 page has depth2_links
        source_html = _make_html_with_links(depth1_links)
        depth1_html = _make_html_with_links(depth2_links)
        depth2_html = _make_html_with_links([])  # No further links

        # Track which URLs were fetched
        fetched_urls: list[str] = []

        async def mock_fetch(url: str, referrer: str = "") -> tuple[str, str | None]:
            fetched_urls.append(url)
            if url == source_url:
                return source_html, None
            elif url.startswith(f"{base}/d1-page-"):
                return depth1_html, None
            elif url.startswith(f"{base}/d2-page-"):
                return depth2_html, None
            return "", "Not found"

        config = ExtractorConfig(
            max_depth=2,
            max_links_per_level=max_links_per_level,
            allowed_domains=["learn.microsoft.com"],
            artifacts_dir="test_artifacts",
        )

        extractor = KnowledgeExtractor(config)

        with patch("src.phases.phase01_extractor.Scraper") as MockScraper:
            mock_scraper_instance = AsyncMock()
            mock_scraper_instance.fetch = mock_fetch
            mock_scraper_instance.error_log = []
            mock_scraper_instance.__aenter__ = AsyncMock(return_value=mock_scraper_instance)
            mock_scraper_instance.__aexit__ = AsyncMock(return_value=None)
            MockScraper.return_value = mock_scraper_instance

            with patch.object(extractor, "_write_artifact"):
                result = await extractor.extract([source_url])

        # Count documents by depth (excluding the source doc at depth 0)
        depth_1_docs = [d for d in result.documents if d.url.startswith(f"{base}/d1-page-")]
        depth_2_docs = [d for d in result.documents if d.url.startswith(f"{base}/d2-page-")]

        # Property: links followed at depth 1 never exceeds max_links_per_level
        assert len(depth_1_docs) <= max_links_per_level, (
            f"Depth 1 docs ({len(depth_1_docs)}) exceeded max_links_per_level ({max_links_per_level})"
        )
        # Property: links followed at depth 2 never exceeds max_links_per_level
        assert len(depth_2_docs) <= max_links_per_level, (
            f"Depth 2 docs ({len(depth_2_docs)}) exceeded max_links_per_level ({max_links_per_level})"
        )

    @given(
        max_depth=st.integers(min_value=0, max_value=2),
        num_links=st.integers(min_value=1, max_value=10),
    )
    @settings(
        max_examples=100,
        deadline=10000,
        suppress_health_check=[HealthCheck.too_slow],
    )
    @pytest.mark.asyncio
    async def test_depth_constraint(
        self,
        max_depth: int,
        num_links: int,
    ) -> None:
        """No document is processed with depth > max_depth."""
        base = "https://learn.microsoft.com"
        source_url = f"{base}/source"
        depth1_links = [f"{base}/d1-page-{i}" for i in range(num_links)]
        depth2_links = [f"{base}/d2-page-{i}" for i in range(num_links)]
        depth3_links = [f"{base}/d3-page-{i}" for i in range(num_links)]

        source_html = _make_html_with_links(depth1_links)
        depth1_html = _make_html_with_links(depth2_links)
        depth2_html = _make_html_with_links(depth3_links)
        depth3_html = _make_html_with_links([])

        fetched_urls: list[str] = []

        async def mock_fetch(url: str, referrer: str = "") -> tuple[str, str | None]:
            fetched_urls.append(url)
            if url == source_url:
                return source_html, None
            elif url.startswith(f"{base}/d1-page-"):
                return depth1_html, None
            elif url.startswith(f"{base}/d2-page-"):
                return depth2_html, None
            elif url.startswith(f"{base}/d3-page-"):
                return depth3_html, None
            return "", "Not found"

        config = ExtractorConfig(
            max_depth=max_depth,
            max_links_per_level=50,
            allowed_domains=["learn.microsoft.com"],
            artifacts_dir="test_artifacts",
        )

        extractor = KnowledgeExtractor(config)

        with patch("src.phases.phase01_extractor.Scraper") as MockScraper:
            mock_scraper_instance = AsyncMock()
            mock_scraper_instance.fetch = mock_fetch
            mock_scraper_instance.error_log = []
            mock_scraper_instance.__aenter__ = AsyncMock(return_value=mock_scraper_instance)
            mock_scraper_instance.__aexit__ = AsyncMock(return_value=None)
            MockScraper.return_value = mock_scraper_instance

            with patch.object(extractor, "_write_artifact"):
                result = await extractor.extract([source_url])

        # Property: no document beyond max_depth is fetched
        # Depth 3 links should NEVER be fetched (max possible depth is 2)
        depth3_fetched = [u for u in fetched_urls if u.startswith(f"{base}/d3-page-")]
        assert len(depth3_fetched) == 0, (
            f"Depth 3 pages were fetched with max_depth={max_depth}: {depth3_fetched}"
        )

        # If max_depth < 2, depth 2 pages should not be fetched
        if max_depth < 2:
            depth2_fetched = [u for u in fetched_urls if u.startswith(f"{base}/d2-page-")]
            assert len(depth2_fetched) == 0, (
                f"Depth 2 pages were fetched with max_depth={max_depth}: {depth2_fetched}"
            )

        # If max_depth < 1, depth 1 pages should not be fetched
        if max_depth < 1:
            depth1_fetched = [u for u in fetched_urls if u.startswith(f"{base}/d1-page-")]
            assert len(depth1_fetched) == 0, (
                f"Depth 1 pages were fetched with max_depth={max_depth}: {depth1_fetched}"
            )


# === Property 2: URL Deduplication ===


# Feature: gh-600-exam-prep, Property 2: URL Deduplication
class TestURLDeduplication:
    """Given any set of source URLs (with duplicates and different representations
    of the same URL), each normalized URL is fetched at most once.

    **Validates: Requirements 1.6**
    """

    @given(
        urls=st.lists(
            _url_with_variations(),
            min_size=1,
            max_size=30,
        ),
    )
    @settings(max_examples=100, deadline=5000)
    def test_url_tracker_marks_each_normalized_url_once(
        self,
        urls: list[str],
    ) -> None:
        """The URLTracker marks each normalized URL only once, regardless of representation."""
        tracker = URLTracker()

        for url in urls:
            tracker.mark_visited(url)

        visited = tracker.get_visited()

        # All visited URLs should be in normalized form
        for v in visited:
            assert v == normalize_url(v), (
                f"Visited URL '{v}' is not in normalized form"
            )

        # The number of unique normalized URLs from input should match visited count
        expected_normalized = {normalize_url(u) for u in urls}
        assert visited == expected_normalized, (
            f"Visited set {visited} != expected normalized set {expected_normalized}"
        )

    @given(
        urls=st.lists(
            _url_with_variations(),
            min_size=1,
            max_size=30,
        ),
    )
    @settings(max_examples=100, deadline=5000)
    def test_has_visited_detects_all_representations(
        self,
        urls: list[str],
    ) -> None:
        """Once a URL is marked visited, all representations of that same URL are detected."""
        tracker = URLTracker()

        for url in urls:
            tracker.mark_visited(url)

        # Every URL in the input (in any form) should now be detected as visited
        for url in urls:
            assert tracker.has_visited(url), (
                f"URL '{url}' (normalized: '{normalize_url(url)}') not detected as visited"
            )

    @given(
        num_source_urls=st.integers(min_value=1, max_value=5),
        num_duplicate_links=st.integers(min_value=1, max_value=10),
    )
    @settings(
        max_examples=100,
        deadline=10000,
        suppress_health_check=[HealthCheck.too_slow],
    )
    @pytest.mark.asyncio
    async def test_extractor_fetches_each_url_at_most_once(
        self,
        num_source_urls: int,
        num_duplicate_links: int,
    ) -> None:
        """The extractor fetches each unique URL at most once even when
        reached via multiple paths."""
        base = "https://learn.microsoft.com"

        # Create source URLs that all link to the same set of shared pages
        source_urls = [f"{base}/source-{i}" for i in range(num_source_urls)]
        shared_links = [f"{base}/shared-page-{i}" for i in range(num_duplicate_links)]

        # Each source page links to ALL shared pages (creating multiple paths)
        source_html = _make_html_with_links(shared_links)
        shared_html = _make_html_with_links([])

        fetch_count: dict[str, int] = {}

        async def mock_fetch(url: str, referrer: str = "") -> tuple[str, str | None]:
            fetch_count[url] = fetch_count.get(url, 0) + 1
            if url.startswith(f"{base}/source-"):
                return source_html, None
            elif url.startswith(f"{base}/shared-page-"):
                return shared_html, None
            return "", "Not found"

        config = ExtractorConfig(
            max_depth=1,
            max_links_per_level=50,
            allowed_domains=["learn.microsoft.com"],
            artifacts_dir="test_artifacts",
        )

        extractor = KnowledgeExtractor(config)

        with patch("src.phases.phase01_extractor.Scraper") as MockScraper:
            mock_scraper_instance = AsyncMock()
            mock_scraper_instance.fetch = mock_fetch
            mock_scraper_instance.error_log = []
            mock_scraper_instance.__aenter__ = AsyncMock(return_value=mock_scraper_instance)
            mock_scraper_instance.__aexit__ = AsyncMock(return_value=None)
            MockScraper.return_value = mock_scraper_instance

            with patch.object(extractor, "_write_artifact"):
                result = await extractor.extract(source_urls)

        # Property: each URL is fetched at most once
        for url, count in fetch_count.items():
            assert count == 1, (
                f"URL '{url}' was fetched {count} times (expected 1)"
            )

        # Property: the number of unique fetches equals number of unique normalized URLs
        all_urls = source_urls + shared_links
        expected_unique = len({normalize_url(u) for u in all_urls})
        # We may not fetch all shared links if max_links_per_level is hit,
        # but we should never fetch MORE than unique count
        assert len(fetch_count) <= expected_unique, (
            f"Fetched {len(fetch_count)} URLs but only {expected_unique} unique URLs exist"
        )

    @given(
        urls=st.lists(
            st.sampled_from([
                "https://learn.microsoft.com/page",
                "https://LEARN.MICROSOFT.COM/page",
                "https://learn.microsoft.com/page#section",
                "https://learn.microsoft.com/page?a=1&b=2",
                "https://learn.microsoft.com/page?b=2&a=1",
                "https://learn.microsoft.com/page/",
            ]),
            min_size=2,
            max_size=10,
        ),
    )
    @settings(max_examples=100, deadline=5000)
    def test_normalize_url_is_idempotent(
        self,
        urls: list[str],
    ) -> None:
        """Normalizing a URL twice produces the same result as normalizing once."""
        for url in urls:
            once = normalize_url(url)
            twice = normalize_url(once)
            assert once == twice, (
                f"normalize_url is not idempotent: "
                f"normalize('{url}') = '{once}', normalize('{once}') = '{twice}'"
            )
