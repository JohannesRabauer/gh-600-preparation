"""Unit tests for the SiteRenderer and artifact loading."""

import json
from pathlib import Path

import pytest

from src.rendering.renderer import (
    PipelineArtifacts,
    SiteRenderer,
    load_artifacts,
)
from src.models.scoring import ScoredTopic, ScoredTopicList
from src.models.study_notes import StudyNotesCollection, TopicNotes
from src.models.curriculum import Curriculum, Module
from src.models.revision import RevisionPackage, Flashcard, CheatSheet, Mnemonic
from src.models.gap_analysis import GapReport, Gap, CoverageStatus
from src.models.readiness import ReadinessAssessment, HighRiskTopic, TimeBlock


@pytest.fixture
def tmp_output_dir(tmp_path):
    """Create a temporary output directory."""
    output = tmp_path / "docs"
    output.mkdir()
    return output


@pytest.fixture
def template_dir():
    """Return the real template directory."""
    return Path("src/rendering/templates")


@pytest.fixture
def sample_scores():
    """Create sample scored topic list with cross-domain concepts."""
    return ScoredTopicList(topics=[
        ScoredTopic(
            topic_id="t-1",
            topic_name="Agent Architecture",
            domain_ids=["domain-1", "domain-2", "domain-4"],
            priority_score=9,
            is_high_priority=True,
            domain_count=3,
        ),
        ScoredTopic(
            topic_id="t-2",
            topic_name="Copilot Tools",
            domain_ids=["domain-2", "domain-5"],
            priority_score=8,
            is_high_priority=True,
            domain_count=2,
        ),
        ScoredTopic(
            topic_id="t-3",
            topic_name="Security Basics",
            domain_ids=["domain-4"],
            priority_score=6,
            is_high_priority=False,
            domain_count=1,
        ),
        ScoredTopic(
            topic_id="t-4",
            topic_name="Low Priority",
            domain_ids=["domain-6"],
            priority_score=4,
            is_high_priority=False,
            domain_count=1,
        ),
    ])


@pytest.fixture
def sample_study_notes():
    """Create sample study notes with cross-domain themes."""
    return StudyNotesCollection(
        notes=[
            TopicNotes(
                topic_id="t-1",
                topic_name="Agent Architecture",
                domain_id="domain-1",
                priority_score=9,
                overview="Agent architecture overview. It covers patterns. It is important.",
                explanation="Detailed explanation " * 50,
                key_facts=["Fact 1", "Fact 2", "Fact 3"],
                common_mistakes=["Mistake 1", "Mistake 2"],
                examples=["Example 1", "Example 2"],
                exam_tips=["Tip 1"],
                code_blocks=[],
                related_topics=[
                    {"topic_id": "t-2", "domain_name": "Design and implement", "relationship": "Uses tools"},
                    {"topic_id": "t-3", "domain_name": "Secure and govern", "relationship": "Needs security"},
                ],
            ),
            TopicNotes(
                topic_id="t-3",
                topic_name="Security Basics",
                domain_id="domain-4",
                priority_score=6,
                overview="Security basics. Cover access controls. Important topic.",
                explanation="Security explanation " * 30,
                key_facts=["Fact 1", "Fact 2", "Fact 3"],
                common_mistakes=["Mistake 1", "Mistake 2"],
                examples=["Example 1"],
                exam_tips=["Tip 1"],
                code_blocks=[],
                related_topics=[],
            ),
        ],
        cross_domain_themes=[
            {
                "theme": "AI Safety and Governance",
                "domains": ["domain-1", "domain-4", "domain-6"],
                "manifestations": [
                    "Architecture patterns for safe AI",
                    "Security controls for agent actions",
                    "Responsible AI practices",
                ],
            },
        ],
    )


@pytest.fixture
def sample_curriculum():
    """Create sample curriculum."""
    return Curriculum(
        modules=[
            Module(
                id="M01",
                title="Introduction",
                topic_ids=["t-1"],
                objectives=["Explain agent architecture"],
                prerequisites=["none"],
                time_estimate_minutes=60,
                contains_high_priority=True,
            ),
        ],
        total_time_minutes=60,
        learning_path=["M01"],
    )


class TestSiteRendererInit:
    """Test SiteRenderer initialization."""

    def test_creates_renderer_with_paths(self, template_dir, tmp_output_dir):
        renderer = SiteRenderer(template_dir=template_dir, output_dir=tmp_output_dir)
        assert renderer.template_dir == template_dir
        assert renderer.output_dir == tmp_output_dir

    def test_jinja_environment_configured(self, template_dir, tmp_output_dir):
        renderer = SiteRenderer(template_dir=template_dir, output_dir=tmp_output_dir)
        assert renderer.env is not None
        # Templates should be loadable
        tmpl = renderer.env.get_template("landing.md.j2")
        assert tmpl is not None


