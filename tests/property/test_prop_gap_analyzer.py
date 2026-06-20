"""Property-based tests for Phase 9: Gap Analyzer.

Tests correctness properties 19 and 20 from the design document:
- Property 19: Coverage Status Classification Consistency
- Property 20: Critical Gap Prioritization

**Validates: Requirements 9.1, 9.2, 9.3, 9.4, 9.5**
"""

from __future__ import annotations

from unittest.mock import patch

from hypothesis import given, settings, HealthCheck
from hypothesis import strategies as st

from src.config import (
    EXAM_DOMAINS,
    FULLY_COVERED_MIN_POINTS,
    HIGH_PRIORITY_THRESHOLD,
    MIN_RECOMMENDATIONS_PER_GAP,
    WEAKLY_COVERED_MIN_POINTS,
)
from src.models.gap_analysis import CoverageStatus, Gap, GapReport
from src.models.knowledge import ExtractionLog
from src.models.scoring import ExamObjective, ScoredTopic, ScoredTopicList
from src.models.study_notes import StudyNotesCollection, TopicNotes
from src.phases.phase09_gap import GapAnalyzer


# === Strategies ===

ALL_DOMAIN_IDS = [d.id for d in EXAM_DOMAINS]


@st.composite
def _exam_objective(
    draw: st.DrawFn,
    *,
    obj_index: int | None = None,
    domain_id: str | None = None,
    keyword: str | None = None,
) -> ExamObjective:
    """Generate a random ExamObjective.

    Args:
        draw: Hypothesis draw function.
        obj_index: If provided, used for deterministic ID generation.
        domain_id: If provided, forces this domain; otherwise random.
        keyword: If provided, includes this keyword in description.
    """
    if obj_index is None:
        obj_index = draw(st.integers(min_value=1, max_value=9999))
    if domain_id is None:
        domain_id = draw(st.sampled_from(ALL_DOMAIN_IDS))

    base_desc = draw(
        st.sampled_from([
            "Design agent architecture patterns",
            "Implement GitHub Copilot agent mode",
            "Configure agent tools and capabilities",
            "Evaluate agent performance metrics",
            "Secure agentic AI solutions",
            "Collaborate with AI agents in workflows",
        ])
    )

    if keyword:
        description = f"{base_desc} for {keyword}"
    else:
        description = base_desc

    num_bullets = draw(st.integers(min_value=1, max_value=4))
    sub_bullets = [
        f"Sub-bullet {i}: {description} detail {i}"
        for i in range(num_bullets)
    ]

    return ExamObjective(
        id=f"obj-{obj_index:04d}",
        domain_id=domain_id,
        description=description,
        sub_bullets=sub_bullets,
    )


@st.composite
def _topic_notes_for_objective(
    draw: st.DrawFn,
    *,
    objective: ExamObjective,
    key_facts_count: int,
) -> TopicNotes:
    """Generate TopicNotes that cover a given objective with a specific number of key facts.

    The note is guaranteed to match the objective by sharing keywords from
    the objective description in its topic_name.

    Args:
        draw: Hypothesis draw function.
        objective: The objective this note should cover.
        key_facts_count: Number of key facts (acts as knowledge points).
    """
    # Extract keywords from objective description for matching
    words = objective.description.split()
    # Use at least 2 words from the objective to ensure matching
    topic_name = " ".join(words[:3]) if len(words) >= 3 else objective.description

    key_facts = [f"Fact {i} about {topic_name}" for i in range(key_facts_count)]

    return TopicNotes(
        topic_id=f"topic-for-{objective.id}",
        topic_name=topic_name,
        domain_id=objective.domain_id,
        priority_score=draw(st.integers(min_value=1, max_value=10)),
        overview="Overview sentence one. Sentence two here. And sentence three.",
        explanation=" ".join(["word"] * 200),
        key_facts=key_facts,
        common_mistakes=["Mistake 1", "Mistake 2"],
        examples=["Example 1"],
        exam_tips=["Tip 1"],
        code_blocks=[],
        related_topics=[],
        is_supplemented=False,
    )


