"""Unit tests for the CurriculumBuilder (Phase 5)."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from src.config import (
    BLOOMS_TAXONOMY_VERBS,
    HIGH_PRIORITY_THRESHOLD,
    HIGH_PRIORITY_TIME_MULTIPLIER,
    MAX_MODULE_OBJECTIVES,
    MIN_MODULE_OBJECTIVES,
    MODULE_MAX_TIME_MINUTES,
    MODULE_MIN_TIME_MINUTES,
)
from src.models.curriculum import Curriculum, Module
from src.models.scoring import ScoredTopic, ScoredTopicList
from src.models.topic_map import CrossReference, Dependency, Topic, TopicHierarchy
from src.phases.phase05_curriculum import CurriculumBuilder


# --- Fixtures and helpers ---


def _make_topic(
    id: str,
    name: str,
    domain_id: str,
    knowledge_point_ids: list[str] | None = None,
) -> Topic:
    """Create a Topic for testing."""
    return Topic(
        id=id,
        name=name,
        domain_id=domain_id,
        knowledge_point_ids=knowledge_point_ids or ["kp-1"],
        description=f"Description for {name}",
    )


def _make_scored_topic(
    topic_id: str,
    topic_name: str,
    domain_ids: list[str],
    priority_score: int,
) -> ScoredTopic:
    """Create a ScoredTopic for testing."""
    return ScoredTopic(
        topic_id=topic_id,
        topic_name=topic_name,
        domain_ids=domain_ids,
        priority_score=priority_score,
        is_high_priority=priority_score >= HIGH_PRIORITY_THRESHOLD,
        domain_count=len(domain_ids),
    )


def _make_hierarchy(
    domains: dict[str, list[Topic]] | None = None,
    learning_order: list[str] | None = None,
    dependencies: list[Dependency] | None = None,
    cross_references: list[CrossReference] | None = None,
) -> TopicHierarchy:
    """Create a TopicHierarchy for testing."""
    if domains is None:
        domains = {}
    if learning_order is None:
        # Derive from domains
        learning_order = []
        for topic_list in domains.values():
            for topic in topic_list:
                learning_order.append(topic.id)

    return TopicHierarchy(
        domains=domains,
        dependencies=dependencies or [],
        cross_references=cross_references or [],
        learning_order=learning_order,
        learning_units=[],
    )


def _make_scores(scored_topics: list[ScoredTopic]) -> ScoredTopicList:
    """Create a ScoredTopicList for testing."""
    return ScoredTopicList(topics=scored_topics)


@pytest.fixture
def builder() -> CurriculumBuilder:
    """Provide a CurriculumBuilder instance."""
    return CurriculumBuilder()


@pytest.fixture
def simple_hierarchy() -> TopicHierarchy:
    """A simple hierarchy with 3 topics in 2 domains."""
    topics_d1 = [
        _make_topic("t-1", "Agent Architecture", "domain-1"),
        _make_topic("t-2", "SDLC Integration", "domain-1"),
    ]
    topics_d2 = [
        _make_topic("t-3", "Copilot Agent Mode", "domain-2"),
    ]
    return _make_hierarchy(
        domains={"domain-1": topics_d1, "domain-2": topics_d2},
        learning_order=["t-1", "t-2", "t-3"],
    )


@pytest.fixture
def simple_scores() -> ScoredTopicList:
    """Scores matching simple_hierarchy: t-1 high, t-2 mid, t-3 high."""
    return _make_scores([
        _make_scored_topic("t-1", "Agent Architecture", ["domain-1"], 9),
        _make_scored_topic("t-2", "SDLC Integration", ["domain-1"], 6),
        _make_scored_topic("t-3", "Copilot Agent Mode", ["domain-2"], 8),
    ])


# --- Tests ---


class TestCurriculumBuilderInit:
    """Tests for CurriculumBuilder initialization."""

    def test_bloom_verbs_loaded(self, builder: CurriculumBuilder) -> None:
        """Builder loads Bloom's Taxonomy verbs from config."""
        assert len(builder._bloom_verbs) > 0
        assert "define" in builder._bloom_verbs
        assert "evaluate" in builder._bloom_verbs
        assert "create" in builder._bloom_verbs


