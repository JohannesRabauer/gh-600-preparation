"""Unit tests for the KnowledgeExtractor (Phase 1)."""

from __future__ import annotations

import json
from pathlib import Path
from unittest.mock import AsyncMock, patch

import pytest

from src.phases.phase01_extractor import ExtractorConfig, KnowledgeExtractor


# --- Fixtures and helpers ---

SAMPLE_HTML = """
<html>
<head><title>Test Page</title></head>
<body>
<h1>GitHub Copilot Agent Mode</h1>
<p>GitHub Copilot agent mode is defined as an AI-powered feature that enables
developers to delegate complex, multi-step tasks to an autonomous agent.
The agent can write code, run terminal commands, and iterate on solutions.</p>

<p>To configure agent mode, follow these steps: First, enable Copilot in your
IDE settings. Second, select the agent mode option. Third, define your task
description clearly.</p>

<p>The agent architecture framework provides a structured approach for building
AI-powered developer tools that integrate with existing development workflows
and CI/CD pipelines.</p>

<p>This is too short.</p>

<a href="https://learn.microsoft.com/en-us/training/modules/copilot-advanced/">Advanced Copilot</a>
<a href="https://docs.github.com/en/copilot/overview">Copilot Overview</a>
<a href="https://external-site.com/unrelated">External Link</a>
</body>
</html>
"""

LINKED_HTML = """
<html>
<head><title>Linked Page</title></head>
<body>
<h1>Advanced Copilot Features</h1>
<p>Advanced features include multi-file editing capabilities that require
knowledge of the repository structure and project conventions for effective use.</p>
</body>
</html>
"""


@pytest.fixture
def config(tmp_path: Path) -> ExtractorConfig:
    """Provide an ExtractorConfig that writes to a temp directory."""
    return ExtractorConfig(
        max_depth=2,
        max_links_per_level=50,
        allowed_domains=["learn.microsoft.com", "docs.github.com"],
        artifacts_dir=str(tmp_path / "artifacts"),
    )


# --- Tests ---


