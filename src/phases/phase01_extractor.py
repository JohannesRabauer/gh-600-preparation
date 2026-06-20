"""Phase 1: Knowledge Extraction.

Ingests source materials from Microsoft Learn and GitHub documentation,
follows links up to 2 levels deep (max 50 per level), extracts knowledge
points, deduplicates content, and writes the ExtractionResult artifact.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path
from urllib.parse import urlparse

from src.config import (
    ALLOWED_DOMAINS,
    ARTIFACTS_DIR,
    ARTIFACT_FILENAMES,
    MAX_LINK_DEPTH,
    MAX_LINKS_PER_LEVEL,
)
from src.models.knowledge import (
    ExtractionResult,
    KnowledgePoint,
    ParsedDocument,
)
from src.utils.dedup import URLTracker
from src.utils.scraper import Scraper, extract_links, extract_text


@dataclass
class ExtractorConfig:
    """Configuration for the KnowledgeExtractor."""

    max_depth: int = MAX_LINK_DEPTH
    max_links_per_level: int = MAX_LINKS_PER_LEVEL
    allowed_domains: list[str] = field(default_factory=lambda: list(ALLOWED_DOMAINS))
    artifacts_dir: str = ARTIFACTS_DIR


# Patterns for classifying knowledge point categories.
_CATEGORY_PATTERNS: dict[str, list[re.Pattern[str]]] = {
    "definition": [
        re.compile(r"\bis defined as\b", re.IGNORECASE),
        re.compile(r"\brefers to\b", re.IGNORECASE),
        re.compile(r"\bis a\b.{5,80}that\b", re.IGNORECASE),
        re.compile(r"\bmeans\b", re.IGNORECASE),
    ],
    "procedure": [
        re.compile(r"^\s*(?:step\s+)?\d+[\.\):]", re.IGNORECASE | re.MULTILINE),
        re.compile(r"\bfollow(?:ing)?\s+(?:these\s+)?steps\b", re.IGNORECASE),
        re.compile(r"\bhow to\b", re.IGNORECASE),
        re.compile(r"\bto configure\b", re.IGNORECASE),
        re.compile(r"\bto set up\b", re.IGNORECASE),
        re.compile(r"\bto create\b", re.IGNORECASE),
    ],
    "framework": [
        re.compile(r"\bframework\b", re.IGNORECASE),
        re.compile(r"\barchitecture\b", re.IGNORECASE),
        re.compile(r"\bpattern\b", re.IGNORECASE),
        re.compile(r"\bmodel\b", re.IGNORECASE),
        re.compile(r"\bpipeline\b", re.IGNORECASE),
    ],
    "theory": [
        re.compile(r"\bprinciple\b", re.IGNORECASE),
        re.compile(r"\btheory\b", re.IGNORECASE),
        re.compile(r"\bapproach\b", re.IGNORECASE),
        re.compile(r"\bmethodology\b", re.IGNORECASE),
        re.compile(r"\bstrategy\b", re.IGNORECASE),
    ],
    "fact": [
        re.compile(r"\bsupports?\b", re.IGNORECASE),
        re.compile(r"\brequires?\b", re.IGNORECASE),
        re.compile(r"\bincludes?\b", re.IGNORECASE),
        re.compile(r"\bprovides?\b", re.IGNORECASE),
        re.compile(r"\benables?\b", re.IGNORECASE),
        re.compile(r"\bmaximum\b", re.IGNORECASE),
        re.compile(r"\bminimum\b", re.IGNORECASE),
        re.compile(r"\bdefault\b", re.IGNORECASE),
    ],
}

# Terms that suggest a prerequisite reference.
_PREREQUISITE_INDICATORS: list[re.Pattern[str]] = [
    re.compile(r"\bprerequisite\b", re.IGNORECASE),
    re.compile(r"\bbefore you (?:begin|start|can)\b", re.IGNORECASE),
    re.compile(r"\brequires? (?:knowledge|understanding|familiarity)\b", re.IGNORECASE),
    re.compile(r"\bassuming you (?:know|understand|have)\b", re.IGNORECASE),
    re.compile(r"\bfamiliarity with\b", re.IGNORECASE),
    re.compile(r"\bmust (?:first|already)\b", re.IGNORECASE),
]


class KnowledgeExtractor:
    """Phase 1: Extracts knowledge from source materials.

    Processes source URLs, follows links up to configured depth,
    extracts knowledge points, and deduplicates content.
    """

    def __init__(self, config: ExtractorConfig | None = None) -> None:
        self._config = config or ExtractorConfig()
        self._url_tracker = URLTracker()
        self._documents: list[ParsedDocument] = []
        self._all_knowledge_points: list[KnowledgePoint] = []
        self._point_id_counter: int = 0

    def _generate_point_id(self) -> str:
        """Generate a unique knowledge point ID."""
        self._point_id_counter += 1
        return f"kp-{self._point_id_counter:04d}"

    def _is_allowed_domain(self, url: str) -> bool:
        """Check if a URL is within the allowed domains."""
        parsed = urlparse(url)
        hostname = (parsed.hostname or "").lower()
        return any(hostname == domain or hostname.endswith(f".{domain}")
                   for domain in self._config.allowed_domains)

    async def extract(self, source_urls: list[str]) -> ExtractionResult:
        """Process source URLs and extract all knowledge points.

        Fetches source documents (depth 0), follows links up to depth 2,
        extracts knowledge points, and reconstructs prerequisites.

        Args:
            source_urls: List of initial source URLs to process.

        Returns:
            ExtractionResult containing all documents, knowledge points,
            error logs, visited URLs, and statistics.
        """
        async with Scraper() as scraper:
            # Process depth 0: source documents
            for url in source_urls:
                if self._url_tracker.has_visited(url):
                    continue
                doc = await self._fetch_and_parse(scraper, url, depth=0)
                if doc:
                    self._documents.append(doc)

            # Process depth 1: links from source documents
            if self._config.max_depth >= 1:
                depth_0_docs = list(self._documents)
                await self._process_links_at_depth(
                    scraper, depth_0_docs, depth=1
                )

            # Process depth 2: links from depth-1 documents
            if self._config.max_depth >= 2:
                depth_1_docs = [
                    d for d in self._documents
                    if d not in depth_0_docs  # noqa: B023 — intentional closure
                ]
                await self._process_links_at_depth(
                    scraper, depth_1_docs, depth=2
                )

            # Reconstruct prerequisites from all collected points
            prerequisite_points = self._reconstruct_prerequisites(
                self._all_knowledge_points
            )
            self._all_knowledge_points.extend(prerequisite_points)

            # Build statistics
            stats = self._build_stats()

            result = ExtractionResult(
                documents=self._documents,
                all_knowledge_points=self._all_knowledge_points,
                error_log=scraper.error_log,
                visited_urls=self._url_tracker.get_visited(),
                stats=stats,
            )

        # Write artifact to disk
        self._write_artifact(result)

        return result

    async def _process_links_at_depth(
        self,
        scraper: Scraper,
        parent_docs: list[ParsedDocument],
        depth: int,
    ) -> None:
        """Follow and process links from parent documents at the given depth.

        Limits to max_links_per_level links total for this depth level.
        Only follows links within allowed domains.
        """
        links_followed = 0

        for doc in parent_docs:
            if links_followed >= self._config.max_links_per_level:
                break

            for link in doc.links:
                if links_followed >= self._config.max_links_per_level:
                    break

                if not self._is_allowed_domain(link):
                    continue

                if self._url_tracker.has_visited(link):
                    continue

                new_doc = await self._fetch_and_parse(scraper, link, depth=depth)
                if new_doc:
                    self._documents.append(new_doc)
                    links_followed += 1

    async def _fetch_and_parse(
        self,
        scraper: Scraper,
        url: str,
        depth: int,
    ) -> ParsedDocument | None:
        """Fetch a URL and parse it into a ParsedDocument.

        Marks the URL as visited, fetches HTML content, extracts text
        and links, then extracts knowledge points from the content.

        Args:
            scraper: The Scraper instance to use for HTTP fetching.
            url: The URL to fetch.
            depth: The current traversal depth (0, 1, or 2).

        Returns:
            A ParsedDocument if successfully fetched, or a document
            with fetch_error set if the fetch failed. Returns None if
            the URL was already visited.
        """
        if self._url_tracker.has_visited(url):
            return None

        self._url_tracker.mark_visited(url)

        html_content, error = await scraper.fetch(url, referrer=url)

        if error:
            # Create a minimal document recording the error
            return ParsedDocument(
                url=url,
                title="",
                content_text="",
                links=[],
                knowledge_points=[],
                fetch_error=error,
            )

        # Extract text content and links from HTML
        text_content = extract_text(html_content)
        links = extract_links(html_content, url)
        title = self._extract_title(html_content)

        # Build the parsed document (without knowledge points first)
        doc = ParsedDocument(
            url=url,
            title=title,
            content_text=text_content,
            links=links,
            knowledge_points=[],
        )

        # Extract knowledge points from the document
        knowledge_points = self._extract_knowledge_points(doc, depth)
        doc.knowledge_points = knowledge_points
        self._all_knowledge_points.extend(knowledge_points)

        return doc

    def _extract_title(self, html: str) -> str:
        """Extract the page title from HTML."""
        from bs4 import BeautifulSoup

        soup = BeautifulSoup(html, "html.parser")
        title_tag = soup.find("title")
        if title_tag and title_tag.string:
            return title_tag.string.strip()

        # Fallback to first h1
        h1_tag = soup.find("h1")
        if h1_tag:
            return h1_tag.get_text(strip=True)

        return ""

    def _extract_knowledge_points(
        self, doc: ParsedDocument, depth: int
    ) -> list[KnowledgePoint]:
        """Extract knowledge points from a parsed document.

        Splits the document text into paragraphs and classifies each
        meaningful paragraph as a knowledge point with a category.

        Categories: concept, definition, fact, theory, procedure, framework.

        Args:
            doc: The parsed document to extract from.
            depth: The traversal depth of this document.

        Returns:
            List of extracted KnowledgePoint instances.
        """
        if not doc.content_text:
            return []

        points: list[KnowledgePoint] = []
        paragraphs = self._split_into_paragraphs(doc.content_text)

        for paragraph in paragraphs:
            # Skip very short paragraphs (likely navigation or noise)
            if len(paragraph.split()) < 8:
                continue

            category = self._classify_paragraph(paragraph)

            point = KnowledgePoint(
                id=self._generate_point_id(),
                content=paragraph.strip(),
                category=category,
                source_url=doc.url,
                source_title=doc.title,
                depth=depth,
                is_prerequisite=False,
            )
            points.append(point)

        return points

    def _split_into_paragraphs(self, text: str) -> list[str]:
        """Split text content into logical paragraphs.

        Uses double newlines as paragraph separators. Also handles
        sections that end with a heading-like line followed by content.
        """
        # Split on double newlines (or more)
        raw_paragraphs = re.split(r"\n{2,}", text)

        paragraphs: list[str] = []
        for para in raw_paragraphs:
            stripped = para.strip()
            if stripped:
                paragraphs.append(stripped)

        return paragraphs

    def _classify_paragraph(self, text: str) -> str:
        """Classify a paragraph into a knowledge point category.

        Uses heuristic pattern matching to determine the most likely
        category. If no specific pattern matches, defaults to 'concept'.

        Args:
            text: The paragraph text to classify.

        Returns:
            One of: concept, definition, fact, theory, procedure, framework.
        """
        # Check each category's patterns, counting matches
        scores: dict[str, int] = {}

        for category, patterns in _CATEGORY_PATTERNS.items():
            match_count = sum(
                1 for pattern in patterns if pattern.search(text)
            )
            if match_count > 0:
                scores[category] = match_count

        if not scores:
            # Default to 'concept' when no specific patterns match
            return "concept"

        # Return the category with the most pattern matches
        return max(scores, key=scores.get)  # type: ignore[arg-type]

    def _reconstruct_prerequisites(
        self, points: list[KnowledgePoint]
    ) -> list[KnowledgePoint]:
        """Identify and reconstruct prerequisite concepts.

        Scans knowledge points for references to prerequisite concepts
        that are not explicitly covered in the extracted sources. Creates
        minimal KnowledgePoint entries for those prerequisites.

        The scope is limited to concepts directly required to understand
        the extracted topics, without expanding into unrelated areas.

        Args:
            points: All currently extracted knowledge points.

        Returns:
            List of reconstructed prerequisite KnowledgePoint instances.
        """
        # Collect full content of non-prerequisite-referencing points.
        # These represent concepts already covered in the source material.
        covered_content_parts: list[str] = []
        for point in points:
            is_prereq_ref = any(
                p.search(point.content) for p in _PREREQUISITE_INDICATORS
            )
            if not is_prereq_ref:
                covered_content_parts.append(point.content.lower())

        covered_content = " ".join(covered_content_parts)

        prerequisite_points: list[KnowledgePoint] = []
        seen_prerequisites: set[str] = set()

        for point in points:
            # Only process the first matching prerequisite pattern per point
            # to avoid extracting multiple overlapping concepts from one sentence
            matched = False
            for pattern in _PREREQUISITE_INDICATORS:
                if matched:
                    break
                match = pattern.search(point.content)
                if match:
                    matched = True
                    # Extract the referenced concept from context around match
                    prereq_concept = self._extract_prerequisite_concept(
                        point.content, match
                    )
                    if not prereq_concept:
                        continue

                    # Check if this prerequisite is already covered as a
                    # topic in non-prerequisite knowledge points
                    prereq_lower = prereq_concept.lower()
                    if prereq_lower in covered_content:
                        continue

                    # Avoid duplicates
                    if prereq_lower in seen_prerequisites:
                        continue
                    seen_prerequisites.add(prereq_lower)

                    # Create a minimal prerequisite knowledge point
                    prereq_point = KnowledgePoint(
                        id=self._generate_point_id(),
                        content=(
                            f"Prerequisite concept: {prereq_concept}. "
                            f"Required for understanding related topics in "
                            f"the source material."
                        ),
                        category="concept",
                        source_url=point.source_url,
                        source_title=f"Prerequisite for: {point.source_title}",
                        depth=point.depth,
                        is_prerequisite=True,
                    )
                    prerequisite_points.append(prereq_point)

        return prerequisite_points

    def _extract_prerequisite_concept(
        self, text: str, match: re.Match[str]
    ) -> str | None:
        """Extract the prerequisite concept name from surrounding context.

        Looks at the text following the prerequisite indicator to find
        the referenced concept or technology name.

        Args:
            text: The full paragraph text.
            match: The regex match for the prerequisite indicator.

        Returns:
            The extracted concept name, or None if extraction fails.
        """
        # Get text after the match
        after_match = text[match.end():].strip()

        # Try to extract a meaningful noun phrase (up to 5 words),
        # stopping at sentence boundaries, commas, and conjunctions
        words = after_match.split()
        if not words:
            return None

        stop_words = {"and", "or", "for", "to", "in", "is", "are", "was", "were",
                      "that", "which", "with", "from", "by", "as", "on", "at"}

        concept_words: list[str] = []
        for word in words[:5]:
            # Stop at punctuation boundaries
            if word.endswith((".", "!", "?", ";", ",")):
                cleaned = word.rstrip(".!?;,")
                if cleaned and cleaned.lower() not in stop_words:
                    concept_words.append(cleaned)
                break
            # Stop at conjunctions/prepositions (but keep first word always)
            if concept_words and word.lower() in stop_words:
                break
            concept_words.append(word)

        concept = " ".join(concept_words).strip()

        # Filter out very short or generic concepts
        if len(concept) < 3 or concept.lower() in ("the", "a", "an", "this", "that"):
            return None

        return concept

    def _build_stats(self) -> dict:
        """Build extraction statistics.

        Returns:
            Dictionary with counts by depth, domain, and category.
        """
        stats: dict[str, dict[str, int]] = {
            "by_depth": {},
            "by_category": {},
            "totals": {
                "documents": len(self._documents),
                "knowledge_points": len(self._all_knowledge_points),
                "errors": 0,  # Will be populated from scraper error_log
            },
        }

        for point in self._all_knowledge_points:
            depth_key = f"depth_{point.depth}"
            stats["by_depth"][depth_key] = stats["by_depth"].get(depth_key, 0) + 1

            stats["by_category"][point.category] = (
                stats["by_category"].get(point.category, 0) + 1
            )

        return stats

    def _write_artifact(self, result: ExtractionResult) -> None:
        """Write the ExtractionResult to the artifacts directory.

        Creates the artifacts directory if it doesn't exist.
        Writes the result as JSON to phase01_extraction.json.
        """
        artifacts_path = Path(self._config.artifacts_dir)
        artifacts_path.mkdir(parents=True, exist_ok=True)

        output_path = artifacts_path / ARTIFACT_FILENAMES["phase01"]
        output_path.write_text(
            result.model_dump_json(indent=2),
            encoding="utf-8",
        )
