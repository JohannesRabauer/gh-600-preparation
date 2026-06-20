"""Models for Phase 3: Exam Relevance Analysis."""

from pydantic import BaseModel, Field


class ExamDomain(BaseModel):
    """One of the 6 official GH-600 exam domains."""

    id: str  # e.g., "domain-1"
    name: str  # e.g., "Prepare agent architecture and SDLC processes"
    weight_min: float  # e.g., 0.15
    weight_max: float  # e.g., 0.20
    sub_topics: list[str]  # Official sub-topic bullet points


class ExamObjective(BaseModel):
    """A single testable objective from the study guide."""

    id: str
    domain_id: str
    description: str
    sub_bullets: list[str]


class ScoredTopic(BaseModel):
    """A topic with its priority score."""

    topic_id: str
    topic_name: str
    domain_ids: list[str]
    priority_score: int = Field(ge=1, le=10)
    is_high_priority: bool  # True if score >= 8
    domain_count: int


class ScoredTopicList(BaseModel):
    """Complete output of Phase 3."""

    topics: list[ScoredTopic]  # Sorted by score desc, domain_count desc, name asc
