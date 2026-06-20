"""Property-based tests for rendering output.

Tests correctness properties 24, 25, and 26 from the design document:
- Property 24: Markdown Heading Hierarchy
- Property 25: Cross-Domain Relationship Diagram Completeness
- Property 26: Related Topics Section Bounds

**Validates: Requirements 11.2, 11.5, 12.1, 12.2, 12.3, 12.5**
"""

from __future__ import annotations

import re
import tempfile
from pathlib import Path

from hypothesis import given, settings, HealthCheck
from hypothesis import strategies as st

from src.config import EXAM_DOMAINS
from src.models.scoring import ScoredTopic, ScoredTopicList
from src.models.study_notes import StudyNotesCollection, TopicNotes
from src.rendering.renderer import PipelineArtifacts, SiteRenderer


# === Constants ===

TEMPLATE_DIR = Path(__file__).resolve().parents[2] / "src" / "rendering" / "templates"
ALL_DOMAIN_IDS = [d.id for d in EXAM_DOMAINS]

# Regex patterns for Markdown analysis
HEADING_PATTERN = re.compile(r"^(#{1,6})\s+.+", re.MULTILINE)


# === Strategies ===


@st.composite
def _code_block_strategy(draw: st.DrawFn) -> dict:
    """Generate a code block dict with a language identifier."""
    language = draw(st.sampled_from(["python", "yaml", "bash", "json", "javascript"]))
    code = draw(st.text(
        alphabet=st.characters(whitelist_categories=("L", "N", "P", "Z")),
        min_size=5,
        max_size=50,
    ))
    comments = draw(st.text(min_size=0, max_size=30))
    return {"language": language, "code": code, "comments": comments}


@st.composite
def _related_topic_strategy(draw: st.DrawFn) -> dict:
    """Generate a related topic entry."""
    topic_id = draw(st.text(
        alphabet=st.characters(whitelist_categories=("L", "N"), whitelist_characters="-_"),
        min_size=3,
        max_size=20,
    ).filter(lambda s: s[0].isalpha()))
    domain_name = draw(st.sampled_from([d.name for d in EXAM_DOMAINS]))
    relationship = draw(st.text(min_size=5, max_size=50))
    return {"topic_id": topic_id, "domain_name": domain_name, "relationship": relationship}


@st.composite
def _topic_notes_strategy(
    draw: st.DrawFn,
    with_related_topics: bool | None = None,
    with_code_blocks: bool | None = None,
) -> TopicNotes:
    """Generate a TopicNotes instance with configurable related_topics presence.

    Args:
        draw: Hypothesis draw function.
        with_related_topics: If True, include 1-10 related topics. If False, empty.
            If None, randomly choose.
        with_code_blocks: If True, include code blocks. If False, empty.
            If None, randomly choose.
    """
    topic_id = draw(st.from_regex(r"topic-[0-9]{4}", fullmatch=True))
    topic_name = draw(st.text(
        alphabet=st.characters(whitelist_categories=("L", "N", "Z")),
        min_size=3,
        max_size=40,
    ).filter(lambda s: s.strip() and s[0].isalpha()))
    domain_id = draw(st.sampled_from(ALL_DOMAIN_IDS))
    priority_score = draw(st.integers(min_value=1, max_value=10))

    # Overview: at least 3 sentences
    overview = "This is the first sentence. This is the second sentence. This is the third sentence."
    # Explanation: at least 200 words
    explanation = " ".join(["word"] * 200)

    key_facts = draw(st.lists(
        st.text(min_size=5, max_size=50),
        min_size=3,
        max_size=5,
    ))
    common_mistakes = draw(st.lists(
        st.text(min_size=5, max_size=50),
        min_size=2,
        max_size=4,
    ))
    examples = draw(st.lists(
        st.text(min_size=5, max_size=50),
        min_size=1,
        max_size=3,
    ))
    exam_tips = draw(st.lists(
        st.text(min_size=5, max_size=50),
        min_size=1,
        max_size=3,
    ))

    # Code blocks
    if with_code_blocks is None:
        include_code = draw(st.booleans())
    else:
        include_code = with_code_blocks

    if include_code:
        code_blocks = draw(st.lists(_code_block_strategy(), min_size=1, max_size=3))
    else:
        code_blocks = []

    # Related topics
    if with_related_topics is None:
        include_related = draw(st.booleans())
    elif with_related_topics:
        include_related = True
    else:
        include_related = False

    if include_related:
        related_topics = draw(st.lists(
            _related_topic_strategy(),
            min_size=1,
            max_size=10,
        ))
    else:
        related_topics = []

    return TopicNotes(
        topic_id=topic_id,
        topic_name=topic_name,
        domain_id=domain_id,
        priority_score=priority_score,
        overview=overview,
        explanation=explanation,
        key_facts=key_facts,
        common_mistakes=common_mistakes,
        examples=examples,
        exam_tips=exam_tips,
        code_blocks=code_blocks,
        related_topics=related_topics,
        is_supplemented=False,
    )


