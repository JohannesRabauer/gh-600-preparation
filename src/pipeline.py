"""Pipeline orchestrator for the GH-600 Exam Prep Generator.

Manages execution of all 10 pipeline phases in DAG order, handles
failures gracefully, logs errors, and produces an execution report
with per-phase metrics.

Exit codes:
    0 - All phases completed successfully.
    1 - Partial success: some phases had warnings or non-critical failures.
    2 - Failure: critical phases failed, output is incomplete.
"""

from __future__ import annotations

import asyncio
import json
import logging
import sys
import time
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Any

from src.config import ARTIFACTS_DIR, ARTIFACT_FILENAMES, EXAM_DOMAINS, SOURCE_URLS
from src.utils.logging import clear_error_log, get_pipeline_logger, log_phase_event


# === DAG Definition ===

# Each phase maps to the phases that must complete before it can run.
PHASE_DEPENDENCIES: dict[str, list[str]] = {
    "phase01": [],
    "phase02": ["phase01"],
    "phase03": ["phase02"],
    "phase04": ["phase03"],
    "phase05": ["phase03"],
    "phase06": ["phase04"],
    "phase07": ["phase04"],
    "phase08": ["phase07"],
    "phase09": ["phase03"],
    "phase10": ["phase09"],
}

PHASE_NAMES: dict[str, str] = {
    "phase01": "Knowledge Extractor",
    "phase02": "Topic Mapper",
    "phase03": "Relevance Analyzer",
    "phase04": "Study Notes Generator",
    "phase05": "Curriculum Builder",
    "phase06": "Revision Generator",
    "phase07": "Question Generator",
    "phase08": "Mock Exam Builder",
    "phase09": "Gap Analyzer",
    "phase10": "Readiness Assessor",
}


class PhaseStatus(str, Enum):
    """Status of a pipeline phase execution."""

    PENDING = "pending"
    RUNNING = "running"
    SUCCESS = "success"
    FAILED = "failed"
    SKIPPED = "skipped"


@dataclass
class PhaseResult:
    """Result of executing a single pipeline phase."""

    phase_id: str
    status: PhaseStatus
    duration_seconds: float = 0.0
    error: str | None = None
    artifact_path: str | None = None


@dataclass
class PipelineReport:
    """Execution report for the full pipeline run."""

    phases: list[PhaseResult] = field(default_factory=list)
    total_duration_seconds: float = 0.0
    exit_code: int = 0
    summary: str = ""

    def to_dict(self) -> dict[str, Any]:
        """Convert the report to a JSON-serializable dictionary."""
        return {
            "total_duration_seconds": round(self.total_duration_seconds, 2),
            "exit_code": self.exit_code,
            "summary": self.summary,
            "phases": [
                {
                    "phase_id": r.phase_id,
                    "name": PHASE_NAMES.get(r.phase_id, r.phase_id),
                    "status": r.status.value,
                    "duration_seconds": round(r.duration_seconds, 2),
                    "error": r.error,
                    "artifact_path": r.artifact_path,
                }
                for r in self.phases
            ],
        }


# === Phase Execution Functions ===


async def _run_phase01() -> None:
    """Execute Phase 1: Knowledge Extractor."""
    from src.phases.phase01_extractor import KnowledgeExtractor

    extractor = KnowledgeExtractor()
    await extractor.extract(SOURCE_URLS)


def _run_phase02() -> None:
    """Execute Phase 2: Topic Mapper."""
    from src.phases.phase02_mapper import TopicMapper

    TopicMapper.from_artifact()


def _run_phase03() -> None:
    """Execute Phase 3: Relevance Analyzer."""
    from src.phases.phase03_analyzer import RelevanceAnalyzer

    RelevanceAnalyzer.from_artifact()


def _run_phase04() -> None:
    """Execute Phase 4: Study Notes Generator."""
    from src.phases.phase04_notes import StudyNotesGenerator

    StudyNotesGenerator.from_artifacts()


def _run_phase05() -> None:
    """Execute Phase 5: Curriculum Builder."""
    from src.phases.phase05_curriculum import CurriculumBuilder

    CurriculumBuilder.from_artifacts()


def _run_phase06() -> None:
    """Execute Phase 6: Revision Generator."""
    from src.phases.phase06_revision import RevisionGenerator

    RevisionGenerator.from_artifacts()