class TestValidateBloomVerbs:
    """Tests for _validate_bloom_verbs method."""

    def test_valid_objectives_pass(self, builder: CurriculumBuilder) -> None:
        """Valid objectives with Bloom's verbs pass validation."""
        objectives = [
            "Define agent architecture patterns",
            "Explain SDLC integration points",
            "Implement custom agent extensions",
        ]
        assert builder._validate_bloom_verbs(objectives) is True

    def test_too_few_objectives_fail(self, builder: CurriculumBuilder) -> None:
        """Fewer than 2 objectives fails validation."""
        objectives = ["Define agent architecture"]
        assert builder._validate_bloom_verbs(objectives) is False

    def test_too_many_objectives_fail(self, builder: CurriculumBuilder) -> None:
        """More than 7 objectives fails validation."""
        objectives = [
            f"Define concept {i}" for i in range(8)
        ]
        assert builder._validate_bloom_verbs(objectives) is False

    def test_non_bloom_verb_fails(self, builder: CurriculumBuilder) -> None:
        """Objective not starting with a Bloom's verb fails."""
        objectives = [
            "Define agent architecture",
            "Learn about SDLC",  # "Learn" is not a Bloom's verb
        ]
        assert builder._validate_bloom_verbs(objectives) is False

    def test_empty_objective_fails(self, builder: CurriculumBuilder) -> None:
        """Empty objective string fails validation."""
        objectives = ["Define something", ""]
        assert builder._validate_bloom_verbs(objectives) is False

    def test_case_insensitive_verb_matching(self, builder: CurriculumBuilder) -> None:
        """Verb matching is case-insensitive."""
        objectives = [
            "DEFINE agent architecture",
            "Explain integration points",
        ]
        assert builder._validate_bloom_verbs(objectives) is True

    def test_exactly_two_objectives_valid(self, builder: CurriculumBuilder) -> None:
        """Exactly 2 objectives (minimum) is valid."""
        objectives = [
            "Define key concepts",
            "Explain core patterns",
        ]
        assert builder._validate_bloom_verbs(objectives) is True

    def test_exactly_seven_objectives_valid(self, builder: CurriculumBuilder) -> None:
        """Exactly 7 objectives (maximum) is valid."""
        verbs = list(BLOOMS_TAXONOMY_VERBS)[:7]
        objectives = [f"{v.capitalize()} topic {i}" for i, v in enumerate(verbs)]
        assert builder._validate_bloom_verbs(objectives) is True


class TestEstimateTime:
    """Tests for _estimate_time method."""

    def test_high_priority_gets_multiplier(self, builder: CurriculumBuilder) -> None:
        """High-priority module gets 1.5× average non-HP time."""
        module = Module(
            id="M01",
            title="High Priority Module",
            topic_ids=["t-1"],
            objectives=["Define concepts", "Explain patterns"],
            prerequisites=["none"],
            time_estimate_minutes=15,  # placeholder
            contains_high_priority=True,
        )
        avg_time = 60.0
        result = builder._estimate_time(module, avg_time)
        expected = round(60.0 * HIGH_PRIORITY_TIME_MULTIPLIER)
        assert result == expected

    def test_non_high_priority_scales_by_topics(self, builder: CurriculumBuilder) -> None:
        """Non-HP module time scales by number of topics."""
        module = Module(
            id="M01",
            title="Normal Module",
            topic_ids=["t-1", "t-2"],
            objectives=["Define concepts", "Explain patterns"],
            prerequisites=["none"],
            time_estimate_minutes=15,
            contains_high_priority=False,
        )
        avg_time = 60.0
        result = builder._estimate_time(module, avg_time)
        # 2 topics × 30 min/topic = 60
        assert result == 60

    def test_time_clamped_to_minimum(self, builder: CurriculumBuilder) -> None:
        """Time estimate never goes below MODULE_MIN_TIME_MINUTES."""
        module = Module(
            id="M01",
            title="Tiny Module",
            topic_ids=["t-1"],
            objectives=["Define concepts", "Explain patterns"],
            prerequisites=["none"],
            time_estimate_minutes=15,
            contains_high_priority=False,
        )
        # Very low avg_time for HP case
        result = builder._estimate_time(module, 5.0)
        assert result >= MODULE_MIN_TIME_MINUTES

    def test_time_clamped_to_maximum(self, builder: CurriculumBuilder) -> None:
        """Time estimate never exceeds MODULE_MAX_TIME_MINUTES."""
        module = Module(
            id="M01",
            title="Huge Module",
            topic_ids=[f"t-{i}" for i in range(20)],
            objectives=["Define concepts", "Explain patterns"],
            prerequisites=["none"],
            time_estimate_minutes=15,
            contains_high_priority=False,
        )
        result = builder._estimate_time(module, 200.0)
        assert result <= MODULE_MAX_TIME_MINUTES

    def test_high_priority_time_clamped_to_max(self, builder: CurriculumBuilder) -> None:
        """High-priority with large avg still clamped to 180."""
        module = Module(
            id="M01",
            title="HP Module",
            topic_ids=["t-1"],
            objectives=["Define concepts", "Explain patterns"],
            prerequisites=["none"],
            time_estimate_minutes=15,
            contains_high_priority=True,
        )
        result = builder._estimate_time(module, 150.0)
        assert result <= MODULE_MAX_TIME_MINUTES


