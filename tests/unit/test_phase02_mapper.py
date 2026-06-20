"""Unit tests for the TopicMapper (Phase 2)."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from src.config import EXAM_DOMAINS, ExamDomain
from src.models.knowledge import ExtractionResult, KnowledgePoint, ParsedDocument
from src.models.topic_map import CrossReference, Dependency, Topic, TopicHierarchy
from src.phases.phase02_mapper import TopicMapper


# --- Fixtures and helpers ---


def _make_kp(
    id: str,
    content: str,
    category: str = "concept",
    is_prerequisite: bool = False,
) -> KnowledgePoint:
    """Create a KnowledgePoint for testing."""
    return KnowledgePoint(
        id=id,
        content=content,
        category=category,
        source_url="https://learn.microsoft.com/test",
        source_title="Test Page",
        depth=0,
        is_prerequisite=is_prerequisite,
    )


def _make_extraction_result(points: list[KnowledgePoint]) -> ExtractionResult:
    """Create an ExtractionResult with the given knowledge points."""
    return ExtractionResult(
        documents=[
            ParsedDocument(
                url="https://learn.microsoft.com/test",
                title="Test Page",
                content_text="Test content.",
                links=[],
                knowledge_points=points,
            )
        ],
        all_knowledge_points=points,
        error_log=[],
        visited_urls={"https://learn.microsoft.com/test"},
        stats={"by_depth": {"depth_0": len(points)}, "by_category": {}},
    )


@pytest.fixture
def mapper() -> TopicMapper:
    """Provide a TopicMapper with default exam domains."""
    return TopicMapper(exam_domains=EXAM_DOMAINS)


@pytest.fixture
def sample_knowledge_points() -> list[KnowledgePoint]:
    """Provide sample knowledge points covering multiple domains."""
    return [
        _make_kp(
            "kp-001",
            "Design agent architecture patterns for building scalable AI systems "
            "that integrate with software development lifecycle processes.",
        ),
        _make_kp(
            "kp-002",
            "Implement GitHub Copilot agent mode to enable multi-step agent "
            "workflows that can write code, run terminal commands, and iterate.",
        ),
        _make_kp(
            "kp-003",
            "Measure agent output quality and evaluate agent task completion "
            "rates using performance monitoring dashboards.",
        ),
        _make_kp(
            "kp-004",
            "Implement access controls for AI agents and configure agent "
            "permissions and boundaries to secure agentic solutions.",
        ),
        _make_kp(
            "kp-005",
            "Use GitHub Copilot for code generation and review in collaborative "
            "development workflow with CI/CD pipeline integration.",
        ),
        _make_kp(
            "kp-006",
            "Apply ethical guidelines to agent behavior and implement "
            "transparency and explainability in responsible AI practices.",
        ),
        _make_kp(
            "kp-007",
            "Before you begin working with agent mode, familiarity with "
            "software development lifecycle and architecture patterns is required.",
            category="concept",
            is_prerequisite=True,
        ),
    ]


# --- Tests ---


class TestTopicMapperInit:
    """Tests for TopicMapper initialization."""

    def test_default_domains(self) -> None:
        """TopicMapper uses EXAM_DOMAINS by default."""
        mapper = TopicMapper()
        assert mapper._exam_domains == EXAM_DOMAINS
        assert len(mapper._exam_domains) == 6

    def test_custom_domains(self) -> None:
        """TopicMapper accepts custom domain list."""
        custom = [
            ExamDomain(
                id="test-1",
                name="Test Domain",
                weight_min=0.5,
                weight_max=0.5,
                sub_topics=["sub-a"],
            )
        ]
        mapper = TopicMapper(exam_domains=custom)
        assert len(mapper._exam_domains) == 1
        assert mapper._exam_domains[0].id == "test-1"


class TestAssignToDomains:
    """Tests for _assign_to_domains method."""

    def test_assigns_all_points_to_domains(
        self, mapper: TopicMapper, sample_knowledge_points: list[KnowledgePoint]
    ) -> None:
        """All knowledge points are assigned to at least one domain."""
        extraction = _make_extraction_result(sample_knowledge_points)
        mapper._kp_data = {
            kp.id: {
                "content": kp.content,
                "category": kp.category,
                "is_prerequisite": kp.is_prerequisite,
                "source_url": kp.source_url,
            }
            for kp in sample_knowledge_points
        }
        domains = mapper._assign_to_domains(sample_knowledge_points)

        # All domain IDs should be present in the result
        for domain in EXAM_DOMAINS:
            assert domain.id in domains

        # Total knowledge point IDs across all topics should cover all input
        all_kp_ids: set[str] = set()
        for topic_list in domains.values():
            for topic in topic_list:
                all_kp_ids.update(topic.knowledge_point_ids)

        input_kp_ids = {kp.id for kp in sample_knowledge_points}
        assert input_kp_ids == all_kp_ids

    def test_architecture_point_assigned_to_domain1(
        self, mapper: TopicMapper
    ) -> None:
        """Point about architecture is assigned to domain-1."""
        points = [
            _make_kp(
                "kp-arch",
                "Design agent architecture patterns for building AI systems "
                "that integrate with SDLC processes and development workflows.",
            )
        ]
        mapper._kp_data = {
            kp.id: {"content": kp.content, "category": kp.category,
                    "is_prerequisite": kp.is_prerequisite, "source_url": kp.source_url}
            for kp in points
        }
        domains = mapper._assign_to_domains(points)
        domain1_kp_ids = set()
        for topic in domains.get("domain-1", []):
            domain1_kp_ids.update(topic.knowledge_point_ids)
        assert "kp-arch" in domain1_kp_ids

    def test_security_point_assigned_to_domain4(
        self, mapper: TopicMapper
    ) -> None:
        """Point about security is assigned to domain-4."""
        points = [
            _make_kp(
                "kp-sec",
                "Implement access controls for AI agents and configure agent "
                "permissions and boundaries to maintain security compliance.",
            )
        ]
        mapper._kp_data = {
            kp.id: {"content": kp.content, "category": kp.category,
                    "is_prerequisite": kp.is_prerequisite, "source_url": kp.source_url}
            for kp in points
        }
        domains = mapper._assign_to_domains(points)
        domain4_kp_ids = set()
        for topic in domains.get("domain-4", []):
            domain4_kp_ids.update(topic.knowledge_point_ids)
        assert "kp-sec" in domain4_kp_ids


class TestTopicGeneration:
    """Tests for topic ID and name generation."""

    def test_topic_ids_sequential(self, mapper: TopicMapper) -> None:
        """Topic IDs are generated sequentially."""
        id1 = mapper._generate_topic_id()
        id2 = mapper._generate_topic_id()
        assert id1 == "topic-001"
        assert id2 == "topic-002"

    def test_topic_name_derived_from_content(self, mapper: TopicMapper) -> None:
        """Topic names are derived from knowledge point content."""
        points = [
            _make_kp("kp-t1", "GitHub Copilot agent mode enables developers to work more efficiently."),
        ]
        name = mapper._derive_topic_name(points, "Fallback Name")
        assert "GitHub Copilot agent mode" in name

    def test_topic_name_truncated_when_long(self, mapper: TopicMapper) -> None:
        """Long topic names are truncated with ellipsis."""
        points = [
            _make_kp(
                "kp-t1",
                "This is a very long first sentence that goes on and on about many "
                "different things and should be truncated. Second sentence.",
            ),
        ]
        name = mapper._derive_topic_name(points, "Fallback")
        assert len(name) <= 63  # 60 + "..."


class TestIdentifyPrerequisites:
    """Tests for _identify_prerequisites method."""

    def test_prerequisite_points_create_dependencies(
        self, mapper: TopicMapper
    ) -> None:
        """Topics with prerequisite knowledge points create dependencies."""
        prereq_topic = Topic(
            id="topic-001",
            name="Prerequisites for Agent Mode",
            domain_id="domain-1",
            knowledge_point_ids=["kp-prereq"],
            description="Prerequisite concepts for understanding agent mode.",
        )
        target_topic = Topic(
            id="topic-002",
            name="Agent Mode Implementation",
            domain_id="domain-2",
            knowledge_point_ids=["kp-agent"],
            description="Implementing agent mode features.",
        )

        mapper._kp_data = {
            "kp-prereq": {
                "content": "Prerequisite concept: understanding of software architecture "
                "patterns, agent design, development workflow integration, and lifecycle processes.",
                "category": "concept",
                "is_prerequisite": True,
                "source_url": "https://example.com",
            },
            "kp-agent": {
                "content": "Agent mode uses software architecture patterns and agent design "
                "principles for development workflow integration and lifecycle management.",
                "category": "procedure",
                "is_prerequisite": False,
                "source_url": "https://example.com",
            },
        }

        deps = mapper._identify_prerequisites([prereq_topic, target_topic])
        # Should detect that prereq_topic is a prerequisite for target_topic
        assert len(deps) >= 1
        assert any(
            d.source_topic_id == "topic-001" and d.target_topic_id == "topic-002"
            for d in deps
        )

    def test_no_self_dependencies(self, mapper: TopicMapper) -> None:
        """A topic cannot be its own prerequisite."""
        topic = Topic(
            id="topic-001",
            name="Test Topic",
            domain_id="domain-1",
            knowledge_point_ids=["kp-1"],
            description="A test topic.",
        )
        mapper._kp_data = {
            "kp-1": {
                "content": "Some content about testing concepts and approaches.",
                "category": "concept",
                "is_prerequisite": False,
                "source_url": "https://example.com",
            },
        }

        deps = mapper._identify_prerequisites([topic])
        assert not any(d.source_topic_id == d.target_topic_id for d in deps)


class TestComputeLearningOrder:
    """Tests for _compute_learning_order (Kahn's algorithm)."""

    def test_respects_prerequisite_ordering(self, mapper: TopicMapper) -> None:
        """Topics appear after their prerequisites in learning order."""
        topics = [
            Topic(id="t-a", name="A", domain_id="domain-1",
                  knowledge_point_ids=[], description="Topic A"),
            Topic(id="t-b", name="B", domain_id="domain-1",
                  knowledge_point_ids=[], description="Topic B"),
            Topic(id="t-c", name="C", domain_id="domain-1",
                  knowledge_point_ids=[], description="Topic C"),
        ]
        deps = [
            Dependency(source_topic_id="t-a", target_topic_id="t-b",
                       relationship="requires understanding of"),
            Dependency(source_topic_id="t-b", target_topic_id="t-c",
                       relationship="requires understanding of"),
        ]

        order = mapper._compute_learning_order(topics, deps)

        # A must come before B, B must come before C
        assert order.index("t-a") < order.index("t-b")
        assert order.index("t-b") < order.index("t-c")

    def test_all_topics_included_in_order(self, mapper: TopicMapper) -> None:
        """All topics appear in the learning order."""
        topics = [
            Topic(id=f"t-{i}", name=f"Topic {i}", domain_id="domain-1",
                  knowledge_point_ids=[], description=f"Topic {i}")
            for i in range(5)
        ]
        deps: list[Dependency] = []

        order = mapper._compute_learning_order(topics, deps)
        assert len(order) == 5
        assert set(order) == {f"t-{i}" for i in range(5)}

    def test_no_topic_before_its_prerequisites(self, mapper: TopicMapper) -> None:
        """No topic appears before any of its prerequisites."""
        topics = [
            Topic(id="t-1", name="Foundations", domain_id="domain-1",
                  knowledge_point_ids=[], description=""),
            Topic(id="t-2", name="Intermediate", domain_id="domain-2",
                  knowledge_point_ids=[], description=""),
            Topic(id="t-3", name="Advanced", domain_id="domain-3",
                  knowledge_point_ids=[], description=""),
        ]
        deps = [
            Dependency(source_topic_id="t-1", target_topic_id="t-2",
                       relationship="prerequisite"),
            Dependency(source_topic_id="t-1", target_topic_id="t-3",
                       relationship="prerequisite"),
            Dependency(source_topic_id="t-2", target_topic_id="t-3",
                       relationship="prerequisite"),
        ]

        order = mapper._compute_learning_order(topics, deps)
        # t-1 before t-2, t-1 before t-3, t-2 before t-3
        assert order.index("t-1") < order.index("t-2")
        assert order.index("t-1") < order.index("t-3")
        assert order.index("t-2") < order.index("t-3")


class TestDetectCycles:
    """Tests for _detect_cycles method."""

    def test_no_cycles_returns_empty(self, mapper: TopicMapper) -> None:
        """When there are no cycles, returns empty list."""
        deps = [
            Dependency(source_topic_id="t-1", target_topic_id="t-2",
                       relationship="prerequisite"),
            Dependency(source_topic_id="t-2", target_topic_id="t-3",
                       relationship="prerequisite"),
        ]
        cycles = mapper._detect_cycles(deps)
        assert cycles == []

    def test_detects_simple_cycle(self, mapper: TopicMapper) -> None:
        """Detects a simple A -> B -> A cycle."""
        deps = [
            Dependency(source_topic_id="t-a", target_topic_id="t-b",
                       relationship="requires"),
            Dependency(source_topic_id="t-b", target_topic_id="t-a",
                       relationship="requires"),
        ]
        cycles = mapper._detect_cycles(deps)
        assert len(cycles) == 1
        assert set(cycles[0]) == {"t-a", "t-b"}

    def test_detects_three_node_cycle(self, mapper: TopicMapper) -> None:
        """Detects A -> B -> C -> A cycle."""
        deps = [
            Dependency(source_topic_id="t-a", target_topic_id="t-b",
                       relationship="requires"),
            Dependency(source_topic_id="t-b", target_topic_id="t-c",
                       relationship="requires"),
            Dependency(source_topic_id="t-c", target_topic_id="t-a",
                       relationship="requires"),
        ]
        cycles = mapper._detect_cycles(deps)
        assert len(cycles) == 1
        assert set(cycles[0]) == {"t-a", "t-b", "t-c"}

    def test_multiple_independent_cycles(self, mapper: TopicMapper) -> None:
        """Detects multiple independent cycles."""
        deps = [
            # Cycle 1: A <-> B
            Dependency(source_topic_id="t-a", target_topic_id="t-b",
                       relationship="requires"),
            Dependency(source_topic_id="t-b", target_topic_id="t-a",
                       relationship="requires"),
            # Cycle 2: C <-> D
            Dependency(source_topic_id="t-c", target_topic_id="t-d",
                       relationship="requires"),
            Dependency(source_topic_id="t-d", target_topic_id="t-c",
                       relationship="requires"),
        ]
        cycles = mapper._detect_cycles(deps)
        assert len(cycles) == 2


class TestIdentifyCrossReferences:
    """Tests for _identify_cross_references method."""

    def test_shared_tool_creates_cross_reference(self, mapper: TopicMapper) -> None:
        """Topics in different domains sharing a tool get cross-referenced."""
        topics = [
            Topic(
                id="t-1", name="Using Copilot in Architecture",
                domain_id="domain-1",
                knowledge_point_ids=["kp-1"],
                description="GitHub Copilot assists in designing architectures.",
            ),
            Topic(
                id="t-2", name="Copilot for Code Review",
                domain_id="domain-5",
                knowledge_point_ids=["kp-2"],
                description="GitHub Copilot enables automated code review in workflows.",
            ),
        ]
        mapper._kp_data = {
            "kp-1": {"content": "Use GitHub Copilot for architecture design.",
                     "category": "concept", "is_prerequisite": False, "source_url": ""},
            "kp-2": {"content": "Use GitHub Copilot for code review.",
                     "category": "concept", "is_prerequisite": False, "source_url": ""},
        }

        refs = mapper._identify_cross_references(topics)
        assert len(refs) >= 1
        assert any(
            (r.topic_id_a == "t-1" and r.topic_id_b == "t-2")
            or (r.topic_id_a == "t-2" and r.topic_id_b == "t-1")
            for r in refs
        )

    def test_same_domain_not_cross_referenced(self, mapper: TopicMapper) -> None:
        """Topics in the same domain do not get cross-referenced."""
        topics = [
            Topic(
                id="t-1", name="Topic A",
                domain_id="domain-1",
                knowledge_point_ids=["kp-1"],
                description="GitHub Copilot for task A.",
            ),
            Topic(
                id="t-2", name="Topic B",
                domain_id="domain-1",
                knowledge_point_ids=["kp-2"],
                description="GitHub Copilot for task B.",
            ),
        ]
        mapper._kp_data = {
            "kp-1": {"content": "GitHub Copilot helps with task A.",
                     "category": "concept", "is_prerequisite": False, "source_url": ""},
            "kp-2": {"content": "GitHub Copilot helps with task B.",
                     "category": "concept", "is_prerequisite": False, "source_url": ""},
        }

        refs = mapper._identify_cross_references(topics)
        # Should be empty since both topics are in domain-1
        assert len(refs) == 0

    def test_no_shared_keywords_no_cross_reference(self, mapper: TopicMapper) -> None:
        """Topics without shared concepts don't get cross-referenced."""
        topics = [
            Topic(
                id="t-1", name="Architecture Design",
                domain_id="domain-1",
                knowledge_point_ids=["kp-1"],
                description="Designing system architecture for scalability.",
            ),
            Topic(
                id="t-2", name="Ethical AI Practices",
                domain_id="domain-6",
                knowledge_point_ids=["kp-2"],
                description="Managing bias and fairness in outputs.",
            ),
        ]
        mapper._kp_data = {
            "kp-1": {"content": "System architecture for scalability.",
                     "category": "concept", "is_prerequisite": False, "source_url": ""},
            "kp-2": {"content": "Managing bias and fairness in outputs.",
                     "category": "concept", "is_prerequisite": False, "source_url": ""},
        }

        refs = mapper._identify_cross_references(topics)
        assert len(refs) == 0


class TestMapTopicsIntegration:
    """Integration tests for the full map_topics pipeline."""

    def test_map_topics_produces_valid_hierarchy(
        self, mapper: TopicMapper, sample_knowledge_points: list[KnowledgePoint]
    ) -> None:
        """map_topics produces a valid TopicHierarchy with all fields populated."""
        extraction = _make_extraction_result(sample_knowledge_points)

        # Temporarily patch _write_artifact to avoid file system writes
        mapper._write_artifact = lambda h: None  # type: ignore[assignment]

        hierarchy = mapper.map_topics(extraction)

        assert isinstance(hierarchy, TopicHierarchy)
        assert len(hierarchy.domains) == 6
        assert isinstance(hierarchy.dependencies, list)
        assert isinstance(hierarchy.cross_references, list)
        assert isinstance(hierarchy.learning_order, list)
        assert isinstance(hierarchy.learning_units, list)

        # All topic IDs should appear in learning_order
        all_topic_ids: set[str] = set()
        for topic_list in hierarchy.domains.values():
            for topic in topic_list:
                all_topic_ids.add(topic.id)

        assert set(hierarchy.learning_order) == all_topic_ids

    def test_map_topics_writes_artifact(self, tmp_path: Path) -> None:
        """map_topics writes the artifact to disk."""
        import src.phases.phase02_mapper as mapper_module

        # Temporarily override ARTIFACTS_DIR
        original_dir = mapper_module.ARTIFACTS_DIR
        mapper_module.ARTIFACTS_DIR = str(tmp_path)

        try:
            points = [
                _make_kp(
                    "kp-001",
                    "Design agent architecture patterns and SDLC integration "
                    "points for AI agent communication and orchestration.",
                ),
            ]
            extraction = _make_extraction_result(points)

            m = TopicMapper()
            hierarchy = m.map_topics(extraction)

            artifact_path = tmp_path / "phase02_topic_map.json"
            assert artifact_path.exists()

            data = json.loads(artifact_path.read_text(encoding="utf-8"))
            assert "domains" in data
            assert "dependencies" in data
            assert "cross_references" in data
            assert "learning_order" in data
            assert "learning_units" in data
        finally:
            mapper_module.ARTIFACTS_DIR = original_dir
