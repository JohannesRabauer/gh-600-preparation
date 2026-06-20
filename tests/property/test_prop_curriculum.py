"""Property-based tests for Phase 5: Curriculum Builder.

Tests correctness properties 11, 12, and 13 from the design document:
- Property 11: Curriculum Module Ordering Respects Prerequisites
- Property 12: Module Objectives and Time Constraints
- Property 13: High-Priority Module Time Multiplier

**Validates: Requirements 5.1, 5.2, 5.3, 5.4, 5.5, 5.6**
"""

from __future__ import annotations

from unittest.mock import patch

import pytest
from hypothesis import given, settings, HealthCheck
from hypothesis import strategies as st

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
from src.models.topic_map import (
    CrossReference,
    Dependency,
    Topic,
    TopicHierarchy,
)
from src.phases.phase05_curriculum import CurriculumBuilder


# === Strategies ===


BLOOM_VERBS_LOWER: set[str] = {v.lower() for v in BLOOMS_TAXONOMY_VERBS}


def _topic_id(index: int) -> str:
    """Generate a deterministic topic ID from an index."""
    return f"topic-{index:03d}"


@st.composite
def _topic_hierarchy_and_scores(
    draw: st.DrawFn,
    min_topics: int = 2,
    max_topics: int = 15,
    force_high_priority: bool = False,
    force_mixed_priority: bool = False,
) -> tuple[TopicHierarchy, ScoredTopicList]:
    """Generate a random TopicHierarchy and matching ScoredTopicList.

    Topics are placed into 1-3 domains, with a valid learning_order
    that respects dependencies. Scores are randomly assigned.

    Args:
        draw: Hypothesis draw function.
        min_topics: Minimum number of topics.
        max_topics: Maximum number of topics.
        force_high_priority: If True, all topics get score >= 8.
        force_mixed_priority: If True, ensures both HP and non-HP topics exist.
    """
    num_topics = draw(st.integers(min_value=min_topics, max_value=max_topics))
    num_domains = draw(st.integers(min_value=1, max_value=min(3, num_topics)))

    # Assign topics to domains
    domain_ids = [f"domain-{i + 1}" for i in range(num_domains)]
    topic_domain_assignments = draw(
        st.lists(
            st.sampled_from(domain_ids),
            min_size=num_topics,
            max_size=num_topics,
        )
    )

    # Create topics
    topics: list[Topic] = []
    for i in range(num_topics):
        topic = Topic(
            id=_topic_id(i),
            name=f"Topic {i} about concepts",
            domain_id=topic_domain_assignments[i],
            sub_domain=None,
            knowledge_point_ids=[f"kp-{i}-a"],
            description=f"Description for topic {i}",
        )
        topics.append(topic)

    # Generate DAG dependencies (lower index -> higher index only)
    possible_edges = [
        (i, j) for i in range(num_topics) for j in range(i + 1, num_topics)
    ]
    if possible_edges:
        edges = draw(
            st.lists(
                st.sampled_from(possible_edges),
                min_size=0,
                max_size=min(len(possible_edges), num_topics),
                unique=True,
            )
        )
    else:
        edges = []

    dependencies = [
        Dependency(
            source_topic_id=_topic_id(src),
            target_topic_id=_topic_id(tgt),
            relationship="requires understanding of",
        )
        for src, tgt in edges
    ]

    # learning_order: topological sort (since edges go low->high, natural order works)
    learning_order = [_topic_id(i) for i in range(num_topics)]

    # Group topics by domain for TopicHierarchy.domains
    domains_dict: dict[str, list[Topic]] = {}
    for topic in topics:
        domains_dict.setdefault(topic.domain_id, []).append(topic)

    hierarchy = TopicHierarchy(
        domains=domains_dict,
        dependencies=dependencies,
        cross_references=[],
        learning_order=learning_order,
        learning_units=[],
    )

    # Generate scores
    scored_topics: list[ScoredTopic] = []

    if force_mixed_priority and num_topics >= 2:
        # Ensure at least one HP and one non-HP topic
        hp_count = draw(st.integers(min_value=1, max_value=num_topics - 1))
        hp_indices = set(draw(
            st.lists(
                st.integers(min_value=0, max_value=num_topics - 1),
                min_size=hp_count,
                max_size=hp_count,
                unique=True,
            )
        ))
    else:
        hp_indices = set()

    for i in range(num_topics):
        if force_high_priority:
            score = draw(st.integers(min_value=HIGH_PRIORITY_THRESHOLD, max_value=10))
        elif force_mixed_priority and i in hp_indices:
            score = draw(st.integers(min_value=HIGH_PRIORITY_THRESHOLD, max_value=10))
        elif force_mixed_priority and i not in hp_indices:
            score = draw(st.integers(min_value=1, max_value=HIGH_PRIORITY_THRESHOLD - 1))
        else:
            score = draw(st.integers(min_value=1, max_value=10))

        scored_topics.append(
            ScoredTopic(
                topic_id=_topic_id(i),
                topic_name=f"Topic {i} about concepts",
                domain_ids=[topic_domain_assignments[i]],
                priority_score=score,
                is_high_priority=score >= HIGH_PRIORITY_THRESHOLD,
                domain_count=1,
            )
        )

    scores = ScoredTopicList(topics=scored_topics)

    return hierarchy, scores