@st.composite
def _gap_analysis_inputs_with_controlled_coverage(
    draw: st.DrawFn,
    *,
    min_objectives: int = 2,
    max_objectives: int = 6,
) -> tuple[list[ExamObjective], StudyNotesCollection, ScoredTopicList, list[ExtractionLog], dict[str, int]]:
    """Generate controlled gap analysis inputs with known coverage levels.

    Returns objectives, notes, scores, extraction log, and a dictionary
    mapping objective_id -> expected knowledge_point_count so that tests
    can verify classification correctness.

    Args:
        draw: Hypothesis draw function.
        min_objectives: Minimum number of objectives.
        max_objectives: Maximum number of objectives.
    """
    num_objectives = draw(st.integers(min_value=min_objectives, max_value=max_objectives))

    objectives: list[ExamObjective] = []
    all_notes: list[TopicNotes] = []
    scored_topics: list[ScoredTopic] = []
    expected_points: dict[str, int] = {}

    for i in range(num_objectives):
        domain_id = draw(st.sampled_from(ALL_DOMAIN_IDS))

        # Choose a distinct keyword to ensure unique matching
        keyword = f"concept{i}"

        objective = ExamObjective(
            id=f"obj-{i:04d}",
            domain_id=domain_id,
            description=f"Understand {keyword} architecture patterns",
            sub_bullets=[f"Detail about {keyword}"],
        )
        objectives.append(objective)

        # Decide how many knowledge points this objective gets
        # This controls the coverage status
        point_count = draw(st.integers(min_value=0, max_value=6))
        expected_points[objective.id] = point_count

        # Create a note that matches this objective (shares keyword in topic_name)
        if point_count > 0:
            note = TopicNotes(
                topic_id=f"topic-{i:04d}",
                topic_name=f"Understanding {keyword} architecture patterns",
                domain_id=domain_id,
                priority_score=draw(st.integers(min_value=1, max_value=10)),
                overview="Overview one. Overview two. Overview three.",
                explanation=" ".join(["word"] * 200),
                key_facts=[f"Fact {j} about {keyword}" for j in range(point_count)],
                common_mistakes=["Mistake 1", "Mistake 2"],
                examples=["Example 1"],
                exam_tips=["Tip 1"],
                code_blocks=[],
                related_topics=[],
                is_supplemented=False,
            )
            all_notes.append(note)

        # Create scored topic for this domain
        priority_score = draw(st.integers(min_value=1, max_value=10))
        scored = ScoredTopic(
            topic_id=f"topic-{i:04d}",
            topic_name=f"Understanding {keyword} architecture patterns",
            domain_ids=[domain_id],
            priority_score=priority_score,
            is_high_priority=priority_score >= HIGH_PRIORITY_THRESHOLD,
            domain_count=1,
        )
        scored_topics.append(scored)

    notes_collection = StudyNotesCollection(
        notes=all_notes,
        cross_domain_themes=[],
    )
    scores = ScoredTopicList(topics=scored_topics)

    return objectives, notes_collection, scores, [], expected_points


@st.composite
def _gap_analysis_with_critical_gaps(
    draw: st.DrawFn,
    *,
    min_objectives: int = 3,
    max_objectives: int = 6,
) -> tuple[list[ExamObjective], StudyNotesCollection, ScoredTopicList, list[ExtractionLog]]:
    """Generate inputs guaranteed to produce critical gaps.

    Creates objectives where at least one has a high-priority scored topic
    (priority >= 8) AND has fewer than 3 knowledge points (gap condition).

    Args:
        draw: Hypothesis draw function.
        min_objectives: Minimum number of objectives.
        max_objectives: Maximum number of objectives.
    """
    num_objectives = draw(st.integers(min_value=min_objectives, max_value=max_objectives))

    objectives: list[ExamObjective] = []
    all_notes: list[TopicNotes] = []
    scored_topics: list[ScoredTopic] = []

    # Ensure at least one critical gap: high priority + weak/not covered
    critical_index = draw(st.integers(min_value=0, max_value=num_objectives - 1))

    for i in range(num_objectives):
        domain_id = draw(st.sampled_from(ALL_DOMAIN_IDS))
        keyword = f"concept{i}"

        objective = ExamObjective(
            id=f"obj-{i:04d}",
            domain_id=domain_id,
            description=f"Understand {keyword} architecture patterns",
            sub_bullets=[f"Detail about {keyword}"],
        )
        objectives.append(objective)

        if i == critical_index:
            # This one is a critical gap: high priority score, few/no points
            priority_score = draw(st.integers(min_value=HIGH_PRIORITY_THRESHOLD, max_value=10))
            point_count = draw(st.integers(min_value=0, max_value=FULLY_COVERED_MIN_POINTS - 1))
        else:
            # Random priority and coverage
            priority_score = draw(st.integers(min_value=1, max_value=10))
            point_count = draw(st.integers(min_value=0, max_value=6))

        # Create matching note if there are points
        if point_count > 0:
            note = TopicNotes(
                topic_id=f"topic-{i:04d}",
                topic_name=f"Understanding {keyword} architecture patterns",
                domain_id=domain_id,
                priority_score=priority_score,
                overview="Overview one. Overview two. Overview three.",
                explanation=" ".join(["word"] * 200),
                key_facts=[f"Fact {j} about {keyword}" for j in range(point_count)],
                common_mistakes=["Mistake 1", "Mistake 2"],
                examples=["Example 1"],
                exam_tips=["Tip 1"],
                code_blocks=[],
                related_topics=[],
                is_supplemented=False,
            )
            all_notes.append(note)

        scored = ScoredTopic(
            topic_id=f"topic-{i:04d}",
            topic_name=f"Understanding {keyword} architecture patterns",
            domain_ids=[domain_id],
            priority_score=priority_score,
            is_high_priority=priority_score >= HIGH_PRIORITY_THRESHOLD,
            domain_count=1,
        )
        scored_topics.append(scored)

    notes_collection = StudyNotesCollection(
        notes=all_notes,
        cross_domain_themes=[],
    )
    scores = ScoredTopicList(topics=scored_topics)

    return objectives, notes_collection, scores, []


