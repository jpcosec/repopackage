---
references:
- desk/tasks/Board.md
- repopackage
files:
- src/repopackage/cli/handlers.py
- src/repopackage/core/
- src/repopackage/repo/
- tests/
pills:
- desk/contexts/pill-001-rp-cli-control-plane.md
- desk/contexts/pill-001-current-desk-execution-gates.md
- desk/contexts/pill-002-modular-task-boundaries.md
id: '018'
domain: repair/moves
status: open
priority: p1
depends_on:
- '017'
created: ''
---

# Implement move and rename repair flow

## Rationale

_Explain why this task exists or the business driver behind it._

## Goal

_Describe the concrete result this task must produce._

Let `rp` plan and repair structural changes such as moving or renaming files and directories without leaving the workspace in a blind broken state.

## Scope

_State what is in scope and what is out of scope._

- There is no command that plans a move, reports blast radius, rewrites deterministic references, and leaves a diagnosis for unresolved breakage.
- Manual moves are risky because imports, docs, contracts, launcher targets, and path-bound config can drift independently.
- Repair output should distinguish rewritten references from unresolved references that need human action.

## Implementation Path

_Outline the expected implementation route or affected surface._

- Add a repair-planning command that computes the impact of a move or rename before mutation.
- Implement deterministic rewrites for supported reference classes and emit unresolved diagnostics for the rest.
- Make the repair flow update workspace inventory and command registry if entrypoint paths move.

## Validation

_List the checks required before this task can close._

- A planned move reports affected packages and reference counts before applying changes.
- Supported references are rewritten automatically and verified afterward.
- Unsupported references are surfaced in a structured diagnosis instead of being ignored.

## Done When

_Name the observable condition that makes the task complete._
