"""Phase 5: Structured Learning Course.

Organizes study material into sequential modules that respect prerequisite
learning order, with Bloom's Taxonomy objectives, time estimates, and
prerequisite tracking.
"""

from __future__ import annotations

from pathlib import Path

from src.config import (
    ARTIFACTS_DIR,
    ARTIFACT_FILENAMES,
    BLOOMS_TAXONOMY_VERBS,
    HIGH_PRIORITY_THRESHOLD,
    HIGH_PRIORITY_TIME_MULTIPLIER,
    MAX_MODULE_OBJECTIVES,
    MIN_MODULE_OBJECTIVES,
    MODULE_MAX_TIME_MINUTES,
    MODULE_MIN_TIME_MINUTES,
)
from src.models.curriculum import Curriculum, Module
from src.models.scoring import ScoredTopicList
from src.models.topic_map import Topic, TopicHierarchy


class CurriculumBuilder:
    """Phase 5: Structures study material into a sequential curriculum.

    Creates modules from topics respecting prerequisite order, assigns
    Bloom's Taxonomy learning objectives, calculates time estimates with
    high-priority multiplier, and tracks inter-module prerequisites.
    """

    def __init__(self) -> None:
        """Initialize the CurriculumBuilder."""
        self._bloom_verbs: set[str] = {v.lower() for v in BLOOMS_TAXONOMY_VERBS}

    def build(
        self, hierarchy: TopicHierarchy, scores: ScoredTopicList
    ) -> Curriculum:
        """Build a complete curriculum from topic hierarchy and scores.

        Organizes topics into sequential modules respecting prerequisite
        order, assigns objectives, calculates time estimates, and produces
        a learning path.

        Args:
            hierarchy: The TopicHierarchy from Phase 2 with learning order.
            scores: The ScoredTopicList from Phase 3 with priority scores.

        Returns:
            A complete Curriculum with modules and total study time.
        """
        # Build score lookup: topic_id -> ScoredTopic
        self._score_map = {st.topic_id: st for st in scores.topics}

        # Get topics ordered by learning_order from hierarchy
        ordered_topics = self._get_ordered_topics(hierarchy)

        # Create modules from ordered topics
        modules = self._create_modules(ordered_topics)

        # Calculate time estimates
        modules = self._apply_time_estimates(modules)

        # Build the curriculum
        total_time = sum(m.time_estimate_minutes for m in modules)
        learning_path = [m.id for m in modules]

        curriculum = Curriculum(
            modules=modules,
            total_time_minutes=total_time,
            learning_path=learning_path,
        )

        # Write artifact to disk
        self._write_artifact(curriculum)

        return curriculum

    def _get_ordered_topics(self, hierarchy: TopicHierarchy) -> list[Topic]:
        """Get all topics ordered by the hierarchy's learning_order.

        Topics are returned in prerequisite-respecting order. Topics
        not in learning_order are appended at the end.

        Args:
            hierarchy: The TopicHierarchy with learning_order.

        Returns:
            List of Topic objects in learning order.
        """
        # Build topic lookup: id -> Topic
        topic_lookup: dict[str, Topic] = {}
        for domain_id, topics in hierarchy.domains.items():
            for topic in topics:
                topic_lookup[topic.id] = topic

        # Order topics by learning_order
        ordered: list[Topic] = []
        seen: set[str] = set()

        for topic_id in hierarchy.learning_order:
            if topic_id in topic_lookup and topic_id not in seen:
                ordered.append(topic_lookup[topic_id])
                seen.add(topic_id)

        # Append any remaining topics not in learning_order
        for topic_id, topic in topic_lookup.items():
            if topic_id not in seen:
                ordered.append(topic)
                seen.add(topic_id)

        return ordered

    def _create_modules(self, topics: list[Topic]) -> list[Module]:
        """Organize topics into sequential modules.

        Groups topics by domain, creating one module per domain grouping.
        Topics are processed in learning order, and consecutive topics
        from the same domain are grouped together. A new module is created
        when the domain changes or when the module reaches a reasonable size.

        Args:
            topics: Topics in prerequisite-respecting order.

        Returns:
            List of Module objects in sequential order.
        """
        if not topics:
            return []

        modules: list[Module] = []
        current_group: list[Topic] = []
        current_domain: str | None = None

        for topic in topics:
            if current_domain is None:
                current_domain = topic.domain_id
                current_group.append(topic)
            elif topic.domain_id == current_domain and len(current_group) < 5:
                # Same domain and group not too large
                current_group.append(topic)
            else:
                # Domain changed or group is large enough
                modules.append(
                    self._build_module(current_group, len(modules) + 1, modules)
                )
                current_group = [topic]
                current_domain = topic.domain_id

        # Don't forget the last group
        if current_group:
            modules.append(
                self._build_module(current_group, len(modules) + 1, modules)
            )

        return modules

    def _build_module(
        self,
        topics: list[Topic],
        module_number: int,
        existing_modules: list[Module],
    ) -> Module:
        """Build a single Module from a group of topics.

        Args:
            topics: The topics for this module.
            module_number: The sequential module number.
            existing_modules: Previously created modules (for prerequisites).

        Returns:
            A Module instance (with placeholder time_estimate_minutes).
        """
        module_id = f"M{module_number:02d}"
        topic_ids = [t.id for t in topics]

        # Determine if module contains high-priority topics
        contains_high_priority = any(
            self._score_map.get(t.id)
            and self._score_map[t.id].priority_score >= HIGH_PRIORITY_THRESHOLD
            for t in topics
        )

        # Generate learning objectives
        objectives = self._generate_objectives(topics)

        # Determine prerequisites
        prerequisites = self._determine_prerequisites(
            topics, existing_modules
        )

        # Title from domain or first topic
        title = self._generate_title(topics)

        return Module(
            id=module_id,
            title=title,
            topic_ids=topic_ids,
            objectives=objectives,
            prerequisites=prerequisites,
            time_estimate_minutes=MODULE_MIN_TIME_MINUTES,  # Placeholder
            contains_high_priority=contains_high_priority,
        )

    def _generate_title(self, topics: list[Topic]) -> str:
        """Generate a module title from its topics.

        Uses the common domain or first topic name.

        Args:
            topics: Topics in this module.

        Returns:
            A descriptive module title string.
        """
        if len(topics) == 1:
            return topics[0].name
        # Use the domain_id or combine first topic names
        domain_id = topics[0].domain_id
        return f"{domain_id.replace('-', ' ').title()}: {topics[0].name}"

    def _generate_objectives(self, topics: list[Topic]) -> list[str]:
        """Generate Bloom's Taxonomy learning objectives for topics.

        Creates between MIN_MODULE_OBJECTIVES and MAX_MODULE_OBJECTIVES
        objectives using Bloom's verbs, based on the topics' content.

        Args:
            topics: Topics to generate objectives for.

        Returns:
            List of objective strings starting with Bloom's verbs.
        """
        bloom_verbs_list = list(BLOOMS_TAXONOMY_VERBS)
        objectives: list[str] = []

        for i, topic in enumerate(topics):
            if len(objectives) >= MAX_MODULE_OBJECTIVES:
                break

            # Select a verb based on topic position (progression through
            # Bloom's levels: remember -> understand -> apply -> analyze)
            verb_index = min(i * 3, len(bloom_verbs_list) - 1)
            verb = bloom_verbs_list[verb_index]

            objective = f"{verb.capitalize()} {topic.name.lower()}"
            objectives.append(objective)

            # Add a second objective for high-priority topics
            scored = self._score_map.get(topic.id)
            if (
                scored
                and scored.priority_score >= HIGH_PRIORITY_THRESHOLD
                and len(objectives) < MAX_MODULE_OBJECTIVES
            ):
                # Use a higher-level verb for the second objective
                higher_verb_index = min(verb_index + 6, len(bloom_verbs_list) - 1)
                higher_verb = bloom_verbs_list[higher_verb_index]
                objective2 = f"{higher_verb.capitalize()} {topic.name.lower()} in practice"
                objectives.append(objective2)

        # Ensure minimum objectives
        while len(objectives) < MIN_MODULE_OBJECTIVES:
            verb = bloom_verbs_list[len(objectives) % len(bloom_verbs_list)]
            topic_name = topics[0].name.lower() if topics else "the concepts"
            objectives.append(
                f"{verb.capitalize()} key aspects of {topic_name}"
            )

        return objectives[:MAX_MODULE_OBJECTIVES]

    def _determine_prerequisites(
        self,
        topics: list[Topic],
        existing_modules: list[Module],
    ) -> list[str]:
        """Determine prerequisite module IDs for the current module.

        A module has a prerequisite on an earlier module if any of its
        topics appear after the earlier module's topics in the learning
        order (the earlier module must be completed first).

        For the first module, prerequisites are ["none"].

        Args:
            topics: Topics in the current module.
            existing_modules: Previously created modules.

        Returns:
            List of prerequisite module IDs, or ["none"].
        """
        if not existing_modules:
            return ["none"]

        # The immediately preceding module is a prerequisite
        # (since learning order is sequential)
        prerequisites = [existing_modules[-1].id]
        return prerequisites

    def _apply_time_estimates(self, modules: list[Module]) -> list[Module]:
        """Apply time estimates to all modules.

        Non-high-priority modules get a base time estimate.
        High-priority modules get 1.5× the average non-high-priority time.

        Args:
            modules: List of modules with placeholder time estimates.

        Returns:
            New list of modules with calculated time estimates.
        """
        if not modules:
            return []

        # Calculate base time for non-high-priority modules
        # Base time scales with number of topics in the module
        non_hp_modules = [m for m in modules if not m.contains_high_priority]
        hp_modules = [m for m in modules if m.contains_high_priority]

        # Compute average base time for non-high-priority modules
        if non_hp_modules:
            # Scale by topic count: more topics = more time
            total_topics_non_hp = sum(
                len(m.topic_ids) for m in non_hp_modules
            )
            avg_topics = (
                total_topics_non_hp / len(non_hp_modules)
                if non_hp_modules
                else 1
            )
            # Target average of ~45 min for single-topic module, scaling up
            base_per_topic = 30
            avg_non_hp_time = max(
                MODULE_MIN_TIME_MINUTES,
                min(MODULE_MAX_TIME_MINUTES, round(avg_topics * base_per_topic)),
            )
        else:
            # All modules are high-priority; use a default average
            avg_non_hp_time = 45

        updated_modules: list[Module] = []
        for module in modules:
            time_est = self._estimate_time(module, avg_non_hp_time)
            # Create updated module with correct time estimate
            updated = Module(
                id=module.id,
                title=module.title,
                topic_ids=module.topic_ids,
                objectives=module.objectives,
                prerequisites=module.prerequisites,
                time_estimate_minutes=time_est,
                contains_high_priority=module.contains_high_priority,
            )
            updated_modules.append(updated)

        return updated_modules

    def _estimate_time(self, module: Module, avg_time: float) -> int:
        """Estimate study time for a module.

        High-priority modules get 1.5× the average non-high-priority time.
        All estimates are clamped to [15, 180] minutes.

        Args:
            module: The module to estimate time for.
            avg_time: Average time of non-high-priority modules.

        Returns:
            Integer time estimate in minutes, clamped to valid range.
        """
        topic_count = len(module.topic_ids)
        base_per_topic = 30

        if module.contains_high_priority:
            # High-priority: 1.5× average non-high-priority time
            time_est = round(avg_time * HIGH_PRIORITY_TIME_MULTIPLIER)
        else:
            # Scale by number of topics
            time_est = round(topic_count * base_per_topic)

        # Clamp to valid range
        return max(
            MODULE_MIN_TIME_MINUTES,
            min(MODULE_MAX_TIME_MINUTES, time_est),
        )

    def _validate_bloom_verbs(self, objectives: list[str]) -> bool:
        """Validate that objectives use Bloom's Taxonomy verbs.

        Checks that:
        1. There are between 2 and 7 objectives
        2. Each objective starts with a recognized Bloom's verb

        Args:
            objectives: List of learning objective strings.

        Returns:
            True if all objectives are valid, False otherwise.
        """
        if not (MIN_MODULE_OBJECTIVES <= len(objectives) <= MAX_MODULE_OBJECTIVES):
            return False

        for objective in objectives:
            first_word = objective.split()[0].lower() if objective.strip() else ""
            if first_word not in self._bloom_verbs:
                return False

        return True

    def _write_artifact(self, curriculum: Curriculum) -> None:
        """Write the Curriculum to the artifacts directory.

        Creates the artifacts directory if it doesn't exist.
        Writes the result as JSON to phase05_curriculum.json.

        Args:
            curriculum: The curriculum to persist.
        """
        artifacts_path = Path(ARTIFACTS_DIR)
        artifacts_path.mkdir(parents=True, exist_ok=True)

        output_path = artifacts_path / ARTIFACT_FILENAMES["phase05"]
        output_path.write_text(
            curriculum.model_dump_json(indent=2),
            encoding="utf-8",
        )

    @classmethod
    def from_artifacts(
        cls,
        topic_map_path: str | None = None,
        scores_path: str | None = None,
    ) -> Curriculum:
        """Load from Phase 2 and Phase 3 artifact files and build curriculum.

        Reads the topic hierarchy and scored topic list from disk,
        then builds the curriculum.

        Args:
            topic_map_path: Path to phase02_topic_map.json.
                Defaults to artifacts/phase02_topic_map.json.
            scores_path: Path to phase03_scores.json.
                Defaults to artifacts/phase03_scores.json.

        Returns:
            The generated Curriculum.
        """
        if topic_map_path is None:
            topic_map_path = str(
                Path(ARTIFACTS_DIR) / ARTIFACT_FILENAMES["phase02"]
            )
        if scores_path is None:
            scores_path = str(
                Path(ARTIFACTS_DIR) / ARTIFACT_FILENAMES["phase03"]
            )

        hierarchy = TopicHierarchy.model_validate_json(
            Path(topic_map_path).read_text(encoding="utf-8")
        )
        scores = ScoredTopicList.model_validate_json(
            Path(scores_path).read_text(encoding="utf-8")
        )

        builder = cls()
        return builder.build(hierarchy, scores)
