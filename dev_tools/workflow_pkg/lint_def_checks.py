"""Definition-level checks for the constraint linter."""

from __future__ import annotations

import ast
from pathlib import Path

from workflow_pkg.lint_ast import code_span, has_docstring
from workflow_pkg.lint_models import (
    FUNC_TYPES,
    MAX_CLASS_LINES,
    MAX_FUNCTION_LINES,
    Violation,
)


def def_violations(path: Path, node: ast.AST) -> list[Violation]:
    """Check class or function constraints."""

    return docstring_violation(path, node) + length_violation(path, node)


def docstring_violation(path: Path, node: ast.AST) -> list[Violation]:
    """Check missing docstrings on definitions."""

    return (
        []
        if has_docstring(node)
        else [
            Violation(
                str(path), node.lineno, "docstring", f"{node.name} missing docstring"
            )
        ]
    )


def length_violation(path: Path, node: ast.AST) -> list[Violation]:
    """Check function and class lengths."""

    if isinstance(node, FUNC_TYPES) and code_span(node) > MAX_FUNCTION_LINES:
        return [violation(path, node, "function-length", code_span(node))]
    if isinstance(node, ast.ClassDef) and code_span(node) > MAX_CLASS_LINES:
        return [violation(path, node, "class-length", code_span(node))]
    return []


def violation(path: Path, node: ast.AST, rule: str, span: int) -> Violation:
    """Build one length violation."""

    return Violation(str(path), node.lineno, rule, f"{node.name} has {span} lines")
