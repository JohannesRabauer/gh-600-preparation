"""Property-based tests for Phase 7: Question Generator.

Tests correctness properties 15 and 16 from the design document:
- Property 15: Question Bank Distribution and Structure
- Property 16: Advanced Questions Scenario Proportion

**Validates: Requirements 7.2, 7.3, 7.4, 7.5, 7.6, 7.7**
"""

from __future__ import annotations

from unittest.mock import patch

from hypothesis import given, settings, HealthCheck
from hypothesis import strategies as st

from src.config import (
    ADVANCED_SCENARIO_MIN_PROPORTION,
    EXAM_DOMAINS,
    HIGH_PRIORITY_THRESHOLD,
    MIN_QUESTIONS_PER_LEVEL,
)
from src.models.questions import (
    DifficultyLevel,
    QuestionBank,
    QuestionFormat,
)
from src.models.scoring import ScoredTopic, ScoredTopicList
from src.models.study_notes import StudyNotesCollection, TopicNotes
from src.phases.phase07_questions import QuestionGenerator


# === Strategies ===

ALL_DOMAIN_IDS = [d.id for d in EXAM_DOMAINS]
DOMAIN_NAMES = {d.id: d.name for d in EXAM_DOMAINS}


@st.composite
def _study_notes_and_scores(
    draw: st.DrawFn,
    min_topics_per_domain: int = 2,
    max_topics_per_domain: int = 4,
) -> tuple[StudyNotesCollection, ScoredTopicList]:
    """Generate a StudyNotesCollection and matching ScoredTopicList.

    Ensures all 6 domains have at least min_topics_per_domain topics
    so that question distribution across all domains is testable.

    Args:
        draw: Hypothesis draw function.
        min_topics_per_domain: Minimum topics per domain.
        max_topics_per_domain: Maximum topics per domain.
    """
    notes_list: list[TopicNotes] = []
    scored_topics: list[ScoredTopic] = []
    topic_index = 0

    for domain in EXAM_DOMAINS:
        num_topics = draw(
            st.integers(
                min_value=min_topics_per_domain,
                max_value=max_topics_per_domain,
            )
        )
        for j in range(num_topics):
            topic_id = f"topic-{topic_index:04d}"
            topic_name = f"Topic {topic_index} in {domain.name[:20]}"

            priority_score = draw(st.integers(min_value=1, max_value=10))

            # Key facts: at least 3
            num_key_facts = draw(st.integers(min_value=3, max_value=5))
            key_facts = [
                f"Key fact {k} for {topic_name}" for k in range(num_key_facts)
            ]

            # Common mistakes: at least 2
            num_mistakes = draw(st.integers(min_value=2, max_value=4))
            common_mistakes = [
                f"Common mistake {k} for {topic_name}"
                for k in range(num_mistakes)
            ]

            # Examples: at least 1
            num_examples = draw(st.integers(min_value=1, max_value=3))
            examples = [
                f"Example {k} demonstrating {topic_name}"
                for k in range(num_examples)
            ]

            # Exam tips: at least 1
            num_tips = draw(st.integers(min_value=1, max_value=3))
            exam_tips = [
                f"Exam tip {k} for {topic_name}" for k in range(num_tips)
            ]

            note = TopicNotes(
                topic_id=topic_id,
                topic_name=topic_name,
                domain_id=domain.id,
                priority_score=priority_score,
                overview=f"{topic_name} is a concept. It is important. It is tested on the exam.",
                explanation=f"Explanation for {topic_name}. " * 50,
                key_facts=key_facts,
                common_mistakes=common_mistakes,
                examples=examples,
                exam_tips=exam_tips,
                code_blocks=[],
                step_by_step=None,
                related_topics=[],
                is_supplemented=False,
            )
            notes_list.append(note)

            scored = ScoredTopic(
                topic_id=topic_id,
                topic_name=topic_name,
                domain_ids=[domain.id],
                priority_score=priority_score,
                is_high_priority=priority_score >= HIGH_PRIORITY_THRESHOLD,
                domain_count=1,
            )
            scored_topics.append(scored)
            topic_index += 1

    notes_collection = StudyNotesCollection(
        notes=notes_list,
        cross_domain_themes=[],
    )
    scores = ScoredTopicList(topics=scored_topics)

    return notes_collection, scores


