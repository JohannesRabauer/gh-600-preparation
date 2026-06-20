"""Models for Phase 8: Mock Exam."""

from pydantic import BaseModel

from src.models.questions import Question


class GradingRubric(BaseModel):
    """Grading rules for the mock exam."""

    total_questions: int
    points_per_single_answer: int  # 1
    multi_select_scoring: str  # "all or nothing"
    max_score: int
    pass_threshold: int  # 700/1000
    pass_percentage: float  # 70%


class MockExam(BaseModel):
    """Complete output of Phase 8."""

    questions: list[Question]  # Min 50
    answer_key: dict[str, list[str]]  # {question_id: correct_ids}
    solutions: list[dict]  # {question_id, reasoning, incorrect_explanations, domain, topic}
    grading_rubric: GradingRubric
    time_limit_minutes: int
    domain_distribution: dict[str, int]
    format_distribution: dict[str, int]
