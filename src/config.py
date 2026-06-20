"""Configuration module for the GH-600 Exam Prep Generator.

Defines exam domain data, pipeline constants, scoring parameters,
and source URLs for the Microsoft Learn GH-600 materials.
"""

from __future__ import annotations

from dataclasses import dataclass, field


# === Exam Domain Configuration ===


@dataclass(frozen=True)
class ExamDomain:
    """One of the 6 official GH-600 exam domains."""

    id: str
    name: str
    weight_min: float
    weight_max: float
    sub_topics: list[str] = field(default_factory=list)


# The 6 official GH-600 exam domains with their percentage weights.
EXAM_DOMAINS: list[ExamDomain] = [
    ExamDomain(
        id="domain-1",
        name="Prepare agent architecture and SDLC processes",
        weight_min=0.15,
        weight_max=0.20,
        sub_topics=[
            "Design agent architecture patterns",
            "Define SDLC integration points for AI agents",
            "Plan agent communication and orchestration",
            "Identify agent roles within development workflows",
            "Select appropriate agent frameworks and tools",
        ],
    ),
    ExamDomain(
        id="domain-2",
        name="Design and implement agentic solutions",
        weight_min=0.20,
        weight_max=0.25,
        sub_topics=[
            "Implement GitHub Copilot agent mode",
            "Design multi-step agent workflows",
            "Configure agent tools and capabilities",
            "Implement agent context management",
            "Build custom agent extensions",
            "Integrate agents with development environments",
        ],
    ),
    ExamDomain(
        id="domain-3",
        name="Evaluate and optimize agent performance",
        weight_min=0.10,
        weight_max=0.15,
        sub_topics=[
            "Measure agent output quality",
            "Optimize agent response latency",
            "Evaluate agent task completion rates",
            "Implement agent performance monitoring",
            "Tune agent parameters for efficiency",
        ],
    ),
    ExamDomain(
        id="domain-4",
        name="Secure and govern agentic AI solutions",
        weight_min=0.15,
        weight_max=0.20,
        sub_topics=[
            "Implement access controls for AI agents",
            "Configure agent permissions and boundaries",
            "Monitor agent actions for security compliance",
            "Implement data governance for agent interactions",
            "Manage secrets and credentials in agent workflows",
        ],
    ),
    ExamDomain(
        id="domain-5",
        name="Collaborate with AI agents in the development workflow",
        weight_min=0.15,
        weight_max=0.20,
        sub_topics=[
            "Use GitHub Copilot for code generation and review",
            "Leverage agent-assisted debugging and testing",
            "Integrate AI agents into CI/CD pipelines",
            "Collaborate with agents for documentation",
            "Manage agent-human interaction patterns",
        ],
    ),
    ExamDomain(
        id="domain-6",
        name="Implement responsible AI practices",
        weight_min=0.10,
        weight_max=0.15,
        sub_topics=[
            "Apply ethical guidelines to agent behavior",
            "Implement transparency and explainability",
            "Manage bias and fairness in agent outputs",
            "Ensure compliance with responsible AI policies",
            "Monitor and audit agent decisions",
        ],
    ),
]

# Lookup dictionary: domain ID -> ExamDomain
DOMAIN_BY_ID: dict[str, ExamDomain] = {d.id: d for d in EXAM_DOMAINS}


# === Pipeline Constants ===


# Link traversal limits (Requirement 1.2)
MAX_LINK_DEPTH: int = 2
MAX_LINKS_PER_LEVEL: int = 50

# Rate limiting and HTTP settings
MAX_CONCURRENT_REQUESTS: int = 5
REQUEST_DELAY_SECONDS: float = 1.0
REQUEST_TIMEOUT_SECONDS: float = 5.0
MAX_RETRIES: int = 1

# Allowed domains for link following
ALLOWED_DOMAINS: list[str] = [
    "learn.microsoft.com",
    "docs.github.com",
]


# === Scoring Parameters ===


# Maps domain weight ranges (as max weight) to base score ranges.
# Higher-weighted domains receive proportionally higher base scores.
# Format: (weight_max_threshold, base_score_min, base_score_max)
DOMAIN_WEIGHT_TO_BASE_SCORE: list[tuple[float, int, int]] = [
    (0.25, 8, 9),   # 20-25% weight → base score 8-9
    (0.20, 6, 8),   # 15-20% weight → base score 6-8
    (0.15, 5, 7),   # 10-15% weight → base score 5-7
]

# Cross-domain scoring bonus: +1 per additional domain (capped at max score)
CROSS_DOMAIN_BONUS: int = 1
MAX_PRIORITY_SCORE: int = 10
MIN_PRIORITY_SCORE: int = 1

# High-priority threshold
HIGH_PRIORITY_THRESHOLD: int = 8


# === Source URLs ===


