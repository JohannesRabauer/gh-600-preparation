"""Models for Phase 1: Knowledge Extraction."""

from typing import Optional

from pydantic import BaseModel


class KnowledgePoint(BaseModel):
    """A single extracted piece of knowledge."""

    id: str
    content: str
    category: str  # concept | definition | fact | theory | procedure | framework
    source_url: str
    source_title: str
    depth: int  # 0, 1, or 2
    is_prerequisite: bool = False


class ParsedDocument(BaseModel):
    """A fetched and parsed source document."""

    url: str
    title: str
    content_text: str
    links: list[str]
    knowledge_points: list[KnowledgePoint]
    fetch_error: Optional[str] = None


class ExtractionResult(BaseModel):
    """Complete output of Phase 1."""

    documents: list[ParsedDocument]
    all_knowledge_points: list[KnowledgePoint]
    error_log: list[dict]  # {url, error, referrer}
    visited_urls: set[str]
    stats: dict  # counts by depth, domain, category


class ExtractionLog(BaseModel):
    """Log entry for extraction errors."""

    url: str
    error: str
    referrer: str