class TestCreateModules:
    """Tests for _create_modules method."""

    def test_single_topic_single_module(self, builder: CurriculumBuilder) -> None:
        """A single topic produces a single module."""
        builder._score_map = {
            "t-1": _make_scored_topic("t-1", "Topic A", ["domain-1"], 5)
        }
        topics = [_make_topic("t-1", "Topic A", "domain-1")]
        modules = builder._create_modules(topics)
        assert len(modules) == 1
        assert modules[0].id == "M01"
        assert modules[0].topic_ids == ["t-1"]

    def test_same_domain_grouped(self, builder: CurriculumBuilder) -> None:
        """Topics in the same domain are grouped into one module."""
        builder._score_map = {
            "t-1": _make_scored_topic("t-1", "A", ["domain-1"], 5),
            "t-2": _make_scored_topic("t-2", "B", ["domain-1"], 5),
        }
        topics = [
            _make_topic("t-1", "Topic A", "domain-1"),
            _make_topic("t-2", "Topic B", "domain-1"),
        ]
        modules = builder._create_modules(topics)
        assert len(modules) == 1
        assert set(modules[0].topic_ids) == {"t-1", "t-2"}

    def test_different_domains_split(self, builder: CurriculumBuilder) -> None:
        """Topics in different domains produce separate modules."""
        builder._score_map = {
            "t-1": _make_scored_topic("t-1", "A", ["domain-1"], 5),
            "t-2": _make_scored_topic("t-2", "B", ["domain-2"], 5),
        }
        topics = [
            _make_topic("t-1", "Topic A", "domain-1"),
            _make_topic("t-2", "Topic B", "domain-2"),
        ]
        modules = builder._create_modules(topics)
        assert len(modules) == 2
        assert modules[0].topic_ids == ["t-1"]
        assert modules[1].topic_ids == ["t-2"]

    def test_module_ids_sequential(self, builder: CurriculumBuilder) -> None:
        """Module IDs are sequential: M01, M02, M03..."""
        builder._score_map = {
            f"t-{i}": _make_scored_topic(f"t-{i}", f"T{i}", [f"domain-{i}"], 5)
            for i in range(1, 4)
        }
        topics = [
            _make_topic("t-1", "T1", "domain-1"),
            _make_topic("t-2", "T2", "domain-2"),
            _make_topic("t-3", "T3", "domain-3"),
        ]
        modules = builder._create_modules(topics)
        ids = [m.id for m in modules]
        assert ids == ["M01", "M02", "M03"]

    def test_empty_topics_returns_empty(self, builder: CurriculumBuilder) -> None:
        """Empty topic list produces no modules."""
        builder._score_map = {}
        modules = builder._create_modules([])
        assert modules == []

    def test_large_domain_splits_at_5(self, builder: CurriculumBuilder) -> None:
        """A domain with more than 5 topics splits into multiple modules."""
        builder._score_map = {
            f"t-{i}": _make_scored_topic(f"t-{i}", f"T{i}", ["domain-1"], 5)
            for i in range(1, 8)
        }
        topics = [
            _make_topic(f"t-{i}", f"Topic {i}", "domain-1")
            for i in range(1, 8)
        ]
        modules = builder._create_modules(topics)
        # 7 topics in same domain, max 5 per group → 2 modules
        assert len(modules) == 2
        assert len(modules[0].topic_ids) == 5
        assert len(modules[1].topic_ids) == 2