# Primary source URLs for Microsoft Learn GH-600 materials.
SOURCE_URLS: list[str] = [
    # GH-600 study guide
    "https://learn.microsoft.com/en-us/credentials/certifications/resources/study-guides/gh-600",
    # Certification overview page
    "https://learn.microsoft.com/en-us/credentials/certifications/github-certified-agentic-ai-developer/",
    # Microsoft Learn training modules for GitHub Copilot agentic AI
    "https://learn.microsoft.com/en-us/training/modules/introduction-to-github-copilot/",
    "https://learn.microsoft.com/en-us/training/modules/configure-github-copilot/",
    "https://learn.microsoft.com/en-us/training/modules/github-copilot-agent-mode/",
    "https://learn.microsoft.com/en-us/training/modules/responsible-ai-with-github-copilot/",
]


# === Artifact Paths ===


ARTIFACTS_DIR: str = "artifacts"
DOCS_DIR: str = "docs"

# Phase output artifact filenames
ARTIFACT_FILENAMES: dict[str, str] = {
    "phase01": "phase01_extraction.json",
    "phase02": "phase02_topic_map.json",
    "phase03": "phase03_scores.json",
    "phase04": "phase04_notes.json",
    "phase05": "phase05_curriculum.json",
    "phase06": "phase06_revision.json",
    "phase07": "phase07_questions.json",
    "phase08": "phase08_mock_exam.json",
    "phase09": "phase09_gap_report.json",
    "phase10": "phase10_readiness.json",
}

# Pipeline error log
PIPELINE_ERROR_LOG: str = "pipeline_errors.json"


# === Study Notes Parameters ===


# Minimum content thresholds for study notes (Requirement 4)
MIN_OVERVIEW_SENTENCES: int = 3
MIN_EXPLANATION_WORDS: int = 200
MIN_EXPLANATION_WORDS_HIGH_PRIORITY: int = 400
MIN_KEY_FACTS: int = 3
MIN_COMMON_MISTAKES: int = 2
MIN_EXAMPLES: int = 1
MIN_EXAMPLES_HIGH_PRIORITY: int = 2
MIN_EXAM_TIPS: int = 1

# Sparse topic threshold (Requirement 4.6)
SPARSE_TOPIC_KNOWLEDGE_POINT_THRESHOLD: int = 3


# === Curriculum Parameters ===


# Module time estimates (Requirement 5.4)
MODULE_MIN_TIME_MINUTES: int = 15
MODULE_MAX_TIME_MINUTES: int = 180

# High-priority module time multiplier (Requirement 5.6)
HIGH_PRIORITY_TIME_MULTIPLIER: float = 1.5

# Bloom's Taxonomy verbs for learning objectives (Requirement 5.2)
BLOOMS_TAXONOMY_VERBS: list[str] = [
    "define", "describe", "identify", "list", "name", "recall", "recognize",
    "explain", "summarize", "classify", "compare", "contrast", "interpret",
    "apply", "demonstrate", "implement", "solve", "use", "execute",
    "analyze", "differentiate", "distinguish", "examine", "organize",
    "evaluate", "assess", "critique", "justify", "recommend",
    "create", "design", "develop", "construct", "produce", "propose",
]

# Module objectives count range (Requirement 5.2)
MIN_MODULE_OBJECTIVES: int = 2
MAX_MODULE_OBJECTIVES: int = 7


# === Revision Parameters ===


# Executive summary word limit (Requirement 6.1)
EXECUTIVE_SUMMARY_MAX_WORDS: int = 2000

# Minimum flashcard count (Requirement 6.3)
MIN_FLASHCARDS_TOTAL: int = 100

# Mnemonic threshold: topics with 3+ sequential steps (Requirement 6.4)
MNEMONIC_MIN_STEPS: int = 3


# === Question Parameters ===


# Minimum questions per difficulty level (Requirement 7.2)
MIN_QUESTIONS_PER_LEVEL: int = 20

# Advanced question scenario proportion (Requirement 7.5)
ADVANCED_SCENARIO_MIN_PROPORTION: float = 0.50


# === Mock Exam Parameters ===


# Minimum mock exam questions (Requirement 8.1)
MIN_MOCK_EXAM_QUESTIONS: int = 50

# Domain distribution tolerance (Requirement 8.2)
DOMAIN_DISTRIBUTION_TOLERANCE_PP: float = 5.0

# Minimum format proportion (Requirement 8.6)
MIN_FORMAT_PROPORTION: float = 0.15

# Grading (Requirement 8.5)
PASS_THRESHOLD_SCORE: int = 700
PASS_THRESHOLD_MAX: int = 1000


# === Gap Analysis Parameters ===


# Coverage thresholds (Requirements 9.1-9.3)
FULLY_COVERED_MIN_POINTS: int = 3
WEAKLY_COVERED_MIN_POINTS: int = 1

# Minimum resource recommendations per gap (Requirement 9.4)
MIN_RECOMMENDATIONS_PER_GAP: int = 2


# === Readiness Parameters ===


# Maximum high-risk topics (Requirement 10.2)
MAX_HIGH_RISK_TOPICS: int = 10

# Maximum last-minute revision areas (Requirement 10.3)
MAX_LAST_MINUTE_AREAS: int = 10

# Study plan time block duration (Requirement 10.4)
STUDY_BLOCK_MINUTES: int = 60

# Deferral threshold (Requirement 10.5)
READINESS_DEFERRAL_THRESHOLD: int = 70
