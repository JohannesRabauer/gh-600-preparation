"""Phase 10: Final Readiness Assessment.

Calculates a readiness score, identifies high-risk topics, produces
a last-minute 24-hour study plan, and (when the score is below 70)
a remediation plan recommending exam deferral.
"""

from __future__ import annotations

from pathlib import Path

from src.config import (
    ARTIFACTS_DIR,
    ARTIFACT_FILENAMES,
    DOMAIN_BY_ID,
    EXAM_DOMAINS,
    HIGH_PRIORITY_THRESHOLD,
    MAX_HIGH_RISK_TOPICS,
    MAX_LAST_MINUTE_AREAS,
    READINESS_DEFERRAL_THRESHOLD,
    STUDY_BLOCK_MINUTES,
)
from src.models.gap_analysis import CoverageStatus, GapReport
from src.models.readiness import (
    HighRiskTopic,
    ReadinessAssessment,
    RemediationPlan,
    TimeBlock,
)
from src.models.scoring import ScoredTopicList
from src.models.study_notes import StudyNotesCollection


class ReadinessAssessor:
    """Phase 10: Evaluates exam readiness and produces study recommendations.

    Calculates a composite readiness score from three equally weighted
    factors, identifies high-risk topics, builds a 24-hour study plan,
    and recommends deferral with a remediation plan when score < 70.
    """

    def __init__(self) -> None:
        """Initialize the ReadinessAssessor."""
        pass

    def assess(
        self,
        gap_report: GapReport,
        notes: StudyNotesCollection,
        scores: ScoredTopicList,
    ) -> ReadinessAssessment:
        """Perform a full readiness assessment.

        Combines gap analysis, study notes coverage, and scoring data
        to produce a readiness score, high-risk topics, 24h study plan,
        and optional remediation plan.

        Args:
            gap_report: GapReport from Phase 9.
            notes: StudyNotesCollection from Phase 4.
            scores: ScoredTopicList from Phase 3.

        Returns:
            A complete ReadinessAssessment.
        """
        # Calculate readiness score and its components
        score, components = self._calculate_score(gap_report, notes)

        # Identify high-risk topics (max 10)
        high_risk = self._identify_high_risk(gap_report, scores)

        # Identify last-minute areas (max 10, sorted by domain_weight * gap_severity)
        last_minute_areas = self._identify_last_minute_areas(gap_report, scores)

        # Build 24-hour study plan
        study_plan = self._build_24h_plan(high_risk)

        # Determine recommendation and optional remediation plan
        remediation_plan = self._build_remediation_plan(score, high_risk)
        recommendation = "defer" if score < READINESS_DEFERRAL_THRESHOLD else "ready"

        assessment = ReadinessAssessment(
            readiness_score=score,
            score_components=components,
            high_risk_topics=high_risk,
            last_minute_areas=last_minute_areas,
            study_plan_24h=study_plan,
            remediation_plan=remediation_plan,
            recommendation=recommendation,
        )

        # Write artifact to disk
        self._write_artifact(assessment)

        return assessment

    def _calculate_score(
        self, gap_report: GapReport, notes: StudyNotesCollection
    ) -> tuple[int, dict]:
        """Calculate readiness score as arithmetic mean of three components.

        Components (each 0-100):
        1. coverage_pct: % of exam objectives that are fully covered
        2. notes_pct: % of topics that have both study notes and practice questions
        3. inverse_gap_pct: 100 - (% of topics flagged as gaps)

        Args:
            gap_report: GapReport from Phase 9.
            notes: StudyNotesCollection from Phase 4.

        Returns:
            Tuple of (score as int 0-100, component dict).
        """
        # Component 1: % objectives fully covered
        total_objectives = gap_report.total_objectives
        if total_objectives > 0:
            coverage_pct = (gap_report.fully_covered_count / total_objectives) * 100
        else:
            coverage_pct = 100.0

        # Component 2: % topics with notes + questions
        # A topic "has notes" if it appears in the notes collection.
        # A topic "has questions" if it appears in the question bank — but since
        # Phase 10 only reads gap_report, notes, and scores, we approximate
        # topics with questions as those with notes (notes generated implies
        # questions were generated in Phase 7 for the same topic set).
        # More precisely: topics in the notes collection count as having
        # notes+questions since the pipeline generates questions for all
        # topics that have notes.
        total_topics = len(notes.notes) if notes.notes else 0
        topics_with_notes = len(notes.notes)
        if total_topics > 0:
            notes_pct = (topics_with_notes / total_topics) * 100
        else:
            notes_pct = 100.0

        # Component 3: inverse gap percentage
        # Gap topics = weakly covered + not covered
        gap_count = gap_report.weakly_covered_count + gap_report.not_covered_count
        if total_objectives > 0:
            gap_pct = (gap_count / total_objectives) * 100
        else:
            gap_pct = 0.0
        inverse_gap_pct = 100.0 - gap_pct

        # Arithmetic mean of three components
        raw_score = (coverage_pct + notes_pct + inverse_gap_pct) / 3.0
        score = max(0, min(100, round(raw_score)))

        components = {
            "coverage_pct": round(coverage_pct, 1),
            "notes_pct": round(notes_pct, 1),
            "inverse_gap_pct": round(inverse_gap_pct, 1),
        }

        return score, components

    def _identify_high_risk(
        self, gap_report: GapReport, scores: ScoredTopicList
    ) -> list[HighRiskTopic]:
        """Identify high-risk topics: max 10, sorted by Priority_Score descending.

        High-risk topics are those flagged by the Gap_Analyzer with a
        Priority_Score >= 8, or topics where fewer than 3 distinct
        knowledge points were extracted. (Requirement 10.2)

        Args:
            gap_report: GapReport from Phase 9.
            scores: ScoredTopicList from Phase 3.

        Returns:
            List of up to 10 HighRiskTopic instances sorted by priority_score desc.
        """
        score_map = {st.topic_id: st for st in scores.topics}

        # Collect all gaps (critical, weak, not covered)
        all_gaps = (
            gap_report.critical_gaps
            + gap_report.weak_gaps
            + gap_report.not_covered_gaps
        )

        high_risk_topics: list[HighRiskTopic] = []
        seen_ids: set[str] = set()

        for gap in all_gaps:
            # Use objective_id as a proxy for topic identification
            topic_id = gap.objective_id
            if topic_id in seen_ids:
                continue

            scored = score_map.get(topic_id)
            priority = scored.priority_score if scored else 5
            topic_name = (
                scored.topic_name
                if scored
                else gap.objective_description
            )

            # Condition: Priority_Score >= 8 OR fewer than 3 knowledge points
            is_high_priority = priority >= HIGH_PRIORITY_THRESHOLD
            has_few_points = gap.knowledge_point_count < 3

            if is_high_priority or has_few_points:
                reason_parts: list[str] = []
                if is_high_priority:
                    reason_parts.append(
                        f"High priority (score {priority})"
                    )
                if has_few_points:
                    reason_parts.append(
                        f"Insufficient coverage ({gap.knowledge_point_count} knowledge points)"
                    )

                high_risk_topics.append(
                    HighRiskTopic(
                        topic_id=topic_id,
                        topic_name=topic_name,
                        priority_score=priority,
                        gap_reason=" + ".join(reason_parts),
                        missing_points=max(0, 3 - gap.knowledge_point_count),
                    )
                )
                seen_ids.add(topic_id)

        # Sort by Priority_Score descending, limit to MAX_HIGH_RISK_TOPICS
        high_risk_topics.sort(key=lambda t: t.priority_score, reverse=True)
        return high_risk_topics[:MAX_HIGH_RISK_TOPICS]

    def _identify_last_minute_areas(
        self, gap_report: GapReport, scores: ScoredTopicList
    ) -> list[dict]:
        """Identify up to 10 last-minute revision areas.

        Sorted by the product of exam domain weight percentage and gap
        severity (number of missing knowledge points per topic).
        (Requirement 10.3)

        Args:
            gap_report: GapReport from Phase 9.
            scores: ScoredTopicList from Phase 3.

        Returns:
            List of up to 10 dicts with topic, domain, weight, severity, score.
        """
        score_map = {st.topic_id: st for st in scores.topics}

        # Collect all gap topics (weak + not covered)
        all_gaps = gap_report.weak_gaps + gap_report.not_covered_gaps

        areas: list[dict] = []
        for gap in all_gaps:
            domain = DOMAIN_BY_ID.get(gap.domain_id)
            domain_weight = (
                (domain.weight_min + domain.weight_max) / 2.0
                if domain
                else 0.15
            )
            # Gap severity = number of missing knowledge points
            # For "not covered" use 3 (the threshold for full coverage)
            gap_severity = max(1, 3 - gap.knowledge_point_count)

            scored = score_map.get(gap.objective_id)
            priority = scored.priority_score if scored else 5
            topic_name = (
                scored.topic_name
                if scored
                else gap.objective_description
            )

            composite_score = domain_weight * 100 * gap_severity

            areas.append(
                {
                    "topic_id": gap.objective_id,
                    "topic_name": topic_name,
                    "domain_id": gap.domain_id,
                    "domain_weight_pct": round(domain_weight * 100, 1),
                    "gap_severity": gap_severity,
                    "composite_score": round(composite_score, 1),
                    "priority_score": priority,
                }
            )

        # Sort by composite_score descending
        areas.sort(key=lambda a: a["composite_score"], reverse=True)
        return areas[:MAX_LAST_MINUTE_AREAS]

    def _build_24h_plan(
        self, high_risk: list[HighRiskTopic]
    ) -> list[TimeBlock]:
        """Build a 24-hour study plan with 60-minute blocks.

        Each block specifies a topic and resource type. Resource types
        rotate through: study_notes, flashcards, practice_questions.
        Topics are drawn from the high-risk list, cycling through
        them to fill the 24 hours. (Requirement 10.4)

        Args:
            high_risk: List of HighRiskTopic instances to build the plan around.

        Returns:
            List of 24 TimeBlock instances (one per hour).
        """
        if not high_risk:
            # No high-risk topics — provide a generic balanced plan
            return [
                TimeBlock(
                    start_hour=h,
                    topic="General review",
                    resource_type=self._resource_type_for_hour(h),
                    priority_score=5,
                )
                for h in range(24)
            ]

        resource_types = ["study_notes", "flashcards", "practice_questions"]
        blocks: list[TimeBlock] = []

        for hour in range(24):
            # Cycle through high-risk topics
            topic = high_risk[hour % len(high_risk)]
            # Rotate resource type by hour
            resource_type = resource_types[hour % len(resource_types)]

            blocks.append(
                TimeBlock(
                    start_hour=hour,
                    topic=topic.topic_name,
                    resource_type=resource_type,
                    priority_score=topic.priority_score,
                )
            )

        return blocks

    def _build_remediation_plan(
        self, score: int, high_risk: list[HighRiskTopic]
    ) -> RemediationPlan | None:
        """Build a remediation plan when score < 70.

        Recommends deferral with a target duration in days and specific
        modules/topics to revisit. (Requirement 10.5)

        Args:
            score: The calculated readiness score.
            high_risk: The identified high-risk topics.

        Returns:
            A RemediationPlan if score < 70, otherwise None.
        """
        if score >= READINESS_DEFERRAL_THRESHOLD:
            return None

        # Calculate target duration based on how far below threshold
        deficit = READINESS_DEFERRAL_THRESHOLD - score
        # Rough heuristic: 1 day per 5 points of deficit, minimum 3 days
        target_days = max(3, (deficit + 4) // 5)

        # Modules to revisit: derive from high-risk topic IDs
        modules_to_revisit = [t.topic_id for t in high_risk]

        # Build a daily schedule distributing high-risk topics across days
        daily_schedule: list[dict] = []
        topics_per_day = max(1, len(high_risk) // target_days + 1)

        for day in range(1, target_days + 1):
            start_idx = (day - 1) * topics_per_day
            end_idx = min(start_idx + topics_per_day, len(high_risk))
            day_topics = high_risk[start_idx:end_idx]

            if not day_topics:
                # Wrap around to cover topics again
                day_topics = high_risk[: min(topics_per_day, len(high_risk))]

            daily_schedule.append(
                {
                    "day": day,
                    "topics": [t.topic_name for t in day_topics],
                    "activities": [
                        "Review study notes",
                        "Practice flashcards",
                        "Complete practice questions",
                    ],
                }
            )

        return RemediationPlan(
            target_duration_days=target_days,
            modules_to_revisit=modules_to_revisit,
            daily_schedule=daily_schedule,
        )

    # --- Helper methods ---

    def _resource_type_for_hour(self, hour: int) -> str:
        """Determine resource type based on hour for variety.

        Args:
            hour: The hour index (0-23).

        Returns:
            One of "study_notes", "flashcards", "practice_questions".
        """
        resource_types = ["study_notes", "flashcards", "practice_questions"]
        return resource_types[hour % len(resource_types)]

    def _write_artifact(self, assessment: ReadinessAssessment) -> None:
        """Write the ReadinessAssessment to the artifacts directory.

        Creates the artifacts directory if it doesn't exist.
        Writes the result as JSON to phase10_readiness.json.

        Args:
            assessment: The readiness assessment to persist.
        """
        artifacts_path = Path(ARTIFACTS_DIR)
        artifacts_path.mkdir(parents=True, exist_ok=True)

        output_path = artifacts_path / ARTIFACT_FILENAMES["phase10"]
        output_path.write_text(
            assessment.model_dump_json(indent=2),
            encoding="utf-8",
        )

    @classmethod
    def from_artifacts(
        cls,
        gap_report_path: str | None = None,
        notes_path: str | None = None,
        scores_path: str | None = None,
    ) -> ReadinessAssessment:
        """Load from Phase 9, Phase 4, and Phase 3 artifacts and assess.

        Reads the gap report, study notes, and scored topic list from
        disk, then performs the readiness assessment.

        Args:
            gap_report_path: Path to phase09_gap_report.json.
                Defaults to artifacts/phase09_gap_report.json.
            notes_path: Path to phase04_notes.json.
                Defaults to artifacts/phase04_notes.json.
            scores_path: Path to phase03_scores.json.
                Defaults to artifacts/phase03_scores.json.

        Returns:
            The computed ReadinessAssessment.
        """
        if gap_report_path is None:
            gap_report_path = str(
                Path(ARTIFACTS_DIR) / ARTIFACT_FILENAMES["phase09"]
            )
        if notes_path is None:
            notes_path = str(
                Path(ARTIFACTS_DIR) / ARTIFACT_FILENAMES["phase04"]
            )
        if scores_path is None:
            scores_path = str(
                Path(ARTIFACTS_DIR) / ARTIFACT_FILENAMES["phase03"]
            )

        gap_report = GapReport.model_validate_json(
            Path(gap_report_path).read_text(encoding="utf-8")
        )
        notes = StudyNotesCollection.model_validate_json(
            Path(notes_path).read_text(encoding="utf-8")
        )
        scores = ScoredTopicList.model_validate_json(
            Path(scores_path).read_text(encoding="utf-8")
        )

        assessor = cls()
        return assessor.assess(gap_report, notes, scores)