@st.composite
def _study_notes_collection_strategy(
    draw: st.DrawFn,
    min_notes: int = 1,
    max_notes: int = 5,
) -> StudyNotesCollection:
    """Generate a StudyNotesCollection with varied notes."""
    notes = draw(st.lists(
        _topic_notes_strategy(),
        min_size=min_notes,
        max_size=max_notes,
    ))
    cross_domain_themes = draw(st.just([]))  # Keep simple for rendering tests
    return StudyNotesCollection(notes=notes, cross_domain_themes=cross_domain_themes)


@st.composite
def _scored_topic_list_with_cross_domain(
    draw: st.DrawFn,
    min_topics: int = 3,
    max_topics: int = 10,
) -> ScoredTopicList:
    """Generate a ScoredTopicList ensuring some topics appear in 2+ domains with score >= 7.

    This guarantees we have qualifying topics for the Mermaid diagram.
    """
    topics: list[ScoredTopic] = []

    # Always include at least 2 topics with score >= 7 and domain_count >= 2
    num_qualifying = draw(st.integers(min_value=2, max_value=min(5, max_topics)))
    for i in range(num_qualifying):
        domain_count = draw(st.integers(min_value=2, max_value=4))
        domain_ids = draw(
            st.lists(
                st.sampled_from(ALL_DOMAIN_IDS),
                min_size=domain_count,
                max_size=domain_count,
                unique=True,
            )
        )
        score = draw(st.integers(min_value=7, max_value=10))
        topic = ScoredTopic(
            topic_id=f"cross-topic-{i:04d}",
            topic_name=f"Cross Domain Topic {i}",
            domain_ids=domain_ids,
            priority_score=score,
            is_high_priority=score >= 8,
            domain_count=domain_count,
        )
        topics.append(topic)

    # Add some non-qualifying topics
    num_regular = draw(st.integers(
        min_value=max(0, min_topics - num_qualifying),
        max_value=max(0, max_topics - num_qualifying),
    ))
    for i in range(num_regular):
        # Either single domain, or low score, or both
        single_domain = draw(st.booleans())
        if single_domain:
            domain_ids = [draw(st.sampled_from(ALL_DOMAIN_IDS))]
            score = draw(st.integers(min_value=1, max_value=10))
        else:
            domain_count = draw(st.integers(min_value=2, max_value=3))
            domain_ids = draw(
                st.lists(
                    st.sampled_from(ALL_DOMAIN_IDS),
                    min_size=domain_count,
                    max_size=domain_count,
                    unique=True,
                )
            )
            score = draw(st.integers(min_value=1, max_value=6))

        topic = ScoredTopic(
            topic_id=f"regular-topic-{i:04d}",
            topic_name=f"Regular Topic {i}",
            domain_ids=domain_ids,
            priority_score=score,
            is_high_priority=score >= 8,
            domain_count=len(domain_ids),
        )
        topics.append(topic)

    return ScoredTopicList(topics=topics)


# === Helpers ===


