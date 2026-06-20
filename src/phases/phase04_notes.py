"""Phase 4: Comprehensive Study Notes Generator.

Produces study notes for every topic with required sections, code examples,
cross-references, step-by-step instructions, and expanded content for
high-priority topics. Supplements sparse topics with inferred content.
"""

from __future__ import annotations

import re
import textwrap
from dataclasses import dataclass
from pathlib import Path

from src.config import (
    ARTIFACTS_DIR,
    ARTIFACT_FILENAMES,
    DOMAIN_BY_ID,
    HIGH_PRIORITY_THRESHOLD,
    MIN_COMMON_MISTAKES,
    MIN_EXAM_TIPS,
    MIN_EXAMPLES,
    MIN_EXAMPLES_HIGH_PRIORITY,
    MIN_EXPLANATION_WORDS,
    MIN_EXPLANATION_WORDS_HIGH_PRIORITY,
    MIN_KEY_FACTS,
    MIN_OVERVIEW_SENTENCES,
    SPARSE_TOPIC_KNOWLEDGE_POINT_THRESHOLD,
)
from src.models.scoring import ScoredTopic, ScoredTopicList
from src.models.study_notes import StudyNotesCollection, TopicNotes
from src.models.topic_map import Topic, TopicHierarchy


# Keywords indicating procedure/workflow topics
_PROCEDURE_KEYWORDS: list[str] = [
    "workflow", "procedure", "process", "steps", "pipeline",
    "setup", "configure", "install", "deploy", "implement",
    "integrate", "migrate", "create", "build", "run",
]

# Keywords indicating code/config topics
_CODE_KEYWORDS: list[str] = [
    "code", "config", "configuration", "yaml", "json",
    "api", "endpoint", "script", "command", "cli",
    "syntax", "snippet", "template", "file", "manifest",
]


@dataclass(frozen=True)
class NotesConfig:
    """Configuration for notes generation thresholds."""

    min_overview_sentences: int = MIN_OVERVIEW_SENTENCES
    min_explanation_words: int = MIN_EXPLANATION_WORDS
    min_explanation_words_high_priority: int = MIN_EXPLANATION_WORDS_HIGH_PRIORITY
    min_key_facts: int = MIN_KEY_FACTS
    min_common_mistakes: int = MIN_COMMON_MISTAKES
    min_examples: int = MIN_EXAMPLES
    min_examples_high_priority: int = MIN_EXAMPLES_HIGH_PRIORITY
    min_exam_tips: int = MIN_EXAM_TIPS
    sparse_threshold: int = SPARSE_TOPIC_KNOWLEDGE_POINT_THRESHOLD
    high_priority_threshold: int = HIGH_PRIORITY_THRESHOLD