# === Helpers ===


def _run_gap_analysis(
    objectives: list[ExamObjective],
    notes: StudyNotesCollection,
    scores: ScoredTopicList,
    extraction_log: list[ExtractionLog],
) -> GapReport:
    """Run the GapAnalyzer with _write_artifact patched out."""
    analyzer = GapAnalyzer(objectives)
    with patch.object(analyzer, "_write_artifact"):
        return analyzer.analyze(notes, scores, extraction_log)


# === Property 19: Coverage Status Classification Consistency ===


# Feature: gh-600-exam-prep, Property 19: Coverage Status Classification Consistency
class TestCoverageStatusClassificationConsistency:
    """For any objective:
    - If knowledge_point_count >= 3, status must be "fully_covered"
    - If knowledge_point_count is 1 or 2, status must be "weakly_covered"
    - If knowledge_point_count is 0, status must be "not_covered"

    The classification must be consistent across all objectives in the report,
    and the counts in the report must sum correctly.

    **Validates: Requirements 9.1, 9.2, 9.3**
    """

    @given(data=_gap_analysis_inputs_with_controlled_coverage())
    @settings(max_examples=50, deadline=30000, suppress_health_check=[HealthCheck.too_slow])
    def test_fully_covered_when_3_or_more_points(
        self,
        data: tuple[list[ExamObjective], StudyNotesCollection, ScoredTopicList, list[ExtractionLog], dict[str, int]],
    ) -> None:
        """Objectives with >= 3 knowledge points are classified as fully_covered."""
        objectives, notes, scores, log, expected_points = data
        report = _run_gap_analysis(objectives, notes, scores, log)

        for item in report.coverage_items:
            obj_id = item["objective_id"]
            point_count = item["point_count"]
            status = item["status"]

            if point_count >= FULLY_COVERED_MIN_POINTS:
                assert status == CoverageStatus.FULLY_COVERED.value, (
                    f"Objective '{obj_id}' has {point_count} points "
                    f"(>= {FULLY_COVERED_MIN_POINTS}) but status is '{status}', "
                    f"expected '{CoverageStatus.FULLY_COVERED.value}'"
                )

    @given(data=_gap_analysis_inputs_with_controlled_coverage())
    @settings(max_examples=50, deadline=30000, suppress_health_check=[HealthCheck.too_slow])
    def test_weakly_covered_when_1_or_2_points(
        self,
        data: tuple[list[ExamObjective], StudyNotesCollection, ScoredTopicList, list[ExtractionLog], dict[str, int]],
    ) -> None:
        """Objectives with 1-2 knowledge points are classified as weakly_covered."""
        objectives, notes, scores, log, expected_points = data
        report = _run_gap_analysis(objectives, notes, scores, log)

        for item in report.coverage_items:
            obj_id = item["objective_id"]
            point_count = item["point_count"]
            status = item["status"]

            if WEAKLY_COVERED_MIN_POINTS <= point_count < FULLY_COVERED_MIN_POINTS:
                assert status == CoverageStatus.WEAKLY_COVERED.value, (
                    f"Objective '{obj_id}' has {point_count} points "
                    f"(between {WEAKLY_COVERED_MIN_POINTS} and {FULLY_COVERED_MIN_POINTS - 1}) "
                    f"but status is '{status}', "
                    f"expected '{CoverageStatus.WEAKLY_COVERED.value}'"
                )

    @given(data=_gap_analysis_inputs_with_controlled_coverage())
    @settings(max_examples=50, deadline=30000, suppress_health_check=[HealthCheck.too_slow])
    def test_not_covered_when_0_points(
        self,
        data: tuple[list[ExamObjective], StudyNotesCollection, ScoredTopicList, list[ExtractionLog], dict[str, int]],
    ) -> None:
        """Objectives with 0 knowledge points are classified as not_covered."""
        objectives, notes, scores, log, expected_points = data
        report = _run_gap_analysis(objectives, notes, scores, log)

        for item in report.coverage_items:
            obj_id = item["objective_id"]
            point_count = item["point_count"]
            status = item["status"]

            if point_count == 0:
                assert status == CoverageStatus.NOT_COVERED.value, (
                    f"Objective '{obj_id}' has 0 points but status is '{status}', "
                    f"expected '{CoverageStatus.NOT_COVERED.value}'"
                )

    @given(data=_gap_analysis_inputs_with_controlled_coverage())
    @settings(max_examples=50, deadline=30000, suppress_health_check=[HealthCheck.too_slow])
    def test_coverage_counts_sum_to_total(
        self,
        data: tuple[list[ExamObjective], StudyNotesCollection, ScoredTopicList, list[ExtractionLog], dict[str, int]],
    ) -> None:
        """The sum of fully_covered + weakly_covered + not_covered equals total_objectives."""
        objectives, notes, scores, log, expected_points = data
        report = _run_gap_analysis(objectives, notes, scores, log)

        total_from_counts = (
            report.fully_covered_count
            + report.weakly_covered_count
            + report.not_covered_count
        )
        assert total_from_counts == report.total_objectives, (
            f"Coverage counts sum to {total_from_counts} "
            f"(fully={report.fully_covered_count}, "
            f"weak={report.weakly_covered_count}, "
            f"not_covered={report.not_covered_count}) "
            f"but total_objectives is {report.total_objectives}"
        )

    @given(data=_gap_analysis_inputs_with_controlled_coverage())
    @settings(max_examples=50, deadline=30000, suppress_health_check=[HealthCheck.too_slow])
    def test_coverage_items_count_matches_total_objectives(
        self,
        data: tuple[list[ExamObjective], StudyNotesCollection, ScoredTopicList, list[ExtractionLog], dict[str, int]],
    ) -> None:
        """The coverage_items list has exactly total_objectives entries."""
        objectives, notes, scores, log, expected_points = data
        report = _run_gap_analysis(objectives, notes, scores, log)

        assert len(report.coverage_items) == report.total_objectives, (
            f"coverage_items has {len(report.coverage_items)} entries "
            f"but total_objectives is {report.total_objectives}"
        )


