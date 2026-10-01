---
pills:
- desk/contexts/pill-001-rp-cli-control-plane.md
- desk/contexts/pill-002-state-and-false-success-failure-mode.md
- desk/contexts/pill-001-current-desk-execution-gates.md
- desk/contexts/pill-002-modular-task-boundaries.md
- desk/contexts/pill-003-cli-stress-test-validation.md
files:
- src/repopackage/cli/handlers.py
- handle_sync
id: '003'
domain: repopackage/sync
status: open
priority: p0
depends_on: []
created: '2026-06-07'
---

# Fix rp sync crash and error messages

## Rationale

_Explain why this task exists or the business driver behind it._

## Goal

_Describe the concrete result this task must produce._

`rp sync` must handle missing repos gracefully with actionable messages instead of multi-layered tracebacks.

## Scope

_State what is in scope and what is out of scope._

- **RP-09** (high): `rp sync` crashes with full traceback + Google Repo tool SyncError + GitCommandError when local repos are missing.
- **RP-34** (medium): Hard dependency on Google Repo tool (`repo`) is not checked upfront; failure happens mid-execution.

## Implementation Path

_Outline the expected implementation route or affected surface._

## Validation

_List the checks required before this task can close._

- `rp sync` with missing local repos shows a graceful, actionable error message without traceback.
- If `repo` tool is missing, sync fails early with a clear message before attempting any operation.

## Done When

_Name the observable condition that makes the task complete._
