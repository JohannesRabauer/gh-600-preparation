"""Models for Phase 5: Structured Learning Course."""

from pydantic import BaseModel, Field


class Module(BaseModel):
    """A single curriculum module."""

    id: str  # e.g., "M01"
    title: str
    topic_ids: list[str]
    objectives: list[str]  # 2-7 items, Bloom's verbs
    prerequisites: list[str]  # Module IDs or ["none"]
    time_estimate_minutes: int = Field(ge=15, le=180)
    contains_high_priority: bool


class Curriculum(BaseModel):
    """Complete output of Phase 5."""

    modules: list[Module]
    total_time_minutes: int
    learning_path: list[str]  # Ordered module IDs
