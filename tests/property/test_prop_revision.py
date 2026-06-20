"""Property-based tests for Phase 6: Revision Generator.

Tests correctness property 14 from the design document:
- Property 14: Flashcard Completeness and Format

**Validates: Requirements 6.3, 6.5, 6.6**
"""

from __future__ import annotations

from unittest.mock import patch

from hypothesis import given, settings, HealthCheck
from hypothesis import strategies as st

from src.config import (
    EXAM_DOMAINS,
    HIGH_PRIORITY_THRESHOLD,
    MIN_FLASHCARDS_TOTAL,
)
from src.models.revision import RevisionPackage
from src.models.scoring import ScoredTopic, ScoredTopicList
from src.models.study_notes import StudyNotesCollection, TopicNotes
from src.phases.phase06_revision import RevisionGenerator


# === Strategies ===

ALL_DOMAIN_IDS = [d.id for d in EXAM_DOMAINS]
DOMAIN_NAMES = {d.id: d.name for d in EXAM_DOMAINS}


@st.composite
def _study_notes_and_scores(
    draw: st.DrawFn,
    min_topics_per_domain: int = 1,
    max_topics_per_domain: int = 4,
) -> tuple[StudyNotesCollection, ScoredTopicList]:
    """Generate a StudyNotesCollection and matching ScoredTopicList.

    Ensures all 6 domains have at least one topic so that flashcard
    distribution across all domains is testable.

    Args:
        draw: Hypothesis draw function.
        min_topics_per_domain: Minimum topics per domain.
        max_topics_per_domain: Maximum topics per domain.
    """
    notes_list: list[TopicNotes] = []
    scored_topics: list[ScoredTopic] = []
    topic_index = 0

    for domain in EXAM_DOMAINS:
        num_topics = draw(
            st.integers(
                min_value=min_topics_per_domain,
                max_value=max_topics_per_domain,
            )
        )
        for j in range(num_topics):
            topic_id = f"topic-{topic_index:04d}"
            topic_name = f"Topic {topic_index} in {domain.name[:20]}"

            priority_score = draw(st.integers(min_value=1, max_value=10))

            # Generate realistic study notes content
            overview = draw(
                st.text(
                    alphabet=st.characters(
                        whitelist_categories=("L", "Nd"),
                        whitelist_characters=" .,-",
                    ),
                    min_size=50,
                    max_size=150,
                ).filter(lambda s: len(s.strip()) >= 30)
            )

            # Key facts: at least 3
            num_key_facts = draw(st.integers(min_value=3, max_value=6))
            key_facts = [
                f"Key fact {k} for {topic_name}" for k in range(num_key_facts)
            ]

            # Common mistakes: at least 2
            num_mistakes = draw(st.integers(min_value=2, max_value=4))
            common_mistakes = [
                f"Common mistake {k} for {topic_name}"
                for k in range(num_mistakes)
            ]

            # Examples: at least 1
            num_examples = draw(st.integers(min_value=1, max_value=3))
            examples = [
                f"Example {k} demonstrating {topic_name}"
                for k in range(num_examples)
            ]

            # Exam tips: at least 1
            num_tips = draw(st.integers(min_value=1, max_value=3))
            exam_tips = [
                f"Exam tip {k} for {topic_name}" for k in range(num_tips)
            ]

            # Optionally include step_by_step
            has_steps = draw(st.booleans())
            step_by_step = None
            if has_steps:
                num_steps = draw(st.integers(min_value=3, max_value=5))
                step_by_step = [
                    {"step": f"Step {s+1}: Do thing {s}", "rationale": f"Because reason {s}"}
                    for s in range(num_steps)
                ]

            note = TopicNotes(
                topic_id=topic_id,
                topic_name=topic_name,
                domain_id=domain.id,
                priority_score=priority_score,
                overview=overview,
                explanation=f"Explanation for {topic_name}. " * 50,
                key_facts=key_facts,
                common_mistakes=common_mistakes,
                examples=examples,
                exam_tips=exam_tips,
                code_blocks=[],
                step_by_step=step_by_step,
                related_topics=[],
                is_supplemented=False,
            )
            notes_list.append(note)

            scored = ScoredTopic(
                topic_id=topic_id,
                topic_name=topic_name,
                domain_ids=[domain.id],
                priority_score=priority_score,
                is_high_priority=priority_score >= HIGH_PRIORITY_THRESHOLD,
                domain_count=1,
            )
            scored_topics.append(scored)
            topic_index += 1

    notes_collection = StudyNotesCollection(
        notes=notes_list,
        cross_domain_themes=[],
    )
    scores = ScoredTopicList(topics=scored_topics)

    return notes_collection, scores


# === Helpers ===


