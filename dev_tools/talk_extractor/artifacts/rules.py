"""Artifact extraction rules and constants."""

from __future__ import annotations

import re


FENCED_BLOCK = re.compile(r"```(?P<lang>[^\n`]*)\n(?P<body>.*?)```", re.DOTALL)
PLANTUML_BLOCK = re.compile(r"@startuml\b.*?@enduml", re.DOTALL)
LANGUAGE_ALIASES = {
    "py": "python",
    "mmd": "mermaid",
    "plainuml": "plantuml",
    "puml": "plantuml",
    "yml": "yaml",
    "md": "markdown",
    "txt": "text",
    "shell": "bash",
    "sh": "bash",
    "zsh": "bash",
    "js": "javascript",
    "ts": "typescript",
}
EXTENSIONS = {
    "python": "py",
    "mermaid": "mmd",
    "plantuml": "puml",
    "yaml": "yaml",
    "json": "json",
    "markdown": "md",
    "text": "txt",
    "bash": "sh",
    "javascript": "js",
    "typescript": "ts",
    "html": "html",
    "xml": "xml",
}
GENERIC_LABELS = {
    "fragmento de codigo",
    "fragmento de código",
    "codigo",
    "código",
    "ejemplo",
    "diagrama",
}


class ArtifactRules:
    """Expose artifact-related constants through a small object."""

    def fenced_block(self) -> re.Pattern[str]:
        """Return the fenced block regex."""

        return FENCED_BLOCK

    def plantuml(self) -> re.Pattern[str]:
        """Return the PlantUML regex."""

        return PLANTUML_BLOCK

    def aliases(self) -> dict[str, str]:
        """Return language aliases."""

        return LANGUAGE_ALIASES

    def extensions(self) -> dict[str, str]:
        """Return file extensions by kind."""

        return EXTENSIONS

    def generic_labels(self) -> set[str]:
        """Return weak labels that should be skipped."""

        return GENERIC_LABELS
