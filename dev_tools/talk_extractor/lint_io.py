"""IO helpers for the constraint linter."""

from __future__ import annotations

from pathlib import Path

from talk_extractor.lint_models import ROOT, Violation


def python_files() -> list[Path]:
    """List tracked Python files under talk_extractor."""

    return sorted(
        path for path in ROOT.rglob("*.py") if "__pycache__" not in path.parts
    )


def print_violations(items: list[Violation]) -> None:
    """Print violations in a readable format."""

    for item in items:
        print(f"{item.path}:{item.line}: {item.rule}: {item.message}")