class TestRenderAll:
    """Test render_all produces expected output files."""

    def test_renders_landing_page_always(self, template_dir, tmp_output_dir, sample_scores):
        renderer = SiteRenderer(template_dir=template_dir, output_dir=tmp_output_dir)
        artifacts = PipelineArtifacts(scores=sample_scores)
        renderer.render_all(artifacts)

        assert (tmp_output_dir / "index.md").exists()

    def test_renders_study_notes_when_available(
        self, template_dir, tmp_output_dir, sample_scores, sample_study_notes
    ):
        renderer = SiteRenderer(template_dir=template_dir, output_dir=tmp_output_dir)
        artifacts = PipelineArtifacts(scores=sample_scores, study_notes=sample_study_notes)
        renderer.render_all(artifacts)

        assert (tmp_output_dir / "study_notes.md").exists()
        content = (tmp_output_dir / "study_notes.md").read_text()
        assert "Agent Architecture" in content

    def test_renders_curriculum_when_available(
        self, template_dir, tmp_output_dir, sample_scores, sample_curriculum
    ):
        renderer = SiteRenderer(template_dir=template_dir, output_dir=tmp_output_dir)
        artifacts = PipelineArtifacts(scores=sample_scores, curriculum=sample_curriculum)
        renderer.render_all(artifacts)

        assert (tmp_output_dir / "curriculum.md").exists()
        content = (tmp_output_dir / "curriculum.md").read_text()
        assert "Introduction" in content

    def test_renders_cross_domain_page(self, template_dir, tmp_output_dir, sample_scores):
        renderer = SiteRenderer(template_dir=template_dir, output_dir=tmp_output_dir)
        artifacts = PipelineArtifacts(scores=sample_scores)
        renderer.render_all(artifacts)

        assert (tmp_output_dir / "cross_domain.md").exists()
        content = (tmp_output_dir / "cross_domain.md").read_text()
        assert "Cross-Domain Connections" in content


class TestCrossDomainContent:
    """Test cross-domain content generation (Requirements 12.1-12.5)."""

    def test_mermaid_diagram_includes_high_score_cross_domain_concepts(
        self, template_dir, tmp_output_dir, sample_scores, sample_study_notes
    ):
        """Req 12.2: Mermaid diagram shows concepts with Priority_Score ≥ 7 across 2+ domains."""
        renderer = SiteRenderer(template_dir=template_dir, output_dir=tmp_output_dir)
        artifacts = PipelineArtifacts(scores=sample_scores, study_notes=sample_study_notes)
        renderer.render_all(artifacts)

        content = (tmp_output_dir / "cross_domain.md").read_text()
        assert "```mermaid" in content
        assert "Agent Architecture" in content
        assert "Copilot Tools" in content
        # Low-score topics should not be in diagram
        assert "Low Priority" not in content

    def test_mermaid_diagram_excludes_single_domain_concepts(
        self, template_dir, tmp_output_dir, sample_scores
    ):
        """Req 12.2: Only concepts in 2+ domains appear in diagram."""
        renderer = SiteRenderer(template_dir=template_dir, output_dir=tmp_output_dir)
        artifacts = PipelineArtifacts(scores=sample_scores)
        renderer.render_all(artifacts)

        content = (tmp_output_dir / "cross_domain.md").read_text()
        # Security Basics is single-domain, should not be in diagram
        assert "Security Basics" not in content

    def test_cross_reference_links_resolve_to_study_notes(
        self, template_dir, tmp_output_dir, sample_scores, sample_study_notes
    ):
        """Req 12.1: Cross-reference links between domains for concepts in 2+ domains."""
        renderer = SiteRenderer(template_dir=template_dir, output_dir=tmp_output_dir)
        artifacts = PipelineArtifacts(scores=sample_scores, study_notes=sample_study_notes)
        renderer.render_all(artifacts)

        content = (tmp_output_dir / "cross_domain.md").read_text()
        # Should contain links to study_notes.md with anchors
        assert "study_notes.md#" in content

    def test_integrative_themes_3_plus_domains(
        self, template_dir, tmp_output_dir, sample_scores, sample_study_notes
    ):
        """Req 12.4: Integrative summary for themes spanning 3+ domains."""
        renderer = SiteRenderer(template_dir=template_dir, output_dir=tmp_output_dir)
        artifacts = PipelineArtifacts(scores=sample_scores, study_notes=sample_study_notes)
        renderer.render_all(artifacts)

        content = (tmp_output_dir / "cross_domain.md").read_text()
        assert "Integrative Themes" in content
        assert "AI Safety and Governance" in content

    def test_related_topics_in_study_notes(
        self, template_dir, tmp_output_dir, sample_scores, sample_study_notes
    ):
        """Req 12.3: Related Topics section (1-10 entries) for cross-domain topics."""
        renderer = SiteRenderer(template_dir=template_dir, output_dir=tmp_output_dir)
        artifacts = PipelineArtifacts(scores=sample_scores, study_notes=sample_study_notes)
        renderer.render_all(artifacts)

        content = (tmp_output_dir / "study_notes.md").read_text()
        # Agent Architecture has related_topics, so Related Topics section should appear
        assert "Related Topics" in content
        assert "Uses tools" in content

    def test_related_topics_omitted_when_empty(
        self, template_dir, tmp_output_dir, sample_scores, sample_study_notes
    ):
        """Req 12.5: Omit Related Topics section for topics without connections."""
        renderer = SiteRenderer(template_dir=template_dir, output_dir=tmp_output_dir)
        artifacts = PipelineArtifacts(scores=sample_scores, study_notes=sample_study_notes)
        renderer.render_all(artifacts)

        content = (tmp_output_dir / "study_notes.md").read_text()
        # Security Basics has empty related_topics, section should be omitted
        # Check that after Security Basics heading, there's no Related Topics before next topic
        security_section_start = content.find("## Security Basics")
        next_section = content.find("---", security_section_start + 1)
        security_section = content[security_section_start:next_section]
        assert "Related Topics" not in security_section