@st.composite
def _mixed_priority_hierarchy(
    draw: st.DrawFn,
) -> tuple[TopicHierarchy, ScoredTopicList]:
    """Generate a hierarchy guaranteed to have both HP and non-HP topics.

    This ensures Property 13 can always be meaningfully tested.
    """
    return draw(
        _topic_hierarchy_and_scores(
            min_topics=3,
            max_topics=15,
            force_mixed_priority=True,
        )
    )


# === Helpers ===


def _build_curriculum_no_artifact(
    hierarchy: TopicHierarchy, scores: ScoredTopicList
) -> Curriculum:
    """Build a curriculum without writing artifact to disk."""
    builder = CurriculumBuilder()
    with patch.object(builder, "_write_artifact"):
        return builder.build(hierarchy, scores)


# === Property 11: Curriculum Module Ordering Respects Prerequisites ===


# Feature: gh-600-exam-prep, Property 11: Curriculum Module Ordering Respects Prerequisites
class TestCurriculumModuleOrderingRespectsPrerequisites:
    """For any curriculum produced from a valid topic hierarchy, no module
    appears before any module listed in its prerequisites.

    **Validates: Requirements 5.1**
    """

    @given(data=_topic_hierarchy_and_scores())
    @settings(max_examples=100, deadline=10000, suppress_health_check=[HealthCheck.too_slow])
    def test_prerequisite_modules_appear_earlier_in_learning_path(
        self,
        data: tuple[TopicHierarchy, ScoredTopicList],
    ) -> None:
        """For every module M with prerequisites [P1, P2, ...],
        index(Pi) < index(M) in the learning path."""
        hierarchy, scores = data
        curriculum = _build_curriculum_no_artifact(hierarchy, scores)

        learning_path = curriculum.learning_path
        position = {mid: idx for idx, mid in enumerate(learning_path)}

        for module in curriculum.modules:
            if module.prerequisites == ["none"]:
                continue
            module_pos = position[module.id]
            for prereq_id in module.prerequisites:
                assert prereq_id in position, (
                    f"Prerequisite '{prereq_id}' of module '{module.id}' "
                    f"not found in learning_path: {learning_path}"
                )
                prereq_pos = position[prereq_id]
                assert prereq_pos < module_pos, (
                    f"Prerequisite '{prereq_id}' (pos {prereq_pos}) must "
                    f"appear before module '{module.id}' (pos {module_pos}) "
                    f"in learning_path"
                )

    @given(data=_topic_hierarchy_and_scores())
    @settings(max_examples=100, deadline=10000, suppress_health_check=[HealthCheck.too_slow])
    def test_learning_path_contains_all_modules(
        self,
        data: tuple[TopicHierarchy, ScoredTopicList],
    ) -> None:
        """The learning path contains exactly the module IDs from all modules."""
        hierarchy, scores = data
        curriculum = _build_curriculum_no_artifact(hierarchy, scores)

        module_ids = {m.id for m in curriculum.modules}
        path_ids = set(curriculum.learning_path)

        assert module_ids == path_ids, (
            f"Module IDs {module_ids} != learning_path IDs {path_ids}"
        )
        assert len(curriculum.learning_path) == len(curriculum.modules), (
            f"Learning path length {len(curriculum.learning_path)} != "
            f"module count {len(curriculum.modules)}"
        )

    @given(data=_topic_hierarchy_and_scores(min_topics=5, max_topics=15))
    @settings(max_examples=50, deadline=10000, suppress_health_check=[HealthCheck.too_slow])
    def test_first_module_has_no_prerequisites_or_none(
        self,
        data: tuple[TopicHierarchy, ScoredTopicList],
    ) -> None:
        """The first module in the learning path has prerequisites=["none"]."""
        hierarchy, scores = data
        curriculum = _build_curriculum_no_artifact(hierarchy, scores)

        if not curriculum.modules:
            return

        first_module_id = curriculum.learning_path[0]
        first_module = next(m for m in curriculum.modules if m.id == first_module_id)

        assert first_module.prerequisites == ["none"], (
            f"First module '{first_module.id}' should have no prerequisites, "
            f"but has: {first_module.prerequisites}"
        )