class TestKnowledgeExtractor:
    """Tests for the KnowledgeExtractor class."""

    @pytest.mark.asyncio
    async def test_extract_processes_source_urls(self, config: ExtractorConfig) -> None:
        """Verify that source URLs are fetched and processed."""
        extractor = KnowledgeExtractor(config=config)

        with patch("src.phases.phase01_extractor.Scraper") as MockScraper:
            mock_scraper = AsyncMock()
            mock_scraper.fetch = AsyncMock(return_value=(SAMPLE_HTML, None))
            mock_scraper.error_log = []
            MockScraper.return_value.__aenter__ = AsyncMock(return_value=mock_scraper)
            MockScraper.return_value.__aexit__ = AsyncMock(return_value=None)

            result = await extractor.extract(
                ["https://learn.microsoft.com/en-us/test"]
            )

        assert len(result.documents) >= 1
        assert result.documents[0].title == "Test Page"
        assert len(result.all_knowledge_points) > 0

    @pytest.mark.asyncio
    async def test_extract_only_follows_allowed_domains(
        self, config: ExtractorConfig
    ) -> None:
        """Verify that links to external domains are not followed."""
        extractor = KnowledgeExtractor(config=config)

        fetch_calls: list[str] = []

        async def mock_fetch(url: str, referrer: str = "") -> tuple[str, str | None]:
            fetch_calls.append(url)
            if "learn.microsoft.com" in url or "docs.github.com" in url:
                return LINKED_HTML, None
            return "", "Not allowed"

        with patch("src.phases.phase01_extractor.Scraper") as MockScraper:
            mock_scraper = AsyncMock()
            mock_scraper.fetch = mock_fetch
            mock_scraper.error_log = []
            MockScraper.return_value.__aenter__ = AsyncMock(return_value=mock_scraper)
            MockScraper.return_value.__aexit__ = AsyncMock(return_value=None)

            await extractor.extract(["https://learn.microsoft.com/en-us/test"])

        # Should NOT have fetched the external-site.com link
        assert not any("external-site.com" in url for url in fetch_calls)

    @pytest.mark.asyncio
    async def test_extract_deduplicates_urls(self, config: ExtractorConfig) -> None:
        """Verify that the same URL is only processed once."""
        config.max_depth = 0  # No link following, just test dedup of sources
        extractor = KnowledgeExtractor(config=config)

        fetch_count = {"count": 0}

        async def mock_fetch(url: str, referrer: str = "") -> tuple[str, str | None]:
            fetch_count["count"] += 1
            return SAMPLE_HTML, None

        with patch("src.phases.phase01_extractor.Scraper") as MockScraper:
            mock_scraper = AsyncMock()
            mock_scraper.fetch = mock_fetch
            mock_scraper.error_log = []
            MockScraper.return_value.__aenter__ = AsyncMock(return_value=mock_scraper)
            MockScraper.return_value.__aexit__ = AsyncMock(return_value=None)

            # Pass the same URL twice
            await extractor.extract([
                "https://learn.microsoft.com/en-us/test",
                "https://learn.microsoft.com/en-us/test",
            ])

        # The URL should only be fetched once despite being passed twice
        assert fetch_count["count"] == 1

    @pytest.mark.asyncio
    async def test_extract_handles_fetch_errors(
        self, config: ExtractorConfig
    ) -> None:
        """Verify that fetch errors are logged and processing continues."""
        config.max_depth = 0  # Only process source URLs
        extractor = KnowledgeExtractor(config=config)

        async def mock_fetch(url: str, referrer: str = "") -> tuple[str, str | None]:
            return "", "HTTP 404"

        with patch("src.phases.phase01_extractor.Scraper") as MockScraper:
            mock_scraper = AsyncMock()
            mock_scraper.fetch = mock_fetch
            mock_scraper.error_log = [{"url": "test", "error": "HTTP 404", "referrer": ""}]
            MockScraper.return_value.__aenter__ = AsyncMock(return_value=mock_scraper)
            MockScraper.return_value.__aexit__ = AsyncMock(return_value=None)

            result = await extractor.extract(
                ["https://learn.microsoft.com/en-us/test"]
            )

        # Document should exist but with error
        assert len(result.documents) == 1
        assert result.documents[0].fetch_error == "HTTP 404"
        assert len(result.error_log) == 1

    @pytest.mark.asyncio
    async def test_extract_writes_artifact(self, config: ExtractorConfig) -> None:
        """Verify that the extraction result is written to disk."""
        extractor = KnowledgeExtractor(config=config)

        with patch("src.phases.phase01_extractor.Scraper") as MockScraper:
            mock_scraper = AsyncMock()
            mock_scraper.fetch = AsyncMock(return_value=(SAMPLE_HTML, None))
            mock_scraper.error_log = []
            MockScraper.return_value.__aenter__ = AsyncMock(return_value=mock_scraper)
            MockScraper.return_value.__aexit__ = AsyncMock(return_value=None)

            await extractor.extract(["https://learn.microsoft.com/en-us/test"])

        artifact_path = Path(config.artifacts_dir) / "phase01_extraction.json"
        assert artifact_path.exists()

        data = json.loads(artifact_path.read_text(encoding="utf-8"))
        assert "documents" in data
        assert "all_knowledge_points" in data
        assert "stats" in data

    @pytest.mark.asyncio
    async def test_max_links_per_level_respected(
        self, config: ExtractorConfig
    ) -> None:
        """Verify that at most max_links_per_level links are followed per depth."""
        config.max_links_per_level = 2
        config.max_depth = 1
        extractor = KnowledgeExtractor(config=config)

        # Source page with many links
        many_links_html = "<html><head><title>Source</title></head><body>"
        for i in range(10):
            many_links_html += (
                f'<a href="https://learn.microsoft.com/page-{i}">Link {i}</a>\n'
            )
        many_links_html += "<p>This page has some content about agent architecture patterns and design approaches for development.</p></body></html>"

        fetch_count = {"count": 0}

        async def mock_fetch(url: str, referrer: str = "") -> tuple[str, str | None]:
            fetch_count["count"] += 1
            if fetch_count["count"] == 1:
                return many_links_html, None
            return LINKED_HTML, None

        with patch("src.phases.phase01_extractor.Scraper") as MockScraper:
            mock_scraper = AsyncMock()
            mock_scraper.fetch = mock_fetch
            mock_scraper.error_log = []
            MockScraper.return_value.__aenter__ = AsyncMock(return_value=mock_scraper)
            MockScraper.return_value.__aexit__ = AsyncMock(return_value=None)

            await extractor.extract(["https://learn.microsoft.com/source"])

        # 1 source + at most 2 linked pages = max 3
        assert fetch_count["count"] <= 3


