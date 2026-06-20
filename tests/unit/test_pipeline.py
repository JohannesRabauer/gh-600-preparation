"""Unit tests for the pipeline orchestrator and structured logging."""

from __future__ import annotations

import asyncio
import json
import logging
from pathlib import Path
from unittest.mock import patch

import pytest

from src.pipeline import (
    PHASE_DEPENDENCIES,
    PHASE_NAMES,
    PhaseResult,
    PhaseStatus,
    PipelineReport,
    _can_run_phase,
    _topological_order,
    run_pipeline,
)
from src.utils.logging import (
    clear_error_log,
    get_pipeline_logger,
    log_phase_event,
)


# === Logging Tests ===


class TestStructuredLogging:
    """Tests for src/utils/logging.py."""

    def test_get_pipeline_logger_returns_logger(self):
        logger = get_pipeline_logger("test_pipeline_logger")
        assert isinstance(logger, logging.Logger)
        assert logger.name == "test_pipeline_logger"

    def test_get_pipeline_logger_has_handlers(self):
        logger = get_pipeline_logger("test_handlers")
        # Should have console + JSON file handler
        assert len(logger.handlers) >= 2

    def test_get_pipeline_logger_idempotent(self):
        logger1 = get_pipeline_logger("test_idempotent")
        handler_count = len(logger1.handlers)
        logger2 = get_pipeline_logger("test_idempotent")
        assert logger1 is logger2
        assert len(logger2.handlers) == handler_count

    def test_clear_error_log_creates_empty_json(self, tmp_path, monkeypatch):
        monkeypatch.setattr("src.utils.logging.ARTIFACTS_DIR", str(tmp_path))
        monkeypatch.setattr(
            "src.utils.logging.PIPELINE_ERROR_LOG", "pipeline_errors.json"
        )
        clear_error_log()
        error_path = tmp_path / "pipeline_errors.json"
        assert error_path.exists()
        assert json.loads(error_path.read_text(encoding="utf-8")) == []

    def test_error_log_writes_json_entries(self, tmp_path, monkeypatch):
        monkeypatch.setattr("src.utils.logging.ARTIFACTS_DIR", str(tmp_path))
        monkeypatch.setattr(
            "src.utils.logging.PIPELINE_ERROR_LOG", "pipeline_errors.json"
        )
        clear_error_log()

        # Get a fresh logger for this test
        logger_name = "test_error_log_write"
        logger = logging.getLogger(logger_name)
        logger.handlers.clear()
        logger.setLevel(logging.DEBUG)

        from src.utils.logging import _JSONFileHandler

        handler = _JSONFileHandler(tmp_path / "pipeline_errors.json")
        logger.addHandler(handler)

        log_phase_event(
            logger, logging.ERROR, "phase01",
            "Test error message",
        )

        error_path = tmp_path / "pipeline_errors.json"
        entries = json.loads(error_path.read_text(encoding="utf-8"))
        assert len(entries) == 1
        assert entries[0]["level"] == "ERROR"
        assert entries[0]["phase"] == "phase01"
        assert entries[0]["message"] == "Test error message"
        assert "timestamp" in entries[0]

    def test_log_phase_event_with_exception(self, tmp_path, monkeypatch):
        monkeypatch.setattr("src.utils.logging.ARTIFACTS_DIR", str(tmp_path))
        monkeypatch.setattr(
            "src.utils.logging.PIPELINE_ERROR_LOG", "pipeline_errors.json"
        )
        clear_error_log()

        logger_name = "test_exc_log"
        logger = logging.getLogger(logger_name)
        logger.handlers.clear()
        logger.setLevel(logging.DEBUG)

        from src.utils.logging import _JSONFileHandler

        handler = _JSONFileHandler(tmp_path / "pipeline_errors.json")
        logger.addHandler(handler)

        exc = ValueError("something broke")
        log_phase_event(
            logger, logging.ERROR, "phase03",
            "Phase failed",
            exc_info=exc,
        )

        error_path = tmp_path / "pipeline_errors.json"
        entries = json.loads(error_path.read_text(encoding="utf-8"))
        assert len(entries) == 1
        assert entries[0]["error"]["type"] == "ValueError"
        assert "something broke" in entries[0]["error"]["detail"]


# === Topological Order Tests ===