# === Helpers ===


def _generate_questions(
    notes: StudyNotesCollection, scores: ScoredTopicList
) -> QuestionBank:
    """Run the QuestionGenerator with _write_artifact patched out."""
    generator = QuestionGenerator()
    with patch.object(generator, "_write_artifact"):
        return generator.generate(notes, scores)


# === Property 15: Question Bank Distribution and Structure ===


# Feature: gh-600-exam-prep, Property 15: Question Bank Distribution and Structure
class TestQuestionBankDistributionAndStructure:
    """For any generated question bank, each difficulty level (easy, intermediate,
    advanced) SHALL contain at least 20 questions, every question SHALL have a
    non-empty domain_id and at least one topic_id, all three QuestionFormat values
    SHALL be represented, every question SHALL have a non-empty explanation, and
    incorrect_explanations SHALL contain an entry for every non-correct option.

    **Validates: Requirements 7.2, 7.3, 7.4, 7.6, 7.7**
    """

    @given(data=_study_notes_and_scores())
    @settings(max_examples=50, deadline=30000, suppress_health_check=[HealthCheck.too_slow])
    def test_easy_level_minimum_count(
        self,
        data: tuple[StudyNotesCollection, ScoredTopicList],
    ) -> None:
        """Easy difficulty level has >= MIN_QUESTIONS_PER_LEVEL (20) questions."""
        notes, scores = data
        bank = _generate_questions(notes, scores)

        assert len(bank.easy) >= MIN_QUESTIONS_PER_LEVEL, (
            f"Easy level has {len(bank.easy)} questions, "
            f"expected >= {MIN_QUESTIONS_PER_LEVEL}"
        )

    @given(data=_study_notes_and_scores())
    @settings(max_examples=50, deadline=30000, suppress_health_check=[HealthCheck.too_slow])
    def test_intermediate_level_minimum_count(
        self,
        data: tuple[StudyNotesCollection, ScoredTopicList],
    ) -> None:
        """Intermediate difficulty level has >= MIN_QUESTIONS_PER_LEVEL (20) questions."""
        notes, scores = data
        bank = _generate_questions(notes, scores)

        assert len(bank.intermediate) >= MIN_QUESTIONS_PER_LEVEL, (
            f"Intermediate level has {len(bank.intermediate)} questions, "
            f"expected >= {MIN_QUESTIONS_PER_LEVEL}"
        )

    @given(data=_study_notes_and_scores())
    @settings(max_examples=50, deadline=30000, suppress_health_check=[HealthCheck.too_slow])
    def test_advanced_level_minimum_count(
        self,
        data: tuple[StudyNotesCollection, ScoredTopicList],
    ) -> None:
        """Advanced difficulty level has >= MIN_QUESTIONS_PER_LEVEL (20) questions."""
        notes, scores = data
        bank = _generate_questions(notes, scores)

        assert len(bank.advanced) >= MIN_QUESTIONS_PER_LEVEL, (
            f"Advanced level has {len(bank.advanced)} questions, "
            f"expected >= {MIN_QUESTIONS_PER_LEVEL}"
        )

    @given(data=_study_notes_and_scores())
    @settings(max_examples=50, deadline=30000, suppress_health_check=[HealthCheck.too_slow])
    def test_every_question_has_non_empty_domain_id(
        self,
        data: tuple[StudyNotesCollection, ScoredTopicList],
    ) -> None:
        """Every question has a non-empty domain_id."""
        notes, scores = data
        bank = _generate_questions(notes, scores)

        all_questions = bank.easy + bank.intermediate + bank.advanced
        for q in all_questions:
            assert q.domain_id and len(q.domain_id.strip()) > 0, (
                f"Question '{q.id}' has empty domain_id"
            )

    @given(data=_study_notes_and_scores())
    @settings(max_examples=50, deadline=30000, suppress_health_check=[HealthCheck.too_slow])
    def test_every_question_has_at_least_one_topic_id(
        self,
        data: tuple[StudyNotesCollection, ScoredTopicList],
    ) -> None:
        """Every question has at least one topic_id."""
        notes, scores = data
        bank = _generate_questions(notes, scores)

        all_questions = bank.easy + bank.intermediate + bank.advanced
        for q in all_questions:
            assert len(q.topic_ids) >= 1, (
                f"Question '{q.id}' has no topic_ids"
            )

    @given(data=_study_notes_and_scores())
    @settings(max_examples=50, deadline=30000, suppress_health_check=[HealthCheck.too_slow])
    def test_all_three_formats_represented(
        self,
        data: tuple[StudyNotesCollection, ScoredTopicList],
    ) -> None:
        """All three QuestionFormat values are represented in the question bank."""
        notes, scores = data
        bank = _generate_questions(notes, scores)

        all_questions = bank.easy + bank.intermediate + bank.advanced
        formats_present = {q.format for q in all_questions}

        assert QuestionFormat.MULTIPLE_CHOICE in formats_present, (
            "MULTIPLE_CHOICE format not represented in question bank"
        )
        assert QuestionFormat.MULTIPLE_SELECT in formats_present, (
            "MULTIPLE_SELECT format not represented in question bank"
        )
        assert QuestionFormat.SCENARIO_BASED in formats_present, (
            "SCENARIO_BASED format not represented in question bank"
        )

    @given(data=_study_notes_and_scores())
    @settings(max_examples=50, deadline=30000, suppress_health_check=[HealthCheck.too_slow])
    def test_every_question_has_non_empty_explanation(
        self,
        data: tuple[StudyNotesCollection, ScoredTopicList],
    ) -> None:
        """Every question has a non-empty explanation."""
        notes, scores = data
        bank = _generate_questions(notes, scores)

        all_questions = bank.easy + bank.intermediate + bank.advanced
        for q in all_questions:
            assert q.explanation and len(q.explanation.strip()) > 0, (
                f"Question '{q.id}' has empty explanation"
            )

    @given(data=_study_notes_and_scores())
    @settings(max_examples=50, deadline=30000, suppress_health_check=[HealthCheck.too_slow])
    def test_incorrect_explanations_cover_all_non_correct_options(
        self,
        data: tuple[StudyNotesCollection, ScoredTopicList],
    ) -> None:
        """incorrect_explanations has an entry for every non-correct option."""
        notes, scores = data
        bank = _generate_questions(notes, scores)

        all_questions = bank.easy + bank.intermediate + bank.advanced
        for q in all_questions:
            # Get all option IDs that are NOT correct
            non_correct_ids = [
                opt["id"] for opt in q.options if not opt["is_correct"]
            ]
            for opt_id in non_correct_ids:
                assert opt_id in q.incorrect_explanations, (
                    f"Question '{q.id}' missing incorrect_explanation for "
                    f"option '{opt_id}'. Has keys: {list(q.incorrect_explanations.keys())}"
                )

    @given(data=_study_notes_and_scores())
    @settings(max_examples=50, deadline=30000, suppress_health_check=[HealthCheck.too_slow])
    def test_multiple_choice_has_4_options_1_correct(
        self,
        data: tuple[StudyNotesCollection, ScoredTopicList],
    ) -> None:
        """Multiple choice questions have exactly 4 options with exactly 1 correct."""
        notes, scores = data
        bank = _generate_questions(notes, scores)

        all_questions = bank.easy + bank.intermediate + bank.advanced
        mc_questions = [
            q for q in all_questions
            if q.format == QuestionFormat.MULTIPLE_CHOICE
        ]

        for q in mc_questions:
            assert len(q.options) == 4, (
                f"MC question '{q.id}' has {len(q.options)} options, expected 4"
            )
            correct_count = sum(1 for opt in q.options if opt["is_correct"])
            assert correct_count == 1, (
                f"MC question '{q.id}' has {correct_count} correct options, expected 1"
            )

    @given(data=_study_notes_and_scores())
    @settings(max_examples=50, deadline=30000, suppress_health_check=[HealthCheck.too_slow])
    def test_multiple_select_has_4_to_6_options_2_plus_correct(
        self,
        data: tuple[StudyNotesCollection, ScoredTopicList],
    ) -> None:
        """Multiple select questions have 4-6 options with 2+ correct."""
        notes, scores = data
        bank = _generate_questions(notes, scores)

        all_questions = bank.easy + bank.intermediate + bank.advanced
        ms_questions = [
            q for q in all_questions
            if q.format == QuestionFormat.MULTIPLE_SELECT
        ]

        for q in ms_questions:
            assert 4 <= len(q.options) <= 6, (
                f"MS question '{q.id}' has {len(q.options)} options, expected 4-6"
            )
            correct_count = sum(1 for opt in q.options if opt["is_correct"])
            assert correct_count >= 2, (
                f"MS question '{q.id}' has {correct_count} correct options, expected >= 2"
            )