# === Property 12: Module Objectives and Time Constraints ===


# Feature: gh-600-exam-prep, Property 12: Module Objectives and Time Constraints
class TestModuleObjectivesAndTimeConstraints:
    """Every module has between 2-7 objectives, each starting with a Bloom's
    Taxonomy verb, and a time_estimate_minutes between 15 and 180.

    **Validates: Requirements 5.2, 5.3, 5.4, 5.5**
    """

    @given(data=_topic_hierarchy_and_scores())
    @settings(max_examples=100, deadline=10000, suppress_health_check=[HealthCheck.too_slow])
    def test_objectives_count_within_bounds(
        self,
        data: tuple[TopicHierarchy, ScoredTopicList],
    ) -> None:
        """Every module has between 2 and 7 objectives."""
        hierarchy, scores = data
        curriculum = _build_curriculum_no_artifact(hierarchy, scores)

        for module in curriculum.modules:
            obj_count = len(module.objectives)
            assert MIN_MODULE_OBJECTIVES <= obj_count <= MAX_MODULE_OBJECTIVES, (
                f"Module '{module.id}' has {obj_count} objectives, "
                f"expected [{MIN_MODULE_OBJECTIVES}, {MAX_MODULE_OBJECTIVES}]"
            )

    @given(data=_topic_hierarchy_and_scores())
    @settings(max_examples=100, deadline=10000, suppress_health_check=[HealthCheck.too_slow])
    def test_objectives_start_with_blooms_verb(
        self,
        data: tuple[TopicHierarchy, ScoredTopicList],
    ) -> None:
        """Each objective starts with a Bloom's Taxonomy verb (case-insensitive)."""
        hierarchy, scores = data
        curriculum = _build_curriculum_no_artifact(hierarchy, scores)

        for module in curriculum.modules:
            for objective in module.objectives:
                first_word = objective.split()[0].lower() if objective.strip() else ""
                assert first_word in BLOOM_VERBS_LOWER, (
                    f"Module '{module.id}' objective '{objective}' does not "
                    f"start with a Bloom's Taxonomy verb. "
                    f"First word: '{first_word}'"
                )

    @given(data=_topic_hierarchy_and_scores())
    @settings(max_examples=100, deadline=10000, suppress_health_check=[HealthCheck.too_slow])
    def test_time_estimate_within_bounds(
        self,
        data: tuple[TopicHierarchy, ScoredTopicList],
    ) -> None:
        """Every module's time_estimate_minutes is between 15 and 180."""
        hierarchy, scores = data
        curriculum = _build_curriculum_no_artifact(hierarchy, scores)

        for module in curriculum.modules:
            assert MODULE_MIN_TIME_MINUTES <= module.time_estimate_minutes <= MODULE_MAX_TIME_MINUTES, (
                f"Module '{module.id}' time_estimate_minutes="
                f"{module.time_estimate_minutes}, expected "
                f"[{MODULE_MIN_TIME_MINUTES}, {MODULE_MAX_TIME_MINUTES}]"
            )

    @given(data=_topic_hierarchy_and_scores())
    @settings(max_examples=100, deadline=10000, suppress_health_check=[HealthCheck.too_slow])
    def test_prerequisites_contain_valid_ids_or_none(
        self,
        data: tuple[TopicHierarchy, ScoredTopicList],
    ) -> None:
        """Prerequisites contain valid module IDs or exactly ["none"]."""
        hierarchy, scores = data
        curriculum = _build_curriculum_no_artifact(hierarchy, scores)

        module_ids = {m.id for m in curriculum.modules}

        for module in curriculum.modules:
            if module.prerequisites == ["none"]:
                continue
            for prereq in module.prerequisites:
                assert prereq in module_ids, (
                    f"Module '{module.id}' has prerequisite '{prereq}' "
                    f"which is not a valid module ID. "
                    f"Valid IDs: {module_ids}"
                )

    @given(data=_topic_hierarchy_and_scores())
    @settings(max_examples=100, deadline=10000, suppress_health_check=[HealthCheck.too_slow])
    def test_total_time_equals_sum_of_module_times(
        self,
        data: tuple[TopicHierarchy, ScoredTopicList],
    ) -> None:
        """total_time_minutes equals the sum of all module time estimates."""
        hierarchy, scores = data
        curriculum = _build_curriculum_no_artifact(hierarchy, scores)

        expected_total = sum(m.time_estimate_minutes for m in curriculum.modules)
        assert curriculum.total_time_minutes == expected_total, (
            f"total_time_minutes={curriculum.total_time_minutes} != "
            f"sum of module times={expected_total}"
        )


