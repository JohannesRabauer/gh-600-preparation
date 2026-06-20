"""Models for Phase 6: Revision Resources."""

from pydantic import BaseModel


class Flashcard(BaseModel):
    """A single flashcard."""

    id: str
    question: str  # Prefixed with "Q: "
    answer: str  # Prefixed with "A: "
    domain_name: str
    topic_id: str
    priority_score: int


class CheatSheet(BaseModel):
    """A domain-specific cheat sheet."""

    domain_id: str
    domain_name: str
    tables: list[dict]  # {title, headers, rows}
    key_commands: list[str]
    patterns: list[str]


class Mnemonic(BaseModel):
    """A mnemonic device for a complex topic."""

    topic_id: str
    topic_name: str
    mnemonic: str
    components: list[str]  # The 3+ items being memorized


class RevisionPackage(BaseModel):
    """Complete output of Phase 6."""

    executive_summary: str  # Max 2000 words
    cheat_sheets: list[CheatSheet]  # At least 1 per domain
    flashcards: list[Flashcard]  # Min 100 total
    mnemonics: list[Mnemonic]