class TestPrerequisites:
    """Tests for prerequisite determination."""

    def test_first_module_has_none(
        self, builder: CurriculumBuilder, simple_hierarchy: TopicHierarchy, simple_scores: ScoredTopicList
    ) -> None:
        """First module has prerequisites = ['none']."""
        curriculum = builder.build(simple_hierarchy, simple_scores)
        assert curriculum.modules[0].prerequisites == ["none"]

    def test_subsequent_modules_reference_previous(
        self, builder: CurriculumBuilder, simple_hierarchy: TopicHierarchy, simple_scores: ScoredTopicList
    ) -> None:
        """Subsequent modules reference their predecessor."""
        curriculum = builder.build(simple_hierarchy, simple_scores)
        if len(curriculum.modules) > 1:
            second = curriculum.modules[1]
            assert second.prerequisites == [curriculum.modules[0].id]


class TestHighPriorityTimeMultiplier:
    """Tests for high-priority time estimation behavior."""

    def test_hp_module_time_greater_than_non_hp(
        self, builder: CurriculumBuilder
    ) -> None:
        """High-priority modules get more time than non-HP modules."""
        topics_d1 = [_make_topic("t-1", "Normal Topic", "domain-1")]
        topics_d2 = [_make_topic("t-2", "High Priority Topic", "domain-2")]

        hierarchy = _make_hierarchy(
            domains={"domain-1": topics_d1, "domain-2": topics_d2},
            learning_order=["t-1", "t-2"],
        )
        scores = _make_scores([
            _make_scored_topic("t-1", "Normal Topic", ["domain-1"], 5),
            _make_scored_topic("t-2", "High Priority Topic", ["domain-2"], 9),
        ])

        curriculum = builder.build(hierarchy, scores)

        # Find HP and non-HP modules
        hp_modules = [m for m in curriculum.modules if m.contains_high_priority]
        non_hp_modules = [m for m in curriculum.modules if not m.contains_high_priority]

        assert len(hp_modules) >= 1
        assert len(non_hp_modules) >= 1

        # HP module should have more time
        hp_time = hp_modules[0].time_estimate_minutes
        non_hp_time = non_hp_modules[0].time_estimate_minutes
        assert hp_time > non_hp_time


