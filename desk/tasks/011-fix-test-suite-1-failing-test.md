---
pills:
- desk/contexts/pill-001-rp-cli-control-plane.md
- desk/contexts/pill-002-state-and-false-success-failure-mode.md
- desk/contexts/pill-001-current-desk-execution-gates.md
- desk/contexts/pill-002-modular-task-boundaries.md
- desk/contexts/pill-003-cli-stress-test-validation.md
files:
- tests/
id: '011'
domain: repopackage/tests
status: open
priority: p1
depends_on:
  - '002'
created: '2026-06-07'
---

# Fix test suite (1 failing test)

## Rationale

_Explain why this task exists or the business driver behind it._

## Goal

_Describe the concrete result this task must produce._

All 52 tests in the repopackage test suite must pass.

## Scope

_State what is in scope and what is out of scope._

- **RP-30** (high): 1 test fails: `test_ecosystem_fixture_resolution_and_validation` — fails because `compose.lock.yaml` not found after resolve (same root cause as RP-06 in Task 002). References a different project path (`/home/jp/proyectos/wikipu-ecosystem/repopackage/tests/`).
- **RP-31** to **RP-33** (positive findings): Existing tests for error clarity should be preserved.

## Implementation Path

_Outline the expected implementation route or affected surface._

## Validation

_List the checks required before this task can close._

- `python -m pytest tests/ -v` shows all 52 tests passing.
- The fix likely depends on Task 002 (fix resolve false success).

## Done When

_Name the observable condition that makes the task complete._
