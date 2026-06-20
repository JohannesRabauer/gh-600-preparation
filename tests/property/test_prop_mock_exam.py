"""Property-based tests for Phase 8: Mock Exam Builder.

Tests correctness properties 17 and 18 from the design document:
- Property 17: Mock Exam Domain and Format Distribution
- Property 18: Mock Exam Answer Key Completeness

**Validates: Requirements 8.1, 8.2, 8.3, 8.4, 8.6**
"""

from __future__ import annotations

from unittest.mock import patch

from hypothesis import given, settings, HealthCheck
from hypothesis import strategies as st

from src.config import (
    DOMAIN_DISTRIBUTION_TOLERANCE_PP,
    EXAM_DOMAINS,
    HIGH_PRIORITY_THRESHOLD,
    MIN_FORMAT_PROPORTION,
    MIN_MOCK_EXAM_QUESTIONS,
)
from src.models.mock_exam import MockExam
from src.models.questions import (
    DifficultyLevel,
    Question,
    QuestionBank,
    QuestionFormat,
)
from src.models.scoring import ScoredTopic, ScoredTopicList
from src.phases.phase08_mock_exam import MockExamBuilder


# === Strategies ===

ALL_DOMAIN_IDS = [d.id for d in EXAM_DOMAINS]
DOMAIN_NAMES = {d.id: d.name for d in EXAM_DOMAINS}

# Available formats for generation
FORMATS = [
    QuestionFormat.MULTIPLE_CHOICE,
    QuestionFormat.MULTIPLE_SELECT,
    QuestionFormat.SCENARIO_BASED,
]


@st.composite
def _question_bank_and_scores(
    draw: st.DrawFn,
    min_questions_per_domain: int = 10,
    max_questions_per_domain: int = 15,
) -> tuple[QuestionBank, ScoredTopicList]:
    """Generate a QuestionBank and matching ScoredTopicList.

    Produces a question bank with enough questions across all 6 domains
    and all 3 formats so that the MockExamBuilder can meet its constraints.

    Args:
        draw: Hypothesis draw function.
        min_questions_per_domain: Minimum questions per domain.
        max_questions_per_domain: Maximum questions per domain.
    """
    all_easy: list[Question] = []
    all_intermediate: list[Question] = []
    all_advanced: list[Question] = []
    scored_topics: list[ScoredTopic] = []
    question_index = 0
    topic_index = 0
    domain_distribution: dict[str, int] = {}

    for domain in EXAM_DOMAINS:
        num_questions = draw(
            st.integers(
                min_value=min_questions_per_domain,
                max_value=max_questions_per_domain,
            )
        )
        domain_distribution[domain.id] = num_questions

        # Create a topic for this domain
        topic_id = f"topic-{topic_index:04d}"
        topic_name = f"Topic {topic_index} in {domain.name[:20]}"
        priority_score = draw(st.integers(min_value=1, max_value=10))

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

        # Generate questions for this domain, distributing across formats
        for i in range(num_questions):
            q_id = f"q-{question_index:04d}"

            # Cycle through formats to ensure all are represented
            fmt = FORMATS[i % len(FORMATS)]

            # Assign difficulty levels
            if i % 3 == 0:
                difficulty = DifficultyLevel.EASY
            elif i % 3 == 1:
                difficulty = DifficultyLevel.INTERMEDIATE
            else:
                difficulty = DifficultyLevel.ADVANCED

            # Build options based on format
            if fmt == QuestionFormat.MULTIPLE_SELECT:
                options = [
                    {"id": f"opt-{q_id}-a", "text": "Option A", "is_correct": True},
                    {"id": f"opt-{q_id}-b", "text": "Option B", "is_correct": True},
                    {"id": f"opt-{q_id}-c", "text": "Option C", "is_correct": False},
                    {"id": f"opt-{q_id}-d", "text": "Option D", "is_correct": False},
                    {"id": f"opt-{q_id}-e", "text": "Option E", "is_correct": False},
                ]
                correct_ids = [f"opt-{q_id}-a", f"opt-{q_id}-b"]
            else:
                options = [
                    {"id": f"opt-{q_id}-a", "text": "Option A", "is_correct": True},
                    {"id": f"opt-{q_id}-b", "text": "Option B", "is_correct": False},
                    {"id": f"opt-{q_id}-c", "text": "Option C", "is_correct": False},
                    {"id": f"opt-{q_id}-d", "text": "Option D", "is_correct": False},
                ]
                correct_ids = [f"opt-{q_id}-a"]

            incorrect_explanations = {
                opt["id"]: f"Wrong because {opt['text']}"
                for opt in options
                if not opt["is_correct"]
            }

            question = Question(
                id=q_id,
                format=fmt,
                difficulty=difficulty,
                domain_id=domain.id,
                topic_ids=[topic_id],
                scenario=f"Scenario for {q_id}" if fmt == QuestionFormat.SCENARIO_BASED else None,
                stem=f"Question stem for {q_id}?",
                options=options,
                correct_answer_ids=correct_ids,
                explanation=f"Explanation for question {q_id}.",
                incorrect_explanations=incorrect_explanations,
            )

            if difficulty == DifficultyLevel.EASY:
                all_easy.append(question)
            elif difficulty == DifficultyLevel.INTERMEDIATE:
                all_intermediate.append(question)
            else:
                all_advanced.append(question)

            question_index += 1

    question_bank = QuestionBank(
        easy=all_easy,
        intermediate=all_intermediate,
        advanced=all_advanced,
        domain_distribution=domain_distribution,
    )
    scores = ScoredTopicList(topics=scored_topics)

    return question_bank, scores


