"""Module and file checks for the constraint linter."""

from __future__ import annotations

import ast
from pathlib import Path

from workflow_pkg.lint_ast import has_docstring, public_classes
from workflow_pkg.lint_models import MAX_FILE_LINES, Violation


def file_violation(path: Path) -> list[Violation]:
    """Check file-level constraints."""

    lines = len(path.read_text(encoding="utf-8").splitlines())
    return (
        []
        if lines <= MAX_FILE_LINES
        else [
            Violation(str(path), 1, "file-length", f"{lines} lines > {MAX_FILE_LINES}")
        ]
    )


def module_violation(path: Path, tree: ast.Module) -> list[Violation]:
    """Check module-level docstring and class count."""

    items = (
        []
        if has_docstring(tree)
        else [Violation(str(path), 1, "module-docstring", "missing module docstring")]
    )
    return items + class_count_violation(path, tree)


def class_count_violation(path: Path, tree: ast.Module) -> list[Violation]:
    """Check public top-level class count."""

    classes = public_classes(tree)
    return (
        []
        if len(classes) <= 1
        else [
            Violation(str(path), 1, "public-classes", f"{len(classes)} public classes")
        ]
    )
