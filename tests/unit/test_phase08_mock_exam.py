"""Unit tests for the MockExamBuilder (Phase 8)."""

from __future__ import annotations

import pytest

from src.config import (
    HIGH_PRIORITY_THRESHOLD,
    MIN_FORMAT_PROPORTION,
    MIN_MOCK_EXAM_QUESTIONS,
    PASS_THRESHOLD_MAX,
    PASS_THRESHOLD_SCORE,
)
from src.models.mock_exam import GradingRubric, MockExam
from src.models.questions import (
    DifficultyLevel,
    Question,
    QuestionBank,
    QuestionFormat,
)
from src.models.scoring import ScoredTopic, ScoredTopicList
from src.phases.phase08_mock_exam import MockExamBuilder


# --- Fixtures and helpers ---


def _make_question(
    id: str,
    domain_id: str = "domain-1",
    fmt: QuestionFormat = QuestionFormat.MULTIPLE_CHOICE,
    difficulty: DifficultyLevel = DifficultyLevel.EASY,
    topic_ids: list[str] | None = None,
    correct_ids: list[str] | None = None,
) -> Question:
    """Create a minimal Question for testing."""
    if topic_ids is None:
        topic_ids = ["t-a"]
    if correct_ids is None:
        correct_ids = ["A"]

    return Question(
        id=id,
        format=fmt,
        difficulty=difficulty,
        domain_id=domain_id,
        topic_ids=topic_ids,
        scenario="Scenario text" if fmt == QuestionFormat.SCENARIO_BASED else None,
        stem=f"Question stem for {id}",
        options=[
            {"id": "A", "text": "Option A", "is_correct": True},
            {"id": "B", "text": "Option B", "is_correct": False},
            {"id": "C", "text": "Option C", "is_correct": False},
            {"id": "D", "text": "Option D", "is_correct": False},
        ],
        correct_answer_ids=correct_ids,
        explanation="Explanation text",
        incorrect_explanations={"B": "Wrong B", "C": "Wrong C", "D": "Wrong D"},
    )


def _make_scored_topic(
    topic_id: str,
    topic_name: str,
    domain_ids: list[str],
    priority_score: int,
) -> ScoredTopic:
    """Create a ScoredTopic for testing."""
    return ScoredTopic(
        topic_id=topic_id,
        topic_name=topic_name,
        domain_ids=domain_ids,
        priority_score=priority_score,
        is_high_priority=priority_score >= HIGH_PRIORITY_THRESHOLD,
        domain_count=len(domain_ids),
    )


def _build_question_bank(
    n_easy: int = 20,
    n_intermediate: int = 20,
    n_advanced: int = 20,
) -> QuestionBank:
    """Build a question bank with a mix of formats and domains."""
    domains = ["domain-1", "domain-2", "domain-3", "domain-4", "domain-5", "domain-6"]
    formats_easy = [QuestionFormat.MULTIPLE_CHOICE]
    formats_inter = [QuestionFormat.MULTIPLE_CHOICE, QuestionFormat.MULTIPLE_SELECT]
    formats_adv = [QuestionFormat.SCENARIO_BASED, QuestionFormat.MULTIPLE_CHOICE]

    easy: list[Question] = []
    for i in range(n_easy):
        d = domains[i % len(domains)]
        easy.append(_make_question(
            f"easy-{i}", domain_id=d,
            fmt=formats_easy[i % len(formats_easy)],
            difficulty=DifficultyLevel.EASY,
        ))

    intermediate: list[Question] = []
    for i in range(n_intermediate):
        d = domains[i % len(domains)]
        fmt = formats_inter[i % len(formats_inter)]
        cids = ["A", "B"] if fmt == QuestionFormat.MULTIPLE_SELECT else ["A"]
        intermediate.append(_make_question(
            f"inter-{i}", domain_id=d, fmt=fmt,
            difficulty=DifficultyLevel.INTERMEDIATE,
            correct_ids=cids,
        ))

    advanced: list[Question] = []
    for i in range(n_advanced):
        d = domains[i % len(domains)]
        fmt = formats_adv[i % len(formats_adv)]
        advanced.append(_make_question(
            f"adv-{i}", domain_id=d, fmt=fmt,
            difficulty=DifficultyLevel.ADVANCED,
            topic_ids=["t-a", "t-b"],
        ))

    return QuestionBank(
        easy=easy,
        intermediate=intermediate,
        advanced=advanced,
        domain_distribution={d: 10 for d in domains},
    )


def _build_scores() -> ScoredTopicList:
    """Build a scored topic list with a high-priority topic."""
    return ScoredTopicList(
        topics=[
            _make_scored_topic("t-a", "Topic A", ["domain-1", "domain-2"], 9),
            _make_scored_topic("t-b", "Topic B", ["domain-2"], 7),
            _make_scored_topic("t-c", "Topic C", ["domain-3"], 5),
        ]
    )


# --- Tests ---