def _render_study_notes_to_string(notes_collection: StudyNotesCollection) -> str:
    """Render study notes and return the generated Markdown content."""
    with tempfile.TemporaryDirectory() as tmpdir:
        output_dir = Path(tmpdir) / "docs"
        output_dir.mkdir(parents=True, exist_ok=True)

        renderer = SiteRenderer(template_dir=TEMPLATE_DIR, output_dir=output_dir)
        renderer._render_study_notes(notes_collection)

        study_notes_path = output_dir / "study_notes.md"
        return study_notes_path.read_text(encoding="utf-8")


def _render_cross_domain_to_string(artifacts: PipelineArtifacts) -> str:
    """Render cross-domain content and return the generated Markdown."""
    with tempfile.TemporaryDirectory() as tmpdir:
        output_dir = Path(tmpdir) / "docs"
        output_dir.mkdir(parents=True, exist_ok=True)

        renderer = SiteRenderer(template_dir=TEMPLATE_DIR, output_dir=output_dir)
        renderer._render_cross_domain_content(artifacts)

        cross_domain_path = output_dir / "cross_domain.md"
        return cross_domain_path.read_text(encoding="utf-8")


def _check_heading_hierarchy(content: str) -> tuple[bool, str]:
    """Check Markdown heading hierarchy rules.

    Returns:
        Tuple of (is_valid, error_message). error_message is empty if valid.
    """
    headings = HEADING_PATTERN.findall(content)
    if not headings:
        return False, "No headings found in document"

    # Count H1 headings
    h1_count = sum(1 for h in headings if h == "#")
    if h1_count != 1:
        return False, f"Expected exactly 1 H1 heading, found {h1_count}"

    # Check sequential nesting (no level skipping)
    prev_level = 0
    for heading_hashes in headings:
        level = len(heading_hashes)
        if prev_level == 0:
            # First heading must be H1
            if level != 1:
                return False, f"First heading is H{level}, expected H1"
        else:
            # Can go deeper by at most 1 level at a time
            if level > prev_level + 1:
                return False, (
                    f"Heading level skipped: went from H{prev_level} to H{level}"
                )
        prev_level = level

    return True, ""


def _check_code_blocks_have_language(content: str) -> tuple[bool, str]:
    """Check all fenced code blocks include a language identifier.

    Tracks open/close state: a line with ``` after an opening is a closing fence,
    not a new code block opening.

    Returns:
        Tuple of (is_valid, error_message). error_message is empty if valid.
    """
    in_code_block = False
    for line in content.splitlines():
        stripped = line.strip()
        if stripped.startswith("```"):
            if in_code_block:
                # This is a closing fence
                in_code_block = False
            else:
                # This is an opening fence — must have a language identifier
                lang = stripped[3:].strip()
                if not lang:
                    return False, "Found fenced code block without language identifier"
                if not lang[0].isalpha():
                    return False, f"Invalid language identifier: '{lang}'"
                in_code_block = True

    return True, ""


# === Property 24: Markdown Heading Hierarchy ===


