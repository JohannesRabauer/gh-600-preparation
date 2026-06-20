"""Property-based tests for Phase 10: Readiness Assessor.

Tests correctness properties 21, 22, and 23 from the design document:
- Property 21: Readiness Score Calculation
- Property 22: High-Risk Topic Constraints
- Property 23: Readiness Score Triggers Deferral Recommendation

**Validates: Requirements 10.1, 10.2, 10.3, 10.5**
"""

from __future__ import annotations

from unittest.mock import patch

from hypothesis import given, settings, HealthCheck
from hypothesis import strategies as st

from src.config import (
    EXAM_DOMAINS,
    HIGH_PRIORITY_THRESHOLD,
    MAX_HIGH_RISK_TOPICS,
    READINESS_DEFERRAL_THRESHOLD,
)
from src.models.gap_analysis import CoverageStatus, Gap, GapReport
from src.models.readiness import (
    HighRiskTopic,
    ReadinessAssessment,
    RemediationPlan,
)
from src.models.scoring import ScoredTopic, ScoredTopicList
from src.models.study_notes import StudyNotesCollection, TopicNotes
from src.phases.phase10_readiness import ReadinessAssessor


# === Strategies ===

ALL_DOMAIN_IDS = [d.id for d in EXAM_DOMAINS]


@st.composite
def _gap_report(
    draw: st.DrawFn,
    *,
    min_objectives: int = 2,
    max_objectives: int = 10,
) -> GapReport:
    """Generate a random GapReport with controlled coverage counts.

    Ensures that fully_covered + weakly_covered + not_covered == total_objectives
    and that gap lists are consistent with counts.
    """
    total = draw(st.integers(min_value=min_objectives, max_value=max_objectives))

    # Decide counts for each category
    fully_covered = draw(st.integers(min_value=0, max_value=total))
    remaining = total - fully_covered
    weakly_covered = draw(st.integers(min_value=0, max_value=remaining))
    not_covered = remaining - weakly_covered

    coverage_items: list[dict] = []
    critical_gaps: list[Gap] = []
    weak_gaps: list[Gap] = []
    not_covered_gaps: list[Gap] = []

    obj_index = 0

    # Generate fully covered objectives (no gaps)
    for _ in range(fully_covered):
        domain_id = draw(st.sampled_from(ALL_DOMAIN_IDS))
        coverage_items.append({
            "objective_id": f"obj-{obj_index:04d}",
            "status": CoverageStatus.FULLY_COVERED.value,
            "point_count": draw(st.integers(min_value=3, max_value=8)),
        })
        obj_index += 1

    # Generate weakly covered objectives (gaps with 1-2 points)
    for _ in range(weakly_covered):
        domain_id = draw(st.sampled_from(ALL_DOMAIN_IDS))
        point_count = draw(st.integers(min_value=1, max_value=2))
        obj_id = f"obj-{obj_index:04d}"
        is_critical = draw(st.booleans())

        gap = Gap(
            objective_id=obj_id,
            objective_description=f"Understand concept {obj_index}",
            domain_id=domain_id,
            status=CoverageStatus.WEAKLY_COVERED,
            knowledge_point_count=point_count,
            is_critical=is_critical,
            recommendations=[
                {"resource": "Resource A", "description": "Desc A", "topic_area": "Area A"},
                {"resource": "Resource B", "description": "Desc B", "topic_area": "Area B"},
            ],
        )

        if is_critical:
            critical_gaps.append(gap)
        else:
            weak_gaps.append(gap)

        coverage_items.append({
            "objective_id": obj_id,
            "status": CoverageStatus.WEAKLY_COVERED.value,
            "point_count": point_count,
        })
        obj_index += 1

    # Generate not covered objectives (gaps with 0 points)
    for _ in range(not_covered):
        domain_id = draw(st.sampled_from(ALL_DOMAIN_IDS))
        obj_id = f"obj-{obj_index:04d}"
        is_critical = draw(st.booleans())

        gap = Gap(
            objective_id=obj_id,
            objective_description=f"Understand concept {obj_index}",
            domain_id=domain_id,
            status=CoverageStatus.NOT_COVERED,
            knowledge_point_count=0,
            is_critical=is_critical,
            recommendations=[
                {"resource": "Resource A", "description": "Desc A", "topic_area": "Area A"},
                {"resource": "Resource B", "description": "Desc B", "topic_area": "Area B"},
            ],
        )

        if is_critical:
            critical_gaps.append(gap)
        else:
            not_covered_gaps.append(gap)

        coverage_items.append({
            "objective_id": obj_id,
            "status": CoverageStatus.NOT_COVERED.value,
            "point_count": 0,
        })
        obj_index += 1

    return GapReport(
        coverage_items=coverage_items,
        critical_gaps=critical_gaps,
        weak_gaps=weak_gaps,
        not_covered_gaps=not_covered_gaps,
        total_objectives=total,
        fully_covered_count=fully_covered,
        weakly_covered_count=weakly_covered,
        not_covered_count=not_covered,
    )


