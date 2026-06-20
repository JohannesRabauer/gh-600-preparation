"""Models for Phase 10: Final Readiness Assessment."""

from typing import Optional

from pydantic import BaseModel, Field


class TimeBlock(BaseModel):
    """A 60-minute study block."""

    start_hour: int  # e.g., 0 = first hour
    topic: str
    resource_type: str  # "study_notes" | "flashcards" | "practice_questions"
    priority_score: int


class HighRiskTopic(BaseModel):
    """A topic identified as high-risk."""

    topic_id: str
    topic_name: str
    priority_score: int
    gap_reason: str  # Why it's high-risk
    missing_points: int


class RemediationPlan(BaseModel):
    """Plan for when readiness score < 70."""

    target_duration_days: int
    modules_to_revisit: list[str]  # Module IDs
    daily_schedule: list[dict]  # {day, topics, activities}


class ReadinessAssessment(BaseModel):
    """Complete output of Phase 10."""

    readiness_score: int = Field(ge=0, le=100)
    score_components: dict  # {coverage_pct, notes_pct, inverse_gap_pct}
    high_risk_topics: list[HighRiskTopic]  # Max 10
    last_minute_areas: list[dict]  # Max 10, sorted by domain_weight * gap_severity
    study_plan_24h: list[TimeBlock]
    remediation_plan: Optional[RemediationPlan] = None  # Only if score < 70
    recommendation: str  # "ready" | "defer"
