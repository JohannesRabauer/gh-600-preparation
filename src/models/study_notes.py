"""Models for Phase 4: Comprehensive Study Notes."""

from typing import Optional

from pydantic import BaseModel


class TopicNotes(BaseModel):
    """Study notes for a single topic."""

    topic_id: str
    topic_name: str
    domain_id: str
    priority_score: int
    overview: str  # Min 3 sentences
    explanation: str  # Min 200 words (400 for high-priority)
    key_facts: list[str]  # Min 3 items
    common_mistakes: list[str]  # Min 2 items
    examples: list[str]  # Min 1 (min 2 for high-priority)
    exam_tips: list[str]  # Min 1
    code_blocks: list[dict]  # {language, code, comments}
    step_by_step: Optional[list[dict]] = None  # {step, rationale}
    related_topics: list[dict]  # {topic_id, domain_name, relationship}
    is_supplemented: bool = False  # True if content was inferred


class StudyNotesCollection(BaseModel):
    """Complete output of Phase 4."""

    notes: list[TopicNotes]
    cross_domain_themes: list[dict]  # {theme, domains, manifestations}
