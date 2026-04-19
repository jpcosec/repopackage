"""Specs scaffold builder."""

from __future__ import annotations


SPEC_TEMPLATE = """# Spec

## Topic
- TBD

## Work Type
- TBD

## Problem Statement
- TBD

## Final State
- TBD

## Core Concepts
- TBD

## Final Architecture
- TBD

## Final Artifacts
- TBD

## Accepted Decisions
- TBD

## Open Questions
- TBD

## Explicitly Rejected Or Not Chosen
- TBD

## Evidence
- TBD
"""


class SpecsScaffoldBuilder:
    """Build the initial specs markdown scaffold."""

    def build(self) -> str:
        """Return the default spec scaffold."""

        return SPEC_TEMPLATE
