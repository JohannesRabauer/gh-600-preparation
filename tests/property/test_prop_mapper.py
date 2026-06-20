"""Property-based tests for Phase 2: Topic Mapper.

Tests correctness properties 3 and 4 from the design document:
- Property 3: Topic Learning Order is Valid Topological Sort
- Property 4: Cycle Detection Groups Mutually Dependent Topics

**Validates: Requirements 2.4, 2.6**
"""

from __future__ import annotations

from collections import defaultdict, deque

import pytest
from hypothesis import given, settings, HealthCheck
from hypothesis import strategies as st

from src.models.topic_map import Dependency, Topic
from src.phases.phase02_mapper import TopicMapper


# === Strategies ===


def _topic_id(index: int) -> str:
    """Generate a deterministic topic ID from an index."""
    return f"topic-{index:03d}"


@st.composite
def _dag_topics_and_deps(
    draw: st.DrawFn,
    min_topics: int = 2,
    max_topics: int = 20,
) -> tuple[list[Topic], list[Dependency]]:
    """Generate a random DAG of topics with dependency edges.

    Uses the strategy of assigning an ordering to nodes, then only
    creating edges from lower-indexed to higher-indexed nodes,
    guaranteeing acyclicity.
    """
    num_topics = draw(st.integers(min_value=min_topics, max_value=max_topics))

    topics = [
        Topic(
            id=_topic_id(i),
            name=f"Topic {i}",
            domain_id="domain-1",
            sub_domain=None,
            knowledge_point_ids=[f"kp-{i}"],
            description=f"Description for topic {i}",
        )
        for i in range(num_topics)
    ]

    # Generate edges only from lower-indexed to higher-indexed nodes (DAG)
    possible_edges = [
        (i, j) for i in range(num_topics) for j in range(i + 1, num_topics)
    ]

    # Draw a subset of possible edges
    if possible_edges:
        edges = draw(
            st.lists(
                st.sampled_from(possible_edges),
                min_size=0,
                max_size=min(len(possible_edges), num_topics * 2),
                unique=True,
            )
        )
    else:
        edges = []

    # source_topic_id is the prerequisite (must come BEFORE target in learning order)
    dependencies = [
        Dependency(
            source_topic_id=_topic_id(src),
            target_topic_id=_topic_id(tgt),
            relationship="requires understanding of",
        )
        for src, tgt in edges
    ]

    return topics, dependencies


@st.composite
def _graph_with_cycles(
    draw: st.DrawFn,
    min_topics: int = 3,
    max_topics: int = 15,
) -> tuple[list[Dependency], list[set[str]]]:
    """Generate a directed graph that contains at least one cycle.

    Returns the dependency list and the expected cycle groups (sets of
    node IDs that form strongly connected components with size > 1).
    """
    num_topics = draw(st.integers(min_value=min_topics, max_value=max_topics))

    # First, create at least one guaranteed cycle
    num_cycle_nodes = draw(st.integers(min_value=2, max_value=min(num_topics, 6)))
    cycle_node_indices = list(range(num_cycle_nodes))

    # Create a cycle: 0 -> 1 -> 2 -> ... -> (n-1) -> 0
    cycle_edges: list[tuple[int, int]] = []
    for i in range(num_cycle_nodes):
        next_i = (i + 1) % num_cycle_nodes
        cycle_edges.append((cycle_node_indices[i], cycle_node_indices[next_i]))

    # Optionally add extra edges within the cycle to strengthen connectivity
    extra_cycle_edges = draw(
        st.lists(
            st.tuples(
                st.sampled_from(cycle_node_indices),
                st.sampled_from(cycle_node_indices),
            ).filter(lambda t: t[0] != t[1]),
            min_size=0,
            max_size=num_cycle_nodes,
        )
    )
    cycle_edges.extend(extra_cycle_edges)

    # Add non-cycle nodes with edges that don't create cycles
    # Non-cycle nodes only have edges TO cycle nodes or between themselves in DAG order
    non_cycle_indices = list(range(num_cycle_nodes, num_topics))
    non_cycle_edges: list[tuple[int, int]] = []

    if non_cycle_indices:
        # Edges from non-cycle nodes to cycle nodes (won't create cycles
        # as long as there's no edge back from cycle to non-cycle nodes)
        for idx in non_cycle_indices:
            if draw(st.booleans()):
                target = draw(st.sampled_from(cycle_node_indices))
                non_cycle_edges.append((idx, target))

        # DAG edges among non-cycle nodes only (lower to higher index)
        for i in range(len(non_cycle_indices)):
            for j in range(i + 1, len(non_cycle_indices)):
                if draw(st.booleans()) and draw(st.booleans()):  # ~25% chance
                    non_cycle_edges.append(
                        (non_cycle_indices[i], non_cycle_indices[j])
                    )

    all_edges = list(set(cycle_edges + non_cycle_edges))

    dependencies = [
        Dependency(
            source_topic_id=_topic_id(src),
            target_topic_id=_topic_id(tgt),
            relationship="requires understanding of",
        )
        for src, tgt in all_edges
    ]

    # Compute the actual SCCs using Tarjan's algorithm to know expected cycles
    expected_cycles = _compute_sccs(num_topics, all_edges)

    return dependencies, expected_cycles