@st.composite
def _notes_collection(
    draw: st.DrawFn,
    *,
    min_notes: int = 0,
    max_notes: int = 8,
) -> StudyNotesCollection:
    """Generate a random StudyNotesCollection."""
    num_notes = draw(st.integers(min_value=min_notes, max_value=max_notes))

    notes: list[TopicNotes] = []
    for i in range(num_notes):
        domain_id = draw(st.sampled_from(ALL_DOMAIN_IDS))
        notes.append(
            TopicNotes(
                topic_id=f"topic-{i:04d}",
                topic_name=f"Topic {i} study content",
                domain_id=domain_id,
                priority_score=draw(st.integers(min_value=1, max_value=10)),
                overview="Overview sentence one. Sentence two. Sentence three.",
                explanation=" ".join(["word"] * 200),
                key_facts=[f"Fact {j}" for j in range(3)],
                common_mistakes=["Mistake 1", "Mistake 2"],
                examples=["Example 1"],
                exam_tips=["Tip 1"],
                code_blocks=[],
                related_topics=[],
                is_supplemented=False,
            )
        )

    return StudyNotesCollection(notes=notes, cross_domain_themes=[])


@st.composite
def _scored_topic_list(
    draw: st.DrawFn,
    *,
    gap_report: GapReport,
) -> ScoredTopicList:
    """Generate a ScoredTopicList that includes topics matching gap report objectives.

    Ensures scored topics align with the objectives in the gap report so
    the ReadinessAssessor can look up priority scores.
    """
    topics: list[ScoredTopic] = []

    # Combine all gaps to create scored topics for them
    all_gaps = gap_report.critical_gaps + gap_report.weak_gaps + gap_report.not_covered_gaps

    for gap in all_gaps:
        priority = draw(st.integers(min_value=1, max_value=10))
        topics.append(
            ScoredTopic(
                topic_id=gap.objective_id,
                topic_name=f"Topic for {gap.objective_id}",
                domain_ids=[gap.domain_id],
                priority_score=priority,
                is_high_priority=priority >= HIGH_PRIORITY_THRESHOLD,
                domain_count=1,
            )
        )

    return ScoredTopicList(topics=topics)


@st.composite
def _scored_topic_list_with_high_risk(
    draw: st.DrawFn,
    *,
    gap_report: GapReport,
) -> ScoredTopicList:
    """Generate a ScoredTopicList ensuring at least one high-priority topic in gaps.

    Forces at least one gap topic to have priority_score >= 8 to guarantee
    that high-risk topics can be identified.
    """
    topics: list[ScoredTopic] = []

    all_gaps = gap_report.critical_gaps + gap_report.weak_gaps + gap_report.not_covered_gaps

    if not all_gaps:
        return ScoredTopicList(topics=[])

    # Force first gap to be high-priority
    forced_high_index = draw(st.integers(min_value=0, max_value=max(0, len(all_gaps) - 1)))

    for i, gap in enumerate(all_gaps):
        if i == forced_high_index:
            priority = draw(st.integers(min_value=HIGH_PRIORITY_THRESHOLD, max_value=10))
        else:
            priority = draw(st.integers(min_value=1, max_value=10))

        topics.append(
            ScoredTopic(
                topic_id=gap.objective_id,
                topic_name=f"Topic for {gap.objective_id}",
                domain_ids=[gap.domain_id],
                priority_score=priority,
                is_high_priority=priority >= HIGH_PRIORITY_THRESHOLD,
                domain_count=1,
            )
        )

    return ScoredTopicList(topics=topics)


@st.composite
def _readiness_inputs(
    draw: st.DrawFn,
) -> tuple[GapReport, StudyNotesCollection, ScoredTopicList]:
    """Generate a complete set of inputs for the ReadinessAssessor."""
    gap_report = draw(_gap_report())
    notes = draw(_notes_collection())
    scores = draw(_scored_topic_list(gap_report=gap_report))
    return gap_report, notes, scores