# === Property 16: Advanced Questions Scenario Proportion ===


# Feature: gh-600-exam-prep, Property 16: Advanced Questions Scenario Proportion
class TestAdvancedQuestionsScenarioProportion:
    """For any set of advanced-level questions, at least 50% SHALL be
    scenario-based (format = SCENARIO_BASED) and each scenario-based
    question SHALL reference at least 2 distinct topics in its topic_ids.

    **Validates: Requirements 7.5**
    """

    @given(data=_study_notes_and_scores())
    @settings(max_examples=50, deadline=30000, suppress_health_check=[HealthCheck.too_slow])
    def test_advanced_at_least_50_percent_scenario_based(
        self,
        data: tuple[StudyNotesCollection, ScoredTopicList],
    ) -> None:
        """At least 50% of advanced questions are scenario-based."""
        notes, scores = data
        bank = _generate_questions(notes, scores)

        total_advanced = len(bank.advanced)
        scenario_count = sum(
            1 for q in bank.advanced
            if q.format == QuestionFormat.SCENARIO_BASED
        )

        assert total_advanced > 0, "No advanced questions generated"
        actual_proportion = scenario_count / total_advanced

        assert actual_proportion >= ADVANCED_SCENARIO_MIN_PROPORTION, (
            f"Advanced scenario proportion = {actual_proportion:.2f} "
            f"({scenario_count}/{total_advanced}), "
            f"expected >= {ADVANCED_SCENARIO_MIN_PROPORTION}"
        )

    @given(data=_study_notes_and_scores())
    @settings(max_examples=50, deadline=30000, suppress_health_check=[HealthCheck.too_slow])
    def test_scenario_questions_reference_at_least_2_topics(
        self,
        data: tuple[StudyNotesCollection, ScoredTopicList],
    ) -> None:
        """Every scenario-based question references at least 2 distinct topics."""
        notes, scores = data
        bank = _generate_questions(notes, scores)

        scenario_questions = [
            q for q in bank.advanced
            if q.format == QuestionFormat.SCENARIO_BASED
        ]

        for q in scenario_questions:
            unique_topics = set(q.topic_ids)
            assert len(unique_topics) >= 2, (
                f"Scenario question '{q.id}' references only "
                f"{len(unique_topics)} distinct topic(s): {q.topic_ids}. "
                f"Expected >= 2 distinct topics."
            )

    @given(data=_study_notes_and_scores())
    @settings(max_examples=50, deadline=30000, suppress_health_check=[HealthCheck.too_slow])
    def test_scenario_questions_have_non_empty_scenario_field(
        self,
        data: tuple[StudyNotesCollection, ScoredTopicList],
    ) -> None:
        """Every scenario-based question has a non-empty scenario field."""
        notes, scores = data
        bank = _generate_questions(notes, scores)

        scenario_questions = [
            q for q in bank.advanced
            if q.format == QuestionFormat.SCENARIO_BASED
        ]

        for q in scenario_questions:
            assert q.scenario and len(q.scenario.strip()) > 0, (
                f"Scenario question '{q.id}' has empty or None scenario field"
            )
