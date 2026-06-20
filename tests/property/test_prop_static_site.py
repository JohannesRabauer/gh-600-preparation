"""Property-based tests for static site output.

Tests correctness property 27 from the design document:
- Property 27: No External CDN Dependencies

The built static site must not contain any external CDN references.
All styles, scripts, and fonts must be bundled locally.

**Validates: Requirements 14.7**
"""

from __future__ import annotations

import re
import subprocess
import sys
import tempfile
from pathlib import Path

import pytest
import yaml


# === Constants ===

PROJECT_ROOT = Path(__file__).resolve().parents[2]
MKDOCS_YML = PROJECT_ROOT / "mkdocs.yml"

# Common CDN domains that should NOT appear in the built site
EXTERNAL_CDN_DOMAINS = [
    "fonts.googleapis.com",
    "fonts.gstatic.com",
    "cdn.jsdelivr.net",
    "cdnjs.cloudflare.com",
    "unpkg.com",
    "maxcdn.bootstrapcdn.com",
    "ajax.googleapis.com",
    "stackpath.bootstrapcdn.com",
    "code.jquery.com",
]

# Regex pattern matching src/href attributes pointing to external CDN hosts
EXTERNAL_CDN_PATTERN = re.compile(
    r'(?:src|href)\s*=\s*["\']'
    r'https?://(?:' + "|".join(re.escape(d) for d in EXTERNAL_CDN_DOMAINS) + r')'
    r'[^"\']*["\']',
    re.IGNORECASE,
)


# === Custom YAML Loader ===

class _MkDocsLoader(yaml.SafeLoader):
    """YAML loader that handles !!python/name tags used by MkDocs plugins."""
    pass


# Add a generic handler for all !!python/name: tags
_MkDocsLoader.add_multi_constructor(
    "tag:yaml.org,2002:python/name:",
    lambda loader, suffix, node: loader.construct_scalar(node),
)


def _load_mkdocs_config() -> dict:
    """Load mkdocs.yml using the custom loader that handles !!python/name tags."""
    with open(MKDOCS_YML, "r", encoding="utf-8") as f:
        return yaml.load(f, Loader=_MkDocsLoader)


def _run_mkdocs_build(site_dir: Path) -> subprocess.CompletedProcess:
    """Run mkdocs build, falling back to python -m mkdocs if not on PATH."""
    try:
        return subprocess.run(
            ["mkdocs", "build", "--site-dir", str(site_dir)],
            cwd=str(PROJECT_ROOT),
            capture_output=True,
            text=True,
            timeout=120,
        )
    except FileNotFoundError:
        return subprocess.run(
            [sys.executable, "-m", "mkdocs", "build", "--site-dir", str(site_dir)],
            cwd=str(PROJECT_ROOT),
            capture_output=True,
            text=True,
            timeout=120,
        )


# === Property 27: No External CDN Dependencies ===


# Feature: gh-600-exam-prep, Property 27: No External CDN Dependencies
class TestNoExternalCDNDependencies:
    """The built static site must not contain any external CDN references.
    All styles, scripts, and fonts must be bundled locally so that the site
    functions without external CDN dependencies.

    **Validates: Requirements 14.7**
    """

    def test_mkdocs_config_disables_external_fonts(self) -> None:
        """mkdocs.yml must set font: false to disable Google Fonts CDN."""
        assert MKDOCS_YML.exists(), (
            f"mkdocs.yml not found at {MKDOCS_YML}"
        )

        config = _load_mkdocs_config()

        theme = config.get("theme", {})
        font_setting = theme.get("font")

        # font: false disables external Google Fonts in MkDocs Material
        assert font_setting is False, (
            f"mkdocs.yml theme.font should be 'false' to disable external "
            f"Google Fonts CDN, but got: {font_setting!r}"
        )

    def test_mkdocs_config_no_external_css_or_js(self) -> None:
        """mkdocs.yml must not reference external CDN URLs in extra_css or extra_javascript."""
        assert MKDOCS_YML.exists(), (
            f"mkdocs.yml not found at {MKDOCS_YML}"
        )

        config = _load_mkdocs_config()

        # Check extra_css entries
        extra_css = config.get("extra_css", []) or []
        for css_url in extra_css:
            for cdn_domain in EXTERNAL_CDN_DOMAINS:
                assert cdn_domain not in css_url, (
                    f"extra_css references external CDN: {css_url}"
                )

        # Check extra_javascript entries
        extra_js = config.get("extra_javascript", []) or []
        for js_url in extra_js:
            if isinstance(js_url, dict):
                js_url = js_url.get("src", "")
            for cdn_domain in EXTERNAL_CDN_DOMAINS:
                assert cdn_domain not in str(js_url), (
                    f"extra_javascript references external CDN: {js_url}"
                )

    def test_built_site_html_has_no_external_cdn_references(self) -> None:
        """After mkdocs build, all HTML files must not reference external CDN hosts.

        This test builds the MkDocs site and scans all generated HTML files
        for <link>, <script>, or <img> tags that reference known CDN domains.
        """
        # Build the site into a temporary directory
        with tempfile.TemporaryDirectory() as tmpdir:
            site_dir = Path(tmpdir) / "site"

            result = _run_mkdocs_build(site_dir)

            assert result.returncode == 0, (
                f"mkdocs build failed with return code {result.returncode}.\n"
                f"STDOUT: {result.stdout[:500]}\n"
                f"STDERR: {result.stderr[:500]}"
            )

            # Scan all HTML files in the built site
            html_files = list(site_dir.rglob("*.html"))
            assert len(html_files) > 0, (
                f"No HTML files found in built site at {site_dir}"
            )

            violations: list[str] = []

            for html_file in html_files:
                content = html_file.read_text(encoding="utf-8", errors="ignore")
                matches = EXTERNAL_CDN_PATTERN.findall(content)
                if matches:
                    rel_path = html_file.relative_to(site_dir)
                    for match in matches:
                        violations.append(
                            f"  {rel_path}: {match}"
                        )

            assert len(violations) == 0, (
                f"Found {len(violations)} external CDN reference(s) in built site HTML:\n"
                + "\n".join(violations[:20])
            )

    def test_built_site_no_google_fonts_link(self) -> None:
        """After mkdocs build, no HTML file should contain a Google Fonts stylesheet link."""
        with tempfile.TemporaryDirectory() as tmpdir:
            site_dir = Path(tmpdir) / "site"

            result = _run_mkdocs_build(site_dir)

            if result.returncode != 0:
                pytest.skip(
                    f"mkdocs build failed (returncode={result.returncode}); "
                    f"skipping HTML scan. stderr: {result.stderr[:200]}"
                )

            html_files = list(site_dir.rglob("*.html"))

            # Pattern specifically for Google Fonts stylesheet links
            google_fonts_pattern = re.compile(
                r'<link[^>]+href=["\']https?://fonts\.googleapis\.com[^"\']*["\']',
                re.IGNORECASE,
            )

            violations: list[str] = []

            for html_file in html_files:
                content = html_file.read_text(encoding="utf-8", errors="ignore")
                matches = google_fonts_pattern.findall(content)
                if matches:
                    rel_path = html_file.relative_to(site_dir)
                    for match in matches:
                        violations.append(f"  {rel_path}: {match}")

            assert len(violations) == 0, (
                f"Found Google Fonts CDN references in {len(violations)} location(s):\n"
                + "\n".join(violations[:20])
            )