# === Helpers ===


def _build_mock_exam(
    question_bank: QuestionBank, scores: ScoredTopicList
) -> MockExam:
    """Run the MockExamBuilder with _write_artifact patched out."""
    builder = MockExamBuilder()
    with patch.object(builder, "_write_artifact"):
        return builder.build(question_bank, scores)


# === Property 17: Mock Exam Domain and Format Distribution ===


# Feature: gh-600-exam-prep, Property 17: Mock Exam Domain and Format Distribution
class TestMockExamDomainAndFormatDistribution:
    """For any mock exam with N total questions (N >= 50): each exam domain's
    percentage of questions SHALL be within ±5 percentage points of its official
    target weight, and each of the three question formats SHALL represent at
    least 15% of total questions.

    **Validates: Requirements 8.1, 8.2, 8.6**
    """

    @given(data=_question_bank_and_scores())
    @settings(max_examples=50, deadline=30000, suppress_health_check=[HealthCheck.too_slow])
    def test_total_questions_at_least_minimum(
        self,
        data: tuple[QuestionBank, ScoredTopicList],
    ) -> None:
        """Total questions in mock exam >= MIN_MOCK_EXAM_QUESTIONS (50)."""
        bank, scores = data
        exam = _build_mock_exam(bank, scores)

        assert len(exam.questions) >= MIN_MOCK_EXAM_QUESTIONS, (
            f"Mock exam has {len(exam.questions)} questions, "
            f"expected >= {MIN_MOCK_EXAM_QUESTIONS}"
        )

    @given(data=_question_bank_and_scores())
    @settings(max_examples=50, deadline=30000, suppress_health_check=[HealthCheck.too_slow])
    def test_domain_distribution_within_tolerance(
        self,
        data: tuple[QuestionBank, ScoredTopicList],
    ) -> None:
        """Each domain's question percentage is within ±5pp of its target weight."""
        bank, scores = data
        exam = _build_mock_exam(bank, scores)

        total = len(exam.questions)
        assert total > 0, "Mock exam has 0 questions"

        # Count questions per domain
        domain_counts: dict[str, int] = {}
        for q in exam.questions:
            domain_counts[q.domain_id] = domain_counts.get(q.domain_id, 0) + 1

        # Compute target weights (average of min and max)
        total_weight = sum(
            (d.weight_min + d.weight_max) / 2 for d in EXAM_DOMAINS
        )

        for domain in EXAM_DOMAINS:
            avg_weight = (domain.weight_min + domain.weight_max) / 2
            target_pct = (avg_weight / total_weight) * 100.0

            actual_count = domain_counts.get(domain.id, 0)
            actual_pct = (actual_count / total) * 100.0

            deviation = abs(actual_pct - target_pct)
            assert deviation <= DOMAIN_DISTRIBUTION_TOLERANCE_PP, (
                f"Domain '{domain.name}' ({domain.id}): "
                f"actual={actual_pct:.1f}%, target={target_pct:.1f}%, "
                f"deviation={deviation:.1f}pp > tolerance={DOMAIN_DISTRIBUTION_TOLERANCE_PP}pp"
            )

    @given(data=_question_bank_and_scores())
    @settings(max_examples=50, deadline=30000, suppress_health_check=[HealthCheck.too_slow])
    def test_each_format_at_least_15_percent(
        self,
        data: tuple[QuestionBank, ScoredTopicList],
    ) -> None:
        """Each format (MC, MS, scenario) represents >= 15% of total questions."""
        bank, scores = data
        exam = _build_mock_exam(bank, scores)

        total = len(exam.questions)
        assert total > 0, "Mock exam has 0 questions"

        # Count questions per format
        format_counts: dict[str, int] = {}
        for q in exam.questions:
            format_counts[q.format.value] = format_counts.get(q.format.value, 0) + 1

        for fmt in [
            QuestionFormat.MULTIPLE_CHOICE.value,
            QuestionFormat.MULTIPLE_SELECT.value,
            QuestionFormat.SCENARIO_BASED.value,
        ]:
            count = format_counts.get(fmt, 0)
            proportion = count / total

            assert proportion >= MIN_FORMAT_PROPORTION, (
                f"Format '{fmt}': proportion={proportion:.2f} "
                f"({count}/{total}), expected >= {MIN_FORMAT_PROPORTION}"
            )