def _run_phase07() -> None:
    """Execute Phase 7: Question Generator."""
    from src.phases.phase07_questions import QuestionGenerator

    QuestionGenerator.from_artifacts()


def _run_phase08() -> None:
    """Execute Phase 8: Mock Exam Builder."""
    from src.phases.phase08_mock_exam import MockExamBuilder

    MockExamBuilder.from_artifacts()


def _run_phase09() -> None:
    """Execute Phase 9: Gap Analyzer."""
    from src.models.scoring import ExamObjective
    from src.phases.phase09_gap import GapAnalyzer

    # Build exam objectives from domain sub-topics
    objectives: list[ExamObjective] = []
    for domain in EXAM_DOMAINS:
        for i, sub_topic in enumerate(domain.sub_topics, start=1):
            objectives.append(
                ExamObjective(
                    id=f"{domain.id}-obj-{i:02d}",
                    domain_id=domain.id,
                    description=sub_topic,
                    sub_bullets=[],
                )
            )

    GapAnalyzer.from_artifacts(objectives)


def _run_phase10() -> None:
    """Execute Phase 10: Readiness Assessor."""
    from src.phases.phase10_readiness import ReadinessAssessor

    ReadinessAssessor.from_artifacts()


# Registry of phase runners. Async runners are wrapped during execution.
_PHASE_RUNNERS: dict[str, Any] = {
    "phase01": _run_phase01,
    "phase02": _run_phase02,
    "phase03": _run_phase03,
    "phase04": _run_phase04,
    "phase05": _run_phase05,
    "phase06": _run_phase06,
    "phase07": _run_phase07,
    "phase08": _run_phase08,
    "phase09": _run_phase09,
    "phase10": _run_phase10,
}


# === Orchestrator ===


def _topological_order(
    phases: list[str], dependencies: dict[str, list[str]]
) -> list[str]:
    """Compute a valid execution order for the requested phases.

    Uses Kahn's algorithm to produce a topological ordering that
    respects the DAG dependencies.

    Args:
        phases: List of phase IDs to include.
        dependencies: Full dependency map.

    Returns:
        Ordered list of phase IDs respecting dependencies.
    """
    # Filter dependencies to only include requested phases
    phase_set = set(phases)
    in_degree: dict[str, int] = {p: 0 for p in phases}
    adj: dict[str, list[str]] = {p: [] for p in phases}

    for phase in phases:
        for dep in dependencies.get(phase, []):
            if dep in phase_set:
                in_degree[phase] += 1
                adj[dep].append(phase)

    # Kahn's algorithm
    queue: list[str] = [p for p in phases if in_degree[p] == 0]
    order: list[str] = []

    while queue:
        # Sort for deterministic ordering
        queue.sort()
        node = queue.pop(0)
        order.append(node)

        for neighbor in adj[node]:
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)

    return order


def _can_run_phase(
    phase_id: str,
    results: dict[str, PhaseResult],
    dependencies: dict[str, list[str]],
    phases_to_run: set[str],
) -> bool:
    """Check whether a phase's dependencies are all satisfied.

    A dependency is satisfied if it completed successfully or if it
    was not included in the current run (its artifact already exists).

    Args:
        phase_id: The phase to check.
        results: Current execution results.
        dependencies: Full dependency map.
        phases_to_run: Set of phases included in this run.

    Returns:
        True if the phase can execute.
    """
    for dep in dependencies.get(phase_id, []):
        if dep in phases_to_run:
            # Dependency was part of this run — must have succeeded
            dep_result = results.get(dep)
            if not dep_result or dep_result.status != PhaseStatus.SUCCESS:
                return False
        else:
            # Dependency not in current run — check artifact exists
            artifact_file = ARTIFACT_FILENAMES.get(dep)
            if artifact_file:
                artifact_path = Path(ARTIFACTS_DIR) / artifact_file
                if not artifact_path.exists():
                    return False
    return True