class TestMockExamBuilder:
    """Tests for MockExamBuilder.build()."""

    def test_minimum_50_questions(self):
        """The mock exam must contain at least 50 questions."""
        bank = _build_question_bank()
        scores = _build_scores()
        builder = MockExamBuilder()
        exam = builder.build(bank, scores)

        assert len(exam.questions) >= MIN_MOCK_EXAM_QUESTIONS

    def test_answer_key_completeness(self):
        """Every question must have an entry in the answer key."""
        bank = _build_question_bank()
        scores = _build_scores()
        builder = MockExamBuilder()
        exam = builder.build(bank, scores)

        for q in exam.questions:
            assert q.id in exam.answer_key
            assert exam.answer_key[q.id] == q.correct_answer_ids

    def test_solutions_for_every_question(self):
        """Every question must have a corresponding solution."""
        bank = _build_question_bank()
        scores = _build_scores()
        builder = MockExamBuilder()
        exam = builder.build(bank, scores)

        solution_ids = {s["question_id"] for s in exam.solutions}
        for q in exam.questions:
            assert q.id in solution_ids

    def test_format_distribution_minimum_15_percent(self):
        """Each format (MC, MS, scenario) must be >= 15% of total."""
        bank = _build_question_bank()
        scores = _build_scores()
        builder = MockExamBuilder()
        exam = builder.build(bank, scores)

        total = len(exam.questions)
        min_count = int(total * MIN_FORMAT_PROPORTION)

        for fmt in [
            QuestionFormat.MULTIPLE_CHOICE.value,
            QuestionFormat.MULTIPLE_SELECT.value,
            QuestionFormat.SCENARIO_BASED.value,
        ]:
            count = exam.format_distribution.get(fmt, 0)
            assert count >= min_count, (
                f"Format {fmt} has {count} questions, "
                f"expected at least {min_count} (15% of {total})"
            )

    def test_grading_rubric_pass_threshold(self):
        """Grading rubric must have 700/1000 pass threshold."""
        bank = _build_question_bank()
        scores = _build_scores()
        builder = MockExamBuilder()
        exam = builder.build(bank, scores)

        assert exam.grading_rubric.pass_threshold == PASS_THRESHOLD_SCORE
        assert exam.grading_rubric.max_score == PASS_THRESHOLD_MAX
        assert exam.grading_rubric.pass_percentage == pytest.approx(0.7)

    def test_grading_rubric_scoring_rules(self):
        """Rubric must specify 1 point per single answer and all-or-nothing for multi-select."""
        bank = _build_question_bank()
        scores = _build_scores()
        builder = MockExamBuilder()
        exam = builder.build(bank, scores)

        assert exam.grading_rubric.points_per_single_answer == 1
        assert exam.grading_rubric.multi_select_scoring == "all or nothing"

    def test_time_limit_120_minutes(self):
        """Time limit must be 120 minutes based on official GH-600 duration."""
        bank = _build_question_bank()
        scores = _build_scores()
        builder = MockExamBuilder()
        exam = builder.build(bank, scores)

        assert exam.time_limit_minutes == 120

    def test_high_priority_solutions_have_cross_references(self):
        """Solutions for high-priority topics include study notes references."""
        bank = _build_question_bank()
        scores = _build_scores()
        builder = MockExamBuilder()
        exam = builder.build(bank, scores)

        # Find solutions for questions with high-priority topic_ids
        for solution in exam.solutions:
            qid = solution["question_id"]
            question = next(q for q in exam.questions if q.id == qid)
            has_hp = any(
                st.priority_score >= HIGH_PRIORITY_THRESHOLD
                for tid in question.topic_ids
                for st in scores.topics
                if st.topic_id == tid
            )
            if has_hp:
                assert "study_notes_references" in solution
                assert len(solution["study_notes_references"]) > 0

    def test_domain_distribution_within_tolerance(self):
        """Domain distribution must be within ±5pp of target weights."""
        bank = _build_question_bank()
        scores = _build_scores()
        builder = MockExamBuilder()
        exam = builder.build(bank, scores)

        from src.config import EXAM_DOMAINS

        total = len(exam.questions)
        total_weight = sum(
            (d.weight_min + d.weight_max) / 2 for d in EXAM_DOMAINS
        )

        for domain in EXAM_DOMAINS:
            avg_weight = (domain.weight_min + domain.weight_max) / 2
            target_pct = (avg_weight / total_weight) * 100
            actual_count = exam.domain_distribution.get(domain.id, 0)
            actual_pct = (actual_count / total) * 100
            diff = abs(actual_pct - target_pct)
            assert diff <= 5.0, (
                f"Domain {domain.id}: target={target_pct:.1f}% "
                f"actual={actual_pct:.1f}% diff={diff:.1f}pp > 5pp"
            )

    def test_total_questions_in_rubric_matches(self):
        """Grading rubric total_questions must match selected question count."""
        bank = _build_question_bank()
        scores = _build_scores()
        builder = MockExamBuilder()
        exam = builder.build(bank, scores)

        assert exam.grading_rubric.total_questions == len(exam.questions)