# === Property 18: Mock Exam Answer Key Completeness ===


# Feature: gh-600-exam-prep, Property 18: Mock Exam Answer Key Completeness
class TestMockExamAnswerKeyCompleteness:
    """For any mock exam, the answer key SHALL contain an entry for every
    question in the exam, every answer key entry SHALL match the question's
    correct_answer_ids, and every selected question SHALL have a corresponding
    solution entry.

    **Validates: Requirements 8.3, 8.4**
    """

    @given(data=_question_bank_and_scores())
    @settings(max_examples=50, deadline=30000, suppress_health_check=[HealthCheck.too_slow])
    def test_answer_key_has_entry_for_every_question(
        self,
        data: tuple[QuestionBank, ScoredTopicList],
    ) -> None:
        """Every selected question has an entry in the answer key."""
        bank, scores = data
        exam = _build_mock_exam(bank, scores)

        for q in exam.questions:
            assert q.id in exam.answer_key, (
                f"Question '{q.id}' missing from answer key. "
                f"Answer key has {len(exam.answer_key)} entries for "
                f"{len(exam.questions)} questions."
            )

    @given(data=_question_bank_and_scores())
    @settings(max_examples=50, deadline=30000, suppress_health_check=[HealthCheck.too_slow])
    def test_answer_key_matches_correct_answer_ids(
        self,
        data: tuple[QuestionBank, ScoredTopicList],
    ) -> None:
        """Every answer key entry matches the question's correct_answer_ids."""
        bank, scores = data
        exam = _build_mock_exam(bank, scores)

        for q in exam.questions:
            assert q.id in exam.answer_key, (
                f"Question '{q.id}' missing from answer key"
            )
            assert sorted(exam.answer_key[q.id]) == sorted(q.correct_answer_ids), (
                f"Question '{q.id}': answer key={sorted(exam.answer_key[q.id])}, "
                f"expected correct_answer_ids={sorted(q.correct_answer_ids)}"
            )

    @given(data=_question_bank_and_scores())
    @settings(max_examples=50, deadline=30000, suppress_health_check=[HealthCheck.too_slow])
    def test_every_question_has_corresponding_solution(
        self,
        data: tuple[QuestionBank, ScoredTopicList],
    ) -> None:
        """Every selected question has a corresponding solution entry."""
        bank, scores = data
        exam = _build_mock_exam(bank, scores)

        solution_question_ids = {s["question_id"] for s in exam.solutions}

        for q in exam.questions:
            assert q.id in solution_question_ids, (
                f"Question '{q.id}' has no corresponding solution entry. "
                f"Solutions cover {len(solution_question_ids)} questions, "
                f"exam has {len(exam.questions)} questions."
            )

    @given(data=_question_bank_and_scores())
    @settings(max_examples=50, deadline=30000, suppress_health_check=[HealthCheck.too_slow])
    def test_every_solution_has_required_fields(
        self,
        data: tuple[QuestionBank, ScoredTopicList],
    ) -> None:
        """Every solution includes reasoning, incorrect_explanations, domain, and topic."""
        bank, scores = data
        exam = _build_mock_exam(bank, scores)

        for sol in exam.solutions:
            assert "question_id" in sol, (
                f"Solution missing 'question_id' field: {sol}"
            )
            assert "reasoning" in sol, (
                f"Solution for '{sol.get('question_id', '?')}' missing 'reasoning'"
            )
            assert "incorrect_explanations" in sol, (
                f"Solution for '{sol.get('question_id', '?')}' "
                f"missing 'incorrect_explanations'"
            )
            assert "domain" in sol, (
                f"Solution for '{sol.get('question_id', '?')}' missing 'domain'"
            )
            assert "topic" in sol, (
                f"Solution for '{sol.get('question_id', '?')}' missing 'topic'"
            )
