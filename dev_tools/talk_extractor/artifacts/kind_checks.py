"""Artifact kind inference helpers."""

from __future__ import annotations

import re


def infer_kind(text: str) -> str:
    """Infer artifact kind from plain text."""

    for checker in CHECKERS:
        kind = checker(text)
        if kind:
            return kind
    return "text"


def plantuml_kind(text: str) -> str:
    """Infer PlantUML content."""

    return "plantuml" if text.startswith("@startuml") else ""


def mermaid_kind(text: str) -> str:
    """Infer Mermaid content."""

    pattern = (
        r"(^|\n)\s*(flowchart|sequenceDiagram|classDiagram|erDiagram|journey|gantt)\b"
    )
    return "mermaid" if re.search(pattern, text) else ""


def python_kind(text: str) -> str:
    """Infer Python content."""

    pattern = r"(^|\n)(from\s+\w+\s+import|import\s+\w+|def\s+\w+\(|class\s+\w+[:(])"
    return "python" if re.search(pattern, text) else ""


def yaml_kind(text: str) -> str:
    """Infer YAML content."""

    return "yaml" if re.search(r"(^|\n)\s*[\w-]+:\s", text) else ""


def json_kind(text: str) -> str:
    """Infer JSON content."""

    return "json" if text.startswith("{") or text.startswith("[") else ""


def markdown_kind(text: str) -> str:
    """Infer Markdown content."""

    return "markdown" if text.startswith("#") else ""


CHECKERS = [
    plantuml_kind,
    mermaid_kind,
    python_kind,
    yaml_kind,
    json_kind,
    markdown_kind,
]
