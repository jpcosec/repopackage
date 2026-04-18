"""Models and constants for the constraint linter."""

from __future__ import annotations

import ast
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parent
MAX_FILE_LINES = 80
MAX_FUNCTION_LINES = 10
MAX_CLASS_LINES = 50
DEF_TYPES = (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)
FUNC_TYPES = (ast.FunctionDef, ast.AsyncFunctionDef)


@dataclass(slots=True)
class Violation:
    """A single constraint violation."""

    path: str
    line: int
    rule: str
    message: str
