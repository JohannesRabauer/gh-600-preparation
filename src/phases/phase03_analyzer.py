"""Phase 3: Exam Relevance Analysis.

Assigns Priority_Scores (1-10) to all topics based on domain weights and
cross-domain presence. Higher-weighted exam domains produce higher base
scores, and topics appearing in multiple domains receive bonus points.
"""

from __future__ import annotations

from pathlib import Path

from src.config import (
    ARTIFACTS_DIR,
    ARTIFACT_FILENAMES,
    CROSS_DOMAIN_BONUS,
    DOMAIN_WEIGHT_TO_BASE_SCORE,
    EXAM_DOMAINS,
    HIGH_PRIORITY_THRESHOLD,
    MAX_PRIORITY_SCORE,
    MIN_PRIORITY_SCORE,
    ExamDomain,
)
from src.models.scoring import ScoredTopic, ScoredTopicList
from src.models.topic_map import Topic, TopicHierarchy


class RelevanceAnalyzer:
    """Phase 3: Scores and ranks topics by exam importance.

    Uses domain weight percentages to assign base scores, applies
    cross-domain bonuses for topics appearing in multiple domains,
    and produces a sorted, prioritized list of all topics.
    """

    def __init__(
        self,
        domain_weights: dict[str, tuple[float, float]] | None = None,
    ) -> None:
        """Initialize with domain weight ranges.

        Args:
            domain_weights: Mapping of domain ID to (weight_min, weight_max).
                Defaults to weights derived from EXAM_DOMAINS config.
        """
        if domain_weights is None:
            self._domain_weights: dict[str, tuple[float, float]] = {
                d.id: (d.weight_min, d.weight_max) for d in EXAM_DOMAINS
            }
        else:
            self._domain_weights = domain_weights

    def analyze(self, hierarchy: TopicHierarchy) -> ScoredTopicList:
        """Assign priority scores to all topics and produce sorted output.

        Reads the topic hierarchy, computes base scores from domain weights,
        applies cross-domain bonuses, flags high-priority topics, and sorts.

        Args:
            hierarchy: The TopicHierarchy from Phase 2.

        Returns:
            A ScoredTopicList with all topics scored and sorted.
        """
        # Build a lookup of which domains each topic appears in
        self._topic_domain_map = self._build_topic_domain_map(hierarchy)

        scored_topics: list[ScoredTopic] = []

        for domain_id, topics in hierarchy.domains.items():
            for topic in topics:
                # Skip if we already scored this topic (in case of duplicates)
                if any(st.topic_id == topic.id for st in scored_topics):
                    continue

                base_score = self._compute_base_score(topic)
                final_score = self._apply_cross_domain_bonus(topic, base_score)

                domain_ids = self._topic_domain_map.get(topic.id, [domain_id])
                domain_count = len(domain_ids)

                scored_topic = ScoredTopic(
                    topic_id=topic.id,
                    topic_name=topic.name,
                    domain_ids=domain_ids,
                    priority_score=final_score,
                    is_high_priority=final_score >= HIGH_PRIORITY_THRESHOLD,
                    domain_count=domain_count,
                )
                scored_topics.append(scored_topic)

        sorted_topics = self._sort_topics(scored_topics)

        result = ScoredTopicList(topics=sorted_topics)

        # Write artifact to disk
        self._write_artifact(result)

        return result

    def _build_topic_domain_map(
        self, hierarchy: TopicHierarchy
    ) -> dict[str, list[str]]:
        """Build a mapping of topic ID to all domain IDs it appears in.

        A topic can appear in multiple domains either by:
        1. Being directly listed in multiple domain entries
        2. Having cross-references linking it to topics in other domains

        Args:
            hierarchy: The topic hierarchy to analyze.

        Returns:
            Dictionary mapping topic IDs to lists of domain IDs.
        """
        topic_domains: dict[str, set[str]] = {}

        # Direct domain assignments
        for domain_id, topics in hierarchy.domains.items():
            for topic in topics:
                if topic.id not in topic_domains:
                    topic_domains[topic.id] = set()
                topic_domains[topic.id].add(domain_id)

        # Cross-references: if topic A is cross-referenced with topic B
        # in a different domain, topic A gains that domain association
        topic_to_domain: dict[str, str] = {}
        for domain_id, topics in hierarchy.domains.items():
            for topic in topics:
                topic_to_domain[topic.id] = domain_id

        for xref in hierarchy.cross_references:
            domain_a = topic_to_domain.get(xref.topic_id_a)
            domain_b = topic_to_domain.get(xref.topic_id_b)

            if domain_a and xref.topic_id_a in topic_domains:
                if domain_b:
                    topic_domains[xref.topic_id_a].add(domain_b)
            if domain_b and xref.topic_id_b in topic_domains:
                if domain_a:
                    topic_domains[xref.topic_id_b].add(domain_a)

        return {tid: sorted(domains) for tid, domains in topic_domains.items()}

    def _compute_base_score(self, topic: Topic) -> int:
        """Compute base priority score from the topic's primary domain weight.

        Maps domain weight ranges to base score ranges using
        DOMAIN_WEIGHT_TO_BASE_SCORE config:
        - 20-25% weight → base score 8-9
        - 15-20% weight → base score 6-8
        - 10-15% weight → base score 5-7

        Within each range, topics closer to domain core concepts
        (i.e., domains with higher weight_max) score higher within
        the base score range.

        Args:
            topic: The topic to score.

        Returns:
            Integer base score between MIN_PRIORITY_SCORE and MAX_PRIORITY_SCORE.
        """
        domain_id = topic.domain_id
        weight_range = self._domain_weights.get(domain_id)

        if weight_range is None:
            return MIN_PRIORITY_SCORE

        weight_min, weight_max = weight_range

        # Find matching score range based on weight_max
        for threshold_max, score_min, score_max in DOMAIN_WEIGHT_TO_BASE_SCORE:
            if weight_max <= threshold_max:
                # Compute position within the weight range relative to the
                # threshold boundaries. Higher weight_max within the bracket
                # scores closer to score_max.
                # The weight brackets are: 10-15%, 15-20%, 20-25%
                # threshold_max values: 0.15, 0.20, 0.25
                # Corresponding weight_min lower bounds: 0.10, 0.15, 0.20
                bracket_lower = threshold_max - 0.05
                range_width = threshold_max - bracket_lower

                if range_width > 0:
                    # Position within the bracket (0.0 to 1.0)
                    position = (weight_max - bracket_lower) / range_width
                else:
                    position = 0.5

                # Map position to score range
                score_range = score_max - score_min
                base_score = score_min + round(position * score_range)

                return max(MIN_PRIORITY_SCORE, min(MAX_PRIORITY_SCORE, base_score))

        # If weight_max exceeds all thresholds, assign highest score
        _, _, highest_score = DOMAIN_WEIGHT_TO_BASE_SCORE[0]
        return min(MAX_PRIORITY_SCORE, highest_score)

    def _apply_cross_domain_bonus(self, topic: Topic, base: int) -> int:
        """Add cross-domain bonus points to base score.

        Adds +1 per additional domain appearance beyond the first,
        capped at MAX_PRIORITY_SCORE (10).

        Args:
            topic: The topic being scored.
            base: The base score from _compute_base_score.

        Returns:
            Final priority score capped at MAX_PRIORITY_SCORE.
        """
        domain_ids = self._topic_domain_map.get(topic.id, [topic.domain_id])
        additional_domains = len(domain_ids) - 1  # Subtract the primary domain

        bonus = additional_domains * CROSS_DOMAIN_BONUS
        final_score = base + bonus

        return max(MIN_PRIORITY_SCORE, min(MAX_PRIORITY_SCORE, final_score))

    def _sort_topics(self, topics: list[ScoredTopic]) -> list[ScoredTopic]:
        """Sort topics by priority score, domain count, then name.

        Sorting order:
        1. Descending priority_score (highest first)
        2. Descending domain_count (more domains first, for ties)
        3. Ascending topic_name (alphabetical, for remaining ties)

        Args:
            topics: List of scored topics to sort.

        Returns:
            Sorted list of ScoredTopic objects.
        """
        return sorted(
            topics,
            key=lambda t: (-t.priority_score, -t.domain_count, t.topic_name),
        )

    def _write_artifact(self, result: ScoredTopicList) -> None:
        """Write the ScoredTopicList to the artifacts directory.

        Creates the artifacts directory if it doesn't exist.
        Writes the result as JSON to phase03_scores.json.
        """
        artifacts_path = Path(ARTIFACTS_DIR)
        artifacts_path.mkdir(parents=True, exist_ok=True)

        output_path = artifacts_path / ARTIFACT_FILENAMES["phase03"]
        output_path.write_text(
            result.model_dump_json(indent=2),
            encoding="utf-8",
        )

    @classmethod
    def from_artifact(cls, artifact_path: str | None = None) -> ScoredTopicList:
        """Load and process from the Phase 2 artifact file.

        Reads the topic hierarchy from disk and runs relevance analysis.

        Args:
            artifact_path: Optional path to phase02_topic_map.json.
                Defaults to artifacts/phase02_topic_map.json.

        Returns:
            The generated ScoredTopicList.
        """
        if artifact_path is None:
            artifact_path = str(
                Path(ARTIFACTS_DIR) / ARTIFACT_FILENAMES["phase02"]
            )

        path = Path(artifact_path)
        raw_json = path.read_text(encoding="utf-8")
        hierarchy = TopicHierarchy.model_validate_json(raw_json)

        analyzer = cls()
        return analyzer.analyze(hierarchy)
