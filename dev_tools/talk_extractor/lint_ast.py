"""AST helpers for the constraint linter."""

from __future__ import annotations

import ast

from talk_extractor.lint_models import DEF_TYPES


def has_docstring(node: ast.AST) -> bool:
    """Check whether a node has a docstring."""

    return ast.get_docstring(node) is not None


def first_code_line(node: ast.AST) -> int:
    """Return the first non-docstring body line."""

    body = getattr(node, "body", [])
    return (
        body[1].lineno
        if has_docstring(node) and len(body) > 1
        else getattr(node, "lineno", 1)
    )


def code_span(node: ast.AST) -> int:
    """Measure body lines excluding docstring lines."""

    return node.end_lineno - first_code_line(node) + 1


def walk_defs(tree: ast.Module) -> list[ast.AST]:
    """Collect classes and functions."""

    return [node for node in ast.walk(tree) if isinstance(node, DEF_TYPES)]


def public_classes(tree: ast.Module) -> list[ast.ClassDef]:
    """List public top-level classes."""

    return [
        node
        for node in tree.body
        if isinstance(node, ast.ClassDef) and not node.name.startswith("_")
    ]
