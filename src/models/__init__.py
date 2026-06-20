"""Pydantic data models for all pipeline phases."""

from src.models.knowledge import (
    ExtractionLog,
    ExtractionResult,
    KnowledgePoint,
    ParsedDocument,
)
from src.models.topic_map import (
    CrossReference,
    Dependency,
    Topic,
    TopicHierarchy,
)
from src.models.scoring import (
    ExamDomain,
    ExamObjective,
    ScoredTopic,
    ScoredTopicList,
)
from src.models.study_notes import (
    StudyNotesCollection,
    TopicNotes,
)
from src.models.curriculum import (
    Curriculum,
    Module,
)
from src.models.revision import (
    CheatSheet,
    Flashcard,
    Mnemonic,
    RevisionPackage,
)
from src.models.questions import (
    DifficultyLevel,
    Question,
    QuestionBank,
    QuestionFormat,
)
from src.models.mock_exam import (
    GradingRubric,
    MockExam,
)
from src.models.gap_analysis import (
    CoverageStatus,
    Gap,
    GapReport,
)
from src.models.readiness import (
    HighRiskTopic,
    ReadinessAssessment,
    RemediationPlan,
    TimeBlock,
)

__all__ = [
    # Knowledge extraction
    "KnowledgePoint",
    "ParsedDocument",
    "ExtractionResult",
    "ExtractionLog",
    # Topic mapping
    "Topic",
    "Dependency",
    "CrossReference",
    "TopicHierarchy",
    # Scoring
    "ExamDomain",
    "ExamObjective",
    "ScoredTopic",
    "ScoredTopicList",
    # Study notes
    "TopicNotes",
    "StudyNotesCollection",
    # Curriculum
    "Module",
    "Curriculum",
    # Revision
    "Flashcard",
    "CheatSheet",
    "Mnemonic",
    "RevisionPackage",
    # Questions
    "QuestionFormat",
    "DifficultyLevel",
    "Question",
    "QuestionBank",
    # Mock exam
    "GradingRubric",
    "MockExam",
    # Gap analysis
    "CoverageStatus",
    "Gap",
    "GapReport",
    # Readiness
    "TimeBlock",
    "HighRiskTopic",
    "RemediationPlan",
    "ReadinessAssessment",
]