async def run_pipeline(
    phases: list[str] | None = None,
) -> PipelineReport:
    """Execute the pipeline phases in DAG order.

    Runs the specified phases (or all 10 if not specified) in
    topological order. On failure, logs the error, skips dependent
    phases, and continues with independent phases where possible.

    Args:
        phases: Optional list of phase IDs to run.
            Defaults to all 10 phases.

    Returns:
        A PipelineReport with per-phase results and exit code.
    """
    logger = get_pipeline_logger()
    clear_error_log()

    all_phases = list(PHASE_DEPENDENCIES.keys())
    phases_to_run = phases if phases else all_phases

    # Validate requested phases
    invalid = [p for p in phases_to_run if p not in PHASE_DEPENDENCIES]
    if invalid:
        log_phase_event(
            logger, logging.ERROR, "orchestrator",
            f"Unknown phases requested: {invalid}",
        )
        return PipelineReport(
            exit_code=2,
            summary=f"Invalid phase IDs: {invalid}",
        )

    # Compute execution order
    execution_order = _topological_order(phases_to_run, PHASE_DEPENDENCIES)
    phases_set = set(phases_to_run)

    log_phase_event(
        logger, logging.INFO, "orchestrator",
        f"Starting pipeline with {len(execution_order)} phases: "
        f"{', '.join(execution_order)}",
    )

    report = PipelineReport()
    results: dict[str, PhaseResult] = {}
    pipeline_start = time.perf_counter()

    for phase_id in execution_order:
        phase_name = PHASE_NAMES.get(phase_id, phase_id)

        # Check if dependencies are satisfied
        if not _can_run_phase(phase_id, results, PHASE_DEPENDENCIES, phases_set):
            log_phase_event(
                logger, logging.WARNING, phase_id,
                f"Skipping {phase_name}: dependency not satisfied",
            )
            result = PhaseResult(
                phase_id=phase_id,
                status=PhaseStatus.SKIPPED,
                error="Dependency not satisfied",
            )
            results[phase_id] = result
            report.phases.append(result)
            continue

        # Execute the phase
        log_phase_event(
            logger, logging.INFO, phase_id,
            f"Starting {phase_name}...",
        )

        runner = _PHASE_RUNNERS[phase_id]
        phase_start = time.perf_counter()

        try:
            if asyncio.iscoroutinefunction(runner):
                await runner()
            else:
                runner()

            duration = time.perf_counter() - phase_start
            artifact_file = ARTIFACT_FILENAMES.get(phase_id)
            artifact_path = (
                str(Path(ARTIFACTS_DIR) / artifact_file)
                if artifact_file
                else None
            )

            result = PhaseResult(
                phase_id=phase_id,
                status=PhaseStatus.SUCCESS,
                duration_seconds=duration,
                artifact_path=artifact_path,
            )
            log_phase_event(
                logger, logging.INFO, phase_id,
                f"Completed {phase_name} in {duration:.2f}s",
            )

        except Exception as exc:  # noqa: BLE001
            duration = time.perf_counter() - phase_start
            error_msg = f"{type(exc).__name__}: {exc}"

            result = PhaseResult(
                phase_id=phase_id,
                status=PhaseStatus.FAILED,
                duration_seconds=duration,
                error=error_msg,
            )
            log_phase_event(
                logger, logging.ERROR, phase_id,
                f"Failed {phase_name}: {error_msg}",
                exc_info=exc,
            )

        results[phase_id] = result
        report.phases.append(result)

    # Calculate totals and exit code
    report.total_duration_seconds = time.perf_counter() - pipeline_start

    success_count = sum(
        1 for r in report.phases if r.status == PhaseStatus.SUCCESS
    )
    failed_count = sum(
        1 for r in report.phases if r.status == PhaseStatus.FAILED
    )
    skipped_count = sum(
        1 for r in report.phases if r.status == PhaseStatus.SKIPPED
    )

    if failed_count == 0 and skipped_count == 0:
        report.exit_code = 0
        report.summary = (
            f"All {success_count} phases completed successfully "
            f"in {report.total_duration_seconds:.1f}s"
        )
    elif success_count > 0:
        report.exit_code = 1
        report.summary = (
            f"Partial success: {success_count} succeeded, "
            f"{failed_count} failed, {skipped_count} skipped "
            f"in {report.total_duration_seconds:.1f}s"
        )
    else:
        report.exit_code = 2
        report.summary = (
            f"Pipeline failed: {failed_count} failed, "
            f"{skipped_count} skipped "
            f"in {report.total_duration_seconds:.1f}s"
        )

    log_phase_event(
        logger, logging.INFO, "orchestrator",
        report.summary,
    )

    # Write execution report artifact
    _write_report(report)

    return report


