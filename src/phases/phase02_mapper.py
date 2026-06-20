"""Phase 2: Topic Mapping and Hierarchy.

Organizes extracted knowledge points into a hierarchical structure aligned
with the 6 GH-600 exam domains, identifies prerequisite relationships,
computes a learning order via topological sort, detects cycles, and
identifies cross-references between related topics.
"""

from __future__ import annotations

import re
from collections import defaultdict, deque
from itertools import combinations
from pathlib import Path

from src.config import (
    ARTIFACTS_DIR,
    ARTIFACT_FILENAMES,
    EXAM_DOMAINS,
    ExamDomain,
)
from src.models.knowledge import ExtractionResult, KnowledgePoint
from src.models.topic_map import (
    CrossReference,
    Dependency,
    Topic,
    TopicHierarchy,
)


# Common tools, APIs, patterns, and workflows to detect cross-references.
_CROSS_REF_KEYWORDS: list[str] = [
    "github copilot",
    "copilot agent mode",
    "copilot chat",
    "github actions",
    "github codespaces",
    "vs code",
    "visual studio code",
    "api",
    "rest api",
    "graphql",
    "webhook",
    "ci/cd",
    "pull request",
    "code review",
    "testing",
    "debugging",
    "deployment",
    "security",
    "access control",
    "permissions",
    "responsible ai",
    "prompt engineering",
    "llm",
    "large language model",
    "model context protocol",
    "mcp",
    "agent orchestration",
    "multi-agent",
    "sdlc",
    "devops",
]


