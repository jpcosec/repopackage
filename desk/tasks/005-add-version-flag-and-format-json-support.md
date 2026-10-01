---
pills:
- desk/contexts/pill-001-rp-cli-control-plane.md
- desk/contexts/pill-001-current-desk-execution-gates.md
- desk/contexts/pill-002-modular-task-boundaries.md
- desk/contexts/pill-003-cli-stress-test-validation.md
files:
- src/repopackage/cli/main.py
id: '005'
domain: repopackage/cli
status: open
priority: p1
depends_on: []
created: '2026-06-07'
---

# Add --version flag and --format json support

## Rationale

_Explain why this task exists or the business driver behind it._

## Goal

_Describe the concrete result this task must produce._

Add standard `--version` flag to the root CLI and `--format json` to commands for CI/scripting use.

## Scope

_State what is in scope and what is out of scope._

- **RP-05** (medium): `rp --version` and `repopackage --version` both fail with "unrecognized arguments".
- **RP-10** (high): No `--format json` or machine-parseable output on any command (`rp status`, `rp exports`, `rp graph`, etc.).

## Implementation Path

_Outline the expected implementation route or affected surface._

## Validation

_List the checks required before this task can close._

- `rp --version` prints version string (e.g., "0.1.1") and exits 0.
- `rp status --format json` outputs valid JSON.
- Other commands with `--format` flag work consistently.

## Done When

_Name the observable condition that makes the task complete._
