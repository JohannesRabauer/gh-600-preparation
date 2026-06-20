"""Phase 7: Practice Question Generator.

Generates practice questions at three difficulty levels (easy, intermediate,
advanced) with multiple formats (multiple choice, multiple select, scenario-based).
Questions are distributed proportionally to domain weights with detailed
explanations and cross-references to study notes.
"""

from __future__ import annotations

import uuid
from pathlib import Path

from src.config import (
    ADVANCED_SCENARIO_MIN_PROPORTION,
    ARTIFACTS_DIR,
    ARTIFACT_FILENAMES,
    DOMAIN_BY_ID,
    EXAM_DOMAINS,
    HIGH_PRIORITY_THRESHOLD,
    MIN_QUESTIONS_PER_LEVEL,
)
from src.models.questions import (
    DifficultyLevel,
    Question,
    QuestionBank,
    QuestionFormat,
)
from src.models.scoring import ScoredTopic, ScoredTopicList
from src.models.study_notes import StudyNotesCollection, TopicNotes


class QuestionGenerator:
    """Phase 7: Generates practice questions at multiple difficulty levels.

    Creates questions distributed proportionally to domain weights in
    three formats: multiple choice, multiple select, and scenario-based.
    Advanced questions are ≥50% scenario-based referencing 2+ topics.
    Each question includes correct answers, reasoning, concept references,
    study notes links, and explanations for incorrect options.
    """

    def __init__(self) -> None:
        """Initialize the QuestionGenerator."""
        pass

    def generate(
        self, notes: StudyNotesCollection, scores: ScoredTopicList
    ) -> QuestionBank:
        """Generate practice questions from study notes and scores.

        Produces questions at easy, intermediate, and advanced levels,
        distributed proportionally across exam domains.

        Args:
            notes: StudyNotesCollection from Phase 4.
            scores: ScoredTopicList from Phase 3.

        Returns:
            A QuestionBank with questions at all three levels.
        """
        # Build lookup maps
        self._score_map: dict[str, ScoredTopic] = {
            st.topic_id: st for st in scores.topics
        }
        self._notes_map: dict[str, TopicNotes] = {
            n.topic_id: n for n in notes.notes
        }

        # Group notes by domain
        self._notes_by_domain: dict[str, list[TopicNotes]] = {}
        for domain in EXAM_DOMAINS:
            self._notes_by_domain[domain.id] = []
        for note in notes.notes:
            if note.domain_id not in self._notes_by_domain:
                self._notes_by_domain[note.domain_id] = []
            self._notes_by_domain[note.domain_id].append(note)

        # Generate questions at each level
        easy = self._generate_easy()
        intermediate = self._generate_intermediate()
        advanced = self._generate_advanced()

        # Compute domain distribution across all questions
        all_questions = easy + intermediate + advanced
        domain_distribution = self._compute_domain_distribution(all_questions)

        bank = QuestionBank(
            easy=easy,
            intermediate=intermediate,
            advanced=advanced,
            domain_distribution=domain_distribution,
        )

        # Write artifact to disk
        self._write_artifact(bank)

        return bank

    def _generate_easy(self) -> list[Question]:
        """Generate easy-level questions (single-concept recall).

        Easy questions test basic recall of definitions, facts, and
        key concepts. Uses multiple choice format (4 options, 1 correct).

        Returns:
            List of easy-difficulty Question objects (min 20).
        """
        questions: list[Question] = []
        distribution = self._distribute_by_domain(MIN_QUESTIONS_PER_LEVEL)

        for domain in EXAM_DOMAINS:
            domain_notes = self._notes_by_domain.get(domain.id, [])
            target = distribution.get(domain.id, 1)

            if not domain_notes:
                # Generate from domain sub-topics directly
                domain_notes = self._create_placeholder_notes(domain.id)

            note_index = 0
            for i in range(target):
                note = domain_notes[note_index % len(domain_notes)]
                note_index += 1

                question = self._create_recall_question(
                    note, domain.id, i
                )
                questions.append(question)

        # Ensure minimum count
        while len(questions) < MIN_QUESTIONS_PER_LEVEL:
            note = self._get_any_note()
            questions.append(
                self._create_recall_question(note, note.domain_id, len(questions))
            )

        return questions

    def _generate_intermediate(self) -> list[Question]:
        """Generate intermediate-level questions (applying concepts).

        Intermediate questions test application of concepts to specific
        situations. Uses a mix of multiple choice and multiple select.

        Returns:
            List of intermediate-difficulty Question objects (min 20).
        """
        questions: list[Question] = []
        distribution = self._distribute_by_domain(MIN_QUESTIONS_PER_LEVEL)

        for domain in EXAM_DOMAINS:
            domain_notes = self._notes_by_domain.get(domain.id, [])
            target = distribution.get(domain.id, 1)

            if not domain_notes:
                domain_notes = self._create_placeholder_notes(domain.id)

            note_index = 0
            for i in range(target):
                note = domain_notes[note_index % len(domain_notes)]
                note_index += 1

                # Alternate between multiple choice and multiple select
                if i % 2 == 0:
                    question = self._create_application_mc_question(
                        note, domain.id, i
                    )
                else:
                    question = self._create_application_ms_question(
                        note, domain.id, i
                    )
                questions.append(question)

        # Ensure minimum count
        while len(questions) < MIN_QUESTIONS_PER_LEVEL:
            note = self._get_any_note()
            questions.append(
                self._create_application_mc_question(
                    note, note.domain_id, len(questions)
                )
            )

        return questions

    def _generate_advanced(self) -> list[Question]:
        """Generate advanced-level questions (multi-topic analysis).

        Advanced questions require analyzing scenarios that span 2+ topics.
        At least 50% must be scenario-based format.

        Returns:
            List of advanced-difficulty Question objects (min 20).
        """
        questions: list[Question] = []
        distribution = self._distribute_by_domain(MIN_QUESTIONS_PER_LEVEL)

        # Calculate how many scenario-based questions we need (≥50%)
        total_target = sum(distribution.values())
        scenario_target = max(
            int(total_target * ADVANCED_SCENARIO_MIN_PROPORTION) + 1,
            int(MIN_QUESTIONS_PER_LEVEL * ADVANCED_SCENARIO_MIN_PROPORTION) + 1,
        )
        scenario_count = 0

        for domain in EXAM_DOMAINS:
            domain_notes = self._notes_by_domain.get(domain.id, [])
            target = distribution.get(domain.id, 1)

            if not domain_notes:
                domain_notes = self._create_placeholder_notes(domain.id)

            note_index = 0
            for i in range(target):
                note = domain_notes[note_index % len(domain_notes)]
                note_index += 1

                # Ensure ≥50% are scenario-based
                remaining = total_target - len(questions)
                scenarios_still_needed = scenario_target - scenario_count

                if scenarios_still_needed > 0 and (
                    scenarios_still_needed >= remaining or i % 2 == 0
                ):
                    question = self._create_scenario_question(
                        note, domain.id, i
                    )
                    scenario_count += 1
                else:
                    question = self._create_analysis_mc_question(
                        note, domain.id, i
                    )
                questions.append(question)

        # Ensure minimum count and scenario proportion
        while len(questions) < MIN_QUESTIONS_PER_LEVEL:
            note = self._get_any_note()
            questions.append(
                self._create_scenario_question(
                    note, note.domain_id, len(questions)
                )
            )
            scenario_count += 1

        # Ensure ≥50% scenario-based
        actual_scenario_count = sum(
            1 for q in questions if q.format == QuestionFormat.SCENARIO_BASED
        )
        while actual_scenario_count < len(questions) * ADVANCED_SCENARIO_MIN_PROPORTION:
            note = self._get_any_note()
            questions.append(
                self._create_scenario_question(
                    note, note.domain_id, len(questions)
                )
            )
            actual_scenario_count += 1

        return questions

    def _distribute_by_domain(self, count: int) -> dict[str, int]:
        """Distribute question count proportionally to domain weights.

        Higher-weighted domains receive more questions. Each domain gets
        at least 1 question.

        Args:
            count: Total number of questions to distribute.

        Returns:
            Dictionary mapping domain_id to question count.
        """
        distribution: dict[str, int] = {}
        total_weight = sum(
            (d.weight_min + d.weight_max) / 2 for d in EXAM_DOMAINS
        )

        allocated = 0
        for domain in EXAM_DOMAINS:
            avg_weight = (domain.weight_min + domain.weight_max) / 2
            proportion = avg_weight / total_weight if total_weight > 0 else 1 / 6
            target = max(1, round(count * proportion))
            distribution[domain.id] = target
            allocated += target

        # Adjust if we over/under-allocated
        diff = allocated - count
        if diff > 0:
            # Remove from lowest-weight domains
            sorted_domains = sorted(
                EXAM_DOMAINS, key=lambda d: (d.weight_min + d.weight_max) / 2
            )
            for domain in sorted_domains:
                if diff <= 0:
                    break
                if distribution[domain.id] > 1:
                    distribution[domain.id] -= 1
                    diff -= 1
        elif diff < 0:
            # Add to highest-weight domains
            sorted_domains = sorted(
                EXAM_DOMAINS,
                key=lambda d: (d.weight_min + d.weight_max) / 2,
                reverse=True,
            )
            for domain in sorted_domains:
                if diff >= 0:
                    break
                distribution[domain.id] += 1
                diff += 1

        return distribution

    # --- Question creation methods ---

    def _create_recall_question(
        self, note: TopicNotes, domain_id: str, index: int
    ) -> Question:
        """Create an easy recall question (multiple choice, 4 options, 1 correct).

        Tests single-concept recall of definitions or key facts.

        Args:
            note: The TopicNotes to base the question on.
            domain_id: The exam domain ID.
            index: Question index for unique ID generation.

        Returns:
            A Question with DifficultyLevel.EASY and QuestionFormat.MULTIPLE_CHOICE.
        """
        domain_name = self._get_domain_name(domain_id)
        topic_name = note.topic_name

        # Use key facts for correct answer content
        correct_fact = note.key_facts[0] if note.key_facts else note.overview
        stem = f"Which of the following best describes {topic_name}?"

        correct_option_id = "A"
        options = [
            {"id": "A", "text": correct_fact, "is_correct": True},
            {
                "id": "B",
                "text": f"A process unrelated to {domain_name} that focuses on non-AI development practices.",
                "is_correct": False,
            },
            {
                "id": "C",
                "text": f"A deprecated feature that has been replaced in modern GitHub workflows.",
                "is_correct": False,
            },
            {
                "id": "D",
                "text": f"A third-party tool that operates independently of GitHub's ecosystem.",
                "is_correct": False,
            },
        ]

        study_notes_ref = f"See study notes: {topic_name} ({domain_name})"
        explanation = (
            f"The correct answer is A. {correct_fact} "
            f"This is a key concept in the {domain_name} domain. "
            f"{study_notes_ref}"
        )

        incorrect_explanations = {
            "B": f"Incorrect. {topic_name} is directly related to {domain_name} and AI-assisted development.",
            "C": f"Incorrect. {topic_name} is a current, actively used concept in the GH-600 certification scope.",
            "D": f"Incorrect. {topic_name} is integrated within GitHub's ecosystem, not a standalone third-party tool.",
        }

        return Question(
            id=self._generate_id("easy", index),
            format=QuestionFormat.MULTIPLE_CHOICE,
            difficulty=DifficultyLevel.EASY,
            domain_id=domain_id,
            topic_ids=[note.topic_id],
            scenario=None,
            stem=stem,
            options=options,
            correct_answer_ids=[correct_option_id],
            explanation=explanation,
            incorrect_explanations=incorrect_explanations,
        )

    def _create_application_mc_question(
        self, note: TopicNotes, domain_id: str, index: int
    ) -> Question:
        """Create an intermediate multiple-choice question (applying concepts).

        Tests ability to apply a concept in a specific situation.

        Args:
            note: The TopicNotes to base the question on.
            domain_id: The exam domain ID.
            index: Question index for unique ID generation.

        Returns:
            A Question with DifficultyLevel.INTERMEDIATE, MULTIPLE_CHOICE format.
        """
        domain_name = self._get_domain_name(domain_id)
        topic_name = note.topic_name

        stem = (
            f"A developer needs to implement {topic_name} in their "
            f"GitHub Copilot workflow. Which approach should they use?"
        )

        # Build correct answer from examples or exam tips
        correct_text = (
            note.examples[0] if note.examples
            else f"Apply {topic_name} following the recommended practices for {domain_name}."
        )

        options = [
            {"id": "A", "text": correct_text, "is_correct": True},
            {
                "id": "B",
                "text": f"Skip {topic_name} configuration and rely on default settings without validation.",
                "is_correct": False,
            },
            {
                "id": "C",
                "text": f"Implement a custom solution that bypasses GitHub's built-in {topic_name} support.",
                "is_correct": False,
            },
            {
                "id": "D",
                "text": f"Defer {topic_name} implementation to a later phase without any interim measures.",
                "is_correct": False,
            },
        ]

        study_notes_ref = f"See study notes: {topic_name} ({domain_name})"
        explanation = (
            f"The correct answer is A. When implementing {topic_name}, "
            f"developers should follow established best practices that "
            f"align with the {domain_name} domain requirements. "
            f"{study_notes_ref}"
        )

        incorrect_explanations = {
            "B": f"Incorrect. Relying on defaults without validation may miss critical {topic_name} requirements.",
            "C": f"Incorrect. Custom solutions that bypass built-in support add unnecessary complexity and risk.",
            "D": f"Incorrect. Deferring without interim measures can lead to technical debt and security gaps.",
        }

        return Question(
            id=self._generate_id("intermediate-mc", index),
            format=QuestionFormat.MULTIPLE_CHOICE,
            difficulty=DifficultyLevel.INTERMEDIATE,
            domain_id=domain_id,
            topic_ids=[note.topic_id],
            scenario=None,
            stem=stem,
            options=options,
            correct_answer_ids=["A"],
            explanation=explanation,
            incorrect_explanations=incorrect_explanations,
        )

    def _create_application_ms_question(
        self, note: TopicNotes, domain_id: str, index: int
    ) -> Question:
        """Create an intermediate multiple-select question (4-6 options, 2+ correct).

        Tests understanding of multiple valid approaches or components.

        Args:
            note: The TopicNotes to base the question on.
            domain_id: The exam domain ID.
            index: Question index for unique ID generation.

        Returns:
            A Question with DifficultyLevel.INTERMEDIATE, MULTIPLE_SELECT format.
        """
        domain_name = self._get_domain_name(domain_id)
        topic_name = note.topic_name

        stem = (
            f"Which of the following are valid considerations when "
            f"working with {topic_name}? (Select all that apply)"
        )

        # Use key facts and exam tips for correct options
        correct_texts = []
        if note.key_facts:
            correct_texts.append(note.key_facts[0])
        if len(note.key_facts) > 1:
            correct_texts.append(note.key_facts[1])
        if note.exam_tips:
            correct_texts.append(note.exam_tips[0])

        # Ensure at least 2 correct answers
        while len(correct_texts) < 2:
            correct_texts.append(
                f"Understanding {topic_name} in the context of {domain_name}."
            )

        options = [
            {"id": "A", "text": correct_texts[0], "is_correct": True},
            {"id": "B", "text": correct_texts[1], "is_correct": True},
            {
                "id": "C",
                "text": f"Ignoring {topic_name} requirements has no impact on the development workflow.",
                "is_correct": False,
            },
            {
                "id": "D",
                "text": f"{topic_name} is only relevant for non-GitHub platforms.",
                "is_correct": False,
            },
        ]

        # Add a 5th option if we have 3 correct answers
        if len(correct_texts) >= 3:
            options.append(
                {"id": "E", "text": correct_texts[2], "is_correct": True}
            )
            correct_ids = ["A", "B", "E"]
        else:
            correct_ids = ["A", "B"]

        study_notes_ref = f"See study notes: {topic_name} ({domain_name})"
        explanation = (
            f"Options {', '.join(correct_ids)} are correct. "
            f"When working with {topic_name}, developers must consider "
            f"multiple factors that align with {domain_name} best practices. "
            f"{study_notes_ref}"
        )

        incorrect_explanations = {
            "C": f"Incorrect. {topic_name} requirements directly impact workflow quality and outcomes.",
            "D": f"Incorrect. {topic_name} is a core GitHub ecosystem concept relevant to GH-600.",
        }

        return Question(
            id=self._generate_id("intermediate-ms", index),
            format=QuestionFormat.MULTIPLE_SELECT,
            difficulty=DifficultyLevel.INTERMEDIATE,
            domain_id=domain_id,
            topic_ids=[note.topic_id],
            scenario=None,
            stem=stem,
            options=options,
            correct_answer_ids=correct_ids,
            explanation=explanation,
            incorrect_explanations=incorrect_explanations,
        )

    def _create_scenario_question(
        self, note: TopicNotes, domain_id: str, index: int
    ) -> Question:
        """Create an advanced scenario-based question referencing 2+ topics.

        Tests multi-topic analysis with a situational prompt.

        Args:
            note: The primary TopicNotes for the question.
            domain_id: The exam domain ID.
            index: Question index for unique ID generation.

        Returns:
            A Question with DifficultyLevel.ADVANCED, SCENARIO_BASED format.
        """
        domain_name = self._get_domain_name(domain_id)
        topic_name = note.topic_name

        # Find a related topic for cross-topic scenario (must be different)
        related_note = self._find_related_topic(note)
        if related_note and related_note.topic_id != note.topic_id:
            related_name = related_note.topic_name
            topic_ids = [note.topic_id, related_note.topic_id]
        else:
            # Fallback: find any different topic to ensure 2+ topic_ids
            fallback_note = self._find_any_different_topic(note)
            if fallback_note:
                related_name = fallback_note.topic_name
                topic_ids = [note.topic_id, fallback_note.topic_id]
            else:
                # Last resort: use a synthetic cross-domain topic reference
                # to satisfy the 2+ topic_ids requirement
                related_name = "AI agent governance"
                synthetic_id = f"cross-ref-{domain_id}-governance"
                topic_ids = [note.topic_id, synthetic_id]

        scenario = (
            f"A development team is implementing a new AI-assisted workflow "
            f"that involves both {topic_name} and {related_name}. "
            f"During the implementation, they encounter a situation where "
            f"the configuration for {topic_name} conflicts with requirements "
            f"from {related_name}. The team needs to find an approach that "
            f"satisfies both requirements while maintaining best practices "
            f"for the {domain_name} domain."
        )

        stem = (
            f"Given this scenario, what is the most appropriate approach "
            f"to resolve the conflict between {topic_name} and {related_name}?"
        )

        options = [
            {
                "id": "A",
                "text": (
                    f"Analyze both {topic_name} and {related_name} requirements, "
                    f"then implement a unified configuration that addresses the "
                    f"core objectives of both while following {domain_name} principles."
                ),
                "is_correct": True,
            },
            {
                "id": "B",
                "text": (
                    f"Prioritize {topic_name} over {related_name} and disable "
                    f"the conflicting features entirely."
                ),
                "is_correct": False,
            },
            {
                "id": "C",
                "text": (
                    f"Implement separate, disconnected solutions for each "
                    f"requirement without considering their interaction."
                ),
                "is_correct": False,
            },
            {
                "id": "D",
                "text": (
                    f"Remove both {topic_name} and {related_name} configurations "
                    f"and proceed with manual processes instead."
                ),
                "is_correct": False,
            },
        ]

        study_notes_ref = (
            f"See study notes: {topic_name} ({domain_name}), "
            f"{related_name}"
        )
        explanation = (
            f"The correct answer is A. When facing conflicts between "
            f"related concepts like {topic_name} and {related_name}, "
            f"the best practice is to analyze both requirements and find "
            f"a unified solution. This demonstrates advanced understanding "
            f"of how multiple concepts interact within and across domains. "
            f"{study_notes_ref}"
        )

        incorrect_explanations = {
            "B": (
                f"Incorrect. Disabling features entirely ignores the "
                f"requirements of {related_name} and reduces overall capability."
            ),
            "C": (
                f"Incorrect. Disconnected solutions fail to address the "
                f"interaction between {topic_name} and {related_name}, "
                f"potentially causing runtime conflicts."
            ),
            "D": (
                f"Incorrect. Reverting to manual processes eliminates the "
                f"benefits of both {topic_name} and {related_name} and "
                f"doesn't demonstrate AI-assisted development skills."
            ),
        }

        return Question(
            id=self._generate_id("advanced-scenario", index),
            format=QuestionFormat.SCENARIO_BASED,
            difficulty=DifficultyLevel.ADVANCED,
            domain_id=domain_id,
            topic_ids=topic_ids,
            scenario=scenario,
            stem=stem,
            options=options,
            correct_answer_ids=["A"],
            explanation=explanation,
            incorrect_explanations=incorrect_explanations,
        )

    def _create_analysis_mc_question(
        self, note: TopicNotes, domain_id: str, index: int
    ) -> Question:
        """Create an advanced multiple-choice analysis question.

        Tests multi-topic analysis without the full scenario format.

        Args:
            note: The primary TopicNotes for the question.
            domain_id: The exam domain ID.
            index: Question index for unique ID generation.

        Returns:
            A Question with DifficultyLevel.ADVANCED, MULTIPLE_CHOICE format.
        """
        domain_name = self._get_domain_name(domain_id)
        topic_name = note.topic_name

        # Find a related topic for cross-topic reference
        related_note = self._find_related_topic(note)
        if related_note and related_note.topic_id != note.topic_id:
            related_name = related_note.topic_name
            topic_ids = [note.topic_id, related_note.topic_id]
        else:
            fallback_note = self._find_any_different_topic(note)
            if fallback_note:
                related_name = fallback_note.topic_name
                topic_ids = [note.topic_id, fallback_note.topic_id]
            else:
                related_name = "governance"
                synthetic_id = f"cross-ref-{domain_id}-governance"
                topic_ids = [note.topic_id, synthetic_id]

        stem = (
            f"When evaluating the interaction between {topic_name} and "
            f"{related_name} in an enterprise GitHub Copilot deployment, "
            f"which analysis is most accurate?"
        )

        options = [
            {
                "id": "A",
                "text": (
                    f"{topic_name} and {related_name} are complementary "
                    f"concepts that together ensure robust AI-assisted "
                    f"development within the {domain_name} domain."
                ),
                "is_correct": True,
            },
            {
                "id": "B",
                "text": (
                    f"{topic_name} and {related_name} are mutually "
                    f"exclusive and cannot be implemented simultaneously."
                ),
                "is_correct": False,
            },
            {
                "id": "C",
                "text": (
                    f"{topic_name} completely subsumes {related_name}, "
                    f"making the latter unnecessary in practice."
                ),
                "is_correct": False,
            },
            {
                "id": "D",
                "text": (
                    f"Neither {topic_name} nor {related_name} is relevant "
                    f"to enterprise deployments of GitHub Copilot."
                ),
                "is_correct": False,
            },
        ]

        study_notes_ref = (
            f"See study notes: {topic_name} ({domain_name}), "
            f"{related_name}"
        )
        explanation = (
            f"The correct answer is A. In enterprise deployments, "
            f"{topic_name} and {related_name} work together to provide "
            f"comprehensive coverage of {domain_name} requirements. "
            f"Understanding their complementary nature is key for "
            f"advanced GH-600 exam questions. {study_notes_ref}"
        )

        incorrect_explanations = {
            "B": (
                f"Incorrect. {topic_name} and {related_name} are not "
                f"mutually exclusive; they can and should coexist."
            ),
            "C": (
                f"Incorrect. {related_name} addresses distinct concerns "
                f"that are not fully covered by {topic_name} alone."
            ),
            "D": (
                f"Incorrect. Both concepts are directly relevant to "
                f"enterprise GitHub Copilot deployments."
            ),
        }

        return Question(
            id=self._generate_id("advanced-mc", index),
            format=QuestionFormat.MULTIPLE_CHOICE,
            difficulty=DifficultyLevel.ADVANCED,
            domain_id=domain_id,
            topic_ids=topic_ids,
            scenario=None,
            stem=stem,
            options=options,
            correct_answer_ids=["A"],
            explanation=explanation,
            incorrect_explanations=incorrect_explanations,
        )

    # --- Helper methods ---

    def _find_related_topic(self, note: TopicNotes) -> TopicNotes | None:
        """Find a related topic for cross-topic questions.

        Looks for a topic in a different domain or a related topic
        from the same domain that shares conceptual overlap.

        Args:
            note: The primary topic to find a related topic for.

        Returns:
            A related TopicNotes, or None if not found.
        """
        # First try: find a related topic from the related_topics list
        for related in note.related_topics:
            related_id = related.get("topic_id")
            if related_id and related_id in self._notes_map:
                return self._notes_map[related_id]

        # Second try: pick a topic from a different domain
        for domain_id, domain_notes in self._notes_by_domain.items():
            if domain_id != note.domain_id and domain_notes:
                return domain_notes[0]

        # Fallback: any other topic
        for other_note in self._notes_map.values():
            if other_note.topic_id != note.topic_id:
                return other_note

        return None

    def _find_any_different_topic(self, note: TopicNotes) -> TopicNotes | None:
        """Find any topic different from the given one.

        Used as a fallback when _find_related_topic fails to produce
        a distinct topic for cross-topic scenario questions.

        Args:
            note: The topic to avoid duplicating.

        Returns:
            A different TopicNotes, or None if only one topic exists.
        """
        for other_note in self._notes_map.values():
            if other_note.topic_id != note.topic_id:
                return other_note
        return None

    def _get_any_note(self) -> TopicNotes:
        """Get any available TopicNotes for question generation fallback.

        Returns:
            A TopicNotes from the available notes, preferring high-priority.
        """
        # Prefer high-priority notes
        for note in self._notes_map.values():
            if note.priority_score >= HIGH_PRIORITY_THRESHOLD:
                return note
        # Fallback to any note
        return next(iter(self._notes_map.values()))

    def _create_placeholder_notes(self, domain_id: str) -> list[TopicNotes]:
        """Create placeholder notes for domains with no actual notes.

        Used when a domain has no study notes to still generate questions
        from domain sub-topics.

        Args:
            domain_id: The domain identifier.

        Returns:
            A list of minimal TopicNotes for question generation.
        """
        domain = DOMAIN_BY_ID.get(domain_id)
        if not domain:
            return []

        placeholder_notes: list[TopicNotes] = []
        for i, sub_topic in enumerate(domain.sub_topics):
            placeholder_notes.append(
                TopicNotes(
                    topic_id=f"placeholder-{domain_id}-{i}",
                    topic_name=sub_topic,
                    domain_id=domain_id,
                    priority_score=6,
                    overview=f"{sub_topic} is a key concept in {domain.name}.",
                    explanation=f"{sub_topic} involves understanding and applying principles related to {domain.name}.",
                    key_facts=[
                        f"{sub_topic} is part of the {domain.name} domain.",
                        f"This topic is tested in the GH-600 certification exam.",
                        f"Understanding {sub_topic} requires practical experience.",
                    ],
                    common_mistakes=[
                        f"Not understanding the scope of {sub_topic}.",
                        f"Confusing {sub_topic} with unrelated concepts.",
                    ],
                    examples=[f"A developer applies {sub_topic} in their workflow."],
                    exam_tips=[f"Focus on practical applications of {sub_topic}."],
                    code_blocks=[],
                    step_by_step=None,
                    related_topics=[],
                    is_supplemented=False,
                )
            )

        return placeholder_notes

    def _get_domain_name(self, domain_id: str) -> str:
        """Look up the human-readable domain name.

        Args:
            domain_id: The domain identifier.

        Returns:
            The domain name, or the domain_id if not found.
        """
        domain = DOMAIN_BY_ID.get(domain_id)
        if domain:
            return domain.name
        return domain_id

    def _generate_id(self, prefix: str, index: int) -> str:
        """Generate a unique question ID.

        Args:
            prefix: A prefix indicating the question type.
            index: The question index.

        Returns:
            A unique string ID.
        """
        return f"q-{prefix}-{uuid.uuid4().hex[:8]}"

    def _compute_domain_distribution(
        self, questions: list[Question]
    ) -> dict[str, int]:
        """Compute the domain distribution of generated questions.

        Args:
            questions: All generated questions.

        Returns:
            Dictionary mapping domain_id to count of questions.
        """
        distribution: dict[str, int] = {}
        for q in questions:
            distribution[q.domain_id] = distribution.get(q.domain_id, 0) + 1
        return distribution

    def _write_artifact(self, bank: QuestionBank) -> None:
        """Write the QuestionBank to the artifacts directory.

        Creates the artifacts directory if it doesn't exist.
        Writes the result as JSON to phase07_questions.json.

        Args:
            bank: The question bank to persist.
        """
        artifacts_path = Path(ARTIFACTS_DIR)
        artifacts_path.mkdir(parents=True, exist_ok=True)

        output_path = artifacts_path / ARTIFACT_FILENAMES["phase07"]
        output_path.write_text(
            bank.model_dump_json(indent=2),
            encoding="utf-8",
        )

    @classmethod
    def from_artifacts(
        cls,
        notes_path: str | None = None,
        scores_path: str | None = None,
    ) -> QuestionBank:
        """Load from Phase 4 and Phase 3 artifact files and generate questions.

        Reads the study notes and scored topic list from disk,
        then generates the question bank.

        Args:
            notes_path: Path to phase04_notes.json.
                Defaults to artifacts/phase04_notes.json.
            scores_path: Path to phase03_scores.json.
                Defaults to artifacts/phase03_scores.json.

        Returns:
            The generated QuestionBank.
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

        generator = cls()
        return generator.generate(notes, scores)