@st.composite
def _readiness_inputs_with_high_risk(
    draw: st.DrawFn,
) -> tuple[GapReport, StudyNotesCollection, ScoredTopicList]:
    """Generate inputs that guarantee at least one high-risk topic exists."""
    # Ensure there are gaps (weakly/not covered) to form high-risk topics
    gap_report = draw(_gap_report(min_objectives=3, max_objectives=10))

    # If no gaps at all, redraw with forced gaps
    while (gap_report.weakly_covered_count + gap_report.not_covered_count) == 0:
        gap_report = draw(_gap_report(min_objectives=3, max_objectives=10))

    notes = draw(_notes_collection())
    scores = draw(_scored_topic_list_with_high_risk(gap_report=gap_report))
    return gap_report, notes, scores


# === Helpers ===


def _run_readiness_assessment(
    gap_report: GapReport,
    notes: StudyNotesCollection,
    scores: ScoredTopicList,
) -> ReadinessAssessment:
    """Run the ReadinessAssessor with _write_artifact patched out."""
    assessor = ReadinessAssessor()
    with patch.object(assessor, "_write_artifact"):
        return assessor.assess(gap_report, notes, scores)


# === Property 21: Readiness Score Calculation ===


class TestReadinessScoreCalculation:
    """The readiness score must be between 0 and 100 and equal to the arithmetic
    mean of three components (each 0-100):
    1. coverage_pct = (fully_covered_count / total_objectives) * 100
    2. notes_pct = (topics_with_notes / total_topics) * 100
    3. inverse_gap_pct = 100 - ((weakly_covered + not_covered) / total_objectives * 100)

    Components must be consistent with score (their average ≈ score).

    **Validates: Requirements 10.1**
    """

    @given(data=_readiness_inputs())
    @settings(max_examples=50, deadline=30000, suppress_health_check=[HealthCheck.too_slow])
    def test_score_within_valid_range(
        self,
        data: tuple[GapReport, StudyNotesCollection, ScoredTopicList],
    ) -> None:
        """Readiness score must be between 0 and 100 inclusive."""
        gap_report, notes, scores = data
        assessment = _run_readiness_assessment(gap_report, notes, scores)

        assert 0 <= assessment.readiness_score <= 100, (
            f"Readiness score {assessment.readiness_score} is outside "
            f"valid range [0, 100]"
        )

    @given(data=_readiness_inputs())
    @settings(max_examples=50, deadline=30000, suppress_health_check=[HealthCheck.too_slow])
    def test_score_components_within_valid_range(
        self,
        data: tuple[GapReport, StudyNotesCollection, ScoredTopicList],
    ) -> None:
        """Each score component must be between 0 and 100."""
        gap_report, notes, scores = data
        assessment = _run_readiness_assessment(gap_report, notes, scores)

        components = assessment.score_components
        for key in ("coverage_pct", "notes_pct", "inverse_gap_pct"):
            assert key in components, (
                f"Missing component '{key}' in score_components: {components}"
            )
            value = components[key]
            assert 0 <= value <= 100, (
                f"Component '{key}' has value {value}, expected [0, 100]"
            )

    @given(data=_readiness_inputs())
    @settings(max_examples=50, deadline=30000, suppress_health_check=[HealthCheck.too_slow])
    def test_score_is_arithmetic_mean_of_components(
        self,
        data: tuple[GapReport, StudyNotesCollection, ScoredTopicList],
    ) -> None:
        """Score must be the rounded arithmetic mean of the three components."""
        gap_report, notes, scores = data
        assessment = _run_readiness_assessment(gap_report, notes, scores)

        components = assessment.score_components
        expected_mean = (
            components["coverage_pct"]
            + components["notes_pct"]
            + components["inverse_gap_pct"]
        ) / 3.0
        expected_score = max(0, min(100, round(expected_mean)))

        assert assessment.readiness_score == expected_score, (
            f"Readiness score {assessment.readiness_score} != "
            f"expected mean {expected_score} (from components: "
            f"coverage={components['coverage_pct']}, "
            f"notes={components['notes_pct']}, "
            f"inverse_gap={components['inverse_gap_pct']})"
        )

    @given(data=_readiness_inputs())
    @settings(max_examples=50, deadline=30000, suppress_health_check=[HealthCheck.too_slow])
    def test_coverage_pct_matches_gap_report(
        self,
        data: tuple[GapReport, StudyNotesCollection, ScoredTopicList],
    ) -> None:
        """coverage_pct must equal (fully_covered_count / total_objectives) * 100."""
        gap_report, notes, scores = data
        assessment = _run_readiness_assessment(gap_report, notes, scores)

        total = gap_report.total_objectives
        if total > 0:
            expected = round(
                (gap_report.fully_covered_count / total) * 100, 1
            )
        else:
            expected = 100.0

        actual = assessment.score_components["coverage_pct"]
        assert actual == expected, (
            f"coverage_pct is {actual}, expected {expected} "
            f"(fully_covered={gap_report.fully_covered_count}, "
            f"total={total})"
        )

    @given(data=_readiness_inputs())
    @settings(max_examples=50, deadline=30000, suppress_health_check=[HealthCheck.too_slow])
    def test_inverse_gap_pct_matches_gap_report(
        self,
        data: tuple[GapReport, StudyNotesCollection, ScoredTopicList],
    ) -> None:
        """inverse_gap_pct must equal 100 - ((weakly + not_covered) / total * 100)."""
        gap_report, notes, scores = data
        assessment = _run_readiness_assessment(gap_report, notes, scores)

        total = gap_report.total_objectives
        if total > 0:
            gap_count = gap_report.weakly_covered_count + gap_report.not_covered_count
            expected = round(100.0 - (gap_count / total * 100), 1)
        else:
            expected = 100.0

        actual = assessment.score_components["inverse_gap_pct"]
        assert actual == expected, (
            f"inverse_gap_pct is {actual}, expected {expected} "
            f"(weakly={gap_report.weakly_covered_count}, "
            f"not_covered={gap_report.not_covered_count}, "
            f"total={total})"
        )


