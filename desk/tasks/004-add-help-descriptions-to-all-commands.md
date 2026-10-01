---
pills:
- desk/contexts/pill-001-rp-cli-control-plane.md
- desk/contexts/pill-001-current-desk-execution-gates.md
- desk/contexts/pill-002-modular-task-boundaries.md
- desk/contexts/pill-003-cli-stress-test-validation.md
files:
- src/repopackage/cli/main.py
- add_parser
- description=
id: '004'
domain: repopackage/cli
status: open
priority: p1
depends_on: []
created: '2026-06-07'
---

# Add --help descriptions to all commands

## Rationale

_Explain why this task exists or the business driver behind it._

## Goal

_Describe the concrete result this task must produce._

Every subcommand's `--help` output must include a human-readable description of what the command does.

## Scope

_State what is in scope and what is out of scope._

- **RP-01** (medium): All 8 subcommands show only `usage: rp <cmd> [-h]` and `options: -h, --help` — zero description text.
- **RP-36** (low): `rp exports --help` specifically is empty (same root cause).

## Implementation Path

_Outline the expected implementation route or affected surface._

## Validation

_List the checks required before this task can close._

- `rp <cmd> --help` shows a description for each of the 8 subcommands.
- Descriptions are concise (one sentence) and accurate.

## Done When

_Name the observable condition that makes the task complete._