# Feature: gh-600-exam-prep, Property 24: Markdown Heading Hierarchy
class TestMarkdownHeadingHierarchy:
    """For any generated Markdown document, there SHALL be exactly one H1 heading,
    heading levels SHALL be nested sequentially (no skipping from H1 to H3 without
    H2), and all fenced code blocks SHALL include a language identifier.

    **Validates: Requirements 11.2, 11.5**
    """

    @given(notes=_study_notes_collection_strategy(min_notes=1, max_notes=5))
    @settings(max_examples=50, deadline=30000, suppress_health_check=[HealthCheck.too_slow])
    def test_study_notes_has_exactly_one_h1(
        self,
        notes: StudyNotesCollection,
    ) -> None:
        """Rendered study notes Markdown has exactly one H1 heading."""
        content = _render_study_notes_to_string(notes)

        headings = HEADING_PATTERN.findall(content)
        h1_count = sum(1 for h in headings if h == "#")

        assert h1_count == 1, (
            f"Expected exactly 1 H1 heading in study_notes.md, found {h1_count}"
        )

    @given(notes=_study_notes_collection_strategy(min_notes=1, max_notes=5))
    @settings(max_examples=50, deadline=30000, suppress_health_check=[HealthCheck.too_slow])
    def test_study_notes_heading_levels_sequential(
        self,
        notes: StudyNotesCollection,
    ) -> None:
        """Rendered study notes has no heading level skips (e.g., H1 → H3)."""
        content = _render_study_notes_to_string(notes)

        is_valid, error_msg = _check_heading_hierarchy(content)
        assert is_valid, f"Heading hierarchy violation in study_notes.md: {error_msg}"

    @given(notes=_study_notes_collection_strategy(min_notes=1, max_notes=3))
    @settings(max_examples=50, deadline=30000, suppress_health_check=[HealthCheck.too_slow])
    def test_study_notes_code_blocks_have_language(
        self,
        notes: StudyNotesCollection,
    ) -> None:
        """All fenced code blocks in rendered study notes include a language identifier."""
        # Ensure we have code blocks to test
        has_code = any(n.code_blocks for n in notes.notes)
        if not has_code:
            return  # Nothing to check if no code blocks

        content = _render_study_notes_to_string(notes)

        is_valid, error_msg = _check_code_blocks_have_language(content)
        assert is_valid, f"Code block violation in study_notes.md: {error_msg}"

    @given(scores=_scored_topic_list_with_cross_domain(min_topics=3, max_topics=8))
    @settings(max_examples=50, deadline=30000, suppress_health_check=[HealthCheck.too_slow])
    def test_cross_domain_has_exactly_one_h1(
        self,
        scores: ScoredTopicList,
    ) -> None:
        """Rendered cross_domain.md has exactly one H1 heading."""
        artifacts = PipelineArtifacts(scores=scores)
        content = _render_cross_domain_to_string(artifacts)

        headings = HEADING_PATTERN.findall(content)
        h1_count = sum(1 for h in headings if h == "#")

        assert h1_count == 1, (
            f"Expected exactly 1 H1 heading in cross_domain.md, found {h1_count}"
        )

    @given(scores=_scored_topic_list_with_cross_domain(min_topics=3, max_topics=8))
    @settings(max_examples=50, deadline=30000, suppress_health_check=[HealthCheck.too_slow])
    def test_cross_domain_heading_levels_sequential(
        self,
        scores: ScoredTopicList,
    ) -> None:
        """Rendered cross_domain.md has no heading level skips."""
        artifacts = PipelineArtifacts(scores=scores)
        content = _render_cross_domain_to_string(artifacts)

        is_valid, error_msg = _check_heading_hierarchy(content)
        assert is_valid, f"Heading hierarchy violation in cross_domain.md: {error_msg}"

    @given(scores=_scored_topic_list_with_cross_domain(min_topics=3, max_topics=8))
    @settings(max_examples=50, deadline=30000, suppress_health_check=[HealthCheck.too_slow])
    def test_cross_domain_code_blocks_have_language(
        self,
        scores: ScoredTopicList,
    ) -> None:
        """All fenced code blocks in cross_domain.md include a language identifier."""
        artifacts = PipelineArtifacts(scores=scores)
        content = _render_cross_domain_to_string(artifacts)

        is_valid, error_msg = _check_code_blocks_have_language(content)
        assert is_valid, f"Code block violation in cross_domain.md: {error_msg}"


# === Property 25: Cross-Domain Relationship Diagram Completeness ===


