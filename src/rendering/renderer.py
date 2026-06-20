"""Site Renderer: transforms pipeline artifacts into MkDocs-compatible Markdown.

Loads all phase artifacts from the artifacts/ directory, renders Jinja2 templates
into Markdown files in docs/, generates cross-domain content (Mermaid diagrams,
integrative summaries, related topics), and dynamically produces the mkdocs.yml
nav structure.

Satisfies Requirements: 12.1, 12.2, 12.3, 12.4, 12.5, 13.8
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Optional

import yaml
from jinja2 import Environment, FileSystemLoader

from src.config import (
    ARTIFACT_FILENAMES,
    ARTIFACTS_DIR,
    DOCS_DIR,
    DOMAIN_BY_ID,
    EXAM_DOMAINS,
)
from src.models.curriculum import Curriculum
from src.models.gap_analysis import GapReport
from src.models.mock_exam import MockExam
from src.models.questions import QuestionBank
from src.models.readiness import ReadinessAssessment
from src.models.revision import RevisionPackage
from src.models.scoring import ScoredTopicList
from src.models.study_notes import StudyNotesCollection


@dataclass
class PipelineArtifacts:
    """Container holding all loaded pipeline phase artifacts."""

    scores: Optional[ScoredTopicList] = None
    study_notes: Optional[StudyNotesCollection] = None
    curriculum: Optional[Curriculum] = None
    revision: Optional[RevisionPackage] = None
    questions: Optional[QuestionBank] = None
    mock_exam: Optional[MockExam] = None
    gap_report: Optional[GapReport] = None
    readiness: Optional[ReadinessAssessment] = None
    # Raw JSON data for phases that may not have Pydantic models loaded
    raw: dict[str, Any] = field(default_factory=dict)


class SiteRenderer:
    """Renders all pipeline artifacts into MkDocs Markdown pages.

    Loads Jinja2 templates, renders each phase artifact, generates cross-domain
    content (Mermaid diagrams, integrative summaries), and produces the mkdocs.yml
    nav structure dynamically.
    """

    def __init__(self, template_dir: Path, output_dir: Path) -> None:
        """Initialize the renderer.

        Args:
            template_dir: Path to the Jinja2 templates directory.
            output_dir: Path to the docs/ output directory.
        """
        self.template_dir = template_dir
        self.output_dir = output_dir
        self.env = Environment(
            loader=FileSystemLoader(str(template_dir)),
            autoescape=False,
            keep_trailing_newline=True,
        )

    def render_all(self, artifacts: PipelineArtifacts) -> None:
        """Render all artifacts into Markdown files and generate mkdocs.yml nav.

        Args:
            artifacts: Container with all loaded pipeline artifacts.
        """
        self.output_dir.mkdir(parents=True, exist_ok=True)

        self._render_landing_page(artifacts)

        if artifacts.study_notes:
            self._render_study_notes(artifacts.study_notes)

        if artifacts.curriculum:
            self._render_curriculum(artifacts.curriculum)

        if artifacts.revision:
            self._render_revision(artifacts.revision)

        if artifacts.questions:
            self._render_questions(artifacts.questions)

        if artifacts.mock_exam:
            self._render_mock_exam(artifacts.mock_exam)

        if artifacts.gap_report:
            self._render_gap_report(artifacts.gap_report)

        if artifacts.readiness:
            self._render_readiness(artifacts.readiness)

        # Generate cross-domain content (Req 12.1, 12.2, 12.3, 12.4)
        self._render_cross_domain_content(artifacts)

        # Dynamically generate mkdocs.yml nav
        nav = self._generate_mkdocs_nav(artifacts)
        self._write_mkdocs_nav(nav)

    def _render_landing_page(self, artifacts: PipelineArtifacts) -> None:
        """Render the landing/index page with exam overview and quick links."""
        template = self.env.get_template("landing.md.j2")

        # Build domain progress data for the landing page
        domains_data = []
        scores = artifacts.scores
        notes = artifacts.study_notes

        for domain in EXAM_DOMAINS:
            domain_topics_total = 0
            domain_topics_covered = 0
            domain_high_priority = 0

            if scores:
                for topic in scores.topics:
                    if domain.id in topic.domain_ids:
                        domain_topics_total += 1
                        if topic.is_high_priority:
                            domain_high_priority += 1

            if notes:
                note_topic_ids = {n.topic_id for n in notes.notes}
                if scores:
                    for topic in scores.topics:
                        if domain.id in topic.domain_ids and topic.topic_id in note_topic_ids:
                            domain_topics_covered += 1

            domains_data.append({
                "name": domain.name,
                "weight_min": int(domain.weight_min * 100),
                "weight_max": int(domain.weight_max * 100),
                "total": domain_topics_total,
                "covered": domain_topics_covered,
                "high_priority": domain_high_priority,
                "completion_pct": (
                    round(domain_topics_covered / domain_topics_total * 100)
                    if domain_topics_total > 0
                    else 0
                ),
            })

        total_topics = sum(d["total"] for d in domains_data)
        high_priority_count = sum(d["high_priority"] for d in domains_data)
        total_study_time_hours = (
            round(artifacts.curriculum.total_time_minutes / 60, 1)
            if artifacts.curriculum
            else 0
        )
        readiness_score = artifacts.readiness.readiness_score if artifacts.readiness else 0

        content = template.render(
            domains=domains_data,
            total_topics=total_topics,
            high_priority_count=high_priority_count,
            total_study_time_hours=total_study_time_hours,
            readiness_score=readiness_score,
        )
        self._write_file("index.md", content)

    def _render_study_notes(self, notes: StudyNotesCollection) -> None:
        """Render study notes for all topics."""
        template = self.env.get_template("study_notes.md.j2")

        # Convert Pydantic models to dicts for template rendering
        notes_data = [note.model_dump() for note in notes.notes]

        content = template.render(
            notes=notes_data,
            cross_domain_themes=notes.cross_domain_themes,
        )
        self._write_file("study_notes.md", content)

    def _render_curriculum(self, curriculum: Curriculum) -> None:
        """Render the curriculum/learning path."""
        template = self.env.get_template("curriculum.md.j2")

        modules_data = [m.model_dump() for m in curriculum.modules]

        content = template.render(
            modules=modules_data,
            total_time_minutes=curriculum.total_time_minutes,
            learning_path=curriculum.learning_path,
        )
        self._write_file("curriculum.md", content)

    def _render_revision(self, revision: RevisionPackage) -> None:
        """Render revision resources (summary, cheat sheets, flashcards, mnemonics)."""
        template = self.env.get_template("revision.md.j2")

        content = template.render(
            executive_summary=revision.executive_summary,
            cheat_sheets=[cs.model_dump() for cs in revision.cheat_sheets],
            flashcards=[fc.model_dump() for fc in revision.flashcards],
            mnemonics=[m.model_dump() for m in revision.mnemonics],
        )
        self._write_file("revision.md", content)

    def _render_questions(self, bank: QuestionBank) -> None:
        """Render practice questions at all difficulty levels."""
        template = self.env.get_template("questions.md.j2")

        content = template.render(
            easy=[q.model_dump() for q in bank.easy],
            intermediate=[q.model_dump() for q in bank.intermediate],
            advanced=[q.model_dump() for q in bank.advanced],
            domain_distribution=bank.domain_distribution,
        )
        self._write_file("questions.md", content)

    def _render_mock_exam(self, exam: MockExam) -> None:
        """Render the mock exam with questions, answer key, and solutions."""
        template = self.env.get_template("mock_exam.md.j2")

        content = template.render(
            questions=[q.model_dump() for q in exam.questions],
            answer_key=exam.answer_key,
            solutions=exam.solutions,
            grading_rubric=exam.grading_rubric.model_dump(),
            time_limit_minutes=exam.time_limit_minutes,
            domain_distribution=exam.domain_distribution,
            format_distribution=exam.format_distribution,
        )
        self._write_file("mock_exam.md", content)

    def _render_gap_report(self, report: GapReport) -> None:
        """Render the gap analysis report."""
        template = self.env.get_template("gap_report.md.j2")

        content = template.render(
            coverage_items=report.coverage_items,
            critical_gaps=[g.model_dump() for g in report.critical_gaps],
            weak_gaps=[g.model_dump() for g in report.weak_gaps],
            not_covered_gaps=[g.model_dump() for g in report.not_covered_gaps],
            total_objectives=report.total_objectives,
            fully_covered_count=report.fully_covered_count,
            weakly_covered_count=report.weakly_covered_count,
            not_covered_count=report.not_covered_count,
        )
        self._write_file("gap_report.md", content)

    def _render_readiness(self, assessment: ReadinessAssessment) -> None:
        """Render the readiness assessment."""
        template = self.env.get_template("readiness.md.j2")

        content = template.render(
            readiness_score=assessment.readiness_score,
            score_components=assessment.score_components,
            recommendation=assessment.recommendation,
            high_risk_topics=[t.model_dump() for t in assessment.high_risk_topics],
            last_minute_areas=assessment.last_minute_areas,
            study_plan_24h=[b.model_dump() for b in assessment.study_plan_24h],
            remediation_plan=(
                assessment.remediation_plan.model_dump()
                if assessment.remediation_plan
                else None
            ),
        )
        self._write_file("readiness.md", content)

    def _render_cross_domain_content(self, artifacts: PipelineArtifacts) -> None:
        """Generate cross-domain pages: Mermaid diagram and integrative summaries.

        Satisfies:
        - Req 12.1: Cross-reference links between domains for concepts in 2+ domains
        - Req 12.2: Mermaid relationship diagram (Priority_Score ≥ 7, 2+ domains)
        - Req 12.3: Related Topics section (1-10 entries) already in study_notes template
        - Req 12.4: Integrative summary for themes spanning 3+ domains
        - Req 12.5: Omit Related Topics for topics without connections (template logic)
        """
        lines: list[str] = ["# Cross-Domain Connections\n"]

        # --- Mermaid Relationship Diagram (Req 12.2) ---
        lines.append("## Relationship Diagram\n")
        lines.append(
            "The following diagram shows how high-priority concepts "
            "(Priority_Score ≥ 7) relate across exam domains.\n"
        )

        mermaid_lines = self._generate_mermaid_diagram(artifacts)
        lines.append("```mermaid")
        lines.extend(mermaid_lines)
        lines.append("```\n")

        # --- Cross-Reference Links (Req 12.1) ---
        lines.append("## Cross-Domain Concepts\n")
        lines.append(
            "Concepts that appear in multiple exam domains with links to "
            "their coverage in each domain.\n"
        )

        cross_domain_concepts = self._get_cross_domain_concepts(artifacts)
        if cross_domain_concepts:
            lines.append("| Concept | Domains | Priority Score |")
            lines.append("|---------|---------|---------------|")
            for concept in cross_domain_concepts:
                domain_links = ", ".join(
                    f"[{DOMAIN_BY_ID[d].name}](study_notes.md"
                    f"#{concept['name'].lower().replace(' ', '-')})"
                    for d in concept["domain_ids"]
                    if d in DOMAIN_BY_ID
                )
                lines.append(
                    f"| [{concept['name']}](study_notes.md"
                    f"#{concept['name'].lower().replace(' ', '-')}) "
                    f"| {domain_links} | {concept['score']}/10 |"
                )
            lines.append("")
        else:
            lines.append("No cross-domain concepts identified.\n")

        # --- Integrative Summaries (Req 12.4) ---
        themes_3plus = self._get_themes_spanning_3_domains(artifacts)
        if themes_3plus:
            lines.append("## Integrative Themes\n")
            lines.append(
                "Themes that span 3 or more exam domains, showing how "
                "concepts integrate across the certification scope.\n"
            )
            for theme in themes_3plus:
                lines.append(f"### {theme['theme']}\n")
                lines.append(f"**Domains**: {', '.join(theme['domains'])}\n")
                if theme.get("manifestations"):
                    for manifestation in theme["manifestations"]:
                        lines.append(f"- {manifestation}")
                lines.append("")

        content = "\n".join(lines)
        self._write_file("cross_domain.md", content)

    def _generate_mermaid_diagram(self, artifacts: PipelineArtifacts) -> list[str]:
        """Generate Mermaid graph lines for concepts with score ≥ 7 in 2+ domains.

        Returns:
            List of Mermaid syntax lines (without the fences).
        """
        lines: list[str] = ["graph LR"]

        if not artifacts.scores:
            lines.append("    NoData[No scoring data available]")
            return lines

        # Find concepts with Priority_Score >= 7 and domain_count >= 2
        qualifying_topics = [
            t for t in artifacts.scores.topics
            if t.priority_score >= 7 and t.domain_count >= 2
        ]

        if not qualifying_topics:
            lines.append("    NoTopics[No cross-domain high-priority concepts found]")
            return lines

        # Create domain subgraphs and connections
        domain_topics: dict[str, list[str]] = {}
        for topic in qualifying_topics:
            for domain_id in topic.domain_ids:
                domain_topics.setdefault(domain_id, []).append(topic.topic_id)

        # Create subgraphs for each domain that has qualifying topics
        for domain_id, topic_ids in sorted(domain_topics.items()):
            domain_name = DOMAIN_BY_ID[domain_id].name if domain_id in DOMAIN_BY_ID else domain_id
            safe_domain_id = domain_id.replace("-", "_")
            lines.append(f"    subgraph {safe_domain_id}[{domain_name}]")
            for tid in sorted(set(topic_ids)):
                # Find topic name
                topic = next(
                    (t for t in qualifying_topics if t.topic_id == tid), None
                )
                if topic:
                    safe_tid = tid.replace("-", "_").replace(" ", "_")
                    lines.append(f"        {safe_tid}[{topic.topic_name}]")
            lines.append("    end")

        # Create edges for topics that span multiple domains
        for topic in qualifying_topics:
            if len(topic.domain_ids) >= 2:
                safe_tid = topic.topic_id.replace("-", "_").replace(" ", "_")
                # Connect the topic node to itself across domains
                # (it appears in multiple subgraphs conceptually, but Mermaid
                # needs explicit links between domain groups)
                for i in range(len(topic.domain_ids) - 1):
                    d1 = topic.domain_ids[i].replace("-", "_")
                    d2 = topic.domain_ids[i + 1].replace("-", "_")
                    lines.append(
                        f"    {safe_tid} -.- |spans| {d1} & {d2}"
                    )
                    break  # One connection line per topic is sufficient

        return lines

    def _get_cross_domain_concepts(
        self, artifacts: PipelineArtifacts
    ) -> list[dict[str, Any]]:
        """Get concepts that appear in 2+ domains for cross-reference links.

        Returns:
            List of dicts with name, domain_ids, and score.
        """
        if not artifacts.scores:
            return []

        return [
            {
                "name": t.topic_name,
                "topic_id": t.topic_id,
                "domain_ids": t.domain_ids,
                "score": t.priority_score,
            }
            for t in artifacts.scores.topics
            if t.domain_count >= 2
        ]

    def _get_themes_spanning_3_domains(
        self, artifacts: PipelineArtifacts
    ) -> list[dict[str, Any]]:
        """Identify themes spanning 3+ domains for integrative summaries (Req 12.4).

        Uses cross_domain_themes from study notes if available, otherwise
        derives from scoring data.

        Returns:
            List of theme dicts with theme, domains, and manifestations.
        """
        themes: list[dict[str, Any]] = []

        # First use cross_domain_themes from study notes (preferred source)
        if artifacts.study_notes and artifacts.study_notes.cross_domain_themes:
            for theme in artifacts.study_notes.cross_domain_themes:
                if len(theme.get("domains", [])) >= 3:
                    themes.append(theme)

        # If no themes from study notes, derive from scoring data
        if not themes and artifacts.scores:
            for topic in artifacts.scores.topics:
                if topic.domain_count >= 3:
                    domain_names = [
                        DOMAIN_BY_ID[d].name
                        for d in topic.domain_ids
                        if d in DOMAIN_BY_ID
                    ]
                    themes.append({
                        "theme": topic.topic_name,
                        "domains": domain_names,
                        "manifestations": [
                            f"Appears in {d} as a core concept"
                            for d in domain_names
                        ],
                    })

        return themes

    def _generate_mkdocs_nav(self, artifacts: PipelineArtifacts) -> list[Any]:
        """Dynamically generate the mkdocs.yml nav structure from artifacts.

        Returns:
            Nav list structure for mkdocs.yml.
        """
        nav: list[Any] = [{"Home": "index.md"}]

        if artifacts.study_notes:
            nav.append({"Study Notes": "study_notes.md"})

        if artifacts.curriculum:
            nav.append({"Curriculum": "curriculum.md"})

        if artifacts.revision:
            nav.append({"Revision Resources": "revision.md"})

        if artifacts.questions:
            nav.append({"Practice Questions": "questions.md"})

        if artifacts.mock_exam:
            nav.append({"Mock Exam": "mock_exam.md"})

        if artifacts.gap_report:
            nav.append({"Gap Analysis": "gap_report.md"})

        if artifacts.readiness:
            nav.append({"Readiness Assessment": "readiness.md"})

        # Cross-domain page is always generated when scores are available
        if artifacts.scores:
            nav.append({"Cross-Domain Connections": "cross_domain.md"})

        return nav

    def _write_mkdocs_nav(self, nav: list[Any]) -> None:
        """Update the mkdocs.yml file with the dynamically generated nav.

        Uses text-based replacement to update the nav section while preserving
        the rest of the file (including !!python/name tags that safe_load
        cannot handle).
        """
        mkdocs_path = self.output_dir.parent / "mkdocs.yml"
        if not mkdocs_path.exists():
            # If mkdocs.yml doesn't exist, we can't update it
            return

        with open(mkdocs_path, "r", encoding="utf-8") as f:
            lines = f.readlines()

        # Find the nav section and replace it
        nav_start = None
        nav_end = None
        for i, line in enumerate(lines):
            if line.rstrip() == "nav:":
                nav_start = i
            elif nav_start is not None and nav_end is None:
                # Nav ends when we hit a non-indented, non-empty line
                stripped = line.rstrip()
                if stripped and not stripped.startswith(" ") and not stripped.startswith("-"):
                    nav_end = i
                    break

        if nav_start is None:
            # No nav section found; append one
            lines.append("\nnav:\n")
            nav_start = len(lines) - 1
            nav_end = len(lines)

        if nav_end is None:
            nav_end = len(lines)

        # Generate new nav YAML
        nav_yaml = yaml.dump(
            {"nav": nav},
            default_flow_style=False,
            allow_unicode=True,
            sort_keys=False,
        )
        # Extract just the nav lines (skip the "nav:" header since we keep
        # the original line)
        nav_content_lines = nav_yaml.split("\n")
        # nav_content_lines[0] is "nav:", rest are the entries
        new_nav_lines = [line + "\n" for line in nav_content_lines if line]

        # Replace the nav section
        lines[nav_start:nav_end] = new_nav_lines

        with open(mkdocs_path, "w", encoding="utf-8") as f:
            f.writelines(lines)

    def _write_file(self, filename: str, content: str) -> None:
        """Write content to a file in the output directory.

        Args:
            filename: Relative path within the output directory.
            content: File content to write.
        """
        filepath = self.output_dir / filename
        filepath.parent.mkdir(parents=True, exist_ok=True)
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)


def load_artifacts(artifacts_dir: Path) -> PipelineArtifacts:
    """Load all available pipeline artifacts from the artifacts directory.

    Loads each phase artifact JSON file if it exists, parsing into the
    corresponding Pydantic model. Missing artifacts are left as None.

    Args:
        artifacts_dir: Path to the artifacts/ directory.

    Returns:
        PipelineArtifacts container with all available data loaded.
    """
    artifacts = PipelineArtifacts()

    # Map of phase key -> (filename, model_class, attribute_name)
    phase_mapping: list[tuple[str, type, str]] = [
        ("phase03", ScoredTopicList, "scores"),
        ("phase04", StudyNotesCollection, "study_notes"),
        ("phase05", Curriculum, "curriculum"),
        ("phase06", RevisionPackage, "revision"),
        ("phase07", QuestionBank, "questions"),
        ("phase08", MockExam, "mock_exam"),
        ("phase09", GapReport, "gap_report"),
        ("phase10", ReadinessAssessment, "readiness"),
    ]

    for phase_key, model_class, attr_name in phase_mapping:
        filename = ARTIFACT_FILENAMES.get(phase_key)
        if not filename:
            continue

        filepath = artifacts_dir / filename
        if not filepath.exists():
            continue

        try:
            with open(filepath, "r", encoding="utf-8") as f:
                data = json.load(f)
            model_instance = model_class.model_validate(data)
            setattr(artifacts, attr_name, model_instance)
            artifacts.raw[phase_key] = data
        except (json.JSONDecodeError, ValueError) as e:
            # Log error but continue with other artifacts
            print(f"Warning: Failed to load {filepath}: {e}")

    return artifacts


def render_site(
    artifacts_dir: Optional[Path] = None,
    template_dir: Optional[Path] = None,
    output_dir: Optional[Path] = None,
) -> None:
    """High-level entry point: load artifacts and render the complete site.

    Args:
        artifacts_dir: Path to artifacts/ directory. Defaults to ARTIFACTS_DIR.
        template_dir: Path to Jinja2 templates. Defaults to src/rendering/templates/.
        output_dir: Path to docs/ output. Defaults to DOCS_DIR.
    """
    if artifacts_dir is None:
        artifacts_dir = Path(ARTIFACTS_DIR)
    if template_dir is None:
        template_dir = Path("src/rendering/templates")
    if output_dir is None:
        output_dir = Path(DOCS_DIR)

    artifacts = load_artifacts(artifacts_dir)
    renderer = SiteRenderer(template_dir=template_dir, output_dir=output_dir)
    renderer.render_all(artifacts)
