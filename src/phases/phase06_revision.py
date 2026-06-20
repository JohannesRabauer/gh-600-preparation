"""Phase 6: Revision Resources Generator.

Produces condensed revision materials including an executive summary,
cheat sheets, flashcards, and mnemonics from study notes and scores.
"""

from __future__ import annotations

import uuid
from pathlib import Path

from src.config import (
    ARTIFACTS_DIR,
    ARTIFACT_FILENAMES,
    DOMAIN_BY_ID,
    EXAM_DOMAINS,
    EXECUTIVE_SUMMARY_MAX_WORDS,
    HIGH_PRIORITY_THRESHOLD,
    MNEMONIC_MIN_STEPS,
    MIN_FLASHCARDS_TOTAL,
)
from src.models.revision import (
    CheatSheet,
    Flashcard,
    Mnemonic,
    RevisionPackage,
)
from src.models.scoring import ScoredTopicList
from src.models.study_notes import StudyNotesCollection, TopicNotes


class RevisionGenerator:
    """Phase 6: Produces condensed revision resources.

    Generates an executive summary, cheat sheets with tables, flashcards
    in Q:/A: format tagged with domain and priority, and mnemonics for
    sequential topics.
    """

    def __init__(self) -> None:
        """Initialize the RevisionGenerator."""
        pass

    def generate(
        self, notes: StudyNotesCollection, scores: ScoredTopicList
    ) -> RevisionPackage:
        """Generate revision resources from study notes and scores.

        Produces executive summary, cheat sheets, flashcards, and
        mnemonics covering all 6 exam domains.

        Args:
            notes: StudyNotesCollection from Phase 4.
            scores: ScoredTopicList from Phase 3.

        Returns:
            A complete RevisionPackage with all revision resources.
        """
        # Build score lookup: topic_id -> ScoredTopic
        self._score_map = {st.topic_id: st for st in scores.topics}

        # Build notes grouped by domain
        self._notes_by_domain: dict[str, list[TopicNotes]] = {}
        for domain in EXAM_DOMAINS:
            self._notes_by_domain[domain.id] = []
        for note in notes.notes:
            domain_id = note.domain_id
            if domain_id not in self._notes_by_domain:
                self._notes_by_domain[domain_id] = []
            self._notes_by_domain[domain_id].append(note)

        executive_summary = self._generate_executive_summary(notes)
        cheat_sheets = self._generate_cheat_sheets(notes)
        flashcards = self._generate_flashcards(notes, scores)
        mnemonics = self._generate_mnemonics(notes)

        package = RevisionPackage(
            executive_summary=executive_summary,
            cheat_sheets=cheat_sheets,
            flashcards=flashcards,
            mnemonics=mnemonics,
        )

        # Write artifact to disk
        self._write_artifact(package)

        return package

    def _generate_executive_summary(
        self, notes: StudyNotesCollection
    ) -> str:
        """Generate an executive summary covering all 6 domains.

        The summary is capped at 2000 words and covers each exam domain
        with its key concepts and exam relevance.

        Args:
            notes: The study notes collection.

        Returns:
            A string executive summary of at most 2000 words.
        """
        sections: list[str] = []
        sections.append(
            "Executive Summary: GH-600 GitHub Certified Agentic AI Developer"
        )
        sections.append("")
        sections.append(
            "This summary covers the six exam domains of the GH-600 "
            "certification, providing a condensed overview of key concepts, "
            "patterns, and exam-relevant information for efficient revision."
        )
        sections.append("")

        # Budget words per domain (leave room for intro/outro)
        # ~2000 words total, ~100 for intro/outro, ~300 per domain
        words_per_domain = (
            EXECUTIVE_SUMMARY_MAX_WORDS - 100
        ) // len(EXAM_DOMAINS)

        for domain in EXAM_DOMAINS:
            domain_notes = self._notes_by_domain.get(domain.id, [])
            section = self._summarize_domain(
                domain.id, domain.name, domain_notes, words_per_domain
            )
            sections.append(section)
            sections.append("")

        full_summary = "\n".join(sections)

        # Enforce word limit by trimming if necessary
        words = full_summary.split()
        if len(words) > EXECUTIVE_SUMMARY_MAX_WORDS:
            full_summary = " ".join(words[:EXECUTIVE_SUMMARY_MAX_WORDS])

        return full_summary

    def _summarize_domain(
        self,
        domain_id: str,
        domain_name: str,
        domain_notes: list[TopicNotes],
        max_words: int,
    ) -> str:
        """Summarize a single domain for the executive summary.

        Args:
            domain_id: The domain identifier.
            domain_name: Human-readable domain name.
            domain_notes: Study notes for topics in this domain.
            max_words: Maximum word budget for this domain section.

        Returns:
            A summary section string for the domain.
        """
        domain_config = DOMAIN_BY_ID.get(domain_id)
        weight_str = ""
        if domain_config:
            weight_str = (
                f" ({int(domain_config.weight_min * 100)}-"
                f"{int(domain_config.weight_max * 100)}% of exam)"
            )

        lines: list[str] = []
        lines.append(f"## {domain_name}{weight_str}")
        lines.append("")

        if not domain_notes:
            lines.append(
                f"This domain covers {domain_name.lower()}. "
                "Key topics include understanding the principles, "
                "patterns, and best practices relevant to this area "
                "of the GH-600 certification."
            )
        else:
            # Include overview from high-priority topics first
            high_priority_notes = sorted(
                [n for n in domain_notes if n.priority_score >= HIGH_PRIORITY_THRESHOLD],
                key=lambda n: n.priority_score,
                reverse=True,
            )
            other_notes = [
                n for n in domain_notes if n.priority_score < HIGH_PRIORITY_THRESHOLD
            ]

            # Summarize high-priority topics
            for note in high_priority_notes:
                # Use overview as a condensed representation
                overview_trimmed = " ".join(
                    note.overview.split()[:50]
                )
                lines.append(f"**{note.topic_name}** (Priority: {note.priority_score}): {overview_trimmed}")
                lines.append("")

            # Summarize remaining topics more briefly
            if other_notes:
                topic_names = [n.topic_name for n in other_notes[:10]]
                lines.append(
                    "Additional topics: " + ", ".join(topic_names) + "."
                )
                lines.append("")

            # Add key facts from domain
            all_facts = []
            for note in domain_notes[:5]:
                all_facts.extend(note.key_facts[:2])
            if all_facts:
                lines.append("Key points:")
                for fact in all_facts[:5]:
                    lines.append(f"- {fact}")
                lines.append("")

        section = "\n".join(lines)
        # Trim to word budget
        words = section.split()
        if len(words) > max_words:
            section = " ".join(words[:max_words])

        return section

    def _generate_cheat_sheets(
        self, notes: StudyNotesCollection
    ) -> list[CheatSheet]:
        """Generate cheat sheets with at least 1 table per domain.

        Each cheat sheet contains key commands, patterns, and quick-reference
        tables organized by exam domain.

        Args:
            notes: The study notes collection.

        Returns:
            A list of CheatSheet objects, at least one per domain.
        """
        cheat_sheets: list[CheatSheet] = []

        for domain in EXAM_DOMAINS:
            domain_notes = self._notes_by_domain.get(domain.id, [])
            cheat_sheet = self._build_domain_cheat_sheet(
                domain.id, domain.name, domain_notes
            )
            cheat_sheets.append(cheat_sheet)

        return cheat_sheets

    def _build_domain_cheat_sheet(
        self,
        domain_id: str,
        domain_name: str,
        domain_notes: list[TopicNotes],
    ) -> CheatSheet:
        """Build a cheat sheet for a single domain.

        Args:
            domain_id: The domain identifier.
            domain_name: Human-readable domain name.
            domain_notes: Study notes for topics in this domain.

        Returns:
            A CheatSheet instance for the domain.
        """
        # Extract key commands from code blocks and step_by_step
        key_commands: list[str] = []
        patterns: list[str] = []
        table_rows: list[list[str]] = []

        for note in domain_notes:
            # Extract commands from code blocks
            for code_block in note.code_blocks:
                code = code_block.get("code", "")
                if code:
                    # Take first line as a command reference
                    first_line = code.strip().split("\n")[0]
                    if first_line and first_line not in key_commands:
                        key_commands.append(first_line)

            # Extract patterns from key facts
            for fact in note.key_facts:
                if fact not in patterns:
                    patterns.append(fact)

            # Build table row: topic, priority, key takeaway
            priority = note.priority_score
            key_takeaway = (
                note.key_facts[0] if note.key_facts else note.topic_name
            )
            table_rows.append([note.topic_name, str(priority), key_takeaway])

        # Ensure at least one table per domain (Requirement 6.2)
        if not table_rows:
            # Create a placeholder table with domain sub-topics
            domain_config = DOMAIN_BY_ID.get(domain_id)
            if domain_config:
                for sub_topic in domain_config.sub_topics:
                    table_rows.append([sub_topic, "-", "Review required"])

        tables: list[dict] = [
            {
                "title": f"{domain_name} - Quick Reference",
                "headers": ["Topic", "Priority", "Key Point"],
                "rows": table_rows,
            }
        ]

        # If no key commands, provide domain-relevant placeholders
        if not key_commands:
            domain_config = DOMAIN_BY_ID.get(domain_id)
            if domain_config:
                key_commands = [
                    f"# {sub}" for sub in domain_config.sub_topics[:3]
                ]

        # If no patterns, derive from domain sub-topics
        if not patterns:
            domain_config = DOMAIN_BY_ID.get(domain_id)
            if domain_config:
                patterns = domain_config.sub_topics[:3]

        return CheatSheet(
            domain_id=domain_id,
            domain_name=domain_name,
            tables=tables,
            key_commands=key_commands[:10],
            patterns=patterns[:10],
        )

    def _generate_flashcards(
        self, notes: StudyNotesCollection, scores: ScoredTopicList
    ) -> list[Flashcard]:
        """Generate 100+ flashcards distributed across all 6 domains.

        Each flashcard is tagged with domain name and Priority_Score,
        formatted with "Q: " / "A: " prefixes.

        Args:
            notes: The study notes collection.
            scores: The scored topic list.

        Returns:
            A list of Flashcard objects, minimum 100 total.
        """
        flashcards: list[Flashcard] = []

        # Determine how many flashcards per domain (distribute evenly,
        # with higher-weighted domains getting more)
        total_target = max(MIN_FLASHCARDS_TOTAL, len(notes.notes) * 3)
        domain_targets = self._distribute_flashcard_targets(total_target)

        for domain in EXAM_DOMAINS:
            domain_notes = self._notes_by_domain.get(domain.id, [])
            target = domain_targets.get(domain.id, 17)
            domain_flashcards = self._generate_domain_flashcards(
                domain.id, domain.name, domain_notes, target
            )
            flashcards.extend(domain_flashcards)

        # Ensure minimum of 100 flashcards total
        # If we don't have enough, generate more from available notes
        while len(flashcards) < MIN_FLASHCARDS_TOTAL:
            for domain in EXAM_DOMAINS:
                if len(flashcards) >= MIN_FLASHCARDS_TOTAL:
                    break
                domain_notes = self._notes_by_domain.get(domain.id, [])
                extra = self._generate_supplementary_flashcards(
                    domain.id, domain.name, domain_notes, flashcards
                )
                flashcards.extend(extra)
            # Safety: if we've exhausted all generation possibilities, break
            if len(flashcards) >= MIN_FLASHCARDS_TOTAL:
                break
            # Generate generic flashcards to reach minimum
            remaining = MIN_FLASHCARDS_TOTAL - len(flashcards)
            flashcards.extend(
                self._generate_generic_flashcards(remaining, flashcards)
            )
            break

        return flashcards

    def _distribute_flashcard_targets(
        self, total_target: int
    ) -> dict[str, int]:
        """Distribute flashcard targets across domains by weight.

        Higher-weighted domains get proportionally more flashcards.

        Args:
            total_target: Total number of flashcards to target.

        Returns:
            Dictionary mapping domain_id to target flashcard count.
        """
        targets: dict[str, int] = {}
        total_weight = sum(
            (d.weight_min + d.weight_max) / 2 for d in EXAM_DOMAINS
        )

        for domain in EXAM_DOMAINS:
            avg_weight = (domain.weight_min + domain.weight_max) / 2
            proportion = avg_weight / total_weight if total_weight > 0 else 1 / 6
            target = max(5, round(total_target * proportion))
            targets[domain.id] = target

        return targets

    def _generate_domain_flashcards(
        self,
        domain_id: str,
        domain_name: str,
        domain_notes: list[TopicNotes],
        target_count: int,
    ) -> list[Flashcard]:
        """Generate flashcards for a specific domain.

        Creates flashcards from topic overviews, key facts, common mistakes,
        and exam tips.

        Args:
            domain_id: The domain identifier.
            domain_name: Human-readable domain name.
            domain_notes: Study notes for topics in this domain.
            target_count: Target number of flashcards for this domain.

        Returns:
            List of Flashcard objects for this domain.
        """
        flashcards: list[Flashcard] = []

        for note in domain_notes:
            if len(flashcards) >= target_count:
                break

            priority = note.priority_score

            # Flashcard from overview - "What is [topic]?"
            flashcards.append(
                Flashcard(
                    id=self._generate_id(),
                    question=f"Q: What is {note.topic_name}?",
                    answer=f"A: {self._truncate_to_sentence(note.overview)}",
                    domain_name=domain_name,
                    topic_id=note.topic_id,
                    priority_score=priority,
                )
            )

            # Flashcards from key facts
            for i, fact in enumerate(note.key_facts):
                if len(flashcards) >= target_count:
                    break
                flashcards.append(
                    Flashcard(
                        id=self._generate_id(),
                        question=f"Q: What is a key fact about {note.topic_name}?",
                        answer=f"A: {fact}",
                        domain_name=domain_name,
                        topic_id=note.topic_id,
                        priority_score=priority,
                    )
                )

            # Flashcard from common mistakes
            for mistake in note.common_mistakes:
                if len(flashcards) >= target_count:
                    break
                flashcards.append(
                    Flashcard(
                        id=self._generate_id(),
                        question=f"Q: What is a common mistake regarding {note.topic_name}?",
                        answer=f"A: {mistake}",
                        domain_name=domain_name,
                        topic_id=note.topic_id,
                        priority_score=priority,
                    )
                )

            # Flashcard from exam tips
            for tip in note.exam_tips:
                if len(flashcards) >= target_count:
                    break
                flashcards.append(
                    Flashcard(
                        id=self._generate_id(),
                        question=f"Q: What exam tip should you remember for {note.topic_name}?",
                        answer=f"A: {tip}",
                        domain_name=domain_name,
                        topic_id=note.topic_id,
                        priority_score=priority,
                    )
                )

        return flashcards

    def _generate_supplementary_flashcards(
        self,
        domain_id: str,
        domain_name: str,
        domain_notes: list[TopicNotes],
        existing: list[Flashcard],
    ) -> list[Flashcard]:
        """Generate additional flashcards from deeper content.

        Uses explanations and examples to create more flashcards when
        the initial pass didn't reach the target count.

        Args:
            domain_id: The domain identifier.
            domain_name: Human-readable domain name.
            domain_notes: Study notes for topics in this domain.
            existing: Already-generated flashcards (to check for domain coverage).

        Returns:
            Additional Flashcard objects.
        """
        flashcards: list[Flashcard] = []

        for note in domain_notes:
            priority = note.priority_score

            # From examples
            for example in note.examples:
                flashcards.append(
                    Flashcard(
                        id=self._generate_id(),
                        question=f"Q: Give an example of {note.topic_name} in practice.",
                        answer=f"A: {example}",
                        domain_name=domain_name,
                        topic_id=note.topic_id,
                        priority_score=priority,
                    )
                )

            # From step_by_step if available
            if note.step_by_step:
                steps_summary = "; ".join(
                    s.get("step", "") for s in note.step_by_step[:3]
                )
                if steps_summary:
                    flashcards.append(
                        Flashcard(
                            id=self._generate_id(),
                            question=f"Q: What are the key steps for {note.topic_name}?",
                            answer=f"A: {steps_summary}",
                            domain_name=domain_name,
                            topic_id=note.topic_id,
                            priority_score=priority,
                        )
                    )

        return flashcards

    def _generate_generic_flashcards(
        self, count: int, existing: list[Flashcard]
    ) -> list[Flashcard]:
        """Generate generic domain flashcards to reach minimum count.

        Creates flashcards from domain sub-topics when topic notes
        don't provide enough material.

        Args:
            count: Number of flashcards to generate.
            existing: Already-generated flashcards.

        Returns:
            List of generic Flashcard objects.
        """
        flashcards: list[Flashcard] = []
        domain_index = 0

        while len(flashcards) < count:
            domain = EXAM_DOMAINS[domain_index % len(EXAM_DOMAINS)]
            domain_index += 1

            for sub_topic in domain.sub_topics:
                if len(flashcards) >= count:
                    break
                flashcards.append(
                    Flashcard(
                        id=self._generate_id(),
                        question=f"Q: Explain the concept of: {sub_topic}",
                        answer=(
                            f"A: {sub_topic} is a key concept in the "
                            f"{domain.name} domain of the GH-600 exam. "
                            f"It involves understanding and applying "
                            f"principles related to this area."
                        ),
                        domain_name=domain.name,
                        topic_id=f"generic-{domain.id}",
                        priority_score=6,
                    )
                )

            # Safety: break if we've cycled through all domains
            if domain_index > len(EXAM_DOMAINS) * len(EXAM_DOMAINS[0].sub_topics):
                break

        return flashcards[:count]

    def _generate_mnemonics(
        self, notes: StudyNotesCollection
    ) -> list[Mnemonic]:
        """Generate mnemonics for topics with 3+ sequential steps.

        Creates mnemonic devices for topics that have step_by_step
        procedures with MNEMONIC_MIN_STEPS or more components.

        Args:
            notes: The study notes collection.

        Returns:
            A list of Mnemonic objects.
        """
        mnemonics: list[Mnemonic] = []

        for note in notes.notes:
            # Check for step-by-step procedures with 3+ steps
            if note.step_by_step and len(note.step_by_step) >= MNEMONIC_MIN_STEPS:
                components = [
                    step.get("step", f"Step {i+1}")
                    for i, step in enumerate(note.step_by_step)
                ]
                mnemonic_str = self._create_mnemonic(
                    note.topic_name, components
                )
                mnemonics.append(
                    Mnemonic(
                        topic_id=note.topic_id,
                        topic_name=note.topic_name,
                        mnemonic=mnemonic_str,
                        components=components,
                    )
                )

            # Also check key_facts with 3+ items as sequential concepts
            elif len(note.key_facts) >= MNEMONIC_MIN_STEPS:
                components = note.key_facts[:7]  # Cap at 7 for readability
                mnemonic_str = self._create_mnemonic(
                    note.topic_name, components
                )
                mnemonics.append(
                    Mnemonic(
                        topic_id=note.topic_id,
                        topic_name=note.topic_name,
                        mnemonic=mnemonic_str,
                        components=components,
                    )
                )

        return mnemonics

    def _create_mnemonic(
        self, topic_name: str, components: list[str]
    ) -> str:
        """Create a mnemonic string from component first letters.

        Uses the first letter of each component's first significant word
        to form an acronym, then provides the full expansion.

        Args:
            topic_name: The topic the mnemonic is for.
            components: The 3+ items to memorize.

        Returns:
            A mnemonic string with acronym and expansion.
        """
        # Extract first letter of each component's first significant word
        letters: list[str] = []
        for component in components:
            words = component.strip().split()
            # Skip common starting words to get more meaningful letters
            skip_words = {"a", "an", "the", "is", "are", "to", "for", "in", "of"}
            first_word = ""
            for word in words:
                if word.lower() not in skip_words:
                    first_word = word
                    break
            if not first_word and words:
                first_word = words[0]
            if first_word:
                letters.append(first_word[0].upper())

        acronym = "".join(letters)

        # Build expansion
        expansion_parts = [
            f"{letter} = {comp}"
            for letter, comp in zip(letters, components)
        ]
        expansion = "; ".join(expansion_parts)

        return f"Remember '{acronym}' for {topic_name}: {expansion}"

    def _truncate_to_sentence(self, text: str) -> str:
        """Truncate text to the first complete sentence.

        Args:
            text: Input text to truncate.

        Returns:
            The first sentence of the text, or first 100 chars if no
            sentence boundary found.
        """
        # Find first sentence boundary
        for i, char in enumerate(text):
            if char == "." and i > 10:
                return text[: i + 1]
        # Fallback: first 100 characters
        if len(text) > 100:
            return text[:100] + "..."
        return text

    def _generate_id(self) -> str:
        """Generate a unique ID for flashcards.

        Returns:
            A UUID4-based string ID.
        """
        return f"fc-{uuid.uuid4().hex[:8]}"

    def _write_artifact(self, package: RevisionPackage) -> None:
        """Write the RevisionPackage to the artifacts directory.

        Creates the artifacts directory if it doesn't exist.
        Writes the result as JSON to phase06_revision.json.

        Args:
            package: The revision package to persist.
        """
        artifacts_path = Path(ARTIFACTS_DIR)
        artifacts_path.mkdir(parents=True, exist_ok=True)

        output_path = artifacts_path / ARTIFACT_FILENAMES["phase06"]
        output_path.write_text(
            package.model_dump_json(indent=2),
            encoding="utf-8",
        )

    @classmethod
    def from_artifacts(
        cls,
        notes_path: str | None = None,
        scores_path: str | None = None,
    ) -> RevisionPackage:
        """Load from Phase 4 and Phase 3 artifact files and generate revision.

        Reads the study notes and scored topic list from disk,
        then generates revision resources.

        Args:
            notes_path: Path to phase04_notes.json.
                Defaults to artifacts/phase04_notes.json.
            scores_path: Path to phase03_scores.json.
                Defaults to artifacts/phase03_scores.json.

        Returns:
            The generated RevisionPackage.
        """
        if notes_path is None:
            notes_path = str(
                Path(ARTIFACTS_DIR) / ARTIFACT_FILENAMES["phase04"]
            )
        if scores_path is None:
            scores_path = str(
                Path(ARTIFACTS_DIR) / ARTIFACT_FILENAMES["phase03"]
            )

        notes = StudyNotesCollection.model_validate_json(
            Path(notes_path).read_text(encoding="utf-8")
        )
        scores = ScoredTopicList.model_validate_json(
            Path(scores_path).read_text(encoding="utf-8")
        )

        generator = cls()
        return generator.generate(notes, scores)