def _generate_revision(
    notes: StudyNotesCollection, scores: ScoredTopicList
) -> RevisionPackage:
    """Run the RevisionGenerator with _write_artifact patched out."""
    generator = RevisionGenerator()
    with patch.object(generator, "_write_artifact"):
        return generator.generate(notes, scores)


# === Property 14: Flashcard Completeness and Format ===


# Feature: gh-600-exam-prep, Property 14: Flashcard Completeness and Format
class TestFlashcardCompletenessAndFormat:
    """For any generated revision package, the total flashcard count SHALL be
    at least 100, every exam domain SHALL be represented by at least one
    flashcard, every flashcard SHALL have a non-empty domain_name and a valid
    priority_score, and every flashcard's question SHALL start with "Q: " and
    answer SHALL start with "A: ".

    **Validates: Requirements 6.3, 6.5, 6.6**
    """

    @given(data=_study_notes_and_scores())
    @settings(max_examples=50, deadline=30000, suppress_health_check=[HealthCheck.too_slow])
    def test_total_flashcard_count_at_least_minimum(
        self,
        data: tuple[StudyNotesCollection, ScoredTopicList],
    ) -> None:
        """Total flashcard count >= MIN_FLASHCARDS_TOTAL (100)."""
        notes, scores = data
        package = _generate_revision(notes, scores)

        assert len(package.flashcards) >= MIN_FLASHCARDS_TOTAL, (
            f"Total flashcards={len(package.flashcards)}, "
            f"expected >= {MIN_FLASHCARDS_TOTAL}"
        )

    @given(data=_study_notes_and_scores())
    @settings(max_examples=50, deadline=30000, suppress_health_check=[HealthCheck.too_slow])
    def test_every_flashcard_question_has_q_prefix(
        self,
        data: tuple[StudyNotesCollection, ScoredTopicList],
    ) -> None:
        """Every flashcard's question starts with 'Q: ' prefix."""
        notes, scores = data
        package = _generate_revision(notes, scores)

        for fc in package.flashcards:
            assert fc.question.startswith("Q: "), (
                f"Flashcard '{fc.id}' question does not start with 'Q: '. "
                f"Question: {fc.question[:50]}"
            )

    @given(data=_study_notes_and_scores())
    @settings(max_examples=50, deadline=30000, suppress_health_check=[HealthCheck.too_slow])
    def test_every_flashcard_answer_has_a_prefix(
        self,
        data: tuple[StudyNotesCollection, ScoredTopicList],
    ) -> None:
        """Every flashcard's answer starts with 'A: ' prefix."""
        notes, scores = data
        package = _generate_revision(notes, scores)

        for fc in package.flashcards:
            assert fc.answer.startswith("A: "), (
                f"Flashcard '{fc.id}' answer does not start with 'A: '. "
                f"Answer: {fc.answer[:50]}"
            )

    @given(data=_study_notes_and_scores())
    @settings(max_examples=50, deadline=30000, suppress_health_check=[HealthCheck.too_slow])
    def test_every_flashcard_has_non_empty_domain_name(
        self,
        data: tuple[StudyNotesCollection, ScoredTopicList],
    ) -> None:
        """Every flashcard is tagged with a non-empty domain_name."""
        notes, scores = data
        package = _generate_revision(notes, scores)

        for fc in package.flashcards:
            assert fc.domain_name and len(fc.domain_name.strip()) > 0, (
                f"Flashcard '{fc.id}' has empty domain_name"
            )

    @given(data=_study_notes_and_scores())
    @settings(max_examples=50, deadline=30000, suppress_health_check=[HealthCheck.too_slow])
    def test_every_flashcard_has_valid_priority_score(
        self,
        data: tuple[StudyNotesCollection, ScoredTopicList],
    ) -> None:
        """Every flashcard has a priority_score between 1 and 10."""
        notes, scores = data
        package = _generate_revision(notes, scores)

        for fc in package.flashcards:
            assert 1 <= fc.priority_score <= 10, (
                f"Flashcard '{fc.id}' has priority_score={fc.priority_score}, "
                f"expected [1, 10]"
            )

    @given(data=_study_notes_and_scores())
    @settings(max_examples=50, deadline=30000, suppress_health_check=[HealthCheck.too_slow])
    def test_flashcards_distributed_across_all_domains(
        self,
        data: tuple[StudyNotesCollection, ScoredTopicList],
    ) -> None:
        """Flashcards are distributed across all 6 domains (each has at least 1)."""
        notes, scores = data
        package = _generate_revision(notes, scores)

        # Collect domain names present in flashcards
        domains_present = {fc.domain_name for fc in package.flashcards}

        # All 6 official exam domain names should be represented
        expected_domain_names = {d.name for d in EXAM_DOMAINS}

        for domain_name in expected_domain_names:
            assert domain_name in domains_present, (
                f"Domain '{domain_name}' has no flashcards. "
                f"Domains with flashcards: {domains_present}"
            )