def _compute_sccs(
    num_nodes: int, edges: list[tuple[int, int]]
) -> list[set[str]]:
    """Compute strongly connected components with size > 1 (reference implementation)."""
    adjacency: dict[int, list[int]] = defaultdict(list)
    for src, tgt in edges:
        adjacency[src].append(tgt)

    index_counter = [0]
    stack: list[int] = []
    lowlink: dict[int, int] = {}
    index: dict[int, int] = {}
    on_stack: set[int] = set()
    sccs: list[set[str]] = []

    def strongconnect(node: int) -> None:
        index[node] = index_counter[0]
        lowlink[node] = index_counter[0]
        index_counter[0] += 1
        stack.append(node)
        on_stack.add(node)

        for neighbor in adjacency.get(node, []):
            if neighbor not in index:
                strongconnect(neighbor)
                lowlink[node] = min(lowlink[node], lowlink[neighbor])
            elif neighbor in on_stack:
                lowlink[node] = min(lowlink[node], index[neighbor])

        if lowlink[node] == index[node]:
            scc: set[str] = set()
            while True:
                w = stack.pop()
                on_stack.discard(w)
                scc.add(_topic_id(w))
                if w == node:
                    break
            if len(scc) > 1:
                sccs.append(scc)

    for node in range(num_nodes):
        if node not in index:
            strongconnect(node)

    return sccs


@st.composite
def _dag_chain(draw: st.DrawFn) -> tuple[list[Topic], list[Dependency]]:
    """Generate a simple linear chain of topics (A -> B -> C -> ...)."""
    length = draw(st.integers(min_value=2, max_value=10))

    topics = [
        Topic(
            id=_topic_id(i),
            name=f"Chain Topic {i}",
            domain_id="domain-1",
            sub_domain=None,
            knowledge_point_ids=[f"kp-{i}"],
            description=f"Chain topic {i}",
        )
        for i in range(length)
    ]

    # Chain: each topic depends on the previous one
    dependencies = [
        Dependency(
            source_topic_id=_topic_id(i),
            target_topic_id=_topic_id(i + 1),
            relationship="requires understanding of",
        )
        for i in range(length - 1)
    ]

    return topics, dependencies


@st.composite
def _dag_wide(draw: st.DrawFn) -> tuple[list[Topic], list[Dependency]]:
    """Generate a wide/flat DAG where one root has many children."""
    num_children = draw(st.integers(min_value=2, max_value=12))

    topics = [
        Topic(
            id=_topic_id(0),
            name="Root Topic",
            domain_id="domain-1",
            sub_domain=None,
            knowledge_point_ids=["kp-root"],
            description="Root topic",
        )
    ] + [
        Topic(
            id=_topic_id(i + 1),
            name=f"Child Topic {i}",
            domain_id="domain-1",
            sub_domain=None,
            knowledge_point_ids=[f"kp-child-{i}"],
            description=f"Child topic {i}",
        )
        for i in range(num_children)
    ]

    # Root is prerequisite for all children
    dependencies = [
        Dependency(
            source_topic_id=_topic_id(0),
            target_topic_id=_topic_id(i + 1),
            relationship="requires understanding of",
        )
        for i in range(num_children)
    ]

    return topics, dependencies


# === Helpers ===