class TestTopologicalOrder:
    """Tests for _topological_order function."""

    def test_all_phases_ordered(self):
        all_phases = list(PHASE_DEPENDENCIES.keys())
        order = _topological_order(all_phases, PHASE_DEPENDENCIES)
        assert set(order) == set(all_phases)

    def test_dependencies_come_first(self):
        all_phases = list(PHASE_DEPENDENCIES.keys())
        order = _topological_order(all_phases, PHASE_DEPENDENCIES)
        index_of = {phase: i for i, phase in enumerate(order)}

        for phase, deps in PHASE_DEPENDENCIES.items():
            for dep in deps:
                assert index_of[dep] < index_of[phase], (
                    f"{dep} should come before {phase}"
                )

    def test_subset_of_phases(self):
        subset = ["phase03", "phase04", "phase07"]
        order = _topological_order(subset, PHASE_DEPENDENCIES)
        # phase03 must come before phase04, phase04 before phase07
        assert order.index("phase03") < order.index("phase04")
        assert order.index("phase04") < order.index("phase07")

    def test_single_phase(self):
        order = _topological_order(["phase01"], PHASE_DEPENDENCIES)
        assert order == ["phase01"]

    def test_independent_phases_sorted_deterministically(self):
        # phase04 and phase05 are both after phase03, independent of each other
        order = _topological_order(
            ["phase04", "phase05"], PHASE_DEPENDENCIES
        )
        # Both should appear, sorted alphabetically since they're independent
        assert set(order) == {"phase04", "phase05"}
        assert order == ["phase04", "phase05"]  # deterministic alphabetical


# === Dependency Check Tests ===


class TestCanRunPhase:
    """Tests for _can_run_phase function."""

    def test_phase_with_no_deps_can_run(self):
        assert _can_run_phase("phase01", {}, PHASE_DEPENDENCIES, {"phase01"})

    def test_phase_blocked_by_failed_dep(self):
        results = {
            "phase01": PhaseResult(
                phase_id="phase01", status=PhaseStatus.FAILED
            )
        }
        assert not _can_run_phase(
            "phase02", results, PHASE_DEPENDENCIES, {"phase01", "phase02"}
        )

    def test_phase_runs_after_successful_dep(self):
        results = {
            "phase01": PhaseResult(
                phase_id="phase01", status=PhaseStatus.SUCCESS
            )
        }
        assert _can_run_phase(
            "phase02", results, PHASE_DEPENDENCIES, {"phase01", "phase02"}
        )

    def test_phase_with_dep_not_in_run_checks_artifact(self, tmp_path, monkeypatch):
        monkeypatch.setattr("src.pipeline.ARTIFACTS_DIR", str(tmp_path))
        # phase02 depends on phase01, but phase01 is not in the current run
        # and artifact doesn't exist
        assert not _can_run_phase(
            "phase02", {}, PHASE_DEPENDENCIES, {"phase02"}
        )

        # Now create the artifact
        (tmp_path / "phase01_extraction.json").write_text("{}")
        assert _can_run_phase(
            "phase02", {}, PHASE_DEPENDENCIES, {"phase02"}
        )


# === Pipeline Report Tests ===


class TestPipelineReport:
    """Tests for PipelineReport data class."""

    def test_report_to_dict(self):
        report = PipelineReport(
            phases=[
                PhaseResult(
                    phase_id="phase01",
                    status=PhaseStatus.SUCCESS,
                    duration_seconds=1.234,
                    artifact_path="artifacts/phase01_extraction.json",
                ),
                PhaseResult(
                    phase_id="phase02",
                    status=PhaseStatus.FAILED,
                    duration_seconds=0.5,
                    error="ValueError: bad data",
                ),
            ],
            total_duration_seconds=1.734,
            exit_code=1,
            summary="Partial success",
        )
        d = report.to_dict()
        assert d["exit_code"] == 1
        assert len(d["phases"]) == 2
        assert d["phases"][0]["status"] == "success"
        assert d["phases"][1]["error"] == "ValueError: bad data"
        assert d["phases"][0]["name"] == "Knowledge Extractor"


# === Pipeline Integration Tests ===