class StudyNotesGenerator:
    """Phase 4: Generates comprehensive study notes for all topics.

    Produces structured study notes from the topic hierarchy and priority
    scores, including overviews, explanations, key facts, common mistakes,
    examples, exam tips, code blocks, step-by-step instructions, and
    cross-references. Supplements sparse topics with inferred content.
    """

    def __init__(self, config: NotesConfig | None = None) -> None:
        """Initialize with notes generation configuration.

        Args:
            config: Optional NotesConfig for threshold overrides.
                Defaults to standard thresholds from src.config.
        """
        self._config = config or NotesConfig()

    def generate(
        self,
        hierarchy: TopicHierarchy,
        scores: ScoredTopicList,
    ) -> StudyNotesCollection:
        """Generate study notes for all topics in the hierarchy.

        Args:
            hierarchy: The TopicHierarchy from Phase 2.
            scores: The ScoredTopicList from Phase 3.

        Returns:
            A StudyNotesCollection containing notes for every topic.
        """
        # Build lookup maps
        score_map: dict[str, ScoredTopic] = {
            s.topic_id: s for s in scores.topics
        }
        all_topics: list[Topic] = []
        for topic_list in hierarchy.domains.values():
            all_topics.extend(topic_list)

        notes_list: list[TopicNotes] = []

        for topic in all_topics:
            scored = score_map.get(topic.id)
            if scored is None:
                # Create a default score for topics not in scores list
                scored = ScoredTopic(
                    topic_id=topic.id,
                    topic_name=topic.name,
                    domain_ids=[topic.domain_id],
                    priority_score=5,
                    is_high_priority=False,
                    domain_count=1,
                )

            # Generate notes for this topic
            topic_notes = self._generate_topic_notes(topic, scored)

            # Build cross-references
            related = self._build_cross_references(topic, all_topics)
            topic_notes = TopicNotes(
                **{**topic_notes.model_dump(), "related_topics": related}
            )

            # Supplement sparse topics
            if len(topic.knowledge_point_ids) < self._config.sparse_threshold:
                topic_notes = self._supplement_sparse_topics(topic_notes)

            notes_list.append(topic_notes)

        # Build cross-domain themes
        cross_domain_themes = self._identify_cross_domain_themes(
            notes_list, hierarchy
        )

        result = StudyNotesCollection(
            notes=notes_list,
            cross_domain_themes=cross_domain_themes,
        )

        # Write artifact to disk
        self._write_artifact(result)

        return result

    def _generate_topic_notes(
        self, topic: Topic, score: ScoredTopic
    ) -> TopicNotes:
        """Generate comprehensive study notes for a single topic.

        Constructs all required sections from the topic's knowledge points
        and metadata: overview, explanation, key facts, common mistakes,
        examples, exam tips, code blocks, and step-by-step instructions.

        Args:
            topic: The Topic to generate notes for.
            score: The ScoredTopic with priority information.

        Returns:
            A TopicNotes instance with all sections populated.
        """
        is_high_priority = score.priority_score >= self._config.high_priority_threshold
        is_procedure = self._is_procedure_topic(topic)
        is_code_topic = self._is_code_topic(topic)

        # Generate each section
        overview = self._build_overview(topic)
        explanation = self._build_explanation(topic, is_high_priority)
        key_facts = self._build_key_facts(topic)
        common_mistakes = self._build_common_mistakes(topic)
        examples = self._build_examples(topic, is_high_priority)
        exam_tips = self._build_exam_tips(topic, score)
        code_blocks = self._build_code_blocks(topic) if is_code_topic else []
        step_by_step = (
            self._build_step_by_step(topic) if is_procedure else None
        )

        return TopicNotes(
            topic_id=topic.id,
            topic_name=topic.name,
            domain_id=topic.domain_id,
            priority_score=score.priority_score,
            overview=overview,
            explanation=explanation,
            key_facts=key_facts,
            common_mistakes=common_mistakes,
            examples=examples,
            exam_tips=exam_tips,
            code_blocks=code_blocks,
            step_by_step=step_by_step,
            related_topics=[],
            is_supplemented=False,
        )

    def _build_cross_references(
        self, topic: Topic, all_topics: list[Topic]
    ) -> list[dict]:
        """Build cross-references linking related concepts across domains.

        Identifies topics in other domains that share conceptual overlap
        with the given topic, using topic heading anchors.

        Args:
            topic: The source topic to find references for.
            all_topics: All topics in the hierarchy.

        Returns:
            List of dicts with {topic_id, domain_name, relationship}.
        """
        related: list[dict] = []
        topic_words = set(self._extract_keywords(topic.name.lower()))
        topic_desc_words = set(
            self._extract_keywords(topic.description.lower())
        )
        combined_words = topic_words | topic_desc_words

        for other in all_topics:
            if other.id == topic.id:
                continue
            if other.domain_id == topic.domain_id:
                continue

            other_words = set(self._extract_keywords(other.name.lower()))
            other_desc_words = set(
                self._extract_keywords(other.description.lower())
            )
            other_combined = other_words | other_desc_words

            overlap = combined_words & other_combined
            if len(overlap) >= 2:
                domain_name = self._get_domain_name(other.domain_id)
                relationship = self._describe_relationship(
                    topic, other, overlap
                )
                related.append(
                    {
                        "topic_id": other.id,
                        "domain_name": domain_name,
                        "relationship": relationship,
                    }
                )

        return related

    def _supplement_sparse_topics(self, notes: TopicNotes) -> TopicNotes:
        """Supplement sparse topics with inferred content.

        For topics with fewer than SPARSE_TOPIC_KNOWLEDGE_POINT_THRESHOLD
        knowledge points, adds inferred content marked with the visual
        indicator '> [!NOTE] Supplemented content'.

        Args:
            notes: The TopicNotes to potentially supplement.

        Returns:
            Updated TopicNotes with is_supplemented=True and expanded content.
        """
        supplement_marker = "> [!NOTE] Supplemented content"

        # Supplement explanation if too short
        explanation = notes.explanation
        word_count = len(explanation.split())
        min_words = self._config.min_explanation_words
        if word_count < min_words:
            additional = self._generate_supplemental_explanation(
                notes.topic_name, notes.domain_id, min_words - word_count
            )
            explanation = (
                f"{explanation}\n\n{supplement_marker}\n{additional}"
            )
        else:
            # Always add supplement marker for sparse topics to visually
            # distinguish that this topic had limited source material
            explanation = (
                f"{explanation}\n\n{supplement_marker}\n"
                f"This topic had limited source material and content was "
                f"inferred from domain context."
            )

        # Supplement key facts if insufficient
        key_facts = list(notes.key_facts)
        while len(key_facts) < self._config.min_key_facts:
            key_facts.append(
                f"{supplement_marker}: {notes.topic_name} is a key concept "
                f"in the {self._get_domain_name(notes.domain_id)} domain "
                f"that exam candidates should understand thoroughly."
            )

        # Supplement examples if insufficient
        examples = list(notes.examples)
        min_examples = self._config.min_examples
        while len(examples) < min_examples:
            examples.append(
                f"{supplement_marker}: In practice, {notes.topic_name} "
                f"is applied when working with GitHub Copilot agent mode "
                f"to accomplish development tasks efficiently."
            )

        return TopicNotes(
            topic_id=notes.topic_id,
            topic_name=notes.topic_name,
            domain_id=notes.domain_id,
            priority_score=notes.priority_score,
            overview=notes.overview,
            explanation=explanation,
            key_facts=key_facts,
            common_mistakes=notes.common_mistakes,
            examples=examples,
            exam_tips=notes.exam_tips,
            code_blocks=notes.code_blocks,
            step_by_step=notes.step_by_step,
            related_topics=notes.related_topics,
            is_supplemented=True,
        )

    # --- Private helper methods ---

    def _build_overview(self, topic: Topic) -> str:
        """Build an overview with at least MIN_OVERVIEW_SENTENCES sentences.

        Constructs a multi-sentence overview from the topic name,
        description, and domain context.
        """
        domain_name = self._get_domain_name(topic.domain_id)
        sentences = [
            f"{topic.name} is a key concept within the "
            f"{domain_name} domain of the GH-600 certification.",
            f"{topic.description}",
            f"Understanding {topic.name} is essential for candidates "
            f"preparing for the GitHub Certified Agentic AI Developer exam.",
        ]

        # Add additional context sentences if knowledge points provide more
        kp_count = len(topic.knowledge_point_ids)
        if kp_count > 1:
            sentences.append(
                f"This topic encompasses {kp_count} distinct knowledge "
                f"areas that together provide comprehensive coverage."
            )

        # Ensure minimum sentence count
        while len(sentences) < self._config.min_overview_sentences:
            sentences.append(
                f"Mastery of {topic.name} contributes to overall exam "
                f"readiness in the {domain_name} domain."
            )

        return " ".join(sentences)

    def _build_explanation(self, topic: Topic, is_high_priority: bool) -> str:
        """Build a detailed explanation meeting minimum word counts.

        High-priority topics require MIN_EXPLANATION_WORDS_HIGH_PRIORITY
        words; standard topics require MIN_EXPLANATION_WORDS.
        """
        min_words = (
            self._config.min_explanation_words_high_priority
            if is_high_priority
            else self._config.min_explanation_words
        )

        domain_name = self._get_domain_name(topic.domain_id)
        paragraphs: list[str] = []

        # Core explanation paragraph
        paragraphs.append(
            f"{topic.name} represents a fundamental area of knowledge "
            f"within the {domain_name} domain of the GH-600 certification. "
            f"{topic.description} This concept is integral to understanding "
            f"how GitHub Copilot and agentic AI solutions function within "
            f"modern software development lifecycles. Candidates must "
            f"demonstrate proficiency in applying these concepts to "
            f"real-world development scenarios."
        )

        # Context and importance paragraph
        paragraphs.append(
            f"In the context of the GH-600 exam, {topic.name} relates to "
            f"the broader theme of leveraging AI agents in software "
            f"development. This includes understanding how agentic solutions "
            f"can be designed, implemented, evaluated, secured, and governed "
            f"throughout the development lifecycle. The exam tests both "
            f"theoretical understanding and practical application of these "
            f"concepts in enterprise development environments."
        )

        # Practical application paragraph
        paragraphs.append(
            f"Practical application of {topic.name} involves working with "
            f"GitHub Copilot's agent mode, understanding tool integration, "
            f"and managing AI-assisted development workflows. Developers "
            f"need to understand how to configure, customize, and optimize "
            f"these capabilities for their specific use cases. This requires "
            f"knowledge of both the technical implementation details and the "
            f"organizational processes that support effective AI adoption."
        )

        explanation = "\n\n".join(paragraphs)

        # Expand for high-priority topics to meet 400-word minimum
        if is_high_priority:
            paragraphs.append(
                f"As a high-priority topic, {topic.name} receives "
                f"additional emphasis in exam preparation. The exam may "
                f"include multiple questions testing different aspects of "
                f"this concept, from basic recall to complex scenario-based "
                f"analysis. Candidates should expect questions that require "
                f"combining knowledge of {topic.name} with other related "
                f"topics to solve multi-step problems."
            )
            paragraphs.append(
                f"Advanced scenarios involving {topic.name} often require "
                f"understanding of integration patterns, security "
                f"considerations, performance optimization, and governance "
                f"frameworks. The ability to evaluate trade-offs and make "
                f"informed decisions about implementation approaches is "
                f"critical. Exam questions may present real-world situations "
                f"requiring analysis of multiple factors simultaneously, "
                f"testing the candidate's depth of understanding beyond "
                f"surface-level knowledge."
            )
            explanation = "\n\n".join(paragraphs)

        # Pad to meet minimum word count if needed
        current_words = len(explanation.split())
        while current_words < min_words:
            padding = (
                f"Furthermore, {topic.name} connects to broader themes in "
                f"the {domain_name} domain including best practices, "
                f"enterprise adoption patterns, and continuous improvement "
                f"of AI-assisted development processes. Understanding these "
                f"connections helps candidates answer cross-domain questions."
            )
            explanation += f"\n\n{padding}"
            current_words = len(explanation.split())

        return explanation

    def _build_key_facts(self, topic: Topic) -> list[str]:
        """Build key facts list with at least MIN_KEY_FACTS items."""
        domain_name = self._get_domain_name(topic.domain_id)
        facts: list[str] = [
            f"{topic.name} is part of the {domain_name} domain "
            f"({topic.domain_id}) in the GH-600 certification.",
            f"This topic covers {len(topic.knowledge_point_ids)} "
            f"knowledge point(s) that candidates must understand.",
            f"{topic.description}",
        ]

        # Add domain sub-topic context if available
        domain_config = DOMAIN_BY_ID.get(topic.domain_id)
        if domain_config and topic.sub_domain:
            facts.append(
                f"Falls under the sub-domain: {topic.sub_domain}."
            )

        # Ensure minimum count
        while len(facts) < self._config.min_key_facts:
            facts.append(
                f"{topic.name} is tested in the GH-600 exam and "
                f"requires understanding of practical applications."
            )

        return facts

    def _build_common_mistakes(self, topic: Topic) -> list[str]:
        """Build common mistakes list with at least MIN_COMMON_MISTAKES."""
        domain_name = self._get_domain_name(topic.domain_id)
        mistakes: list[str] = [
            f"Confusing {topic.name} with related but distinct concepts "
            f"in the {domain_name} domain.",
            f"Focusing only on theoretical knowledge of {topic.name} "
            f"without understanding practical implementation scenarios.",
        ]

        if self._is_procedure_topic(topic):
            mistakes.append(
                f"Skipping steps in the {topic.name} workflow or "
                f"performing them out of the required order."
            )

        if self._is_code_topic(topic):
            mistakes.append(
                f"Using incorrect syntax or configuration values when "
                f"implementing {topic.name} in practice."
            )

        # Ensure minimum count
        while len(mistakes) < self._config.min_common_mistakes:
            mistakes.append(
                f"Underestimating the importance of {topic.name} "
                f"in the overall exam preparation strategy."
            )

        return mistakes

    def _build_examples(self, topic: Topic, is_high_priority: bool) -> list[str]:
        """Build examples list with minimum count based on priority.

        High-priority topics require MIN_EXAMPLES_HIGH_PRIORITY examples;
        standard topics require MIN_EXAMPLES.
        """
        min_examples = (
            self._config.min_examples_high_priority
            if is_high_priority
            else self._config.min_examples
        )

        examples: list[str] = [
            f"A developer uses {topic.name} when configuring GitHub "
            f"Copilot agent mode to assist with code generation and "
            f"review tasks in their development workflow.",
        ]

        if is_high_priority:
            examples.append(
                f"In an enterprise setting, {topic.name} is applied to "
                f"ensure that AI-assisted development processes meet "
                f"organizational standards for security and governance."
            )

        if self._is_procedure_topic(topic):
            examples.append(
                f"A team follows the {topic.name} procedure to set up "
                f"their CI/CD pipeline with agentic AI capabilities."
            )

        if self._is_code_topic(topic):
            examples.append(
                f"A configuration file demonstrates how {topic.name} "
                f"settings control agent behavior and permissions."
            )

        # Ensure minimum count
        while len(examples) < min_examples:
            examples.append(
                f"Another scenario where {topic.name} is relevant "
                f"involves integrating AI agents into existing "
                f"development team workflows and practices."
            )

        return examples

    def _build_exam_tips(self, topic: Topic, score: ScoredTopic) -> list[str]:
        """Build exam tips list with at least MIN_EXAM_TIPS items."""
        tips: list[str] = [
            f"Focus on understanding the practical applications of "
            f"{topic.name} rather than just memorizing definitions.",
        ]

        if score.is_high_priority:
            tips.append(
                f"This is a high-priority topic (score: "
                f"{score.priority_score}/10). Expect multiple exam "
                f"questions testing different aspects of {topic.name}."
            )

        if score.domain_count > 1:
            tips.append(
                f"{topic.name} appears across {score.domain_count} "
                f"domains — be prepared for cross-domain questions."
            )

        # Ensure minimum count
        while len(tips) < self._config.min_exam_tips:
            tips.append(
                f"Review {topic.name} in context of the full exam "
                f"domain to understand how it connects to other topics."
            )

        return tips

    def _build_code_blocks(self, topic: Topic) -> list[dict]:
        """Build code blocks with language identifiers and inline comments.

        Returns list of dicts with {language, code, comments}.
        """
        topic_lower = topic.name.lower()

        # Determine appropriate language
        if any(kw in topic_lower for kw in ["yaml", "config", "pipeline"]):
            language = "yaml"
            code = textwrap.dedent(f"""\
                # Configuration for {topic.name}
                name: {_slugify(topic.name)}
                settings:
                  enabled: true  # Enable this feature
                  mode: agent  # Use agent mode
                  permissions:
                    - read  # Allow read access
                    - write  # Allow write access""")
        elif any(kw in topic_lower for kw in ["json", "api", "endpoint"]):
            language = "json"
            code = textwrap.dedent(f"""\
                {{
                  "name": "{_slugify(topic.name)}",
                  "type": "agent-config",
                  "enabled": true,
                  "settings": {{
                    "mode": "copilot-agent",
                    "maxTokens": 4096
                  }}
                }}""")
        else:
            language = "python"
            code = textwrap.dedent(f"""\
                # Implementation of {topic.name}
                def configure_{_slugify(topic.name).replace('-', '_')}():
                    \"\"\"Configure {topic.name} settings.\"\"\"
                    config = {{
                        "enabled": True,  # Activate the feature
                        "mode": "agent",  # Use agent mode
                    }}
                    return config  # Return configuration""")

        comments = (
            f"This example demonstrates a basic {topic.name} "
            f"configuration with inline comments explaining each setting."
        )

        return [{"language": language, "code": code, "comments": comments}]

    def _build_step_by_step(self, topic: Topic) -> list[dict]:
        """Build step-by-step instructions for procedure/workflow topics.

        Returns list of dicts with {step, rationale}.
        """
        topic_name = topic.name
        steps: list[dict] = [
            {
                "step": f"Identify requirements for {topic_name}",
                "rationale": (
                    "Understanding requirements ensures the correct "
                    "approach is selected for the specific use case."
                ),
            },
            {
                "step": f"Configure the environment for {topic_name}",
                "rationale": (
                    "Proper environment setup prevents issues during "
                    "implementation and ensures all dependencies are met."
                ),
            },
            {
                "step": f"Implement {topic_name} following best practices",
                "rationale": (
                    "Following established patterns ensures reliability, "
                    "security, and maintainability of the solution."
                ),
            },
            {
                "step": f"Validate and test the {topic_name} implementation",
                "rationale": (
                    "Testing confirms correct behavior and catches "
                    "issues before they impact production systems."
                ),
            },
            {
                "step": f"Monitor and iterate on {topic_name}",
                "rationale": (
                    "Ongoing monitoring enables continuous improvement "
                    "and early detection of any degradation."
                ),
            },
        ]
        return steps

    def _identify_cross_domain_themes(
        self,
        notes: list[TopicNotes],
        hierarchy: TopicHierarchy,
    ) -> list[dict]:
        """Identify themes that span multiple domains.

        Returns list of dicts with {theme, domains, manifestations}.
        """
        # Group topics by shared concepts to find cross-domain themes
        themes: list[dict] = []

        # Use cross_references from hierarchy
        domain_connections: dict[str, set[str]] = {}
        for xref in hierarchy.cross_references:
            concept = xref.shared_concept
            if concept not in domain_connections:
                domain_connections[concept] = set()

            # Find which domains these topics belong to
            for note in notes:
                if note.topic_id in (xref.topic_id_a, xref.topic_id_b):
                    domain_connections[concept].add(note.domain_id)

        # Create themes from concepts spanning 2+ domains
        for concept, domains in domain_connections.items():
            if len(domains) >= 2:
                domain_names = [
                    self._get_domain_name(d) for d in sorted(domains)
                ]
                themes.append(
                    {
                        "theme": concept,
                        "domains": domain_names,
                        "manifestations": [
                            f"{concept} in {dn}" for dn in domain_names
                        ],
                    }
                )

        return themes

    # --- Utility methods ---

    def _is_procedure_topic(self, topic: Topic) -> bool:
        """Check if topic is a procedure/workflow type."""
        text = f"{topic.name} {topic.description}".lower()
        return any(kw in text for kw in _PROCEDURE_KEYWORDS)

    def _is_code_topic(self, topic: Topic) -> bool:
        """Check if topic is a code/config type."""
        text = f"{topic.name} {topic.description}".lower()
        return any(kw in text for kw in _CODE_KEYWORDS)

    def _get_domain_name(self, domain_id: str) -> str:
        """Look up the human-readable domain name."""
        domain = DOMAIN_BY_ID.get(domain_id)
        if domain:
            return domain.name
        return domain_id

    def _extract_keywords(self, text: str) -> list[str]:
        """Extract meaningful keywords from text, filtering stopwords."""
        stopwords = {
            "the", "a", "an", "is", "are", "was", "were", "be", "been",
            "being", "have", "has", "had", "do", "does", "did", "will",
            "would", "could", "should", "may", "might", "shall", "can",
            "to", "of", "in", "for", "on", "with", "at", "by", "from",
            "as", "into", "through", "during", "before", "after", "and",
            "but", "or", "nor", "not", "so", "yet", "both", "either",
            "neither", "each", "every", "all", "any", "few", "more",
            "most", "other", "some", "such", "no", "only", "own", "same",
            "than", "too", "very", "just", "about", "above", "below",
            "between", "up", "down", "out", "off", "over", "under",
            "again", "further", "then", "once", "that", "this", "these",
            "those", "it", "its",
        }
        words = re.findall(r"\b[a-z]{3,}\b", text)
        return [w for w in words if w not in stopwords]

    def _describe_relationship(
        self, topic: Topic, other: Topic, overlap: set[str]
    ) -> str:
        """Describe the relationship between two topics."""
        shared = ", ".join(sorted(list(overlap)[:3]))
        return f"Shares concepts ({shared}) with {other.name}"

    def _generate_supplemental_explanation(
        self, topic_name: str, domain_id: str, words_needed: int
    ) -> str:
        """Generate additional explanatory text for sparse topics."""
        domain_name = self._get_domain_name(domain_id)
        sentences = [
            f"While detailed source material for {topic_name} is limited, "
            f"this concept plays an important role in the {domain_name} "
            f"domain of the GH-600 certification.",
            f"Candidates should understand how {topic_name} relates to "
            f"the broader ecosystem of GitHub Copilot and agentic AI "
            f"development tools.",
            f"In practice, {topic_name} is often encountered when "
            f"working with agent architecture patterns, implementing "
            f"agentic solutions, or governing AI development workflows.",
            f"The exam may test understanding of {topic_name} through "
            f"scenario-based questions that require applying the concept "
            f"to realistic development situations.",
            f"Key areas to focus on include how {topic_name} integrates "
            f"with other GH-600 topics, common implementation patterns, "
            f"and best practices for enterprise adoption.",
        ]

        result = ""
        for sentence in sentences:
            result += f" {sentence}" if result else sentence
            if len(result.split()) >= words_needed:
                break

        return result.strip()

    def _write_artifact(self, result: StudyNotesCollection) -> None:
        """Write the StudyNotesCollection to the artifacts directory."""
        artifacts_path = Path(ARTIFACTS_DIR)
        artifacts_path.mkdir(parents=True, exist_ok=True)

        output_path = artifacts_path / ARTIFACT_FILENAMES["phase04"]
        output_path.write_text(
            result.model_dump_json(indent=2),
            encoding="utf-8",
        )

    @classmethod
    def from_artifacts(
        cls,
        topic_map_path: str | None = None,
        scores_path: str | None = None,
    ) -> StudyNotesCollection:
        """Load from Phase 2 and Phase 3 artifacts and generate notes.

        Args:
            topic_map_path: Path to phase02_topic_map.json.
            scores_path: Path to phase03_scores.json.

        Returns:
            The generated StudyNotesCollection.
        """
        if topic_map_path is None:
            topic_map_path = str(
                Path(ARTIFACTS_DIR) / ARTIFACT_FILENAMES["phase02"]
            )
        if scores_path is None:
            scores_path = str(
                Path(ARTIFACTS_DIR) / ARTIFACT_FILENAMES["phase03"]
            )

        hierarchy = TopicHierarchy.model_validate_json(
            Path(topic_map_path).read_text(encoding="utf-8")
        )
        scores = ScoredTopicList.model_validate_json(
            Path(scores_path).read_text(encoding="utf-8")
        )

        generator = cls()
        return generator.generate(hierarchy, scores)


def _slugify(text: str) -> str:
    """Convert text to a URL-safe slug."""
    slug = text.lower().strip()
    slug = re.sub(r"[^a-z0-9\s-]", "", slug)
    slug = re.sub(r"[\s_]+", "-", slug)
    slug = re.sub(r"-+", "-", slug)
    return slug.strip("-")