def _is_valid_topological_sort(
    order: list[str], deps: list[Dependency]
) -> tuple[bool, str]:
    """Check if an ordering is a valid topological sort given the dependencies.

    For every dependency (source -> target), source must appear before target.
    Returns (True, "") or (False, reason).
    """
    if not order:
        return True, ""

    position = {topic_id: idx for idx, topic_id in enumerate(order)}

    for dep in deps:
        src = dep.source_topic_id
        tgt = dep.target_topic_id

        if src not in position:
            continue  # source not in the topic set (skip)
        if tgt not in position:
            continue  # target not in the topic set (skip)

        if position[src] >= position[tgt]:
            return False, (
                f"Dependency violation: '{src}' (pos {position[src]}) "
                f"should come before '{tgt}' (pos {position[tgt]})"
            )

    return True, ""


def _has_path(source: str, target: str, adjacency: dict[str, list[str]]) -> bool:
    """Check if there's a path from source to target using BFS."""
    visited: set[str] = set()
    queue: deque[str] = deque([source])

    while queue:
        current = queue.popleft()
        if current == target:
            return True
        if current in visited:
            continue
        visited.add(current)
        for neighbor in adjacency.get(current, []):
            if neighbor not in visited:
                queue.append(neighbor)

    return False


# === Property 3: Topic Learning Order is Valid Topological Sort ===


# Feature: gh-600-exam-prep, Property 3: Topic Learning Order is Valid Topological Sort
class TestTopicLearningOrderIsValidTopologicalSort:
    """For any set of topics with dependency edges forming a DAG, the computed
    learning_order is a valid topological sort: every topic appears exactly once,
    and no topic appears before any of its prerequisites.

    **Validates: Requirements 2.4**
    """

    @given(data=_dag_topics_and_deps())
    @settings(max_examples=100, deadline=5000)
    def test_every_topic_appears_exactly_once(
        self,
        data: tuple[list[Topic], list[Dependency]],
    ) -> None:
        """Every topic in the input appears exactly once in the learning order."""
        topics, deps = data

        mapper = TopicMapper()
        order = mapper._compute_learning_order(topics, deps)

        topic_ids = {t.id for t in topics}

        # Every topic appears in the order
        assert set(order) == topic_ids, (
            f"Learning order topics {set(order)} != input topics {topic_ids}"
        )

        # No duplicates
        assert len(order) == len(set(order)), (
            f"Learning order contains duplicates: {order}"
        )

    @given(data=_dag_topics_and_deps())
    @settings(max_examples=100, deadline=5000)
    def test_prerequisites_appear_before_dependents(
        self,
        data: tuple[list[Topic], list[Dependency]],
    ) -> None:
        """For every dependency (A -> B), A appears before B in the learning order."""
        topics, deps = data

        mapper = TopicMapper()
        order = mapper._compute_learning_order(topics, deps)

        is_valid, reason = _is_valid_topological_sort(order, deps)
        assert is_valid, reason

    @given(data=_dag_chain())
    @settings(max_examples=100, deadline=5000)
    def test_chain_ordering_preserved(
        self,
        data: tuple[list[Topic], list[Dependency]],
    ) -> None:
        """For a linear chain A -> B -> C, the order must be [A, B, C]."""
        topics, deps = data

        mapper = TopicMapper()
        order = mapper._compute_learning_order(topics, deps)

        # All topics present
        assert len(order) == len(topics)

        # Check chain ordering is valid topological sort
        is_valid, reason = _is_valid_topological_sort(order, deps)
        assert is_valid, reason

    @given(data=_dag_wide())
    @settings(max_examples=100, deadline=5000)
    def test_wide_dag_root_comes_first(
        self,
        data: tuple[list[Topic], list[Dependency]],
    ) -> None:
        """For a wide DAG with one root, the root always appears before all children."""
        topics, deps = data

        mapper = TopicMapper()
        order = mapper._compute_learning_order(topics, deps)

        root_id = _topic_id(0)
        root_pos = order.index(root_id)

        # Root must be at position 0 or earlier than all its dependents
        for dep in deps:
            if dep.source_topic_id == root_id:
                child_pos = order.index(dep.target_topic_id)
                assert root_pos < child_pos, (
                    f"Root {root_id} at pos {root_pos} should be before "
                    f"child {dep.target_topic_id} at pos {child_pos}"
                )

    @given(
        num_topics=st.integers(min_value=1, max_value=15),
    )
    @settings(max_examples=100, deadline=5000)
    def test_no_deps_all_topics_present(
        self,
        num_topics: int,
    ) -> None:
        """With no dependencies, all topics still appear exactly once in the output."""
        topics = [
            Topic(
                id=_topic_id(i),
                name=f"Independent Topic {i}",
                domain_id="domain-1",
                sub_domain=None,
                knowledge_point_ids=[f"kp-{i}"],
                description=f"Topic {i} with no deps",
            )
            for i in range(num_topics)
        ]

        mapper = TopicMapper()
        order = mapper._compute_learning_order(topics, [])

        assert set(order) == {t.id for t in topics}
        assert len(order) == num_topics