class TestBuildIntegration:
    """Integration tests for the full build pipeline."""

    def test_produces_valid_curriculum(
        self,
        builder: CurriculumBuilder,
        simple_hierarchy: TopicHierarchy,
        simple_scores: ScoredTopicList,
    ) -> None:
        """build() produces a valid Curriculum."""
        curriculum = builder.build(simple_hierarchy, simple_scores)

        assert isinstance(curriculum, Curriculum)
        assert len(curriculum.modules) > 0
        assert curriculum.total_time_minutes > 0
        assert len(curriculum.learning_path) == len(curriculum.modules)

    def test_total_time_is_sum_of_modules(
        self,
        builder: CurriculumBuilder,
        simple_hierarchy: TopicHierarchy,
        simple_scores: ScoredTopicList,
    ) -> None:
        """Total time equals sum of all module time estimates."""
        curriculum = builder.build(simple_hierarchy, simple_scores)
        expected_total = sum(m.time_estimate_minutes for m in curriculum.modules)
        assert curriculum.total_time_minutes == expected_total

    def test_learning_path_matches_module_order(
        self,
        builder: CurriculumBuilder,
        simple_hierarchy: TopicHierarchy,
        simple_scores: ScoredTopicList,
    ) -> None:
        """Learning path contains module IDs in order."""
        curriculum = builder.build(simple_hierarchy, simple_scores)
        module_ids = [m.id for m in curriculum.modules]
        assert curriculum.learning_path == module_ids

    def test_all_time_estimates_in_range(
        self,
        builder: CurriculumBuilder,
        simple_hierarchy: TopicHierarchy,
        simple_scores: ScoredTopicList,
    ) -> None:
        """All module time estimates are within [15, 180] minutes."""
        curriculum = builder.build(simple_hierarchy, simple_scores)
        for module in curriculum.modules:
            assert MODULE_MIN_TIME_MINUTES <= module.time_estimate_minutes <= MODULE_MAX_TIME_MINUTES

    def test_all_objectives_use_bloom_verbs(
        self,
        builder: CurriculumBuilder,
        simple_hierarchy: TopicHierarchy,
        simple_scores: ScoredTopicList,
    ) -> None:
        """All module objectives start with Bloom's Taxonomy verbs."""
        curriculum = builder.build(simple_hierarchy, simple_scores)
        for module in curriculum.modules:
            assert builder._validate_bloom_verbs(module.objectives)

    def test_objectives_count_in_range(
        self,
        builder: CurriculumBuilder,
        simple_hierarchy: TopicHierarchy,
        simple_scores: ScoredTopicList,
    ) -> None:
        """Each module has between 2 and 7 objectives."""
        curriculum = builder.build(simple_hierarchy, simple_scores)
        for module in curriculum.modules:
            assert MIN_MODULE_OBJECTIVES <= len(module.objectives) <= MAX_MODULE_OBJECTIVES

    def test_high_priority_flagging(
        self,
        builder: CurriculumBuilder,
        simple_hierarchy: TopicHierarchy,
        simple_scores: ScoredTopicList,
    ) -> None:
        """Modules containing high-priority topics are flagged."""
        curriculum = builder.build(simple_hierarchy, simple_scores)
        # t-1 has score 9 (high), t-2 has score 6 (not high)
        # t-1 and t-2 are in domain-1 → grouped together → module contains HP
        hp_modules = [m for m in curriculum.modules if m.contains_high_priority]
        assert len(hp_modules) >= 1

    def test_writes_artifact(
        self,
        builder: CurriculumBuilder,
        simple_hierarchy: TopicHierarchy,
        simple_scores: ScoredTopicList,
        tmp_path: Path,
    ) -> None:
        """build() writes artifact to disk."""
        import src.phases.phase05_curriculum as curriculum_module

        original_dir = curriculum_module.ARTIFACTS_DIR
        curriculum_module.ARTIFACTS_DIR = str(tmp_path)

        try:
            builder.build(simple_hierarchy, simple_scores)

            artifact_path = tmp_path / "phase05_curriculum.json"
            assert artifact_path.exists()

            data = json.loads(artifact_path.read_text(encoding="utf-8"))
            assert "modules" in data
            assert "total_time_minutes" in data
            assert "learning_path" in data
            assert len(data["modules"]) > 0
        finally:
            curriculum_module.ARTIFACTS_DIR = original_dir

    def test_respects_learning_order(self, builder: CurriculumBuilder) -> None:
        """Modules follow the learning_order from hierarchy."""
        # Learning order: t-3 before t-1
        topics_d1 = [_make_topic("t-1", "Architecture", "domain-1")]
        topics_d2 = [_make_topic("t-3", "Basics", "domain-2")]

        hierarchy = _make_hierarchy(
            domains={"domain-1": topics_d1, "domain-2": topics_d2},
            learning_order=["t-3", "t-1"],  # t-3 comes first
        )
        scores = _make_scores([
            _make_scored_topic("t-1", "Architecture", ["domain-1"], 6),
            _make_scored_topic("t-3", "Basics", ["domain-2"], 5),
        ])

        curriculum = builder.build(hierarchy, scores)

        # First module should contain t-3 (it comes first in learning order)
        assert "t-3" in curriculum.modules[0].topic_ids

    def test_from_artifacts_classmethod(self, tmp_path: Path) -> None:
        """from_artifacts() reads Phase 2 and Phase 3 files and builds."""
        # Create Phase 2 artifact
        hierarchy = _make_hierarchy(
            domains={
                "domain-1": [_make_topic("t-1", "Topic One", "domain-1")],
            },
            learning_order=["t-1"],
        )
        phase02_path = tmp_path / "phase02_topic_map.json"
        phase02_path.write_text(hierarchy.model_dump_json(indent=2), encoding="utf-8")

        # Create Phase 3 artifact
        scores = _make_scores([
            _make_scored_topic("t-1", "Topic One", ["domain-1"], 7),
        ])
        phase03_path = tmp_path / "phase03_scores.json"
        phase03_path.write_text(scores.model_dump_json(indent=2), encoding="utf-8")

        # Patch ARTIFACTS_DIR for output
        import src.phases.phase05_curriculum as curriculum_module

        original_dir = curriculum_module.ARTIFACTS_DIR
        curriculum_module.ARTIFACTS_DIR = str(tmp_path)

        try:
            curriculum = CurriculumBuilder.from_artifacts(
                topic_map_path=str(phase02_path),
                scores_path=str(phase03_path),
            )
            assert isinstance(curriculum, Curriculum)
            assert len(curriculum.modules) == 1
            assert curriculum.modules[0].topic_ids == ["t-1"]
        finally:
            curriculum_module.ARTIFACTS_DIR = original_dir
