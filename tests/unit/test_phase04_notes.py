"""Unit tests for the StudyNotesGenerator (Phase 4)."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from src.config import (
    HIGH_PRIORITY_THRESHOLD,
    MIN_COMMON_MISTAKES,
    MIN_EXAM_TIPS,
    MIN_EXAMPLES,
    MIN_EXAMPLES_HIGH_PRIORITY,
    MIN_EXPLANATION_WORDS,
    MIN_EXPLANATION_WORDS_HIGH_PRIORITY,
    MIN_KEY_FACTS,
    MIN_OVERVIEW_SENTENCES,
    SPARSE_TOPIC_KNOWLEDGE_POINT_THRESHOLD,
)
from src.models.scoring import ScoredTopic, ScoredTopicList
from src.models.study_notes import StudyNotesCollection, TopicNotes
from src.models.topic_map import (
    CrossReference,
    Dependency,
    Topic,
    TopicHierarchy,
)
from src.phases.phase04_notes import NotesConfig, StudyNotesGenerator


# --- Fixtures and helpers ---


def _make_topic(
    id: str = "topic-001",
    name: str = "Agent Architecture",
    domain_id: str = "domain-1",
    knowledge_point_ids: list[str] | None = None,
    description: str = "Designing patterns for AI agent systems.",
    sub_domain: str | None = None,
) -> Topic:
    """Create a Topic for testing."""
    return Topic(
        id=id,
        name=name,
        domain_id=domain_id,
        knowledge_point_ids=knowledge_point_ids or ["kp-1", "kp-2", "kp-3"],
        description=description,
        sub_domain=sub_domain,
    )


def _make_scored_topic(
    topic_id: str = "topic-001",
    topic_name: str = "Agent Architecture",
    domain_ids: list[str] | None = None,
    priority_score: int = 7,
    is_high_priority: bool = False,
    domain_count: int = 1,
) -> ScoredTopic:
    """Create a ScoredTopic for testing."""
    return ScoredTopic(
        topic_id=topic_id,
        topic_name=topic_name,
        domain_ids=domain_ids or ["domain-1"],
        priority_score=priority_score,
        is_high_priority=is_high_priority,
        domain_count=domain_count,
    )


def _make_hierarchy(
    domains: dict[str, list[Topic]] | None = None,
    cross_references: list[CrossReference] | None = None,
) -> TopicHierarchy:
    """Create a TopicHierarchy for testing."""
    if domains is None:
        domains = {"domain-1": [_make_topic()]}
    return TopicHierarchy(
        domains=domains,
        dependencies=[],
        cross_references=cross_references or [],
        learning_order=[],
        learning_units=[],
    )


def _make_scores(topics: list[ScoredTopic] | None = None) -> ScoredTopicList:
    """Create a ScoredTopicList for testing."""
    if topics is None:
        topics = [_make_scored_topic()]
    return ScoredTopicList(topics=topics)


@pytest.fixture
def generator() -> StudyNotesGenerator:
    """Provide a StudyNotesGenerator with default config."""
    return StudyNotesGenerator()


@pytest.fixture
def high_priority_topic() -> tuple[Topic, ScoredTopic]:
    """Provide a high-priority topic and its score."""
    topic = _make_topic(
        id="topic-hp",
        name="Copilot Agent Mode Implementation",
        domain_id="domain-2",
        knowledge_point_ids=["kp-1", "kp-2", "kp-3", "kp-4", "kp-5"],
        description="Implementing GitHub Copilot agent mode for development.",
    )
    score = _make_scored_topic(
        topic_id="topic-hp",
        topic_name="Copilot Agent Mode Implementation",
        domain_ids=["domain-2"],
        priority_score=9,
        is_high_priority=True,
        domain_count=1,
    )
    return topic, score


@pytest.fixture
def sparse_topic() -> tuple[Topic, ScoredTopic]:
    """Provide a sparse topic (< 3 knowledge points)."""
    topic = _make_topic(
        id="topic-sparse",
        name="Basic Concept",
        domain_id="domain-3",
        knowledge_point_ids=["kp-1", "kp-2"],
        description="A topic with limited knowledge points.",
    )
    score = _make_scored_topic(
        topic_id="topic-sparse",
        topic_name="Basic Concept",
        domain_ids=["domain-3"],
        priority_score=5,
        is_high_priority=False,
        domain_count=1,
    )
    return topic, score


# --- Tests ---


class TestStudyNotesGeneratorInit:
    """Tests for StudyNotesGenerator initialization."""

    def test_default_config(self) -> None:
        """Uses default NotesConfig values from src.config."""
        gen = StudyNotesGenerator()
        assert gen._config.min_overview_sentences == MIN_OVERVIEW_SENTENCES
        assert gen._config.min_explanation_words == MIN_EXPLANATION_WORDS
        assert gen._config.high_priority_threshold == HIGH_PRIORITY_THRESHOLD

    def test_custom_config(self) -> None:
        """Accepts custom NotesConfig."""
        config = NotesConfig(min_overview_sentences=5, min_key_facts=5)
        gen = StudyNotesGenerator(config=config)
        assert gen._config.min_overview_sentences == 5
        assert gen._config.min_key_facts == 5


class TestGenerateTopicNotes:
    """Tests for _generate_topic_notes method."""

    def test_overview_has_minimum_sentences(
        self, generator: StudyNotesGenerator
    ) -> None:
        """Overview contains at least MIN_OVERVIEW_SENTENCES sentences."""
        topic = _make_topic()
        score = _make_scored_topic()
        notes = generator._generate_topic_notes(topic, score)
        # Count sentences (rough: periods followed by space or end)
        sentences = [s.strip() for s in notes.overview.split(".") if s.strip()]
        assert len(sentences) >= MIN_OVERVIEW_SENTENCES

    def test_explanation_meets_min_word_count(
        self, generator: StudyNotesGenerator
    ) -> None:
        """Standard topic explanation has at least MIN_EXPLANATION_WORDS."""
        topic = _make_topic()
        score = _make_scored_topic(priority_score=5, is_high_priority=False)
        notes = generator._generate_topic_notes(topic, score)
        word_count = len(notes.explanation.split())
        assert word_count >= MIN_EXPLANATION_WORDS

    def test_high_priority_explanation_meets_400_words(
        self,
        generator: StudyNotesGenerator,
        high_priority_topic: tuple[Topic, ScoredTopic],
    ) -> None:
        """High-priority topic explanation has at least 400 words."""
        topic, score = high_priority_topic
        notes = generator._generate_topic_notes(topic, score)
        word_count = len(notes.explanation.split())
        assert word_count >= MIN_EXPLANATION_WORDS_HIGH_PRIORITY

    def test_key_facts_minimum_count(
        self, generator: StudyNotesGenerator
    ) -> None:
        """Key facts list has at least MIN_KEY_FACTS items."""
        topic = _make_topic()
        score = _make_scored_topic()
        notes = generator._generate_topic_notes(topic, score)
        assert len(notes.key_facts) >= MIN_KEY_FACTS

    def test_common_mistakes_minimum_count(
        self, generator: StudyNotesGenerator
    ) -> None:
        """Common mistakes list has at least MIN_COMMON_MISTAKES items."""
        topic = _make_topic()
        score = _make_scored_topic()
        notes = generator._generate_topic_notes(topic, score)
        assert len(notes.common_mistakes) >= MIN_COMMON_MISTAKES

    def test_examples_minimum_count_standard(
        self, generator: StudyNotesGenerator
    ) -> None:
        """Standard topic has at least MIN_EXAMPLES examples."""
        topic = _make_topic()
        score = _make_scored_topic(priority_score=5, is_high_priority=False)
        notes = generator._generate_topic_notes(topic, score)
        assert len(notes.examples) >= MIN_EXAMPLES

    def test_examples_minimum_count_high_priority(
        self,
        generator: StudyNotesGenerator,
        high_priority_topic: tuple[Topic, ScoredTopic],
    ) -> None:
        """High-priority topic has at least MIN_EXAMPLES_HIGH_PRIORITY."""
        topic, score = high_priority_topic
        notes = generator._generate_topic_notes(topic, score)
        assert len(notes.examples) >= MIN_EXAMPLES_HIGH_PRIORITY

    def test_exam_tips_minimum_count(
        self, generator: StudyNotesGenerator
    ) -> None:
        """Exam tips list has at least MIN_EXAM_TIPS items."""
        topic = _make_topic()
        score = _make_scored_topic()
        notes = generator._generate_topic_notes(topic, score)
        assert len(notes.exam_tips) >= MIN_EXAM_TIPS

    def test_procedure_topic_has_step_by_step(
        self, generator: StudyNotesGenerator
    ) -> None:
        """Procedure/workflow topic includes step-by-step instructions."""
        topic = _make_topic(
            name="Deploy Agent Pipeline",
            description="Steps to deploy an agent pipeline workflow.",
        )
        score = _make_scored_topic(topic_name="Deploy Agent Pipeline")
        notes = generator._generate_topic_notes(topic, score)
        assert notes.step_by_step is not None
        assert len(notes.step_by_step) > 0
        # Each step has {step, rationale}
        for item in notes.step_by_step:
            assert "step" in item
            assert "rationale" in item

    def test_non_procedure_topic_no_step_by_step(
        self, generator: StudyNotesGenerator
    ) -> None:
        """Non-procedure topic has step_by_step=None."""
        topic = _make_topic(
            name="Security Principles",
            description="Understanding security concepts for AI agents.",
        )
        score = _make_scored_topic(topic_name="Security Principles")
        notes = generator._generate_topic_notes(topic, score)
        assert notes.step_by_step is None

    def test_code_topic_has_code_blocks(
        self, generator: StudyNotesGenerator
    ) -> None:
        """Code/config topic includes code blocks with language and comments."""
        topic = _make_topic(
            name="API Configuration",
            description="Configure the API endpoint settings.",
        )
        score = _make_scored_topic(topic_name="API Configuration")
        notes = generator._generate_topic_notes(topic, score)
        assert len(notes.code_blocks) >= 1
        for block in notes.code_blocks:
            assert "language" in block
            assert "code" in block
            assert "comments" in block
            assert block["language"] != ""

    def test_non_code_topic_no_code_blocks(
        self, generator: StudyNotesGenerator
    ) -> None:
        """Non-code topic has empty code_blocks list."""
        topic = _make_topic(
            name="Ethics Framework",
            description="Understanding ethical principles for AI agents.",
        )
        score = _make_scored_topic(topic_name="Ethics Framework")
        notes = generator._generate_topic_notes(topic, score)
        assert notes.code_blocks == []

    def test_notes_contain_correct_metadata(
        self, generator: StudyNotesGenerator
    ) -> None:
        """Topic notes preserve correct topic_id, name, domain_id, score."""
        topic = _make_topic(id="t-42", name="Test Topic", domain_id="domain-2")
        score = _make_scored_topic(
            topic_id="t-42", priority_score=8, is_high_priority=True
        )
        notes = generator._generate_topic_notes(topic, score)
        assert notes.topic_id == "t-42"
        assert notes.topic_name == "Test Topic"
        assert notes.domain_id == "domain-2"
        assert notes.priority_score == 8


class TestBuildCrossReferences:
    """Tests for _build_cross_references method."""

    def test_cross_references_different_domains(
        self, generator: StudyNotesGenerator
    ) -> None:
        """References are found between topics in different domains."""
        topic_a = _make_topic(
            id="t-a",
            name="Agent Security Controls",
            domain_id="domain-4",
            description="Implementing access controls for AI agents.",
        )
        topic_b = _make_topic(
            id="t-b",
            name="Agent Access Management",
            domain_id="domain-1",
            description="Managing access controls in agent architecture.",
        )
        all_topics = [topic_a, topic_b]
        refs = generator._build_cross_references(topic_a, all_topics)
        # Should find topic_b as related (shares "access", "controls", "agent")
        assert len(refs) >= 1
        assert refs[0]["topic_id"] == "t-b"
        assert "domain_name" in refs[0]
        assert "relationship" in refs[0]

    def test_no_self_reference(
        self, generator: StudyNotesGenerator
    ) -> None:
        """A topic does not reference itself."""
        topic = _make_topic(id="t-a", name="Same Topic", domain_id="domain-1")
        refs = generator._build_cross_references(topic, [topic])
        assert len(refs) == 0

    def test_no_same_domain_reference(
        self, generator: StudyNotesGenerator
    ) -> None:
        """Topics in the same domain are not cross-referenced."""
        topic_a = _make_topic(
            id="t-a",
            name="Agent Security Controls",
            domain_id="domain-4",
            description="Implementing access controls for AI agents.",
        )
        topic_b = _make_topic(
            id="t-b",
            name="Agent Access Management",
            domain_id="domain-4",
            description="Managing access controls in agent architecture.",
        )
        refs = generator._build_cross_references(topic_a, [topic_a, topic_b])
        assert len(refs) == 0

    def test_no_reference_insufficient_overlap(
        self, generator: StudyNotesGenerator
    ) -> None:
        """Topics with < 2 keyword overlap are not referenced."""
        topic_a = _make_topic(
            id="t-a",
            name="Quantum Physics",
            domain_id="domain-1",
            description="Study of quantum phenomena.",
        )
        topic_b = _make_topic(
            id="t-b",
            name="Cooking Recipes",
            domain_id="domain-2",
            description="Collection of culinary methods.",
        )
        refs = generator._build_cross_references(topic_a, [topic_a, topic_b])
        assert len(refs) == 0


class TestSupplementSparseTopics:
    """Tests for _supplement_sparse_topics method."""

    def test_sets_is_supplemented_flag(
        self, generator: StudyNotesGenerator
    ) -> None:
        """Supplemented topics have is_supplemented=True."""
        topic = _make_topic(knowledge_point_ids=["kp-1"])
        score = _make_scored_topic(priority_score=5, is_high_priority=False)
        notes = generator._generate_topic_notes(topic, score)
        supplemented = generator._supplement_sparse_topics(notes)
        assert supplemented.is_supplemented is True

    def test_supplemented_content_has_marker(
        self, generator: StudyNotesGenerator
    ) -> None:
        """Supplemented content contains the visual indicator."""
        topic = _make_topic(
            knowledge_point_ids=["kp-1"],
            description="Minimal topic.",
        )
        score = _make_scored_topic(priority_score=5, is_high_priority=False)
        notes = generator._generate_topic_notes(topic, score)

        # Force explanation to be short for test
        short_notes = TopicNotes(
            **{**notes.model_dump(), "explanation": "Short text here."}
        )
        supplemented = generator._supplement_sparse_topics(short_notes)
        assert "> [!NOTE] Supplemented content" in supplemented.explanation

    def test_key_facts_supplemented_when_insufficient(
        self, generator: StudyNotesGenerator
    ) -> None:
        """Key facts are supplemented if below minimum count."""
        notes = TopicNotes(
            topic_id="t-1",
            topic_name="Sparse Topic",
            domain_id="domain-1",
            priority_score=5,
            overview="A. B. C.",
            explanation="Word " * 200,
            key_facts=["One fact"],
            common_mistakes=["Mistake 1", "Mistake 2"],
            examples=["Example 1"],
            exam_tips=["Tip 1"],
            code_blocks=[],
            related_topics=[],
            is_supplemented=False,
        )
        supplemented = generator._supplement_sparse_topics(notes)
        assert len(supplemented.key_facts) >= MIN_KEY_FACTS

    def test_examples_supplemented_when_insufficient(
        self, generator: StudyNotesGenerator
    ) -> None:
        """Examples are supplemented if below minimum count."""
        notes = TopicNotes(
            topic_id="t-1",
            topic_name="Sparse Topic",
            domain_id="domain-1",
            priority_score=5,
            overview="A. B. C.",
            explanation="Word " * 200,
            key_facts=["Fact 1", "Fact 2", "Fact 3"],
            common_mistakes=["Mistake 1", "Mistake 2"],
            examples=[],
            exam_tips=["Tip 1"],
            code_blocks=[],
            related_topics=[],
            is_supplemented=False,
        )
        supplemented = generator._supplement_sparse_topics(notes)
        assert len(supplemented.examples) >= MIN_EXAMPLES


class TestGenerateIntegration:
    """Integration tests for the full generate pipeline."""

    def test_produces_notes_for_all_topics(
        self, generator: StudyNotesGenerator
    ) -> None:
        """generate() produces notes for every topic in the hierarchy."""
        topics = [
            _make_topic(id="t-1", name="Topic A", domain_id="domain-1"),
            _make_topic(id="t-2", name="Topic B", domain_id="domain-2"),
            _make_topic(id="t-3", name="Topic C", domain_id="domain-3"),
        ]
        hierarchy = _make_hierarchy(
            domains={
                "domain-1": [topics[0]],
                "domain-2": [topics[1]],
                "domain-3": [topics[2]],
            }
        )
        scores = _make_scores(
            [
                _make_scored_topic(topic_id="t-1", priority_score=7),
                _make_scored_topic(topic_id="t-2", priority_score=9, is_high_priority=True),
                _make_scored_topic(topic_id="t-3", priority_score=5),
            ]
        )
        result = generator.generate(hierarchy, scores)
        assert isinstance(result, StudyNotesCollection)
        assert len(result.notes) == 3

    def test_sparse_topics_get_supplemented(
        self, generator: StudyNotesGenerator
    ) -> None:
        """Topics with < 3 knowledge points are supplemented."""
        sparse = _make_topic(
            id="t-sparse",
            name="Sparse Topic",
            domain_id="domain-1",
            knowledge_point_ids=["kp-1"],
        )
        hierarchy = _make_hierarchy(domains={"domain-1": [sparse]})
        scores = _make_scores(
            [_make_scored_topic(topic_id="t-sparse", priority_score=5)]
        )
        result = generator.generate(hierarchy, scores)
        sparse_notes = result.notes[0]
        assert sparse_notes.is_supplemented is True

    def test_non_sparse_topics_not_supplemented(
        self, generator: StudyNotesGenerator
    ) -> None:
        """Topics with >= 3 knowledge points are NOT supplemented."""
        normal = _make_topic(
            id="t-normal",
            name="Normal Topic",
            domain_id="domain-1",
            knowledge_point_ids=["kp-1", "kp-2", "kp-3"],
        )
        hierarchy = _make_hierarchy(domains={"domain-1": [normal]})
        scores = _make_scores(
            [_make_scored_topic(topic_id="t-normal", priority_score=7)]
        )
        result = generator.generate(hierarchy, scores)
        normal_notes = result.notes[0]
        assert normal_notes.is_supplemented is False

    def test_cross_domain_themes_from_cross_references(
        self, generator: StudyNotesGenerator
    ) -> None:
        """Cross-domain themes are identified from hierarchy cross-references."""
        topic_a = _make_topic(id="t-a", name="Topic A", domain_id="domain-1")
        topic_b = _make_topic(id="t-b", name="Topic B", domain_id="domain-4")
        hierarchy = _make_hierarchy(
            domains={"domain-1": [topic_a], "domain-4": [topic_b]},
            cross_references=[
                CrossReference(
                    topic_id_a="t-a",
                    topic_id_b="t-b",
                    shared_concept="access control",
                )
            ],
        )
        scores = _make_scores(
            [
                _make_scored_topic(topic_id="t-a", priority_score=7),
                _make_scored_topic(topic_id="t-b", priority_score=6),
            ]
        )
        result = generator.generate(hierarchy, scores)
        assert len(result.cross_domain_themes) >= 1
        theme = result.cross_domain_themes[0]
        assert "theme" in theme
        assert "domains" in theme
        assert "manifestations" in theme

    def test_writes_artifact(
        self, tmp_path: Path, generator: StudyNotesGenerator
    ) -> None:
        """generate() writes artifact to disk."""
        import src.phases.phase04_notes as notes_module

        original_dir = notes_module.ARTIFACTS_DIR
        notes_module.ARTIFACTS_DIR = str(tmp_path)

        try:
            topic = _make_topic(id="t-1", name="Test Topic", domain_id="domain-1")
            hierarchy = _make_hierarchy(domains={"domain-1": [topic]})
            scores = _make_scores(
                [_make_scored_topic(topic_id="t-1", priority_score=7)]
            )
            generator.generate(hierarchy, scores)

            artifact_path = tmp_path / "phase04_notes.json"
            assert artifact_path.exists()

            data = json.loads(artifact_path.read_text(encoding="utf-8"))
            assert "notes" in data
            assert "cross_domain_themes" in data
            assert len(data["notes"]) == 1
            assert data["notes"][0]["topic_id"] == "t-1"
        finally:
            notes_module.ARTIFACTS_DIR = original_dir

    def test_high_priority_topic_full_generation(
        self,
        generator: StudyNotesGenerator,
        high_priority_topic: tuple[Topic, ScoredTopic],
    ) -> None:
        """Full generation for high-priority topic meets all requirements."""
        topic, score = high_priority_topic
        hierarchy = _make_hierarchy(domains={"domain-2": [topic]})
        scores = _make_scores([score])
        result = generator.generate(hierarchy, scores)

        notes = result.notes[0]
        assert notes.priority_score >= HIGH_PRIORITY_THRESHOLD
        assert len(notes.explanation.split()) >= MIN_EXPLANATION_WORDS_HIGH_PRIORITY
        assert len(notes.examples) >= MIN_EXAMPLES_HIGH_PRIORITY
        assert len(notes.key_facts) >= MIN_KEY_FACTS
        assert len(notes.common_mistakes) >= MIN_COMMON_MISTAKES
        assert len(notes.exam_tips) >= MIN_EXAM_TIPS

    def test_topic_not_in_scores_gets_default_score(
        self, generator: StudyNotesGenerator
    ) -> None:
        """Topic not found in scores gets default priority_score=5."""
        topic = _make_topic(id="t-missing", name="Missing", domain_id="domain-1")
        hierarchy = _make_hierarchy(domains={"domain-1": [topic]})
        scores = _make_scores([])  # Empty scores list
        result = generator.generate(hierarchy, scores)
        assert result.notes[0].priority_score == 5


class TestCodeBlocks:
    """Tests for code block generation."""

    def test_yaml_code_block_for_config_topic(
        self, generator: StudyNotesGenerator
    ) -> None:
        """Config topics get YAML code blocks."""
        topic = _make_topic(
            name="Pipeline YAML Configuration",
            description="Configure YAML pipeline settings.",
        )
        score = _make_scored_topic()
        notes = generator._generate_topic_notes(topic, score)
        assert len(notes.code_blocks) >= 1
        assert notes.code_blocks[0]["language"] == "yaml"
        # Has inline comments
        assert "#" in notes.code_blocks[0]["code"]

    def test_json_code_block_for_api_topic(
        self, generator: StudyNotesGenerator
    ) -> None:
        """API topics get JSON code blocks."""
        topic = _make_topic(
            name="REST API Endpoint Design",
            description="Design REST API endpoints for agents.",
        )
        score = _make_scored_topic()
        notes = generator._generate_topic_notes(topic, score)
        assert len(notes.code_blocks) >= 1
        assert notes.code_blocks[0]["language"] == "json"

    def test_code_block_has_comments_field(
        self, generator: StudyNotesGenerator
    ) -> None:
        """Code blocks include a comments field explaining the code."""
        topic = _make_topic(
            name="CLI Command Scripts",
            description="Script commands for agent management.",
        )
        score = _make_scored_topic()
        notes = generator._generate_topic_notes(topic, score)
        assert len(notes.code_blocks) >= 1
        assert notes.code_blocks[0]["comments"] != ""
