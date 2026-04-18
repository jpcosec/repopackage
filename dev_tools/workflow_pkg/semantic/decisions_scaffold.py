"""Decision scaffold builder."""

from __future__ import annotations


class DecisionsScaffoldBuilder:
    """Build the initial decisions markdown scaffold."""

    def build(self) -> str:
        """Return the default decision scaffold."""

        return """# Decisions

<!-- Add one block per decision following workflow_pkg/semantic_contracts.md -->
"""