class TestKnowledgePointExtraction:
    """Tests for knowledge point classification."""

    def test_classify_definition(self) -> None:
        """Definitions are correctly classified."""
        from src.phases.phase01_extractor import KnowledgeExtractor

        ext = KnowledgeExtractor()
        result = ext._classify_paragraph(
            "GitHub Copilot is defined as an AI-powered code completion tool "
            "that helps developers write code faster."
        )
        assert result == "definition"

    def test_classify_procedure(self) -> None:
        """Procedures are correctly classified."""
        from src.phases.phase01_extractor import KnowledgeExtractor

        ext = KnowledgeExtractor()
        result = ext._classify_paragraph(
            "To configure agent mode, follow these steps: "
            "1. Open settings 2. Navigate to copilot 3. Enable agent mode"
        )
        assert result == "procedure"

    def test_classify_framework(self) -> None:
        """Framework references are correctly classified."""
        from src.phases.phase01_extractor import KnowledgeExtractor

        ext = KnowledgeExtractor()
        result = ext._classify_paragraph(
            "The agent architecture framework provides a structured approach "
            "for building AI-powered tools in development pipelines."
        )
        assert result == "framework"

    def test_classify_defaults_to_concept(self) -> None:
        """Unmatched content defaults to concept."""
        from src.phases.phase01_extractor import KnowledgeExtractor

        ext = KnowledgeExtractor()
        result = ext._classify_paragraph(
            "GitHub Copilot was announced in 2021 and has been widely "
            "adopted by professional software developers around the world."
        )
        assert result == "concept"

    def test_short_paragraphs_excluded(self) -> None:
        """Paragraphs shorter than 8 words are excluded from extraction."""
        from src.models.knowledge import ParsedDocument
        from src.phases.phase01_extractor import KnowledgeExtractor

        ext = KnowledgeExtractor()
        doc = ParsedDocument(
            url="https://example.com",
            title="Test",
            content_text="Short text.\n\nThis is a longer paragraph that should be extracted as a knowledge point from the document.",
            links=[],
            knowledge_points=[],
        )
        points = ext._extract_knowledge_points(doc, depth=0)
        # Only the longer paragraph should be extracted
        assert len(points) == 1
        assert "longer paragraph" in points[0].content


class TestPrerequisiteReconstruction:
    """Tests for prerequisite reconstruction logic."""

    def test_reconstructs_referenced_prerequisites(self) -> None:
        """Prerequisites referenced but not covered are reconstructed."""
        from src.models.knowledge import KnowledgePoint
        from src.phases.phase01_extractor import KnowledgeExtractor

        ext = KnowledgeExtractor()
        points = [
            KnowledgePoint(
                id="kp-0001",
                content="Before you begin working with agent mode, you need familiarity with VS Code extensions and their configuration.",
                category="procedure",
                source_url="https://example.com",
                source_title="Test",
                depth=0,
            ),
        ]

        prereqs = ext._reconstruct_prerequisites(points)
        assert len(prereqs) >= 1
        assert all(p.is_prerequisite for p in prereqs)

    def test_does_not_reconstruct_covered_concepts(self) -> None:
        """Concepts already covered in sources are not reconstructed."""
        from src.models.knowledge import KnowledgePoint
        from src.phases.phase01_extractor import KnowledgeExtractor

        ext = KnowledgeExtractor()
        points = [
            KnowledgePoint(
                id="kp-0001",
                content="Docker containers provide isolated environments for running applications with all their dependencies bundled together.",
                category="concept",
                source_url="https://example.com",
                source_title="Test",
                depth=0,
            ),
            KnowledgePoint(
                id="kp-0002",
                content="This module assumes familiarity with Docker containers and their lifecycle management for deploying agents.",
                category="procedure",
                source_url="https://example.com",
                source_title="Test",
                depth=0,
            ),
        ]

        prereqs = ext._reconstruct_prerequisites(points)
        # "Docker containers" is already covered in kp-0001 (primary topic),
        # so no prerequisite should be reconstructed for it
        assert len(prereqs) == 0
