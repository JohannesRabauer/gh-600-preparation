"""Phase 9: Gap Analyzer.

Compares generated study material against official exam objectives,
identifies coverage gaps, classifies coverage status, flags critical gaps
for high-priority topics, and recommends additional resources per gap.
"""

from __future__ import annotations

from pathlib import Path

from src.config import (
    ARTIFACTS_DIR,
    ARTIFACT_FILENAMES,
    FULLY_COVERED_MIN_POINTS,
    HIGH_PRIORITY_THRESHOLD,
    MIN_RECOMMENDATIONS_PER_GAP,
    WEAKLY_COVERED_MIN_POINTS,
)
from src.models.gap_analysis import CoverageStatus, Gap, GapReport
from src.models.knowledge import ExtractionLog
from src.models.scoring import ExamObjective, ScoredTopic, ScoredTopicList
from src.models.study_notes import StudyNotesCollection


class GapAnalyzer:
    """Phase 9: Analyzes coverage gaps between study material and exam objectives.

    Classifies each objective as fully covered (≥3 knowledge points),
    weakly covered (1-2 points), or not covered (0 points or inaccessible source).
    Flags high-priority gaps as critical and provides resource recommendations.
    """

    def __init__(self, official_objectives: list[ExamObjective]) -> None:
        """Initialize the GapAnalyzer with official exam objectives.

        Args:
            official_objectives: List of official exam objectives to compare against.
        """
        self._objectives = official_objectives

    def analyze(
        self,
        notes: StudyNotesCollection,
        scores: ScoredTopicList,
        extraction_log: list[ExtractionLog],
    ) -> GapReport:
        """Analyze coverage gaps between study materials and exam objectives.

        Args:
            notes: The generated study notes collection.
            scores: The scored topic list with priority scores.
            extraction_log: Log of extraction errors (inaccessible sources).

        Returns:
            A GapReport with coverage items, critical gaps, weak gaps,
            and not-covered gaps.
        """
        self._score_map: dict[str, ScoredTopic] = {
            st.topic_id: st for st in scores.topics
        }
        self._inaccessible_urls: set[str] = {
            log.url for log in extraction_log
        }

        # Build a mapping of objective_id -> knowledge point count from notes
        objective_point_counts = self._count_knowledge_points(notes)

        # Assess coverage for each objective
        coverage_items: list[dict] = []
        all_gaps: list[Gap] = []

        for objective in self._objectives:
            point_count = objective_point_counts.get(objective.id, 0)
            status = self._assess_coverage(objective, point_count)

            coverage_items.append({
                "objective_id": objective.id,
                "status": status.value,
                "point_count": point_count,
            })

            # If not fully covered, it's a gap
            if status != CoverageStatus.FULLY_COVERED:
                is_critical = self._is_critical_gap(objective, scores, status)
                recommendations = self._recommend_resources(objective)

                gap = Gap(
                    objective_id=objective.id,
                    objective_description=objective.description,
                    domain_id=objective.domain_id,
                    status=status,
                    knowledge_point_count=point_count,
                    is_critical=is_critical,
                    recommendations=recommendations,
                )
                all_gaps.append(gap)

        # Separate gaps into categories
        critical_gaps = [g for g in all_gaps if g.is_critical]
        weak_gaps = [
            g for g in all_gaps
            if g.status == CoverageStatus.WEAKLY_COVERED and not g.is_critical
        ]
        not_covered_gaps = [
            g for g in all_gaps
            if g.status == CoverageStatus.NOT_COVERED and not g.is_critical
        ]

        # Count coverage statuses
        fully_covered_count = sum(
            1 for item in coverage_items
            if item["status"] == CoverageStatus.FULLY_COVERED.value
        )
        weakly_covered_count = sum(
            1 for item in coverage_items
            if item["status"] == CoverageStatus.WEAKLY_COVERED.value
        )
        not_covered_count = sum(
            1 for item in coverage_items
            if item["status"] == CoverageStatus.NOT_COVERED.value
        )

        report = GapReport(
            coverage_items=coverage_items,
            critical_gaps=critical_gaps,
            weak_gaps=weak_gaps,
            not_covered_gaps=not_covered_gaps,
            total_objectives=len(self._objectives),
            fully_covered_count=fully_covered_count,
            weakly_covered_count=weakly_covered_count,
            not_covered_count=not_covered_count,
        )

        self._write_artifact(report)
        return report

    def _count_knowledge_points(
        self, notes: StudyNotesCollection
    ) -> dict[str, int]:
        """Count knowledge points per objective based on study notes coverage.

        Maps each objective to the number of relevant knowledge points
        found in the study notes. Uses topic matching between objectives
        and notes content.

        Args:
            notes: The study notes collection.

        Returns:
            Dictionary mapping objective_id to knowledge point count.
        """
        counts: dict[str, int] = {}

        # Build a lookup of notes by domain
        notes_by_domain: dict[str, list] = {}
        for note in notes.notes:
            if note.domain_id not in notes_by_domain:
                notes_by_domain[note.domain_id] = []
            notes_by_domain[note.domain_id].append(note)

        for objective in self._objectives:
            # Count relevant knowledge points from notes in the same domain
            domain_notes = notes_by_domain.get(objective.domain_id, [])

            point_count = 0
            for note in domain_notes:
                # Check if the note's topic is related to this objective
                # by comparing objective description/sub_bullets with note content
                if self._note_covers_objective(note, objective):
                    # Each matching note contributes its key_facts as knowledge points
                    point_count += len(note.key_facts)

            counts[objective.id] = point_count

        return counts

    def _note_covers_objective(self, note, objective: ExamObjective) -> bool:
        """Check if a study note covers a given objective.

        Uses keyword matching between the objective description/sub-bullets
        and the note's topic name and content.

        Args:
            note: A TopicNotes instance.
            objective: The exam objective to check.

        Returns:
            True if the note covers the objective.
        """
        # Extract keywords from objective
        obj_text = objective.description.lower()
        for bullet in objective.sub_bullets:
            obj_text += " " + bullet.lower()

        # Check if note topic name words overlap with objective text
        note_words = set(note.topic_name.lower().split())
        obj_words = set(obj_text.split())

        # Remove common stop words
        stop_words = {"the", "a", "an", "and", "or", "in", "of", "to", "for", "with", "is", "are"}
        note_words -= stop_words
        obj_words -= stop_words

        # If there's meaningful overlap, the note covers the objective
        overlap = note_words & obj_words
        return len(overlap) >= 2

    def _assess_coverage(
        self, objective: ExamObjective, point_count: int
    ) -> CoverageStatus:
        """Classify coverage status for an objective based on knowledge point count.

        - >= 3 points: fully_covered
        - 1-2 points: weakly_covered
        - 0 points: not_covered

        Args:
            objective: The exam objective being assessed.
            point_count: Number of knowledge points covering this objective.

        Returns:
            The CoverageStatus classification.
        """
        if point_count >= FULLY_COVERED_MIN_POINTS:
            return CoverageStatus.FULLY_COVERED
        elif point_count >= WEAKLY_COVERED_MIN_POINTS:
            return CoverageStatus.WEAKLY_COVERED
        else:
            return CoverageStatus.NOT_COVERED

    def _is_critical_gap(
        self,
        objective: ExamObjective,
        scores: ScoredTopicList,
        status: CoverageStatus,
    ) -> bool:
        """Determine if a gap is critical.

        A gap is critical if the objective's associated topic has
        priority_score >= HIGH_PRIORITY_THRESHOLD and the status is
        weakly_covered or not_covered.

        Args:
            objective: The exam objective with the gap.
            scores: The scored topic list.
            status: The coverage status of the objective.

        Returns:
            True if this is a critical gap.
        """
        if status == CoverageStatus.FULLY_COVERED:
            return False

        # Check if any scored topic in the same domain is high-priority
        # and matches this objective
        for scored_topic in scores.topics:
            if (
                objective.domain_id in scored_topic.domain_ids
                and scored_topic.priority_score >= HIGH_PRIORITY_THRESHOLD
            ):
                # Check if topic name relates to objective
                topic_words = set(scored_topic.topic_name.lower().split())
                obj_words = set(objective.description.lower().split())
                stop_words = {"the", "a", "an", "and", "or", "in", "of", "to", "for", "with"}
                topic_words -= stop_words
                obj_words -= stop_words
                if topic_words & obj_words:
                    return True

        return False

    def _identify_critical_gaps(
        self, gaps: list[Gap], scores: ScoredTopicList
    ) -> list[Gap]:
        """Identify critical gaps from the list of all gaps.

        Critical gaps are those where is_critical is True.

        Args:
            gaps: All identified gaps.
            scores: The scored topic list.

        Returns:
            List of critical Gap objects.
        """
        return [g for g in gaps if g.is_critical]

    def _recommend_resources(self, objective: ExamObjective) -> list[dict]:
        """Generate at least 2 resource recommendations for a gap.

        Produces recommendations based on the objective's domain
        and description.

        Args:
            objective: The exam objective with a coverage gap.

        Returns:
            List of recommendation dictionaries with resource, description,
            and topic_area fields. Always at least MIN_RECOMMENDATIONS_PER_GAP items.
        """
        recommendations: list[dict] = []

        # Always provide at least MIN_RECOMMENDATIONS_PER_GAP recommendations
        recommendations.append({
            "resource": f"Microsoft Learn: {objective.description}",
            "description": (
                f"Review the official Microsoft Learn documentation "
                f"covering {objective.description}"
            ),
            "topic_area": objective.domain_id,
        })

        recommendations.append({
            "resource": f"GitHub Docs: {objective.description}",
            "description": (
                f"Explore GitHub documentation for hands-on examples "
                f"related to {objective.description}"
            ),
            "topic_area": objective.domain_id,
        })

        # Add additional recommendations for objectives with sub-bullets
        for bullet in objective.sub_bullets[:1]:
            recommendations.append({
                "resource": f"Practice Lab: {bullet}",
                "description": (
                    f"Complete a hands-on lab exercise focused on {bullet}"
                ),
                "topic_area": objective.domain_id,
            })

        # Ensure we always meet the minimum
        while len(recommendations) < MIN_RECOMMENDATIONS_PER_GAP:
            recommendations.append({
                "resource": f"Additional study material for {objective.description}",
                "description": "Review supplementary documentation and tutorials",
                "topic_area": objective.domain_id,
            })

        return recommendations

    def _write_artifact(self, report: GapReport) -> None:
        """Write the GapReport to the artifacts directory.

        Args:
            report: The gap report to persist.
        """
        artifacts_path = Path(ARTIFACTS_DIR)
        artifacts_path.mkdir(parents=True, exist_ok=True)

        output_path = artifacts_path / ARTIFACT_FILENAMES["phase09"]
        output_path.write_text(
            report.model_dump_json(indent=2),
            encoding="utf-8",
        )

    @classmethod
    def from_artifacts(
        cls,
        objectives: list[ExamObjective],
        notes_path: str | None = None,
        scores_path: str | None = None,
    ) -> GapReport:
        """Load from artifact files and run gap analysis.

        Args:
            objectives: Official exam objectives.
            notes_path: Path to phase04_notes.json.
            scores_path: Path to phase03_scores.json.

        Returns:
            The GapReport.
        """
        if notes_path is None:
            notes_path = str(
                Path(ARTIFACTS_DIR) / ARTIFACT_FILENAMES["phase04"]
            )
        if scores_path is None:
            scores_path = str(
                Path(ARTIFACTS_DIR) / ARTIFACT_FILENAMES["phase03"]
            )

        notes = StudyNotesCollection.model_validate_json(
            Path(notes_path).read_text(encoding="utf-8")
        )
        scores = ScoredTopicList.model_validate_json(
            Path(scores_path).read_text(encoding="utf-8")
        )

        analyzer = cls(objectives)
        return analyzer.analyze(notes, scores, [])