class TestRunPipeline:
    """Tests for run_pipeline with mocked phases."""

    def test_invalid_phase_returns_exit_code_2(self):
        report = asyncio.run(run_pipeline(["nonexistent_phase"]))
        assert report.exit_code == 2
        assert "Invalid phase IDs" in report.summary

    def test_successful_pipeline_returns_exit_code_0(self, tmp_path, monkeypatch):
        monkeypatch.setattr("src.pipeline.ARTIFACTS_DIR", str(tmp_path))
        monkeypatch.setattr("src.utils.logging.ARTIFACTS_DIR", str(tmp_path))

        # Create a mock runner that always succeeds
        call_order = []

        def mock_runner(phase_id):
            def runner():
                call_order.append(phase_id)
                # Write a fake artifact
                artifact_file = PHASE_DEPENDENCIES.get(phase_id)
                from src.config import ARTIFACT_FILENAMES
                fname = ARTIFACT_FILENAMES.get(phase_id)
                if fname:
                    (tmp_path / fname).write_text("{}")
            return runner

        runners = {pid: mock_runner(pid) for pid in PHASE_DEPENDENCIES}
        monkeypatch.setattr("src.pipeline._PHASE_RUNNERS", runners)

        report = asyncio.run(run_pipeline())
        assert report.exit_code == 0
        assert len(report.phases) == 10
        assert all(r.status == PhaseStatus.SUCCESS for r in report.phases)

    def test_failed_phase_skips_dependents(self, tmp_path, monkeypatch):
        monkeypatch.setattr("src.pipeline.ARTIFACTS_DIR", str(tmp_path))
        monkeypatch.setattr("src.utils.logging.ARTIFACTS_DIR", str(tmp_path))

        def failing_phase01():
            raise RuntimeError("Network error")

        def success_runner():
            pass

        runners = {pid: success_runner for pid in PHASE_DEPENDENCIES}
        runners["phase01"] = failing_phase01
        monkeypatch.setattr("src.pipeline._PHASE_RUNNERS", runners)

        report = asyncio.run(run_pipeline())

        # phase01 should have failed
        phase01_result = next(r for r in report.phases if r.phase_id == "phase01")
        assert phase01_result.status == PhaseStatus.FAILED
        assert "RuntimeError" in phase01_result.error

        # All other phases should be skipped (they all depend on phase01 transitively)
        for r in report.phases:
            if r.phase_id != "phase01":
                assert r.status == PhaseStatus.SKIPPED

        # Exit code should be 2 since no phases succeeded besides none
        assert report.exit_code == 2

    def test_partial_failure_returns_exit_code_1(self, tmp_path, monkeypatch):
        monkeypatch.setattr("src.pipeline.ARTIFACTS_DIR", str(tmp_path))
        monkeypatch.setattr("src.utils.logging.ARTIFACTS_DIR", str(tmp_path))

        from src.config import ARTIFACT_FILENAMES

        def success_with_artifact(phase_id):
            def runner():
                fname = ARTIFACT_FILENAMES.get(phase_id)
                if fname:
                    (tmp_path / fname).write_text("{}")
            return runner

        # Make phase09 fail but let everything else succeed
        runners = {
            pid: success_with_artifact(pid) for pid in PHASE_DEPENDENCIES
        }

        def failing_phase09():
            # First write the earlier artifacts
            raise ValueError("Gap analysis failed")

        runners["phase09"] = failing_phase09
        monkeypatch.setattr("src.pipeline._PHASE_RUNNERS", runners)

        report = asyncio.run(run_pipeline())

        # phase09 failed, phase10 skipped
        phase09 = next(r for r in report.phases if r.phase_id == "phase09")
        phase10 = next(r for r in report.phases if r.phase_id == "phase10")
        assert phase09.status == PhaseStatus.FAILED
        assert phase10.status == PhaseStatus.SKIPPED

        # Other phases should succeed
        succeeded = [
            r for r in report.phases if r.status == PhaseStatus.SUCCESS
        ]
        assert len(succeeded) == 8  # 10 - phase09 - phase10

        assert report.exit_code == 1

    def test_pipeline_writes_report_artifact(self, tmp_path, monkeypatch):
        monkeypatch.setattr("src.pipeline.ARTIFACTS_DIR", str(tmp_path))
        monkeypatch.setattr("src.utils.logging.ARTIFACTS_DIR", str(tmp_path))

        from src.config import ARTIFACT_FILENAMES

        def success_with_artifact(phase_id):
            def runner():
                fname = ARTIFACT_FILENAMES.get(phase_id)
                if fname:
                    (tmp_path / fname).write_text("{}")
            return runner

        runners = {
            pid: success_with_artifact(pid) for pid in PHASE_DEPENDENCIES
        }
        monkeypatch.setattr("src.pipeline._PHASE_RUNNERS", runners)

        asyncio.run(run_pipeline())

        report_path = tmp_path / "pipeline_report.json"
        assert report_path.exists()
        report_data = json.loads(report_path.read_text(encoding="utf-8"))
        assert "exit_code" in report_data
        assert "phases" in report_data
        assert report_data["exit_code"] == 0
