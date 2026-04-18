"""Constraint checks for workflow_pkg."""

from __future__ import annotations

import ast
from pathlib import Path

from workflow_pkg.lint_ast import walk_defs
from workflow_pkg.lint_def_checks import def_violations
from workflow_pkg.lint_module_checks import file_violation, module_violation
from workflow_pkg.lint_models import Violation


def lint_file(path: Path) -> list[Violation]:
    """Lint a single Python file."""

    tree = ast.parse(path.read_text(encoding="utf-8"))
    items = file_violation(path) + module_violation(path, tree)
    return items + [
        issue for node in walk_defs(tree) for issue in def_violations(path, node)
    ]
