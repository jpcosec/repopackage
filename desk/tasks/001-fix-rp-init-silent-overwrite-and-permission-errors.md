---
pills:
- desk/contexts/pill-001-rp-cli-control-plane.md
- desk/contexts/pill-001-current-desk-execution-gates.md
- desk/contexts/pill-002-modular-task-boundaries.md
- desk/contexts/pill-003-cli-stress-test-validation.md
files:
- src/repopackage/cli/handlers.py
- handle_init
id: '001'
domain: repopackage/cli
status: open
priority: p0
depends_on: []
created: '2026-06-07'
---

# Fix rp init silent overwrite and permission errors

## Rationale

_Explain why this task exists or the business driver behind it._

## Goal

_Describe the concrete result this task must produce._

Make `rp init` safe: no silent overwrites, no raw tracebacks, and clear user feedback on argument misuse.

## Scope

_State what is in scope and what is out of scope._

- **RP-02** (high): `rp init` silently overwrites existing compose.yaml without warning or prompt.
- **RP-03** (medium): PermissionError on unwritable directory dumps full Python traceback, and "Initializing new project..." is printed before the crash.
- **RP-04** (low): `rp init .` shows argparse "unrecognized arguments" instead of a helpful message.

## Implementation Path

_Outline the expected implementation route or affected surface._

## Validation

_List the checks required before this task can close._

- `rp init` with existing compose.yaml shows an error message, does not overwrite.
- `rp init` in `chmod -w` directory shows friendly "Permission denied" message, no traceback.
- `rp init .` shows helpful message about no arguments being expected.

## Done When

_Name the observable condition that makes the task complete._