# === Property 4: Cycle Detection Groups Mutually Dependent Topics ===


# Feature: gh-600-exam-prep, Property 4: Cycle Detection Groups Mutually Dependent Topics
class TestCycleDetectionGroupsMutuallyDependentTopics:
    """For any dependency graph containing cycles, all mutually dependent topics
    within a cycle are grouped into the same learning unit, and topics not in a
    cycle are not included in any learning unit.

    **Validates: Requirements 2.6**
    """

    @given(data=_graph_with_cycles())
    @settings(max_examples=100, deadline=5000)
    def test_cycle_members_grouped_together(
        self,
        data: tuple[list[Dependency], list[set[str]]],
    ) -> None:
        """All topics within a cycle are grouped into the same learning unit."""
        deps, expected_sccs = data

        mapper = TopicMapper()
        learning_units = mapper._detect_cycles(deps)

        # Convert learning_units to sets for comparison
        actual_units = [set(unit) for unit in learning_units]

        # Every expected SCC should be fully contained in exactly one learning unit
        for expected_scc in expected_sccs:
            found_in_unit = False
            for actual_unit in actual_units:
                if expected_scc <= actual_unit:
                    found_in_unit = True
                    break
            assert found_in_unit, (
                f"Expected cycle group {expected_scc} not fully contained "
                f"in any learning unit. Actual units: {actual_units}"
            )

    @given(data=_graph_with_cycles())
    @settings(max_examples=100, deadline=5000)
    def test_non_cycle_topics_not_in_units(
        self,
        data: tuple[list[Dependency], list[set[str]]],
    ) -> None:
        """Topics not part of any cycle are not included in any learning unit."""
        deps, expected_sccs = data

        mapper = TopicMapper()
        learning_units = mapper._detect_cycles(deps)

        # All nodes in the graph
        all_nodes: set[str] = set()
        for dep in deps:
            all_nodes.add(dep.source_topic_id)
            all_nodes.add(dep.target_topic_id)

        # Nodes that are in cycles (expected)
        cycle_nodes: set[str] = set()
        for scc in expected_sccs:
            cycle_nodes.update(scc)

        # Non-cycle nodes
        non_cycle_nodes = all_nodes - cycle_nodes

        # Check that non-cycle nodes don't appear in any learning unit
        unit_nodes: set[str] = set()
        for unit in learning_units:
            unit_nodes.update(unit)

        violating_nodes = non_cycle_nodes & unit_nodes
        assert not violating_nodes, (
            f"Non-cycle nodes {violating_nodes} found in learning units. "
            f"Expected cycle nodes: {cycle_nodes}, actual unit nodes: {unit_nodes}"
        )

    @given(data=_graph_with_cycles())
    @settings(max_examples=100, deadline=5000)
    def test_each_learning_unit_is_actual_cycle(
        self,
        data: tuple[list[Dependency], list[set[str]]],
    ) -> None:
        """Every learning unit returned represents an actual cycle:
        every node in the unit can reach every other node in the unit."""
        deps, _ = data

        mapper = TopicMapper()
        learning_units = mapper._detect_cycles(deps)

        # Build adjacency for reachability checks
        adjacency: dict[str, list[str]] = defaultdict(list)
        for dep in deps:
            adjacency[dep.source_topic_id].append(dep.target_topic_id)

        for unit in learning_units:
            unit_nodes = list(unit)
            # Every pair in the unit should be mutually reachable
            for i in range(len(unit_nodes)):
                for j in range(len(unit_nodes)):
                    if i == j:
                        continue
                    assert _has_path(unit_nodes[i], unit_nodes[j], adjacency), (
                        f"In learning unit {unit_nodes}, node '{unit_nodes[i]}' "
                        f"cannot reach '{unit_nodes[j]}' — not a valid SCC"
                    )

    def test_no_cycles_returns_empty(self) -> None:
        """A pure DAG produces no learning units."""
        deps = [
            Dependency(
                source_topic_id="topic-001",
                target_topic_id="topic-002",
                relationship="requires",
            ),
            Dependency(
                source_topic_id="topic-002",
                target_topic_id="topic-003",
                relationship="requires",
            ),
        ]

        mapper = TopicMapper()
        learning_units = mapper._detect_cycles(deps)

        assert learning_units == [], (
            f"Expected no learning units for DAG, got: {learning_units}"
        )

    @given(
        cycle_size=st.integers(min_value=2, max_value=8),
    )
    @settings(max_examples=100, deadline=5000)
    def test_simple_cycle_detected(
        self,
        cycle_size: int,
    ) -> None:
        """A simple cycle of N nodes is detected as a single learning unit of size N."""
        # Create a cycle: 0 -> 1 -> 2 -> ... -> (n-1) -> 0
        deps = [
            Dependency(
                source_topic_id=_topic_id(i),
                target_topic_id=_topic_id((i + 1) % cycle_size),
                relationship="requires understanding of",
            )
            for i in range(cycle_size)
        ]

        mapper = TopicMapper()
        learning_units = mapper._detect_cycles(deps)

        expected_cycle_nodes = {_topic_id(i) for i in range(cycle_size)}
        actual_unit_nodes: set[str] = set()
        for unit in learning_units:
            actual_unit_nodes.update(unit)

        # All cycle nodes should be in learning units
        assert expected_cycle_nodes <= actual_unit_nodes, (
            f"Expected cycle nodes {expected_cycle_nodes} not found in "
            f"learning units {learning_units}"
        )

        # Should be exactly one learning unit containing all cycle nodes
        assert len(learning_units) == 1, (
            f"Expected 1 learning unit for simple cycle, got {len(learning_units)}: "
            f"{learning_units}"
        )

        assert set(learning_units[0]) == expected_cycle_nodes, (
            f"Learning unit {set(learning_units[0])} != expected {expected_cycle_nodes}"
        )

    @given(
        cycle_a_size=st.integers(min_value=2, max_value=5),
        cycle_b_size=st.integers(min_value=2, max_value=5),
    )
    @settings(max_examples=100, deadline=5000)
    def test_multiple_disjoint_cycles_detected_separately(
        self,
        cycle_a_size: int,
        cycle_b_size: int,
    ) -> None:
        """Two disjoint cycles produce two separate learning units."""
        # Cycle A: nodes 0..cycle_a_size-1
        deps_a = [
            Dependency(
                source_topic_id=_topic_id(i),
                target_topic_id=_topic_id((i + 1) % cycle_a_size),
                relationship="requires",
            )
            for i in range(cycle_a_size)
        ]

        # Cycle B: nodes offset by 100 to avoid overlap
        offset = 100
        deps_b = [
            Dependency(
                source_topic_id=_topic_id(offset + i),
                target_topic_id=_topic_id(offset + (i + 1) % cycle_b_size),
                relationship="requires",
            )
            for i in range(cycle_b_size)
        ]

        all_deps = deps_a + deps_b

        mapper = TopicMapper()
        learning_units = mapper._detect_cycles(all_deps)

        expected_a = {_topic_id(i) for i in range(cycle_a_size)}
        expected_b = {_topic_id(offset + i) for i in range(cycle_b_size)}

        actual_units = [set(unit) for unit in learning_units]

        assert len(actual_units) == 2, (
            f"Expected 2 learning units, got {len(actual_units)}: {actual_units}"
        )

        # Each expected cycle should match one actual unit
        assert expected_a in actual_units, (
            f"Cycle A {expected_a} not found in units {actual_units}"
        )
        assert expected_b in actual_units, (
            f"Cycle B {expected_b} not found in units {actual_units}"
        )
