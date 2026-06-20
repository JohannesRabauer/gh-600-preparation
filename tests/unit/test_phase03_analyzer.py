"""Unit tests for the RelevanceAnalyzer (Phase 3)."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from src.config import (
    CROSS_DOMAIN_BONUS,
    DOMAIN_WEIGHT_TO_BASE_SCORE,
    EXAM_DOMAINS,
    HIGH_PRIORITY_THRESHOLD,
    MAX_PRIORITY_SCORE,
    MIN_PRIORITY_SCORE,
)
from src.models.scoring import ScoredTopic, ScoredTopicList
from src.models.topic_map import CrossReference, Dependency, Topic, TopicHierarchy
from src.phases.phase03_analyzer import RelevanceAnalyzer


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


def _make_hierarchy(
    domains: dict[str, list[Topic]] | None = None,
    cross_references: list[CrossReference] | None = None,
    dependencies: list[Dependency] | None = None,
) -> TopicHierarchy:
    """Create a TopicHierarchy for testing."""
    if domains is None:
        domains = {}
    # Ensure all 6 domain keys exist
    for d in EXAM_DOMAINS:
        if d.id not in domains:
            domains[d.id] = []

    return TopicHierarchy(
        domains=domains,
        dependencies=dependencies or [],
        cross_references=cross_references or [],
        learning_order=[],
        learning_units=[],
    )


@pytest.fixture
def analyzer() -> RelevanceAnalyzer:
    """Provide a RelevanceAnalyzer with default domain weights."""
    return RelevanceAnalyzer()


@pytest.fixture
def custom_weights() -> dict[str, tuple[float, float]]:
    """Provide custom domain weights for testing."""
    return {
        "domain-high": (0.20, 0.25),    # 20-25% → base 8-9
        "domain-mid": (0.15, 0.20),     # 15-20% → base 6-8
        "domain-low": (0.10, 0.15),     # 10-15% → base 5-7
    }


# --- Tests ---


class TestRelevanceAnalyzerInit:
    """Tests for RelevanceAnalyzer initialization."""

    def test_default_weights_from_exam_domains(self) -> None:
        """Uses EXAM_DOMAINS weights by default."""
        analyzer = RelevanceAnalyzer()
        assert len(analyzer._domain_weights) == 6
        assert "domain-1" in analyzer._domain_weights
        assert analyzer._domain_weights["domain-1"] == (0.15, 0.20)

    def test_custom_weights(self, custom_weights: dict) -> None:
        """Accepts custom domain weight mapping."""
        analyzer = RelevanceAnalyzer(domain_weights=custom_weights)
        assert analyzer._domain_weights == custom_weights


class TestComputeBaseScore:
    """Tests for _compute_base_score method."""

    def test_high_weight_domain_scores_8_or_9(self, analyzer: RelevanceAnalyzer) -> None:
        """Domain with 20-25% weight gets base score 8-9."""
        # domain-2 has weight 20-25%
        topic = _make_topic("t-1", "Test", "domain-2")
        analyzer._topic_domain_map = {"t-1": ["domain-2"]}
        score = analyzer._compute_base_score(topic)
        assert 8 <= score <= 9

    def test_mid_weight_domain_scores_6_to_8(self, analyzer: RelevanceAnalyzer) -> None:
        """Domain with 15-20% weight gets base score 6-8."""
        # domain-1 has weight 15-20%
        topic = _make_topic("t-1", "Test", "domain-1")
        analyzer._topic_domain_map = {"t-1": ["domain-1"]}
        score = analyzer._compute_base_score(topic)
        assert 6 <= score <= 8

    def test_low_weight_domain_scores_5_to_7(self, analyzer: RelevanceAnalyzer) -> None:
        """Domain with 10-15% weight gets base score 5-7."""
        # domain-3 has weight 10-15%
        topic = _make_topic("t-1", "Test", "domain-3")
        analyzer._topic_domain_map = {"t-1": ["domain-3"]}
        score = analyzer._compute_base_score(topic)
        assert 5 <= score <= 7

    def test_unknown_domain_returns_min_score(self) -> None:
        """Unknown domain returns minimum priority score."""
        analyzer = RelevanceAnalyzer(domain_weights={"domain-x": (0.10, 0.15)})
        topic = _make_topic("t-1", "Test", "unknown-domain")
        analyzer._topic_domain_map = {"t-1": ["unknown-domain"]}
        score = analyzer._compute_base_score(topic)
        assert score == MIN_PRIORITY_SCORE

    def test_score_within_valid_range(self, analyzer: RelevanceAnalyzer) -> None:
        """All base scores are between MIN and MAX priority."""
        for domain in EXAM_DOMAINS:
            topic = _make_topic("t-1", "Test", domain.id)
            analyzer._topic_domain_map = {"t-1": [domain.id]}
            score = analyzer._compute_base_score(topic)
            assert MIN_PRIORITY_SCORE <= score <= MAX_PRIORITY_SCORE

    def test_domain2_scores_higher_than_domain3(self, analyzer: RelevanceAnalyzer) -> None:
        """Higher-weighted domains produce higher base scores."""
        # domain-2 (20-25%) should score higher than domain-3 (10-15%)
        topic_high = _make_topic("t-high", "High", "domain-2")
        topic_low = _make_topic("t-low", "Low", "domain-3")
        analyzer._topic_domain_map = {"t-high": ["domain-2"], "t-low": ["domain-3"]}

        score_high = analyzer._compute_base_score(topic_high)
        score_low = analyzer._compute_base_score(topic_low)
        assert score_high > score_low


class TestApplyCrossDomainBonus:
    """Tests for _apply_cross_domain_bonus method."""

    def test_single_domain_no_bonus(self, analyzer: RelevanceAnalyzer) -> None:
        """Topic in one domain gets no bonus."""
        topic = _make_topic("t-1", "Test", "domain-1")
        analyzer._topic_domain_map = {"t-1": ["domain-1"]}
        result = analyzer._apply_cross_domain_bonus(topic, 6)
        assert result == 6

    def test_two_domains_plus_one(self, analyzer: RelevanceAnalyzer) -> None:
        """Topic in two domains gets +1 bonus."""
        topic = _make_topic("t-1", "Test", "domain-1")
        analyzer._topic_domain_map = {"t-1": ["domain-1", "domain-2"]}
        result = analyzer._apply_cross_domain_bonus(topic, 6)
        assert result == 7

    def test_three_domains_plus_two(self, analyzer: RelevanceAnalyzer) -> None:
        """Topic in three domains gets +2 bonus."""
        topic = _make_topic("t-1", "Test", "domain-1")
        analyzer._topic_domain_map = {"t-1": ["domain-1", "domain-2", "domain-3"]}
        result = analyzer._apply_cross_domain_bonus(topic, 6)
        assert result == 8

    def test_capped_at_max_score(self, analyzer: RelevanceAnalyzer) -> None:
        """Bonus cannot exceed MAX_PRIORITY_SCORE (10)."""
        topic = _make_topic("t-1", "Test", "domain-1")
        analyzer._topic_domain_map = {
            "t-1": ["domain-1", "domain-2", "domain-3", "domain-4", "domain-5", "domain-6"]
        }
        result = analyzer._apply_cross_domain_bonus(topic, 9)
        assert result == MAX_PRIORITY_SCORE

    def test_bonus_from_base_1_with_many_domains(self, analyzer: RelevanceAnalyzer) -> None:
        """Low base + many domains still caps at 10."""
        topic = _make_topic("t-1", "Test", "domain-1")
        analyzer._topic_domain_map = {
            "t-1": [f"domain-{i}" for i in range(1, 7)]
        }
        # 5 additional domains * 1 bonus = +5, base 7 + 5 = 12, capped at 10
        result = analyzer._apply_cross_domain_bonus(topic, 7)
        assert result == MAX_PRIORITY_SCORE

    def test_never_below_min_score(self, analyzer: RelevanceAnalyzer) -> None:
        """Result is never below MIN_PRIORITY_SCORE."""
        topic = _make_topic("t-1", "Test", "domain-1")
        analyzer._topic_domain_map = {"t-1": ["domain-1"]}
        result = analyzer._apply_cross_domain_bonus(topic, MIN_PRIORITY_SCORE)
        assert result >= MIN_PRIORITY_SCORE


class TestSortTopics:
    """Tests for _sort_topics method."""

    def test_sorted_by_score_descending(self, analyzer: RelevanceAnalyzer) -> None:
        """Topics are sorted by descending priority score."""
        topics = [
            ScoredTopic(topic_id="t-1", topic_name="A", domain_ids=["d-1"],
                        priority_score=5, is_high_priority=False, domain_count=1),
            ScoredTopic(topic_id="t-2", topic_name="B", domain_ids=["d-1"],
                        priority_score=9, is_high_priority=True, domain_count=1),
            ScoredTopic(topic_id="t-3", topic_name="C", domain_ids=["d-1"],
                        priority_score=7, is_high_priority=False, domain_count=1),
        ]
        result = analyzer._sort_topics(topics)
        scores = [t.priority_score for t in result]
        assert scores == [9, 7, 5]

    def test_ties_broken_by_domain_count_descending(self, analyzer: RelevanceAnalyzer) -> None:
        """Equal scores broken by descending domain count."""
        topics = [
            ScoredTopic(topic_id="t-1", topic_name="A", domain_ids=["d-1"],
                        priority_score=7, is_high_priority=False, domain_count=1),
            ScoredTopic(topic_id="t-2", topic_name="B", domain_ids=["d-1", "d-2", "d-3"],
                        priority_score=7, is_high_priority=False, domain_count=3),
            ScoredTopic(topic_id="t-3", topic_name="C", domain_ids=["d-1", "d-2"],
                        priority_score=7, is_high_priority=False, domain_count=2),
        ]
        result = analyzer._sort_topics(topics)
        domain_counts = [t.domain_count for t in result]
        assert domain_counts == [3, 2, 1]

    def test_remaining_ties_broken_alphabetically(self, analyzer: RelevanceAnalyzer) -> None:
        """Equal score and domain count broken alphabetically by name."""
        topics = [
            ScoredTopic(topic_id="t-1", topic_name="Zebra", domain_ids=["d-1"],
                        priority_score=7, is_high_priority=False, domain_count=1),
            ScoredTopic(topic_id="t-2", topic_name="Apple", domain_ids=["d-1"],
                        priority_score=7, is_high_priority=False, domain_count=1),
            ScoredTopic(topic_id="t-3", topic_name="Mango", domain_ids=["d-1"],
                        priority_score=7, is_high_priority=False, domain_count=1),
        ]
        result = analyzer._sort_topics(topics)
        names = [t.topic_name for t in result]
        assert names == ["Apple", "Mango", "Zebra"]

    def test_empty_list_returns_empty(self, analyzer: RelevanceAnalyzer) -> None:
        """Sorting an empty list returns an empty list."""
        result = analyzer._sort_topics([])
        assert result == []


class TestHighPriorityFlagging:
    """Tests for high-priority flagging behavior."""

    def test_score_8_is_high_priority(self, analyzer: RelevanceAnalyzer) -> None:
        """Topics with score >= 8 are flagged as high-priority."""
        hierarchy = _make_hierarchy(
            domains={
                "domain-2": [_make_topic("t-1", "Important Topic", "domain-2")],
            }
        )
        result = analyzer.analyze(hierarchy)

        topic = next(t for t in result.topics if t.topic_id == "t-1")
        # domain-2 is 20-25% → base score 8-9
        assert topic.priority_score >= HIGH_PRIORITY_THRESHOLD
        assert topic.is_high_priority is True

    def test_low_score_not_high_priority(self, analyzer: RelevanceAnalyzer) -> None:
        """Topics with score < 8 are not flagged as high-priority."""
        hierarchy = _make_hierarchy(
            domains={
                "domain-3": [_make_topic("t-1", "Low Topic", "domain-3")],
            }
        )
        result = analyzer.analyze(hierarchy)

        topic = next(t for t in result.topics if t.topic_id == "t-1")
        # domain-3 is 10-15% → base score 5-7
        assert topic.priority_score < HIGH_PRIORITY_THRESHOLD
        assert topic.is_high_priority is False


class TestCrossDomainDetection:
    """Tests for cross-domain topic detection via cross-references."""

    def test_cross_reference_adds_domain(self, analyzer: RelevanceAnalyzer) -> None:
        """Cross-references expand domain associations."""
        topic_a = _make_topic("t-a", "Topic A", "domain-1")
        topic_b = _make_topic("t-b", "Topic B", "domain-4")

        hierarchy = _make_hierarchy(
            domains={
                "domain-1": [topic_a],
                "domain-4": [topic_b],
            },
            cross_references=[
                CrossReference(
                    topic_id_a="t-a",
                    topic_id_b="t-b",
                    shared_concept="access control",
                ),
            ],
        )

        result = analyzer.analyze(hierarchy)

        scored_a = next(t for t in result.topics if t.topic_id == "t-a")
        # t-a should now be associated with both domain-1 and domain-4
        assert scored_a.domain_count == 2
        assert "domain-1" in scored_a.domain_ids
        assert "domain-4" in scored_a.domain_ids

    def test_no_cross_references_single_domain(self, analyzer: RelevanceAnalyzer) -> None:
        """Without cross-references, topics stay in their single domain."""
        topic = _make_topic("t-1", "Solo Topic", "domain-3")
        hierarchy = _make_hierarchy(
            domains={"domain-3": [topic]},
        )

        result = analyzer.analyze(hierarchy)
        scored = next(t for t in result.topics if t.topic_id == "t-1")
        assert scored.domain_count == 1
        assert scored.domain_ids == ["domain-3"]


class TestAnalyzeIntegration:
    """Integration tests for the full analyze pipeline."""

    def test_produces_valid_scored_topic_list(self, analyzer: RelevanceAnalyzer) -> None:
        """analyze() produces a valid ScoredTopicList."""
        hierarchy = _make_hierarchy(
            domains={
                "domain-1": [_make_topic("t-1", "Architecture", "domain-1")],
                "domain-2": [_make_topic("t-2", "Implementation", "domain-2")],
                "domain-3": [_make_topic("t-3", "Performance", "domain-3")],
            }
        )

        result = analyzer.analyze(hierarchy)

        assert isinstance(result, ScoredTopicList)
        assert len(result.topics) == 3

        for topic in result.topics:
            assert MIN_PRIORITY_SCORE <= topic.priority_score <= MAX_PRIORITY_SCORE
            assert topic.domain_count >= 1
            assert len(topic.domain_ids) >= 1

    def test_output_is_sorted_correctly(self, analyzer: RelevanceAnalyzer) -> None:
        """Output topics are sorted by score desc, domain_count desc, name asc."""
        hierarchy = _make_hierarchy(
            domains={
                "domain-2": [_make_topic("t-high", "High Score", "domain-2")],
                "domain-3": [_make_topic("t-low", "Low Score", "domain-3")],
            }
        )

        result = analyzer.analyze(hierarchy)
        scores = [t.priority_score for t in result.topics]
        # Should be descending
        assert scores == sorted(scores, reverse=True)

    def test_all_topics_scored(self, analyzer: RelevanceAnalyzer) -> None:
        """Every topic in the hierarchy gets a score."""
        topics_per_domain = {
            "domain-1": [_make_topic(f"t-1-{i}", f"Topic 1-{i}", "domain-1") for i in range(3)],
            "domain-2": [_make_topic(f"t-2-{i}", f"Topic 2-{i}", "domain-2") for i in range(2)],
        }
        hierarchy = _make_hierarchy(domains=topics_per_domain)

        result = analyzer.analyze(hierarchy)
        assert len(result.topics) == 5

    def test_writes_artifact(self, tmp_path: Path, analyzer: RelevanceAnalyzer) -> None:
        """analyze() writes artifact to disk."""
        import src.phases.phase03_analyzer as analyzer_module

        original_dir = analyzer_module.ARTIFACTS_DIR
        analyzer_module.ARTIFACTS_DIR = str(tmp_path)

        try:
            hierarchy = _make_hierarchy(
                domains={
                    "domain-1": [_make_topic("t-1", "Test Topic", "domain-1")],
                }
            )
            analyzer.analyze(hierarchy)

            artifact_path = tmp_path / "phase03_scores.json"
            assert artifact_path.exists()

            data = json.loads(artifact_path.read_text(encoding="utf-8"))
            assert "topics" in data
            assert len(data["topics"]) == 1
            assert data["topics"][0]["topic_id"] == "t-1"
            assert "priority_score" in data["topics"][0]
            assert "is_high_priority" in data["topics"][0]
        finally:
            analyzer_module.ARTIFACTS_DIR = original_dir

    def test_cross_domain_bonus_increases_score(self, analyzer: RelevanceAnalyzer) -> None:
        """Cross-domain presence increases priority score."""
        topic_a = _make_topic("t-a", "Shared Concept", "domain-3")
        topic_b = _make_topic("t-b", "Related Concept", "domain-5")

        # One without cross-reference
        hierarchy_solo = _make_hierarchy(
            domains={"domain-3": [_make_topic("t-solo", "Solo", "domain-3")]},
        )
        result_solo = analyzer.analyze(hierarchy_solo)
        solo_score = result_solo.topics[0].priority_score

        # One with cross-reference
        hierarchy_cross = _make_hierarchy(
            domains={
                "domain-3": [topic_a],
                "domain-5": [topic_b],
            },
            cross_references=[
                CrossReference(
                    topic_id_a="t-a",
                    topic_id_b="t-b",
                    shared_concept="ci/cd",
                ),
            ],
        )
        result_cross = analyzer.analyze(hierarchy_cross)
        cross_topic = next(t for t in result_cross.topics if t.topic_id == "t-a")

        # Cross-domain topic should have higher score
        assert cross_topic.priority_score > solo_score
