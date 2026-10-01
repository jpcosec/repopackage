---
pills:
- desk/contexts/pill-001-rp-cli-control-plane.md
- desk/contexts/pill-002-state-and-false-success-failure-mode.md
- desk/contexts/pill-001-current-desk-execution-gates.md
- desk/contexts/pill-002-modular-task-boundaries.md
- desk/contexts/pill-003-cli-stress-test-validation.md
files:
- src/repopackage/cli/handlers.py
- handle_graph
id: '008'
domain: repopackage/graph
status: open
priority: p2
depends_on: []
created: '2026-06-07'
---

# Fix rp graph for standalone projects and add flags

## Rationale

_Explain why this task exists or the business driver behind it._

## Goal

_Describe the concrete result this task must produce._

`rp graph` must produce valid Mermaid output even for standalone projects, and support filtering/formatting flags.

## Scope

_State what is in scope and what is out of scope._

- **RP-18** (medium): `rp graph` on standalone project (`uses: {}`) outputs only "graph TD" with no nodes/edges — invalid Mermaid.
- **RP-19** (medium): No `--focus`, `--depth`, or `--format` flags available.

## Implementation Path

_Outline the expected implementation route or affected surface._

## Validation

_List the checks required before this task can close._

- `rp graph` on standalone project shows at least one node (the project itself).
- `rp graph --focus X`, `--depth 1`, `--format dot` are accepted (at minimum, not unrecognized).

## Done When

_Name the observable condition that makes the task complete._
