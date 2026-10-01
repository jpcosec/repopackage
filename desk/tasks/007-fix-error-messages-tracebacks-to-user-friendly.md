---
pills:
- desk/contexts/pill-001-rp-cli-control-plane.md
- desk/contexts/pill-001-current-desk-execution-gates.md
- desk/contexts/pill-002-modular-task-boundaries.md
- desk/contexts/pill-003-cli-stress-test-validation.md
files:
- src/repopackage/cli/handlers.py
id: '007'
domain: repopackage/cli
status: open
priority: p1
depends_on: []
created: '2026-06-07'
---

# Fix error messages (tracebacks → user-friendly)

## Rationale

_Explain why this task exists or the business driver behind it._

## Goal

_Describe the concrete result this task must produce._

All error paths must produce semantic, user-friendly messages instead of raw tracebacks or internal class names.

## Scope

_State what is in scope and what is out of scope._

- **RP-07** (low): Resolve error uses "Unexpected error:" prefix (developer-oriented).
- **RP-08** (medium): pygit2 internal error ("remote authentication required but no callback set") exposed to user.
- **RP-17** (high): `rp graph` shows full 12-line traceback for missing local repos.
- **RP-23** (medium): Invalid YAML shows full 18-line ruamel.yaml traceback.
- **RP-27** (medium): Corrupt lockfile error exposes Pydantic constructor internals.

## Implementation Path

_Outline the expected implementation route or affected surface._

## Validation

_List the checks required before this task can close._

- Each error scenario shows a single-line semantic message without traceback.
- Internal library/class names are never exposed in user-facing messages.

## Done When

_Name the observable condition that makes the task complete._