class TopicMapper:
    """Phase 2: Maps extracted knowledge into a hierarchical topic structure.

    Organizes KnowledgePoints into Topics aligned with the 6 GH-600 exam
    domains, identifies prerequisite dependencies, computes learning order,
    detects cycles, and identifies cross-references.
    """

    def __init__(self, exam_domains: list[ExamDomain] | None = None) -> None:
        self._exam_domains = exam_domains or EXAM_DOMAINS
        self._topic_id_counter: int = 0

    def _generate_topic_id(self) -> str:
        """Generate a unique topic ID."""
        self._topic_id_counter += 1
        return f"topic-{self._topic_id_counter:03d}"

    def map_topics(self, knowledge: ExtractionResult) -> TopicHierarchy:
        """Organize knowledge points into a hierarchical topic structure.

        Assigns knowledge points to domains, identifies prerequisites,
        computes learning order, detects cycles, and finds cross-references.

        Args:
            knowledge: The ExtractionResult from Phase 1.

        Returns:
            A TopicHierarchy containing the complete topic map.
        """
        # Store knowledge point data for internal lookups
        self._kp_data: dict[str, dict] = {
            kp.id: {
                "content": kp.content,
                "category": kp.category,
                "is_prerequisite": kp.is_prerequisite,
                "source_url": kp.source_url,
            }
            for kp in knowledge.all_knowledge_points
        }

        # Step 1: Assign knowledge points to domains, creating topics
        domains = self._assign_to_domains(knowledge.all_knowledge_points)

        # Flatten all topics for further processing
        all_topics: list[Topic] = []
        for topic_list in domains.values():
            all_topics.extend(topic_list)

        # Step 2: Identify prerequisite relationships
        dependencies = self._identify_prerequisites(all_topics)

        # Step 3: Detect cycles in dependencies
        learning_units = self._detect_cycles(dependencies)

        # Step 4: Compute learning order (topological sort)
        learning_order = self._compute_learning_order(all_topics, dependencies)

        # Step 5: Identify cross-references
        cross_references = self._identify_cross_references(all_topics)

        hierarchy = TopicHierarchy(
            domains=domains,
            dependencies=dependencies,
            cross_references=cross_references,
            learning_order=learning_order,
            learning_units=learning_units,
        )

        # Write artifact to disk
        self._write_artifact(hierarchy)

        return hierarchy

    def _assign_to_domains(
        self, points: list[KnowledgePoint]
    ) -> dict[str, list[Topic]]:
        """Categorize knowledge points under domains and sub-domains.

        Groups knowledge points by matching their content against domain
        names and sub-topic keywords. Points that match a domain are
        further grouped into topics by sub-domain affinity.

        Args:
            points: All extracted knowledge points from Phase 1.

        Returns:
            Dictionary mapping domain IDs to lists of Topics.
        """
        # Map each point to its best-matching domain(s)
        domain_points: dict[str, list[KnowledgePoint]] = defaultdict(list)

        for point in points:
            content_lower = point.content.lower()

            # Score each domain and pick the best match
            best_domain_id: str | None = None
            best_score = 0

            for domain in self._exam_domains:
                score = self._score_domain_match(content_lower, domain)
                if score > best_score:
                    best_score = score
                    best_domain_id = domain.id

            if best_domain_id and best_score > 0:
                domain_points[best_domain_id].append(point)
            else:
                # Default assignment based on category heuristics
                default_domain = self._infer_domain_from_category(point)
                domain_points[default_domain].append(point)

        # Group points within each domain into topics by sub-domain
        domains: dict[str, list[Topic]] = {}

        for domain in self._exam_domains:
            domain_id = domain.id
            points_for_domain = domain_points.get(domain_id, [])

            if not points_for_domain:
                domains[domain_id] = []
                continue

            topics = self._group_into_topics(points_for_domain, domain)
            domains[domain_id] = topics

        return domains

    def _matches_domain(self, content_lower: str, domain: ExamDomain) -> bool:
        """Check if content matches a domain by name or sub-topic keywords.

        Args:
            content_lower: Lowercased content text.
            domain: The ExamDomain to check against.

        Returns:
            True if the content matches this domain.
        """
        return self._score_domain_match(content_lower, domain) > 0

    def _score_domain_match(self, content_lower: str, domain: ExamDomain) -> int:
        """Score how well content matches a domain.

        Higher scores indicate stronger domain affinity. Sub-topic matches
        are weighted more heavily than domain name matches to ensure
        specific topics get assigned to their correct domain.

        Args:
            content_lower: Lowercased content text.
            domain: The ExamDomain to check against.

        Returns:
            Integer score (0 = no match).
        """
        score = 0

        # Check domain name keywords (lower weight)
        domain_keywords = self._extract_keywords(domain.name.lower())
        name_matches = sum(1 for kw in domain_keywords if kw in content_lower and len(kw) > 3)
        score += name_matches

        # Check sub-topic keywords (higher weight: 3x per match)
        for sub_topic in domain.sub_topics:
            sub_keywords = self._extract_keywords(sub_topic.lower())
            sub_matches = sum(
                1 for kw in sub_keywords if kw in content_lower and len(kw) > 3
            )
            score += sub_matches * 3

        return score

    def _extract_keywords(self, text: str) -> list[str]:
        """Extract meaningful keywords from text, filtering stop words.

        Args:
            text: Text to extract keywords from.

        Returns:
            List of keywords (lowercased).
        """
        stop_words = {
            "a", "an", "the", "and", "or", "for", "to", "in", "of", "is",
            "are", "was", "were", "with", "from", "by", "as", "on", "at",
            "that", "which", "this", "be", "it", "its", "can", "will",
            "do", "does", "has", "have", "had", "been", "would", "should",
        }
        words = re.findall(r"[a-z]+(?:[/-][a-z]+)*", text)
        return [w for w in words if w not in stop_words]

    def _infer_domain_from_category(self, point: KnowledgePoint) -> str:
        """Infer a default domain based on knowledge point category.

        Args:
            point: The knowledge point to classify.

        Returns:
            A domain ID string.
        """
        content_lower = point.content.lower()

        # Heuristic-based fallback assignment
        if any(kw in content_lower for kw in ["security", "access", "permission", "govern"]):
            return "domain-4"
        if any(kw in content_lower for kw in ["responsible", "ethical", "bias", "fairness"]):
            return "domain-6"
        if any(kw in content_lower for kw in ["performance", "optimize", "metric", "evaluate"]):
            return "domain-3"
        if any(kw in content_lower for kw in ["collaborate", "workflow", "ci/cd", "pipeline"]):
            return "domain-5"
        if any(kw in content_lower for kw in ["design", "implement", "build", "create"]):
            return "domain-2"

        # Default to domain-1 (architecture/SDLC)
        return "domain-1"

    def _group_into_topics(
        self, points: list[KnowledgePoint], domain: ExamDomain
    ) -> list[Topic]:
        """Group knowledge points within a domain into topics.

        Points are grouped by sub-domain affinity. Points matching the
        same sub-topic are grouped together into a single topic.

        Args:
            points: Knowledge points assigned to this domain.
            domain: The exam domain these points belong to.

        Returns:
            List of Topic objects.
        """
        # Group points by their best-matching sub-topic
        sub_topic_groups: dict[str, list[KnowledgePoint]] = defaultdict(list)
        unmatched: list[KnowledgePoint] = []

        for point in points:
            content_lower = point.content.lower()
            best_sub = None
            best_score = 0

            for sub_topic in domain.sub_topics:
                sub_keywords = self._extract_keywords(sub_topic.lower())
                score = sum(
                    1 for kw in sub_keywords
                    if kw in content_lower and len(kw) > 3
                )
                if score > best_score:
                    best_score = score
                    best_sub = sub_topic

            if best_sub and best_score >= 1:
                sub_topic_groups[best_sub].append(point)
            else:
                unmatched.append(point)

        topics: list[Topic] = []

        # Create topics for each sub-topic group
        for sub_topic_name, group_points in sub_topic_groups.items():
            topic = Topic(
                id=self._generate_topic_id(),
                name=self._derive_topic_name(group_points, sub_topic_name),
                domain_id=domain.id,
                sub_domain=sub_topic_name,
                knowledge_point_ids=[p.id for p in group_points],
                description=self._derive_description(group_points),
            )
            topics.append(topic)

        # Create a general topic for unmatched points if any
        if unmatched:
            topic = Topic(
                id=self._generate_topic_id(),
                name=self._derive_topic_name(unmatched, domain.name),
                domain_id=domain.id,
                sub_domain=None,
                knowledge_point_ids=[p.id for p in unmatched],
                description=self._derive_description(unmatched),
            )
            topics.append(topic)

        return topics

    def _derive_topic_name(
        self, points: list[KnowledgePoint], fallback: str
    ) -> str:
        """Derive a topic name from knowledge point content.

        Uses the first significant phrase from the first knowledge point,
        or falls back to the sub-topic/domain name.

        Args:
            points: The knowledge points in this topic.
            fallback: Fallback name if no good name can be derived.

        Returns:
            A short, descriptive topic name.
        """
        if not points:
            return fallback

        # Use first point's content to derive a name
        content = points[0].content
        # Take first sentence or first 60 characters
        first_sentence = content.split(".")[0].strip()
        if len(first_sentence) > 60:
            # Truncate at word boundary
            truncated = first_sentence[:57]
            last_space = truncated.rfind(" ")
            if last_space > 20:
                return truncated[:last_space] + "..."
            return truncated + "..."
        if len(first_sentence) < 10:
            return fallback
        return first_sentence

    def _derive_description(self, points: list[KnowledgePoint]) -> str:
        """Derive a description from knowledge points.

        Combines the first sentence of each point (up to 3 points)
        into a summary description.

        Args:
            points: The knowledge points to summarize.

        Returns:
            A brief description string.
        """
        sentences: list[str] = []
        for point in points[:3]:
            first_sentence = point.content.split(".")[0].strip()
            if first_sentence and len(first_sentence) > 10:
                sentences.append(first_sentence + ".")

        if sentences:
            return " ".join(sentences)
        return "Topic covering related knowledge points."

    def _identify_prerequisites(self, topics: list[Topic]) -> list[Dependency]:
        """Detect prerequisite relationships between topics.

        Identifies prerequisites based on:
        1. Topics containing knowledge points marked as is_prerequisite
        2. Content overlap suggesting one topic builds on another

        Args:
            topics: All topics across all domains.

        Returns:
            List of Dependency objects representing prerequisites.
        """
        dependencies: list[Dependency] = []
        seen_pairs: set[tuple[str, str]] = set()

        # Load knowledge points for reference
        kp_lookup = self._build_kp_lookup(topics)

        # Identify prerequisite knowledge points
        prereq_topics: list[Topic] = []
        non_prereq_topics: list[Topic] = []

        for topic in topics:
            has_prereq_points = any(
                kp_lookup.get(kp_id, {}).get("is_prerequisite", False)
                for kp_id in topic.knowledge_point_ids
            )
            if has_prereq_points:
                prereq_topics.append(topic)
            else:
                non_prereq_topics.append(topic)

        # Prerequisite topics are dependencies for related non-prereq topics
        for prereq_topic in prereq_topics:
            prereq_content = self._get_topic_content(prereq_topic, kp_lookup).lower()
            prereq_keywords = set(self._extract_keywords(prereq_content))

            for target_topic in non_prereq_topics:
                if target_topic.id == prereq_topic.id:
                    continue

                target_content = self._get_topic_content(target_topic, kp_lookup).lower()
                target_keywords = set(self._extract_keywords(target_content))

                # Check for significant keyword overlap
                overlap = prereq_keywords & target_keywords
                significant_overlap = {kw for kw in overlap if len(kw) > 4}

                if len(significant_overlap) >= 3:
                    pair = (prereq_topic.id, target_topic.id)
                    if pair not in seen_pairs:
                        seen_pairs.add(pair)
                        dependencies.append(
                            Dependency(
                                source_topic_id=prereq_topic.id,
                                target_topic_id=target_topic.id,
                                relationship="requires understanding of",
                            )
                        )

        # Also identify sequential dependencies based on domain ordering
        # (topics in earlier domains may be prerequisites for later ones)
        domain_order = [d.id for d in self._exam_domains]

        for i, domain_id_a in enumerate(domain_order):
            for domain_id_b in domain_order[i + 1:]:
                topics_a = [t for t in topics if t.domain_id == domain_id_a]
                topics_b = [t for t in topics if t.domain_id == domain_id_b]

                for topic_a in topics_a:
                    content_a = self._get_topic_content(topic_a, kp_lookup).lower()
                    keywords_a = set(self._extract_keywords(content_a))

                    for topic_b in topics_b:
                        content_b = self._get_topic_content(topic_b, kp_lookup).lower()
                        keywords_b = set(self._extract_keywords(content_b))

                        overlap = keywords_a & keywords_b
                        significant = {kw for kw in overlap if len(kw) > 5}

                        if len(significant) >= 4:
                            pair = (topic_a.id, topic_b.id)
                            if pair not in seen_pairs:
                                seen_pairs.add(pair)
                                dependencies.append(
                                    Dependency(
                                        source_topic_id=topic_a.id,
                                        target_topic_id=topic_b.id,
                                        relationship="builds upon concepts from",
                                    )
                                )

        return dependencies

    def _build_kp_lookup(
        self, topics: list[Topic]
    ) -> dict[str, dict]:
        """Build a lookup of knowledge point data by ID.

        Since we don't have direct access to KnowledgePoint objects here,
        we build a minimal lookup from what we loaded from Phase 1 artifact.

        Returns:
            Dictionary mapping KP IDs to their metadata.
        """
        # This will be populated from the extraction result during map_topics
        return getattr(self, "_kp_data", {})

    def _get_topic_content(
        self, topic: Topic, kp_lookup: dict[str, dict]
    ) -> str:
        """Get combined content text for a topic's knowledge points.

        Args:
            topic: The topic to get content for.
            kp_lookup: Knowledge point data lookup.

        Returns:
            Combined content string.
        """
        contents: list[str] = []
        for kp_id in topic.knowledge_point_ids:
            kp_data = kp_lookup.get(kp_id, {})
            content = kp_data.get("content", "")
            if content:
                contents.append(content)

        # Also include the topic name and description
        contents.append(topic.name)
        contents.append(topic.description)

        return " ".join(contents)

    def _compute_learning_order(
        self, topics: list[Topic], deps: list[Dependency]
    ) -> list[str]:
        """Compute a learning order using Kahn's algorithm (topological sort).

        Produces an ordering where no topic appears before any of its
        prerequisites. Topics in cycles are placed together as encountered.

        Args:
            topics: All topics to order.
            deps: Prerequisite dependencies between topics.

        Returns:
            List of topic IDs in recommended learning order.
        """
        # Build adjacency list and in-degree counts
        topic_ids = {t.id for t in topics}
        adjacency: dict[str, list[str]] = defaultdict(list)
        in_degree: dict[str, int] = {t_id: 0 for t_id in topic_ids}

        for dep in deps:
            # source_topic_id is the prerequisite; target depends on source
            # So source must come before target in learning order
            if dep.source_topic_id in topic_ids and dep.target_topic_id in topic_ids:
                adjacency[dep.source_topic_id].append(dep.target_topic_id)
                in_degree[dep.target_topic_id] = in_degree.get(dep.target_topic_id, 0) + 1

        # Kahn's algorithm
        queue: deque[str] = deque()
        for t_id in topic_ids:
            if in_degree.get(t_id, 0) == 0:
                queue.append(t_id)

        # Sort initial queue for deterministic ordering
        queue = deque(sorted(queue))

        learning_order: list[str] = []

        while queue:
            current = queue.popleft()
            learning_order.append(current)

            for neighbor in sorted(adjacency.get(current, [])):
                in_degree[neighbor] -= 1
                if in_degree[neighbor] == 0:
                    queue.append(neighbor)

        # Any topics not in learning_order are part of cycles
        # Add them at the end (they'll be handled by learning_units)
        remaining = [t_id for t_id in sorted(topic_ids) if t_id not in learning_order]
        learning_order.extend(remaining)

        return learning_order

    def _detect_cycles(self, deps: list[Dependency]) -> list[list[str]]:
        """Find circular dependencies and group into learning units.

        Uses DFS-based cycle detection to find strongly connected components
        with more than one node (i.e., actual cycles).

        Args:
            deps: All prerequisite dependencies.

        Returns:
            List of learning units (each a list of topic IDs that form a cycle).
        """
        # Build graph
        all_nodes: set[str] = set()
        adjacency: dict[str, list[str]] = defaultdict(list)

        for dep in deps:
            all_nodes.add(dep.source_topic_id)
            all_nodes.add(dep.target_topic_id)
            adjacency[dep.source_topic_id].append(dep.target_topic_id)

        # Tarjan's algorithm for strongly connected components
        index_counter = [0]
        stack: list[str] = []
        lowlink: dict[str, int] = {}
        index: dict[str, int] = {}
        on_stack: set[str] = set()
        sccs: list[list[str]] = []

        def strongconnect(node: str) -> None:
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

            # If node is a root of an SCC
            if lowlink[node] == index[node]:
                scc: list[str] = []
                while True:
                    w = stack.pop()
                    on_stack.discard(w)
                    scc.append(w)
                    if w == node:
                        break
                if len(scc) > 1:
                    # Only report actual cycles (SCCs with more than 1 node)
                    sccs.append(sorted(scc))

        for node in sorted(all_nodes):
            if node not in index:
                strongconnect(node)

        return sccs

    def _identify_cross_references(
        self, topics: list[Topic]
    ) -> list[CrossReference]:
        """Identify topics sharing tools, APIs, patterns, or workflows.

        Scans topic content for shared keywords from a predefined list
        of tools, APIs, patterns, and workflows relevant to GH-600.

        Args:
            topics: All topics to check for cross-references.

        Returns:
            List of CrossReference objects.
        """
        # Build a map of keyword -> topics that contain it
        keyword_topics: dict[str, list[str]] = defaultdict(list)
        kp_lookup = self._build_kp_lookup(topics)

        for topic in topics:
            content = self._get_topic_content(topic, kp_lookup).lower()

            for keyword in _CROSS_REF_KEYWORDS:
                if keyword in content:
                    keyword_topics[keyword].append(topic.id)

        # Generate cross-references for topics sharing the same keyword
        cross_references: list[CrossReference] = []
        seen_pairs: set[tuple[str, str]] = set()

        for keyword, topic_ids in keyword_topics.items():
            if len(topic_ids) < 2:
                continue

            # Only create cross-references between topics in different domains
            # to prioritize cross-domain connections
            topic_domain_map = {t.id: t.domain_id for t in topics}

            for id_a, id_b in combinations(topic_ids, 2):
                # Prefer cross-domain references
                if topic_domain_map.get(id_a) == topic_domain_map.get(id_b):
                    continue

                pair = tuple(sorted([id_a, id_b]))
                if pair in seen_pairs:
                    continue
                seen_pairs.add(pair)

                cross_references.append(
                    CrossReference(
                        topic_id_a=pair[0],
                        topic_id_b=pair[1],
                        shared_concept=keyword,
                    )
                )

        return cross_references

    def _write_artifact(self, hierarchy: TopicHierarchy) -> None:
        """Write the TopicHierarchy to the artifacts directory.

        Creates the artifacts directory if it doesn't exist.
        Writes the result as JSON to phase02_topic_map.json.
        """
        artifacts_path = Path(ARTIFACTS_DIR)
        artifacts_path.mkdir(parents=True, exist_ok=True)

        output_path = artifacts_path / ARTIFACT_FILENAMES["phase02"]
        output_path.write_text(
            hierarchy.model_dump_json(indent=2),
            encoding="utf-8",
        )

    @classmethod
    def from_artifact(cls, artifact_path: str | None = None) -> TopicHierarchy:
        """Load and process from the Phase 1 artifact file.

        Reads the extraction result from disk and runs the topic mapping.

        Args:
            artifact_path: Optional path to phase01_extraction.json.
                Defaults to artifacts/phase01_extraction.json.

        Returns:
            The generated TopicHierarchy.
        """
        if artifact_path is None:
            artifact_path = str(
                Path(ARTIFACTS_DIR) / ARTIFACT_FILENAMES["phase01"]
            )

        path = Path(artifact_path)
        raw_json = path.read_text(encoding="utf-8")
        extraction_result = ExtractionResult.model_validate_json(raw_json)

        mapper = cls()
        return mapper.map_topics(extraction_result)