# === Property 20: Critical Gap Prioritization ===


# Feature: gh-600-exam-prep, Property 20: Critical Gap Prioritization
class TestCriticalGapPrioritization:
    """All gaps with is_critical=True must appear in critical_gaps list.
    Critical gaps are those where the topic has Priority_Score >= 8 AND
    status is weakly_covered or not_covered. Each gap must have at least
    2 recommendations. Critical gaps section appears at the top (before
    weak_gaps and not_covered_gaps in report structure).

    **Validates: Requirements 9.4, 9.5**
    """

    @given(data=_gap_analysis_with_critical_gaps())
    @settings(max_examples=50, deadline=30000, suppress_health_check=[HealthCheck.too_slow])
    def test_all_critical_gaps_in_critical_section(
        self,
        data: tuple[list[ExamObjective], StudyNotesCollection, ScoredTopicList, list[ExtractionLog]],
    ) -> None:
        """Every gap with is_critical=True appears in the critical_gaps list."""
        objectives, notes, scores, log = data
        report = _run_gap_analysis(objectives, notes, scores, log)

        critical_gap_ids = {g.objective_id for g in report.critical_gaps}

        # Collect all gaps from all sections
        all_gaps = report.critical_gaps + report.weak_gaps + report.not_covered_gaps
        for gap in all_gaps:
            if gap.is_critical:
                assert gap.objective_id in critical_gap_ids, (
                    f"Gap '{gap.objective_id}' has is_critical=True but "
                    f"is not in the critical_gaps section. "
                    f"Found in weak_gaps or not_covered_gaps instead."
                )

    @given(data=_gap_analysis_with_critical_gaps())
    @settings(max_examples=50, deadline=30000, suppress_health_check=[HealthCheck.too_slow])
    def test_critical_gaps_are_not_fully_covered(
        self,
        data: tuple[list[ExamObjective], StudyNotesCollection, ScoredTopicList, list[ExtractionLog]],
    ) -> None:
        """No critical gap has status 'fully_covered'."""
        objectives, notes, scores, log = data
        report = _run_gap_analysis(objectives, notes, scores, log)

        for gap in report.critical_gaps:
            assert gap.status != CoverageStatus.FULLY_COVERED, (
                f"Critical gap '{gap.objective_id}' has status "
                f"'{gap.status.value}' — critical gaps must be "
                f"weakly_covered or not_covered, never fully_covered"
            )

    @given(data=_gap_analysis_with_critical_gaps())
    @settings(max_examples=50, deadline=30000, suppress_health_check=[HealthCheck.too_slow])
    def test_every_gap_has_minimum_recommendations(
        self,
        data: tuple[list[ExamObjective], StudyNotesCollection, ScoredTopicList, list[ExtractionLog]],
    ) -> None:
        """Every gap (critical, weak, or not_covered) has at least 2 recommendations."""
        objectives, notes, scores, log = data
        report = _run_gap_analysis(objectives, notes, scores, log)

        all_gaps = report.critical_gaps + report.weak_gaps + report.not_covered_gaps
        for gap in all_gaps:
            assert len(gap.recommendations) >= MIN_RECOMMENDATIONS_PER_GAP, (
                f"Gap '{gap.objective_id}' has {len(gap.recommendations)} "
                f"recommendations, expected >= {MIN_RECOMMENDATIONS_PER_GAP}"
            )

    @given(data=_gap_analysis_with_critical_gaps())
    @settings(max_examples=50, deadline=30000, suppress_health_check=[HealthCheck.too_slow])
    def test_recommendations_have_required_fields(
        self,
        data: tuple[list[ExamObjective], StudyNotesCollection, ScoredTopicList, list[ExtractionLog]],
    ) -> None:
        """Every recommendation has resource, description, and topic_area fields."""
        objectives, notes, scores, log = data
        report = _run_gap_analysis(objectives, notes, scores, log)

        all_gaps = report.critical_gaps + report.weak_gaps + report.not_covered_gaps
        for gap in all_gaps:
            for rec in gap.recommendations:
                assert "resource" in rec and rec["resource"], (
                    f"Gap '{gap.objective_id}' has a recommendation "
                    f"missing or empty 'resource' field: {rec}"
                )
                assert "description" in rec and rec["description"], (
                    f"Gap '{gap.objective_id}' has a recommendation "
                    f"missing or empty 'description' field: {rec}"
                )
                assert "topic_area" in rec and rec["topic_area"], (
                    f"Gap '{gap.objective_id}' has a recommendation "
                    f"missing or empty 'topic_area' field: {rec}"
                )

    @given(data=_gap_analysis_with_critical_gaps())
    @settings(max_examples=50, deadline=30000, suppress_health_check=[HealthCheck.too_slow])
    def test_non_critical_gaps_not_in_critical_section(
        self,
        data: tuple[list[ExamObjective], StudyNotesCollection, ScoredTopicList, list[ExtractionLog]],
    ) -> None:
        """Gaps with is_critical=False do not appear in the critical_gaps list."""
        objectives, notes, scores, log = data
        report = _run_gap_analysis(objectives, notes, scores, log)

        for gap in report.critical_gaps:
            assert gap.is_critical is True, (
                f"Gap '{gap.objective_id}' is in critical_gaps section "
                f"but has is_critical=False"
            )

    @given(data=_gap_analysis_inputs_with_controlled_coverage())
    @settings(max_examples=50, deadline=30000, suppress_health_check=[HealthCheck.too_slow])
    def test_fully_covered_objectives_not_in_any_gap_list(
        self,
        data: tuple[list[ExamObjective], StudyNotesCollection, ScoredTopicList, list[ExtractionLog], dict[str, int]],
    ) -> None:
        """Objectives classified as fully_covered do not appear in any gap list."""
        objectives, notes, scores, log, expected_points = data
        report = _run_gap_analysis(objectives, notes, scores, log)

        all_gap_ids = {g.objective_id for g in (
            report.critical_gaps + report.weak_gaps + report.not_covered_gaps
        )}

        for item in report.coverage_items:
            if item["status"] == CoverageStatus.FULLY_COVERED.value:
                assert item["objective_id"] not in all_gap_ids, (
                    f"Objective '{item['objective_id']}' is fully_covered "
                    f"but appears in a gap list"
                )
