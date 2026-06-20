"""Property-based tests for Phase 4: Study Notes Generator.

Tests correctness properties 8, 9, and 10 from the design document:
- Property 8: Study Notes Structural Completeness
- Property 9: Sparse Topic Supplementation
- Property 10: Cross-Reference Referential Integrity

**Validates: Requirements 4.1, 4.2, 4.5, 4.6, 4.7**
"""

from __future__ import annotations

from unittest.mock import patch

from hypothesis import given, settings
from hypothesis import strategies as st

from src.config import (
    EXAM_DOMAINS,
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
from src.models.topic_map import CrossReference, Topic, TopicHierarchy
from src.phases.phase04_notes import StudyNotesGenerator


# === Strategies ===

ALL_DOMAIN_IDS = [d.id for d in EXAM_DOMAINS]


@st.composite
def _random_topic(
    draw: st.DrawFn,
    *,
    min_kp: int = 0,
    max_kp: int = 8,
    priority_score: int | None = None,
) -> tuple[Topic, ScoredTopic]:
    """Generate a random topic with a scored entry.

    Args:
        min_kp: Minimum number of knowledge_point_ids.
        max_kp: Maximum number of knowledge_point_ids.
        priority_score: If provided, forces this score; otherwise random 1-10.
    """
    domain_id = draw(st.sampled_from(ALL_DOMAIN_IDS))
    topic_index = draw(st.integers(min_value=1, max_value=9999))
    topic_id = f"topic-{topic_index:04d}"

    topic_name = draw(
        st.text(
            alphabet=st.characters(whitelist_categories=("L",), whitelist_characters=" -"),
            min_size=4,
            max_size=30,
        ).filter(lambda s: s.strip() != "" and len(s.strip()) >= 4)
    )

    num_kps = draw(st.integers(min_value=min_kp, max_value=max_kp))
    knowledge_point_ids = [f"kp-{topic_index}-{i}" for i in range(num_kps)]

    description = draw(
        st.text(
            alphabet=st.characters(whitelist_categories=("L", "Nd"), whitelist_characters=" .,-"),
            min_size=10,
            max_size=60,
        ).filter(lambda s: s.strip() != "")
    )

    topic = Topic(
        id=topic_id,
        name=topic_name.strip(),
        domain_id=domain_id,
        sub_domain=None,
        knowledge_point_ids=knowledge_point_ids,
        description=description.strip(),
    )

    if priority_score is None:
        score_val = draw(st.integers(min_value=1, max_value=10))
    else:
        score_val = priority_score

    scored = ScoredTopic(
        topic_id=topic_id,
        topic_name=topic_name.strip(),
        domain_ids=[domain_id],
        priority_score=score_val,
        is_high_priority=score_val >= HIGH_PRIORITY_THRESHOLD,
        domain_count=1,
    )

    return topic, scored


@st.composite
def _topics_with_scores(
    draw: st.DrawFn,
    min_topics: int = 1,
    max_topics: int = 8,
    min_kp: int = 0,
    max_kp: int = 8,
) -> tuple[TopicHierarchy, ScoredTopicList]:
    """Generate a TopicHierarchy and corresponding ScoredTopicList.

    Creates multiple topics across domains with random priority scores.
    """
    num_topics = draw(st.integers(min_value=min_topics, max_value=max_topics))

    topics: list[Topic] = []
    scored_topics: list[ScoredTopic] = []

    for i in range(num_topics):
        domain_id = draw(st.sampled_from(ALL_DOMAIN_IDS))
        topic_id = f"topic-{i:04d}"
        topic_name = f"Topic {i} {draw(st.text(alphabet='abcdefghijk', min_size=3, max_size=8))}"

        num_kps = draw(st.integers(min_value=min_kp, max_value=max_kp))
        knowledge_point_ids = [f"kp-{i}-{j}" for j in range(num_kps)]

        topic = Topic(
            id=topic_id,
            name=topic_name,
            domain_id=domain_id,
            sub_domain=None,
            knowledge_point_ids=knowledge_point_ids,
            description=f"Description for {topic_name} covering important concepts.",
        )
        topics.append(topic)

        score_val = draw(st.integers(min_value=1, max_value=10))
        scored = ScoredTopic(
            topic_id=topic_id,
            topic_name=topic_name,
            domain_ids=[domain_id],
            priority_score=score_val,
            is_high_priority=score_val >= HIGH_PRIORITY_THRESHOLD,
            domain_count=1,
        )
        scored_topics.append(scored)

    # Build hierarchy domains dict
    domains_dict: dict[str, list[Topic]] = {}
    for topic in topics:
        if topic.domain_id not in domains_dict:
            domains_dict[topic.domain_id] = []
        domains_dict[topic.domain_id].append(topic)

    hierarchy = TopicHierarchy(
        domains=domains_dict,
        dependencies=[],
        cross_references=[],
        learning_order=[t.id for t in topics],
        learning_units=[],
    )

    scores = ScoredTopicList(topics=scored_topics)
    return hierarchy, scores


@st.composite
def _sparse_topics(
    draw: st.DrawFn,
    min_topics: int = 1,
    max_topics: int = 5,
) -> tuple[TopicHierarchy, ScoredTopicList]:
    """Generate topics that are all sparse (< SPARSE_TOPIC_KNOWLEDGE_POINT_THRESHOLD kps)."""
    num_topics = draw(st.integers(min_value=min_topics, max_value=max_topics))

    topics: list[Topic] = []
    scored_topics: list[ScoredTopic] = []

    for i in range(num_topics):
        domain_id = draw(st.sampled_from(ALL_DOMAIN_IDS))
        topic_id = f"sparse-{i:04d}"
        topic_name = f"Sparse Topic {i}"

        # Below the threshold (0, 1, or 2 knowledge points)
        num_kps = draw(st.integers(min_value=0, max_value=SPARSE_TOPIC_KNOWLEDGE_POINT_THRESHOLD - 1))
        knowledge_point_ids = [f"kp-sparse-{i}-{j}" for j in range(num_kps)]

        topic = Topic(
            id=topic_id,
            name=topic_name,
            domain_id=domain_id,
            sub_domain=None,
            knowledge_point_ids=knowledge_point_ids,
            description=f"A sparse topic with limited source material for testing.",
        )
        topics.append(topic)

        score_val = draw(st.integers(min_value=1, max_value=10))
        scored = ScoredTopic(
            topic_id=topic_id,
            topic_name=topic_name,
            domain_ids=[domain_id],
            priority_score=score_val,
            is_high_priority=score_val >= HIGH_PRIORITY_THRESHOLD,
            domain_count=1,
        )
        scored_topics.append(scored)

    domains_dict: dict[str, list[Topic]] = {}
    for topic in topics:
        if topic.domain_id not in domains_dict:
            domains_dict[topic.domain_id] = []
        domains_dict[topic.domain_id].append(topic)

    hierarchy = TopicHierarchy(
        domains=domains_dict,
        dependencies=[],
        cross_references=[],
        learning_order=[t.id for t in topics],
        learning_units=[],
    )

    scores = ScoredTopicList(topics=scored_topics)
    return hierarchy, scores


@st.composite
def _multi_domain_topics_with_cross_refs(
    draw: st.DrawFn,
) -> tuple[TopicHierarchy, ScoredTopicList]:
    """Generate topics across multiple domains with cross-references.

    Ensures at least 2 domains with topics that share keywords to produce
    cross-references from the generator.
    """
    # Use at least 2 different domains
    num_domains = draw(st.integers(min_value=2, max_value=4))
    selected_domains = draw(
        st.lists(
            st.sampled_from(ALL_DOMAIN_IDS),
            min_size=num_domains,
            max_size=num_domains,
            unique=True,
        )
    )

    topics: list[Topic] = []
    scored_topics: list[ScoredTopic] = []

    # Shared keywords to force cross-references between domains
    shared_keywords = ["agent", "copilot", "workflow", "configuration"]

    topic_index = 0
    for domain_id in selected_domains:
        num_in_domain = draw(st.integers(min_value=1, max_value=3))
        for j in range(num_in_domain):
            topic_id = f"xref-{topic_index:04d}"
            # Include shared keywords in name and description to trigger cross-refs
            keyword = shared_keywords[topic_index % len(shared_keywords)]
            topic_name = f"{keyword.capitalize()} Topic {topic_index}"
            description = (
                f"This topic covers {keyword} patterns and agent integration "
                f"approaches for the copilot workflow configuration."
            )

            num_kps = draw(st.integers(min_value=3, max_value=6))
            knowledge_point_ids = [f"kp-xref-{topic_index}-{k}" for k in range(num_kps)]

            topic = Topic(
                id=topic_id,
                name=topic_name,
                domain_id=domain_id,
                sub_domain=None,
                knowledge_point_ids=knowledge_point_ids,
                description=description,
            )
            topics.append(topic)

            score_val = draw(st.integers(min_value=1, max_value=10))
            scored = ScoredTopic(
                topic_id=topic_id,
                topic_name=topic_name,
                domain_ids=[domain_id],
                priority_score=score_val,
                is_high_priority=score_val >= HIGH_PRIORITY_THRESHOLD,
                domain_count=1,
            )
            scored_topics.append(scored)
            topic_index += 1

    domains_dict: dict[str, list[Topic]] = {}
    for topic in topics:
        if topic.domain_id not in domains_dict:
            domains_dict[topic.domain_id] = []
        domains_dict[topic.domain_id].append(topic)

    # Add cross-references between topics in different domains
    cross_refs: list[CrossReference] = []
    for i, t1 in enumerate(topics):
        for t2 in topics[i + 1:]:
            if t1.domain_id != t2.domain_id:
                cross_refs.append(
                    CrossReference(
                        topic_id_a=t1.id,
                        topic_id_b=t2.id,
                        shared_concept="shared agent concept",
                    )
                )

    hierarchy = TopicHierarchy(
        domains=domains_dict,
        dependencies=[],
        cross_references=cross_refs,
        learning_order=[t.id for t in topics],
        learning_units=[],
    )

    scores = ScoredTopicList(topics=scored_topics)
    return hierarchy, scores


# === Helpers ===


def _count_sentences(text: str) -> int:
    """Count sentences by splitting on period followed by space or end."""
    import re
    sentences = re.split(r'(?<=[.!?])\s+', text.strip())
    return len([s for s in sentences if s.strip()])


def _generate_notes(
    hierarchy: TopicHierarchy, scores: ScoredTopicList
):
    """Run the generator with _write_artifact patched out."""
    generator = StudyNotesGenerator()
    with patch.object(generator, "_write_artifact"):
        return generator.generate(hierarchy, scores)


# === Property 8: Study Notes Structural Completeness ===


# Feature: gh-600-exam-prep, Property 8: Study Notes Structural Completeness
class TestStudyNotesStructuralCompleteness:
    """For any topic (with any priority score between 1-10), the generated notes
    have: overview with 3+ sentences, explanation with 200+ words (400+ if
    high-priority), key_facts with 3+ items, common_mistakes with 2+ items,
    examples with 1+ items (2+ if high-priority), exam_tips with 1+ items.

    **Validates: Requirements 4.1, 4.2, 4.7**
    """

    @given(data=_topics_with_scores(min_topics=1, max_topics=5))
    @settings(max_examples=50, deadline=10000)
    def test_overview_has_minimum_sentences(
        self,
        data: tuple[TopicHierarchy, ScoredTopicList],
    ) -> None:
        """Every topic's overview has at least MIN_OVERVIEW_SENTENCES sentences."""
        hierarchy, scores = data
        result = _generate_notes(hierarchy, scores)

        for notes in result.notes:
            sentence_count = _count_sentences(notes.overview)
            assert sentence_count >= MIN_OVERVIEW_SENTENCES, (
                f"Topic '{notes.topic_name}' overview has {sentence_count} "
                f"sentences, expected >= {MIN_OVERVIEW_SENTENCES}. "
                f"Overview: {notes.overview[:100]}..."
            )

    @given(data=_topics_with_scores(min_topics=1, max_topics=5))
    @settings(max_examples=50, deadline=10000)
    def test_explanation_meets_word_count(
        self,
        data: tuple[TopicHierarchy, ScoredTopicList],
    ) -> None:
        """Explanation has 200+ words (400+ for high-priority topics)."""
        hierarchy, scores = data
        result = _generate_notes(hierarchy, scores)

        for notes in result.notes:
            word_count = len(notes.explanation.split())
            if notes.priority_score >= HIGH_PRIORITY_THRESHOLD:
                min_words = MIN_EXPLANATION_WORDS_HIGH_PRIORITY
            else:
                min_words = MIN_EXPLANATION_WORDS

            assert word_count >= min_words, (
                f"Topic '{notes.topic_name}' (priority={notes.priority_score}) "
                f"explanation has {word_count} words, expected >= {min_words}"
            )

    @given(data=_topics_with_scores(min_topics=1, max_topics=5))
    @settings(max_examples=50, deadline=10000)
    def test_key_facts_minimum_count(
        self,
        data: tuple[TopicHierarchy, ScoredTopicList],
    ) -> None:
        """Every topic has at least MIN_KEY_FACTS key facts."""
        hierarchy, scores = data
        result = _generate_notes(hierarchy, scores)

        for notes in result.notes:
            assert len(notes.key_facts) >= MIN_KEY_FACTS, (
                f"Topic '{notes.topic_name}' has {len(notes.key_facts)} "
                f"key_facts, expected >= {MIN_KEY_FACTS}"
            )

    @given(data=_topics_with_scores(min_topics=1, max_topics=5))
    @settings(max_examples=50, deadline=10000)
    def test_common_mistakes_minimum_count(
        self,
        data: tuple[TopicHierarchy, ScoredTopicList],
    ) -> None:
        """Every topic has at least MIN_COMMON_MISTAKES common mistakes."""
        hierarchy, scores = data
        result = _generate_notes(hierarchy, scores)

        for notes in result.notes:
            assert len(notes.common_mistakes) >= MIN_COMMON_MISTAKES, (
                f"Topic '{notes.topic_name}' has {len(notes.common_mistakes)} "
                f"common_mistakes, expected >= {MIN_COMMON_MISTAKES}"
            )

    @given(data=_topics_with_scores(min_topics=1, max_topics=5))
    @settings(max_examples=50, deadline=10000)
    def test_examples_minimum_count(
        self,
        data: tuple[TopicHierarchy, ScoredTopicList],
    ) -> None:
        """Examples have 1+ items (2+ for high-priority topics)."""
        hierarchy, scores = data
        result = _generate_notes(hierarchy, scores)

        for notes in result.notes:
            if notes.priority_score >= HIGH_PRIORITY_THRESHOLD:
                min_examples = MIN_EXAMPLES_HIGH_PRIORITY
            else:
                min_examples = MIN_EXAMPLES

            assert len(notes.examples) >= min_examples, (
                f"Topic '{notes.topic_name}' (priority={notes.priority_score}) "
                f"has {len(notes.examples)} examples, expected >= {min_examples}"
            )

    @given(data=_topics_with_scores(min_topics=1, max_topics=5))
    @settings(max_examples=50, deadline=10000)
    def test_exam_tips_minimum_count(
        self,
        data: tuple[TopicHierarchy, ScoredTopicList],
    ) -> None:
        """Every topic has at least MIN_EXAM_TIPS exam tips."""
        hierarchy, scores = data
        result = _generate_notes(hierarchy, scores)

        for notes in result.notes:
            assert len(notes.exam_tips) >= MIN_EXAM_TIPS, (
                f"Topic '{notes.topic_name}' has {len(notes.exam_tips)} "
                f"exam_tips, expected >= {MIN_EXAM_TIPS}"
            )


# === Property 9: Sparse Topic Supplementation ===


# Feature: gh-600-exam-prep, Property 9: Sparse Topic Supplementation
class TestSparseTopicSupplementation:
    """For any topic with < 3 knowledge points, the generated notes have
    is_supplemented=True and contain the visual indicator
    '> [!NOTE] Supplemented content' in at least one field.

    **Validates: Requirements 4.6**
    """

    @given(data=_sparse_topics(min_topics=1, max_topics=4))
    @settings(max_examples=50, deadline=10000)
    def test_sparse_topics_are_supplemented(
        self,
        data: tuple[TopicHierarchy, ScoredTopicList],
    ) -> None:
        """Topics with < SPARSE_TOPIC_KNOWLEDGE_POINT_THRESHOLD kps have is_supplemented=True."""
        hierarchy, scores = data
        result = _generate_notes(hierarchy, scores)

        for notes in result.notes:
            assert notes.is_supplemented is True, (
                f"Topic '{notes.topic_name}' has < "
                f"{SPARSE_TOPIC_KNOWLEDGE_POINT_THRESHOLD} knowledge points "
                f"but is_supplemented={notes.is_supplemented}"
            )

    @given(data=_sparse_topics(min_topics=1, max_topics=4))
    @settings(max_examples=50, deadline=10000)
    def test_sparse_topics_contain_supplement_marker(
        self,
        data: tuple[TopicHierarchy, ScoredTopicList],
    ) -> None:
        """Sparse topics contain '> [!NOTE] Supplemented content' in at least one field."""
        hierarchy, scores = data
        result = _generate_notes(hierarchy, scores)

        marker = "> [!NOTE] Supplemented content"

        for notes in result.notes:
            # Check explanation, key_facts entries, and examples entries
            marker_found = marker in notes.explanation
            if not marker_found:
                marker_found = any(marker in fact for fact in notes.key_facts)
            if not marker_found:
                marker_found = any(marker in ex for ex in notes.examples)

            assert marker_found, (
                f"Topic '{notes.topic_name}' is supplemented but no field "
                f"contains the visual marker '{marker}'. "
                f"explanation[:100]={notes.explanation[:100]}, "
                f"key_facts={notes.key_facts[:2]}, "
                f"examples={notes.examples[:2]}"
            )

    @given(data=_topics_with_scores(min_topics=1, max_topics=5, min_kp=3, max_kp=8))
    @settings(max_examples=50, deadline=10000)
    def test_non_sparse_topics_not_supplemented(
        self,
        data: tuple[TopicHierarchy, ScoredTopicList],
    ) -> None:
        """Topics with >= SPARSE_TOPIC_KNOWLEDGE_POINT_THRESHOLD kps are NOT supplemented."""
        hierarchy, scores = data
        result = _generate_notes(hierarchy, scores)

        for notes in result.notes:
            assert notes.is_supplemented is False, (
                f"Topic '{notes.topic_name}' has >= "
                f"{SPARSE_TOPIC_KNOWLEDGE_POINT_THRESHOLD} knowledge points "
                f"but is_supplemented={notes.is_supplemented}"
            )


# === Property 10: Cross-Reference Referential Integrity ===


# Feature: gh-600-exam-prep, Property 10: Cross-Reference Referential Integrity
class TestCrossReferenceReferentialIntegrity:
    """Every cross-reference in related_topics contains a topic_id that exists
    in the set of all generated topic IDs, a non-empty domain_name, and a
    non-empty relationship description.

    **Validates: Requirements 4.5**
    """

    @given(data=_multi_domain_topics_with_cross_refs())
    @settings(max_examples=50, deadline=10000)
    def test_cross_reference_topic_ids_exist(
        self,
        data: tuple[TopicHierarchy, ScoredTopicList],
    ) -> None:
        """Every related_topics topic_id references an existing topic in the output."""
        hierarchy, scores = data
        result = _generate_notes(hierarchy, scores)

        all_topic_ids = {notes.topic_id for notes in result.notes}

        for notes in result.notes:
            for ref in notes.related_topics:
                assert ref["topic_id"] in all_topic_ids, (
                    f"Topic '{notes.topic_name}' has cross-reference to "
                    f"topic_id='{ref['topic_id']}' which does not exist in "
                    f"the output. All topic IDs: {all_topic_ids}"
                )

    @given(data=_multi_domain_topics_with_cross_refs())
    @settings(max_examples=50, deadline=10000)
    def test_cross_reference_domain_name_non_empty(
        self,
        data: tuple[TopicHierarchy, ScoredTopicList],
    ) -> None:
        """Every cross-reference has a non-empty domain_name."""
        hierarchy, scores = data
        result = _generate_notes(hierarchy, scores)

        for notes in result.notes:
            for ref in notes.related_topics:
                assert ref["domain_name"] and len(ref["domain_name"].strip()) > 0, (
                    f"Topic '{notes.topic_name}' has cross-reference to "
                    f"'{ref['topic_id']}' with empty domain_name"
                )

    @given(data=_multi_domain_topics_with_cross_refs())
    @settings(max_examples=50, deadline=10000)
    def test_cross_reference_relationship_non_empty(
        self,
        data: tuple[TopicHierarchy, ScoredTopicList],
    ) -> None:
        """Every cross-reference has a non-empty relationship description."""
        hierarchy, scores = data
        result = _generate_notes(hierarchy, scores)

        for notes in result.notes:
            for ref in notes.related_topics:
                assert ref["relationship"] and len(ref["relationship"].strip()) > 0, (
                    f"Topic '{notes.topic_name}' has cross-reference to "
                    f"'{ref['topic_id']}' with empty relationship"
                )

    @given(data=_topics_with_scores(min_topics=2, max_topics=6))
    @settings(max_examples=50, deadline=10000)
    def test_cross_references_never_self_reference(
        self,
        data: tuple[TopicHierarchy, ScoredTopicList],
    ) -> None:
        """No topic has a cross-reference pointing to itself."""
        hierarchy, scores = data
        result = _generate_notes(hierarchy, scores)

        for notes in result.notes:
            for ref in notes.related_topics:
                assert ref["topic_id"] != notes.topic_id, (
                    f"Topic '{notes.topic_name}' has a self-reference "
                    f"in related_topics"
                )