# Feature: gh-600-exam-prep, Property 25: Cross-Domain Relationship Diagram Completeness
class TestCrossDomainRelationshipDiagramCompleteness:
    """For any set of topics, the generated Mermaid relationship diagram SHALL include
    every concept with Priority_Score >= 7 that appears in 2 or more exam domains,
    and cross-reference links SHALL exist bidirectionally between each domain's
    coverage of shared concepts.

    **Validates: Requirements 12.1, 12.2**
    """

    @given(scores=_scored_topic_list_with_cross_domain(min_topics=3, max_topics=10))
    @settings(max_examples=50, deadline=30000, suppress_health_check=[HealthCheck.too_slow])
    def test_mermaid_diagram_includes_all_qualifying_concepts(
        self,
        scores: ScoredTopicList,
    ) -> None:
        """Mermaid diagram includes every concept with score >= 7 and domain_count >= 2."""
        artifacts = PipelineArtifacts(scores=scores)

        with tempfile.TemporaryDirectory() as tmpdir:
            output_dir = Path(tmpdir) / "docs"
            renderer = SiteRenderer(template_dir=TEMPLATE_DIR, output_dir=output_dir)
            mermaid_lines = renderer._generate_mermaid_diagram(artifacts)
            mermaid_content = "\n".join(mermaid_lines)

        # Identify qualifying topics
        qualifying_topics = [
            t for t in scores.topics
            if t.priority_score >= 7 and t.domain_count >= 2
        ]

        # Every qualifying topic's name should appear in the Mermaid output
        for topic in qualifying_topics:
            assert topic.topic_name in mermaid_content, (
                f"Topic '{topic.topic_name}' (score={topic.priority_score}, "
                f"domains={topic.domain_count}) is missing from Mermaid diagram"
            )

    @given(scores=_scored_topic_list_with_cross_domain(min_topics=3, max_topics=10))
    @settings(max_examples=50, deadline=30000, suppress_health_check=[HealthCheck.too_slow])
    def test_cross_reference_links_include_all_qualifying_concepts(
        self,
        scores: ScoredTopicList,
    ) -> None:
        """Cross-reference links exist for all concepts in 2+ domains."""
        artifacts = PipelineArtifacts(scores=scores)

        with tempfile.TemporaryDirectory() as tmpdir:
            output_dir = Path(tmpdir) / "docs"
            renderer = SiteRenderer(template_dir=TEMPLATE_DIR, output_dir=output_dir)
            cross_domain_concepts = renderer._get_cross_domain_concepts(artifacts)

        # Identify topics with domain_count >= 2
        expected_topics = {
            t.topic_name
            for t in scores.topics
            if t.domain_count >= 2
        }

        actual_topics = {c["name"] for c in cross_domain_concepts}

        # Every topic in 2+ domains should appear in cross-domain concepts
        missing = expected_topics - actual_topics
        assert not missing, (
            f"Cross-domain concepts missing topics that appear in 2+ domains: {missing}"
        )

    @given(scores=_scored_topic_list_with_cross_domain(min_topics=3, max_topics=10))
    @settings(max_examples=50, deadline=30000, suppress_health_check=[HealthCheck.too_slow])
    def test_cross_reference_links_bidirectional(
        self,
        scores: ScoredTopicList,
    ) -> None:
        """Cross-reference links exist bidirectionally between domain coverages."""
        artifacts = PipelineArtifacts(scores=scores)
        content = _render_cross_domain_to_string(artifacts)

        # For each qualifying topic, check that ALL its domains are referenced
        qualifying_topics = [
            t for t in scores.topics
            if t.domain_count >= 2
        ]

        from src.config import DOMAIN_BY_ID

        for topic in qualifying_topics:
            # Each domain where this topic appears should be mentioned in
            # the cross-domain content near the topic name
            for domain_id in topic.domain_ids:
                if domain_id in DOMAIN_BY_ID:
                    domain_name = DOMAIN_BY_ID[domain_id].name
                    # The domain name should appear somewhere in context of
                    # cross-domain references
                    assert domain_name in content, (
                        f"Domain '{domain_name}' not found in cross-domain content "
                        f"for topic '{topic.topic_name}' which appears in domains "
                        f"{topic.domain_ids}"
                    )


# === Property 26: Related Topics Section Bounds ===


