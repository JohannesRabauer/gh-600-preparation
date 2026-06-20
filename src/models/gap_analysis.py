"""Models for Phase 9: Knowledge Gap Analysis."""

from enum import Enum

from pydantic import BaseModel


class CoverageStatus(str, Enum):
    """Coverage classification for exam objectives."""

    FULLY_COVERED = "fully_covered"
    WEAKLY_COVERED = "weakly_covered"
    NOT_COVERED = "not_covered"


class Gap(BaseModel):
    """A single coverage gap."""

    objective_id: str
    objective_description: str
    domain_id: str
    status: CoverageStatus
    knowledge_point_count: int
    is_critical: bool  # True if high-priority + gap
    recommendations: list[dict]  # {resource, description, topic_area}


class GapReport(BaseModel):
    """Complete output of Phase 9."""

    coverage_items: list[dict]  # {objective_id, status, point_count}
    critical_gaps: list[Gap]  # High-priority gaps at top
    weak_gaps: list[Gap]
    not_covered_gaps: list[Gap]
    total_objectives: int
    fully_covered_count: int
    weakly_covered_count: int
    not_covered_count: int