def _write_report(report: PipelineReport) -> None:
    """Write the pipeline execution report to artifacts."""
    artifacts_path = Path(ARTIFACTS_DIR)
    artifacts_path.mkdir(parents=True, exist_ok=True)
    report_path = artifacts_path / "pipeline_report.json"
    report_path.write_text(
        json.dumps(report.to_dict(), indent=2),
        encoding="utf-8",
    )


def _render_and_build(logger: logging.Logger) -> int:
    """Render Markdown from artifacts and run MkDocs build.

    Returns:
        0 on success, 1 if rendering succeeds but MkDocs build fails.
    """
    import subprocess

    from src.rendering.renderer import render_site

    log_phase_event(logger, logging.INFO, "renderer", "Rendering site from artifacts...")

    try:
        render_site()
        log_phase_event(logger, logging.INFO, "renderer", "Site rendered to docs/")
    except Exception as exc:  # noqa: BLE001
        log_phase_event(
            logger, logging.ERROR, "renderer",
            f"Rendering failed: {type(exc).__name__}: {exc}",
            exc_info=exc,
        )
        return 1

    # Run MkDocs build to produce the static site
    log_phase_event(logger, logging.INFO, "mkdocs", "Running mkdocs build...")
    try:
        # Try 'mkdocs' on PATH first, fall back to 'python -m mkdocs'
        mkdocs_cmd = ["mkdocs", "build"]
        try:
            result = subprocess.run(
                mkdocs_cmd,
                capture_output=True,
                text=True,
                timeout=120,
            )
        except FileNotFoundError:
            mkdocs_cmd = [sys.executable, "-m", "mkdocs", "build"]
            result = subprocess.run(
                mkdocs_cmd,
                capture_output=True,
                text=True,
                timeout=120,
            )

        if result.returncode == 0:
            log_phase_event(logger, logging.INFO, "mkdocs", "MkDocs build succeeded")
        else:
            log_phase_event(
                logger, logging.WARNING, "mkdocs",
                f"MkDocs build exited with code {result.returncode}: "
                f"{result.stderr.strip()[:500]}",
            )
            return 1
    except FileNotFoundError:
        log_phase_event(
            logger, logging.WARNING, "mkdocs",
            "mkdocs command not found — skipping static site build. "
            "Install with: pip install mkdocs-material",
        )
    except subprocess.TimeoutExpired:
        log_phase_event(
            logger, logging.WARNING, "mkdocs",
            "MkDocs build timed out after 120s",
        )
        return 1

    return 0


def main(phases: list[str] | None = None) -> int:
    """CLI entry point for running the pipeline.

    When invoked as a console_script (via ``gh600-prep``), parses sys.argv
    for optional phase IDs and the ``--no-render`` flag.  When called
    programmatically, *phases* can be passed directly.

    Args:
        phases: Optional list of phase IDs to run (programmatic use).

    Returns:
        Exit code: 0 (success), 1 (partial), 2 (failure).
    """
    import argparse

    parser = argparse.ArgumentParser(
        prog="gh600-prep",
        description="GH-600 Exam Prep Generator pipeline",
    )
    parser.add_argument(
        "phases",
        nargs="*",
        default=None,
        help="Specific phase IDs to run (e.g. phase01 phase03). "
             "Omit to run all 10 phases.",
    )
    parser.add_argument(
        "--no-render",
        action="store_true",
        help="Skip the rendering and MkDocs build step after pipeline phases.",
    )
    parser.add_argument(
        "--render-only",
        action="store_true",
        help="Skip pipeline phases and only render existing artifacts into docs/.",
    )

    # Only parse sys.argv when invoked from CLI (no programmatic phases)
    if phases is None:
        args = parser.parse_args()
        requested_phases: list[str] | None = args.phases if args.phases else None
        no_render = args.no_render
        render_only = args.render_only
    else:
        requested_phases = phases
        no_render = False
        render_only = False

    logger = get_pipeline_logger()

    # --render-only: skip pipeline, go straight to rendering
    if render_only:
        rc = _render_and_build(logger)
        return rc

    # Run pipeline phases
    report = asyncio.run(run_pipeline(requested_phases))

    # After successful or partial pipeline run, render the site
    if not no_render and report.exit_code in (0, 1):
        render_rc = _render_and_build(logger)
        # If pipeline itself was fully successful but rendering failed,
        # report partial success
        if render_rc != 0 and report.exit_code == 0:
            return 1

    return report.exit_code


if __name__ == "__main__":
    sys.exit(main())