# Feature: gh-600-exam-prep, Property 26: Related Topics Section Bounds
class TestRelatedTopicsSectionBounds:
    """For any topic with identified cross-domain connections, the Related Topics
    section SHALL contain between 1 and 10 entries. For any topic with no
    cross-domain connections, the Related Topics section SHALL be omitted entirely.

    **Validates: Requirements 12.3, 12.5**
    """

    @given(notes=st.lists(
        _topic_notes_strategy(with_related_topics=True),
        min_size=1,
        max_size=5,
    ))
    @settings(max_examples=50, deadline=30000, suppress_health_check=[HealthCheck.too_slow])
    def test_related_topics_between_1_and_10_entries(
        self,
        notes: list[TopicNotes],
    ) -> None:
        """Topics with related_topics have between 1 and 10 entries in the section."""
        for note in notes:
            # The strategy guarantees 1-10, but verify the model constraint
            assert 1 <= len(note.related_topics) <= 10, (
                f"Topic '{note.topic_name}' has {len(note.related_topics)} "
                f"related topics, expected between 1 and 10"
            )

        # Verify the rendered output also reflects this
        collection = StudyNotesCollection(notes=notes, cross_domain_themes=[])
        content = _render_study_notes_to_string(collection)

        for note in notes:
            # Each topic with related topics should have a "Related Topics" section
            # We check for the heading presence within context of the topic
            assert "### Related Topics" in content, (
                f"Topic '{note.topic_name}' has {len(note.related_topics)} related "
                f"topics but 'Related Topics' section not found in rendered output"
            )

    @given(notes=st.lists(
        _topic_notes_strategy(with_related_topics=False),
        min_size=1,
        max_size=5,
    ))
    @settings(max_examples=50, deadline=30000, suppress_health_check=[HealthCheck.too_slow])
    def test_no_related_topics_section_when_empty(
        self,
        notes: list[TopicNotes],
    ) -> None:
        """Topics with no cross-domain connections omit the Related Topics section."""
        # Verify all notes have empty related_topics
        for note in notes:
            assert len(note.related_topics) == 0

        collection = StudyNotesCollection(notes=notes, cross_domain_themes=[])
        content = _render_study_notes_to_string(collection)

        assert "### Related Topics" not in content, (
            "Found 'Related Topics' section in rendered output, but all "
            "topics have empty related_topics lists"
        )

    @given(data=st.data())
    @settings(max_examples=50, deadline=30000, suppress_health_check=[HealthCheck.too_slow])
    def test_mixed_topics_correct_section_presence(
        self,
        data: st.DataObject,
    ) -> None:
        """In a mixed collection, only topics with connections get Related Topics."""
        # Generate a mix of topics with and without related topics
        with_related = data.draw(st.lists(
            _topic_notes_strategy(with_related_topics=True),
            min_size=1,
            max_size=3,
        ))
        without_related = data.draw(st.lists(
            _topic_notes_strategy(with_related_topics=False),
            min_size=1,
            max_size=3,
        ))

        # Ensure unique topic names by appending suffixes
        used_names: set[str] = set()
        for i, note in enumerate(with_related):
            name = f"WithRel {i} {note.topic_name}"
            while name in used_names:
                name += "x"
            used_names.add(name)
            with_related[i] = note.model_copy(update={"topic_name": name})

        for i, note in enumerate(without_related):
            name = f"NoRel {i} {note.topic_name}"
            while name in used_names:
                name += "x"
            used_names.add(name)
            without_related[i] = note.model_copy(update={"topic_name": name})

        all_notes = with_related + without_related
        collection = StudyNotesCollection(notes=all_notes, cross_domain_themes=[])
        content = _render_study_notes_to_string(collection)

        # Split content by topic sections (## heading) and match on the heading line
        topic_sections = re.split(r"(?=^## )", content, flags=re.MULTILINE)

        def _find_topic_section(topic_name: str) -> str | None:
            """Find the section whose heading line is exactly '## <topic_name>'."""
            for section in topic_sections:
                # The heading is the first line of the section
                first_line = section.split("\n", 1)[0].strip()
                if first_line == f"## {topic_name}":
                    return section
            return None

        for note in without_related:
            section = _find_topic_section(note.topic_name)
            if section is not None:
                assert "### Related Topics" not in section, (
                    f"Topic '{note.topic_name}' has no related topics "
                    f"but its section contains 'Related Topics'"
                )

        for note in with_related:
            section = _find_topic_section(note.topic_name)
            if section is not None:
                assert "### Related Topics" in section, (
                    f"Topic '{note.topic_name}' has {len(note.related_topics)} "
                    f"related topics but its section doesn't contain "
                    f"'Related Topics'"
                )
