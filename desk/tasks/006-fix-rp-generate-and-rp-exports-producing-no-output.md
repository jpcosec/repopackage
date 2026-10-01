---
pills:
- desk/contexts/pill-001-rp-cli-control-plane.md
- desk/contexts/pill-002-state-and-false-success-failure-mode.md
- desk/contexts/pill-001-current-desk-execution-gates.md
- desk/contexts/pill-002-modular-task-boundaries.md
- desk/contexts/pill-003-cli-stress-test-validation.md
files:
- src/repopackage/cli/handlers.py
- handle_generate
- handle_exports
id: '006'
domain: repopackage/generate
status: open
priority: p1
depends_on: []
created: '2026-06-07'
---

# Fix rp generate and rp exports producing no output

## Rationale

_Explain why this task exists or the business driver behind it._

## Goal

_Describe the concrete result this task must produce._

`rp generate` must produce files on disk in a known location, and `rp exports` must render actual content.

## Scope

_State what is in scope and what is out of scope._

- **RP-16** (high): `rp generate` says "Found 2 contracts" but produces no files; no `--output` flag exists.
- **RP-20** (high): `rp exports` outputs only an empty markdown heading with no package list or export content.
- **RP-21** (low): No `--package` filter on exports.

## Implementation Path

_Outline the expected implementation route or affected surface._

## Validation

_List the checks required before this task can close._

- `rp generate` produces actual files in a known output location (e.g., `generated/` or `--output` dir).
- `rp exports` returns a non-empty list of packages with their commands, contracts, and procedures.

## Done When

_Name the observable condition that makes the task complete._
