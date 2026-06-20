"""Unit tests for the URL deduplication utility."""

import pytest

from src.utils.dedup import normalize_url, URLTracker


class TestNormalizeUrl:
    """Tests for the normalize_url function."""

    def test_lowercases_scheme(self):
        result = normalize_url("HTTPS://example.com/page")
        assert result.startswith("https://")

    def test_lowercases_host(self):
        result = normalize_url("https://EXAMPLE.COM/page")
        assert "example.com" in result

    def test_removes_fragment(self):
        result = normalize_url("https://example.com/page#section")
        assert "#" not in result

    def test_sorts_query_params(self):
        result = normalize_url("https://example.com/page?z=1&a=2&m=3")
        assert result == "https://example.com/page?a=2&m=3&z=1"

    def test_removes_trailing_slash(self):
        result = normalize_url("https://example.com/page/")
        assert result == "https://example.com/page"

    def test_strips_default_http_port(self):
        result = normalize_url("http://example.com:80/page")
        assert result == "http://example.com/page"

    def test_strips_default_https_port(self):
        result = normalize_url("https://example.com:443/page")
        assert result == "https://example.com/page"

    def test_keeps_non_default_port(self):
        result = normalize_url("https://example.com:8080/page")
        assert ":8080" in result

    def test_combined_normalization(self):
        url = "HTTPS://LEARN.MICROSOFT.COM:443/en-us/docs/?b=2&a=1#top"
        result = normalize_url(url)
        assert result == "https://learn.microsoft.com/en-us/docs?a=1&b=2"

    def test_empty_path(self):
        result = normalize_url("https://example.com")
        assert result == "https://example.com"

    def test_preserves_path_segments(self):
        result = normalize_url("https://example.com/a/b/c")
        assert result == "https://example.com/a/b/c"

    def test_handles_no_query_string(self):
        result = normalize_url("https://example.com/page")
        assert result == "https://example.com/page"

    def test_multi_value_query_params_sorted(self):
        result = normalize_url("https://example.com/page?tag=b&tag=a")
        assert result == "https://example.com/page?tag=a&tag=b"


class TestURLTracker:
    """Tests for the URLTracker class."""

    def test_new_tracker_has_no_visited(self):
        tracker = URLTracker()
        assert tracker.get_visited() == set()

    def test_mark_and_check_visited(self):
        tracker = URLTracker()
        tracker.mark_visited("https://example.com/page")
        assert tracker.has_visited("https://example.com/page")

    def test_has_visited_returns_false_for_unvisited(self):
        tracker = URLTracker()
        assert not tracker.has_visited("https://example.com/page")

    def test_deduplicates_with_normalization(self):
        tracker = URLTracker()
        tracker.mark_visited("https://EXAMPLE.COM/page#section")
        assert tracker.has_visited("https://example.com/page")

    def test_deduplicates_trailing_slash(self):
        tracker = URLTracker()
        tracker.mark_visited("https://example.com/page/")
        assert tracker.has_visited("https://example.com/page")

    def test_deduplicates_query_param_order(self):
        tracker = URLTracker()
        tracker.mark_visited("https://example.com/page?b=2&a=1")
        assert tracker.has_visited("https://example.com/page?a=1&b=2")

    def test_deduplicates_default_port(self):
        tracker = URLTracker()
        tracker.mark_visited("https://example.com:443/page")
        assert tracker.has_visited("https://example.com/page")

    def test_get_visited_returns_all(self):
        tracker = URLTracker()
        tracker.mark_visited("https://example.com/a")
        tracker.mark_visited("https://example.com/b")
        visited = tracker.get_visited()
        assert len(visited) == 2
        assert "https://example.com/a" in visited
        assert "https://example.com/b" in visited

    def test_get_visited_returns_copy(self):
        tracker = URLTracker()
        tracker.mark_visited("https://example.com/page")
        visited = tracker.get_visited()
        visited.add("https://other.com")
        assert not tracker.has_visited("https://other.com")

    def test_different_paths_not_deduplicated(self):
        tracker = URLTracker()
        tracker.mark_visited("https://example.com/page-a")
        assert not tracker.has_visited("https://example.com/page-b")