# === Property 22: High-Risk Topic Constraints ===


class TestHighRiskTopicConstraints:
    """High-risk topic list must satisfy:
    - Maximum 10 entries
    - Sorted by Priority_Score descending (each element >= next)
    - Each topic must satisfy: priority_score >= 8 OR missing_points > 0

    **Validates: Requirements 10.2**
    """

    @given(data=_readiness_inputs_with_high_risk())
    @settings(max_examples=50, deadline=30000, suppress_health_check=[HealthCheck.too_slow])
    def test_max_10_high_risk_topics(
        self,
        data: tuple[GapReport, StudyNotesCollection, ScoredTopicList],
    ) -> None:
        """High-risk topic list must contain at most 10 entries."""
        gap_report, notes, scores = data
        assessment = _run_readiness_assessment(gap_report, notes, scores)

        assert len(assessment.high_risk_topics) <= MAX_HIGH_RISK_TOPICS, (
            f"High-risk topics list has {len(assessment.high_risk_topics)} "
            f"entries, expected <= {MAX_HIGH_RISK_TOPICS}"
        )

    @given(data=_readiness_inputs_with_high_risk())
    @settings(max_examples=50, deadline=30000, suppress_health_check=[HealthCheck.too_slow])
    def test_high_risk_sorted_by_priority_descending(
        self,
        data: tuple[GapReport, StudyNotesCollection, ScoredTopicList],
    ) -> None:
        """High-risk topics must be sorted by priority_score descending."""
        gap_report, notes, scores = data
        assessment = _run_readiness_assessment(gap_report, notes, scores)

        topics = assessment.high_risk_topics
        for i in range(len(topics) - 1):
            assert topics[i].priority_score >= topics[i + 1].priority_score, (
                f"High-risk topics not sorted by priority descending: "
                f"topic[{i}].priority_score={topics[i].priority_score} < "
                f"topic[{i+1}].priority_score={topics[i+1].priority_score}"
            )

    @given(data=_readiness_inputs_with_high_risk())
    @settings(max_examples=50, deadline=30000, suppress_health_check=[HealthCheck.too_slow])
    def test_high_risk_topic_qualification_criteria(
        self,
        data: tuple[GapReport, StudyNotesCollection, ScoredTopicList],
    ) -> None:
        """Each high-risk topic must have priority_score >= 8 OR missing_points > 0."""
        gap_report, notes, scores = data
        assessment = _run_readiness_assessment(gap_report, notes, scores)

        for topic in assessment.high_risk_topics:
            qualifies = (
                topic.priority_score >= HIGH_PRIORITY_THRESHOLD
                or topic.missing_points > 0
            )
            assert qualifies, (
                f"High-risk topic '{topic.topic_id}' does not qualify: "
                f"priority_score={topic.priority_score} (threshold={HIGH_PRIORITY_THRESHOLD}), "
                f"missing_points={topic.missing_points} (need > 0)"
            )

    @given(data=_readiness_inputs())
    @settings(max_examples=50, deadline=30000, suppress_health_check=[HealthCheck.too_slow])
    def test_high_risk_topics_never_exceed_max(
        self,
        data: tuple[GapReport, StudyNotesCollection, ScoredTopicList],
    ) -> None:
        """Even with many gaps, the high-risk list never exceeds MAX_HIGH_RISK_TOPICS."""
        gap_report, notes, scores = data
        assessment = _run_readiness_assessment(gap_report, notes, scores)

        assert len(assessment.high_risk_topics) <= MAX_HIGH_RISK_TOPICS, (
            f"High-risk topics count {len(assessment.high_risk_topics)} "
            f"exceeds maximum {MAX_HIGH_RISK_TOPICS}"
        )


