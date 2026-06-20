"""Models for Phase 2: Topic Mapping and Hierarchy."""

from typing import Optional

from pydantic import BaseModel


class Topic(BaseModel):
    """A single topic in the hierarchy."""

    id: str
    name: str
    domain_id: str
    sub_domain: Optional[str] = None
    knowledge_point_ids: list[str]
    description: str


class Dependency(BaseModel):
    """A prerequisite relationship between topics."""

    source_topic_id: str
    target_topic_id: str
    relationship: str  # e.g., "requires understanding of"


class CrossReference(BaseModel):
    """A cross-reference between related topics."""

    topic_id_a: str
    topic_id_b: str
    shared_concept: str  # tool, API, pattern, or workflow name


class TopicHierarchy(BaseModel):
    """Complete output of Phase 2."""

    domains: dict[str, list[Topic]]
    dependencies: list[Dependency]
    cross_references: list[CrossReference]
    learning_order: list[str]  # Ordered topic IDs
    learning_units: list[list[str]]  # Cyclic groups merged into units
