"""Structured logging for the GH-600 Exam Prep pipeline.

Provides JSON-structured logging that writes errors to
`artifacts/pipeline_errors.json` and all levels to the console.
"""

from __future__ import annotations

import json
import logging
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from src.config import ARTIFACTS_DIR, PIPELINE_ERROR_LOG


class _JSONFormatter(logging.Formatter):
    """Formats log records as JSON strings for structured output."""

    def format(self, record: logging.LogRecord) -> str:
        entry: dict[str, Any] = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "level": record.levelname,
            "phase": getattr(record, "phase", None),
            "message": record.getMessage(),
        }
        # Include optional error details
        if record.exc_info and record.exc_info[1]:
            entry["error"] = {
                "type": type(record.exc_info[1]).__name__,
                "detail": str(record.exc_info[1]),
            }
        elif hasattr(record, "error_detail"):
            entry["error"] = record.error_detail  # type: ignore[attr-defined]

        return json.dumps(entry, default=str)


class _ConsoleFormatter(logging.Formatter):
    """Human-readable console formatter with phase context."""

    def format(self, record: logging.LogRecord) -> str:
        phase = getattr(record, "phase", None)
        phase_str = f"[{phase}] " if phase else ""
        ts = datetime.now(timezone.utc).strftime("%H:%M:%S")
        msg = record.getMessage()
        prefix = f"{ts} {record.levelname:<7} {phase_str}"

        if record.exc_info and record.exc_info[1]:
            msg += f" | {type(record.exc_info[1]).__name__}: {record.exc_info[1]}"

        return f"{prefix}{msg}"


class _JSONFileHandler(logging.Handler):
    """Appends JSON error entries to the pipeline errors file.

    Only handles ERROR-level and above. Maintains a valid JSON array
    by reading existing entries, appending, and rewriting.
    """

    def __init__(self, filepath: Path) -> None:
        super().__init__(level=logging.ERROR)
        self._filepath = filepath
        self._filepath.parent.mkdir(parents=True, exist_ok=True)

    def emit(self, record: logging.LogRecord) -> None:
        try:
            entry = json.loads(_JSONFormatter().format(record))
            # Read existing entries
            entries: list[dict[str, Any]] = []
            if self._filepath.exists():
                try:
                    content = self._filepath.read_text(encoding="utf-8")
                    if content.strip():
                        entries = json.loads(content)
                except (json.JSONDecodeError, OSError):
                    entries = []

            entries.append(entry)

            self._filepath.write_text(
                json.dumps(entries, indent=2, default=str),
                encoding="utf-8",
            )
        except Exception:  # noqa: BLE001
            self.handleError(record)


def get_pipeline_logger(name: str = "pipeline") -> logging.Logger:
    """Get a configured pipeline logger.

    Creates a logger that outputs to both console (all levels) and
    the JSON error file (ERROR+ only).

    Args:
        name: Logger name. Defaults to "pipeline".

    Returns:
        Configured Logger instance.
    """
    logger = logging.getLogger(name)

    # Avoid adding duplicate handlers if called multiple times
    if logger.handlers:
        return logger

    logger.setLevel(logging.DEBUG)

    # Console handler — all levels
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.DEBUG)
    console_handler.setFormatter(_ConsoleFormatter())
    logger.addHandler(console_handler)

    # JSON file handler — ERROR+ only
    error_log_path = Path(ARTIFACTS_DIR) / PIPELINE_ERROR_LOG
    json_handler = _JSONFileHandler(error_log_path)
    json_handler.setFormatter(_JSONFormatter())
    logger.addHandler(json_handler)

    return logger


def clear_error_log() -> None:
    """Clear the pipeline error log file.

    Called at the start of a new pipeline run to reset the error log.
    """
    error_log_path = Path(ARTIFACTS_DIR) / PIPELINE_ERROR_LOG
    error_log_path.parent.mkdir(parents=True, exist_ok=True)
    error_log_path.write_text("[]", encoding="utf-8")


def log_phase_event(
    logger: logging.Logger,
    level: int,
    phase: str,
    message: str,
    *,
    error_detail: dict[str, Any] | None = None,
    exc_info: BaseException | None = None,
) -> None:
    """Log a pipeline phase event with structured context.

    Args:
        logger: The logger instance to use.
        level: Logging level (e.g., logging.INFO).
        phase: Phase identifier (e.g., "phase01").
        message: Human-readable log message.
        error_detail: Optional error context dictionary.
        exc_info: Optional exception for traceback logging.
    """
    extra = {"phase": phase}
    if error_detail:
        extra["error_detail"] = error_detail  # type: ignore[assignment]

    logger.log(
        level,
        message,
        exc_info=(type(exc_info), exc_info, exc_info.__traceback__) if exc_info else None,
        extra=extra,
    )