class TestGenerateMkdocsNav:
    """Test dynamic mkdocs.yml nav generation."""

    def test_nav_includes_available_artifacts(self, template_dir, tmp_output_dir, sample_scores):
        renderer = SiteRenderer(template_dir=template_dir, output_dir=tmp_output_dir)
        artifacts = PipelineArtifacts(scores=sample_scores)
        nav = renderer._generate_mkdocs_nav(artifacts)

        # Should always have Home
        assert {"Home": "index.md"} in nav
        # Should have cross-domain page since scores are available
        assert {"Cross-Domain Connections": "cross_domain.md"} in nav

    def test_nav_excludes_missing_artifacts(self, template_dir, tmp_output_dir):
        renderer = SiteRenderer(template_dir=template_dir, output_dir=tmp_output_dir)
        artifacts = PipelineArtifacts()  # No artifacts loaded
        nav = renderer._generate_mkdocs_nav(artifacts)

        # Only Home should be present
        assert nav == [{"Home": "index.md"}]

    def test_nav_includes_all_sections_when_all_artifacts_present(
        self, template_dir, tmp_output_dir, sample_scores, sample_study_notes, sample_curriculum
    ):
        renderer = SiteRenderer(template_dir=template_dir, output_dir=tmp_output_dir)
        artifacts = PipelineArtifacts(
            scores=sample_scores,
            study_notes=sample_study_notes,
            curriculum=sample_curriculum,
        )
        nav = renderer._generate_mkdocs_nav(artifacts)

        nav_titles = [list(item.keys())[0] for item in nav]
        assert "Home" in nav_titles
        assert "Study Notes" in nav_titles
        assert "Curriculum" in nav_titles
        assert "Cross-Domain Connections" in nav_titles


class TestLoadArtifacts:
    """Test artifact loading from JSON files."""

    def test_loads_existing_artifacts(self, tmp_path):
        """Loads artifacts from JSON files that exist."""
        # Create a minimal scores artifact
        scores_data = {
            "topics": [
                {
                    "topic_id": "t-1",
                    "topic_name": "Test Topic",
                    "domain_ids": ["domain-1"],
                    "priority_score": 7,
                    "is_high_priority": False,
                    "domain_count": 1,
                }
            ]
        }
        (tmp_path / "phase03_scores.json").write_text(json.dumps(scores_data))

        artifacts = load_artifacts(tmp_path)
        assert artifacts.scores is not None
        assert len(artifacts.scores.topics) == 1
        assert artifacts.scores.topics[0].topic_name == "Test Topic"

    def test_handles_missing_files_gracefully(self, tmp_path):
        """Missing artifact files result in None attributes."""
        artifacts = load_artifacts(tmp_path)
        assert artifacts.scores is None
        assert artifacts.study_notes is None
        assert artifacts.curriculum is None

    def test_handles_invalid_json_gracefully(self, tmp_path):
        """Invalid JSON files don't crash loading."""
        (tmp_path / "phase03_scores.json").write_text("not valid json")
        artifacts = load_artifacts(tmp_path)
        assert artifacts.scores is None


class TestWriteMkdocsNav:
    """Test mkdocs.yml nav update logic."""

    def test_updates_nav_section_preserving_other_content(self, template_dir, tmp_path):
        """Mkdocs.yml nav is updated while preserving other sections."""
        output_dir = tmp_path / "docs"
        output_dir.mkdir()

        # Create a simple mkdocs.yml
        mkdocs_content = """site_name: Test Site

theme:
  name: material

nav:
  - Home: index.md
  - Old: old.md
"""
        (tmp_path / "mkdocs.yml").write_text(mkdocs_content)

        renderer = SiteRenderer(template_dir=template_dir, output_dir=output_dir)
        nav = [{"Home": "index.md"}, {"New Page": "new.md"}]
        renderer._write_mkdocs_nav(nav)

        updated = (tmp_path / "mkdocs.yml").read_text()
        assert "site_name: Test Site" in updated
        assert "New Page" in updated or "new.md" in updated