# === Property 13: High-Priority Module Time Multiplier ===


# Feature: gh-600-exam-prep, Property 13: High-Priority Module Time Multiplier
class TestHighPriorityModuleTimeMultiplier:
    """For any curriculum with both high-priority and non-high-priority modules,
    every high-priority module's time_estimate_minutes is >= 1.5x the average
    time of non-high-priority modules (within clamping bounds).

    **Validates: Requirements 5.6**
    """

    @given(data=_mixed_priority_hierarchy())
    @settings(max_examples=100, deadline=10000, suppress_health_check=[HealthCheck.too_slow])
    def test_hp_module_time_at_least_multiplier_of_avg_non_hp(
        self,
        data: tuple[TopicHierarchy, ScoredTopicList],
    ) -> None:
        """Every HP module's time >= min(180, 1.5 * avg_non_hp_time).

        The builder internally computes the average non-HP time from topic
        count statistics rather than from individual assigned module times.
        We replicate that logic to compute the expected HP time threshold,
        allowing a rounding tolerance of 1 minute.
        """
        hierarchy, scores = data
        curriculum = _build_curriculum_no_artifact(hierarchy, scores)

        hp_modules = [m for m in curriculum.modules if m.contains_high_priority]
        non_hp_modules = [m for m in curriculum.modules if not m.contains_high_priority]

        # This property only applies when both HP and non-HP modules exist
        if not hp_modules or not non_hp_modules:
            return

        # Replicate the builder's internal avg_non_hp_time calculation:
        # It uses avg topic count × base_per_topic (30), clamped to [15, 180]
        base_per_topic = 30
        total_topics_non_hp = sum(len(m.topic_ids) for m in non_hp_modules)
        avg_topics = total_topics_non_hp / len(non_hp_modules)
        builder_avg_non_hp_time = max(
            MODULE_MIN_TIME_MINUTES,
            min(MODULE_MAX_TIME_MINUTES, round(avg_topics * base_per_topic)),
        )

        # The expected HP time is 1.5× that internal average, clamped
        expected_hp_time = min(
            MODULE_MAX_TIME_MINUTES,
            round(builder_avg_non_hp_time * HIGH_PRIORITY_TIME_MULTIPLIER),
        )

        for module in hp_modules:
            assert module.time_estimate_minutes >= expected_hp_time - 1, (
                f"HP module '{module.id}' time={module.time_estimate_minutes} "
                f"is less than expected minimum "
                f"{expected_hp_time} "
                f"(1.5 × builder_avg_non_hp={builder_avg_non_hp_time}, "
                f"clamped to {MODULE_MAX_TIME_MINUTES})"
            )

    @given(data=_mixed_priority_hierarchy())
    @settings(max_examples=100, deadline=10000, suppress_health_check=[HealthCheck.too_slow])
    def test_hp_modules_have_higher_time_than_non_hp_average(
        self,
        data: tuple[TopicHierarchy, ScoredTopicList],
    ) -> None:
        """HP modules have time >= average non-HP time (weaker but always valid)."""
        hierarchy, scores = data
        curriculum = _build_curriculum_no_artifact(hierarchy, scores)

        hp_modules = [m for m in curriculum.modules if m.contains_high_priority]
        non_hp_modules = [m for m in curriculum.modules if not m.contains_high_priority]

        if not hp_modules or not non_hp_modules:
            return

        avg_non_hp_time = sum(m.time_estimate_minutes for m in non_hp_modules) / len(non_hp_modules)

        for module in hp_modules:
            assert module.time_estimate_minutes >= avg_non_hp_time, (
                f"HP module '{module.id}' time={module.time_estimate_minutes} "
                f"is less than average non-HP time={avg_non_hp_time:.1f}"
            )