# === Property 23: Readiness Score Triggers Deferral Recommendation ===


class TestReadinessScoreTriggersDeferralRecommendation:
    """The relationship between readiness score and recommendation must be:
    - If score < 70: recommendation == "defer" AND remediation_plan is not None
    - If score >= 70: recommendation == "ready" AND remediation_plan is None

    **Validates: Requirements 10.5**
    """

    @given(data=_readiness_inputs())
    @settings(max_examples=50, deadline=30000, suppress_health_check=[HealthCheck.too_slow])
    def test_below_threshold_recommends_defer(
        self,
        data: tuple[GapReport, StudyNotesCollection, ScoredTopicList],
    ) -> None:
        """When score < 70, recommendation must be 'defer'."""
        gap_report, notes, scores = data
        assessment = _run_readiness_assessment(gap_report, notes, scores)

        if assessment.readiness_score < READINESS_DEFERRAL_THRESHOLD:
            assert assessment.recommendation == "defer", (
                f"Score {assessment.readiness_score} < {READINESS_DEFERRAL_THRESHOLD} "
                f"but recommendation is '{assessment.recommendation}', expected 'defer'"
            )

    @given(data=_readiness_inputs())
    @settings(max_examples=50, deadline=30000, suppress_health_check=[HealthCheck.too_slow])
    def test_below_threshold_has_remediation_plan(
        self,
        data: tuple[GapReport, StudyNotesCollection, ScoredTopicList],
    ) -> None:
        """When score < 70, remediation_plan must not be None."""
        gap_report, notes, scores = data
        assessment = _run_readiness_assessment(gap_report, notes, scores)

        if assessment.readiness_score < READINESS_DEFERRAL_THRESHOLD:
            assert assessment.remediation_plan is not None, (
                f"Score {assessment.readiness_score} < {READINESS_DEFERRAL_THRESHOLD} "
                f"but remediation_plan is None"
            )

    @given(data=_readiness_inputs())
    @settings(max_examples=50, deadline=30000, suppress_health_check=[HealthCheck.too_slow])
    def test_at_or_above_threshold_recommends_ready(
        self,
        data: tuple[GapReport, StudyNotesCollection, ScoredTopicList],
    ) -> None:
        """When score >= 70, recommendation must be 'ready'."""
        gap_report, notes, scores = data
        assessment = _run_readiness_assessment(gap_report, notes, scores)

        if assessment.readiness_score >= READINESS_DEFERRAL_THRESHOLD:
            assert assessment.recommendation == "ready", (
                f"Score {assessment.readiness_score} >= {READINESS_DEFERRAL_THRESHOLD} "
                f"but recommendation is '{assessment.recommendation}', expected 'ready'"
            )

    @given(data=_readiness_inputs())
    @settings(max_examples=50, deadline=30000, suppress_health_check=[HealthCheck.too_slow])
    def test_at_or_above_threshold_no_remediation_plan(
        self,
        data: tuple[GapReport, StudyNotesCollection, ScoredTopicList],
    ) -> None:
        """When score >= 70, remediation_plan must be None."""
        gap_report, notes, scores = data
        assessment = _run_readiness_assessment(gap_report, notes, scores)

        if assessment.readiness_score >= READINESS_DEFERRAL_THRESHOLD:
            assert assessment.remediation_plan is None, (
                f"Score {assessment.readiness_score} >= {READINESS_DEFERRAL_THRESHOLD} "
                f"but remediation_plan is not None"
            )

    @given(data=_readiness_inputs())
    @settings(max_examples=50, deadline=30000, suppress_health_check=[HealthCheck.too_slow])
    def test_recommendation_is_valid_value(
        self,
        data: tuple[GapReport, StudyNotesCollection, ScoredTopicList],
    ) -> None:
        """Recommendation must be exactly 'ready' or 'defer'."""
        gap_report, notes, scores = data
        assessment = _run_readiness_assessment(gap_report, notes, scores)

        assert assessment.recommendation in ("ready", "defer"), (
            f"Recommendation '{assessment.recommendation}' is not one of "
            f"the valid values: 'ready', 'defer'"
        )
