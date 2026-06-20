"""Models for Phase 7: Practice Questions."""

from enum import Enum
from typing import Optional

from pydantic import BaseModel


class QuestionFormat(str, Enum):
    """Question format types matching the GH-600 exam."""

    MULTIPLE_CHOICE = "multiple_choice"  # 4 options, 1 correct
    MULTIPLE_SELECT = "multiple_select"  # 4-6 options, 2+ correct
    SCENARIO_BASED = "scenario_based"  # Situational prompt + 4 options


class DifficultyLevel(str, Enum):
    """Question difficulty levels."""

    EASY = "easy"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"


class Question(BaseModel):
    """A single practice question."""

    id: str
    format: QuestionFormat
    difficulty: DifficultyLevel
    domain_id: str
    topic_ids: list[str]
    scenario: Optional[str] = None  # For scenario-based questions
    stem: str  # The question text
    options: list[dict]  # {id, text, is_correct}
    correct_answer_ids: list[str]
    explanation: str  # Reasoning + concept + study notes ref
    incorrect_explanations: dict  # {option_id: why_wrong}


class QuestionBank(BaseModel):
    """Complete output of Phase 7."""

    easy: list[Question]  # Min 20
    intermediate: list[Question]  # Min 20
    advanced: list[Question]  # Min 20
    domain_distribution: dict[str, int]
