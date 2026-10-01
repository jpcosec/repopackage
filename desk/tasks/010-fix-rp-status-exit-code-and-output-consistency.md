---
pills:
- desk/contexts/pill-001-rp-cli-control-plane.md
- desk/contexts/pill-002-state-and-false-success-failure-mode.md
- desk/contexts/pill-001-current-desk-execution-gates.md
- desk/contexts/pill-002-modular-task-boundaries.md
- desk/contexts/pill-003-cli-stress-test-validation.md
files:
- src/repopackage/cli/handlers.py
- handle_status
id: '010'
domain: repopackage/cli
status: open
priority: p2
depends_on: []
created: '2026-06-07'
---

# Fix rp status exit code and output consistency

## Rationale

_Explain why this task exists or the business driver behind it._

## Goal

_Describe the concrete result this task must produce._

`rp status` must exit non-zero when packages are missing and provide machine-parseable output.

## Scope

_State what is in scope and what is out of scope._

- **RP-14** (medium): `rp status` exits 0 when packages are MISSING from workspace.
- **RP-15** (low): No `--format json` or machine-parseable output option.
- **RP-38** (low): `rp status` and `rp validate` show different info levels inconsistently.

## Implementation Path

_Outline the expected implementation route or affected surface._

## Validation

_List the checks required before this task can close._

- `rp status` with missing packages exits non-zero (exit code 1).
- `rp status --format json` outputs valid JSON with per-package details.
- Status output is consistent with validate where they overlap.

## Done When

_Name the observable condition that makes the task complete._
