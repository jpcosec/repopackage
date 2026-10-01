---
pills:
- desk/contexts/pill-001-rp-cli-control-plane.md
- desk/contexts/pill-002-state-and-false-success-failure-mode.md
- desk/contexts/pill-001-current-desk-execution-gates.md
- desk/contexts/pill-002-modular-task-boundaries.md
- desk/contexts/pill-003-cli-stress-test-validation.md
files:
- src/repopackage/cli/handlers.py
- handle_resolve
id: '002'
domain: repopackage/resolve
status: open
priority: p0
depends_on: []
created: '2026-06-07'
---

# Fix rp resolve false success (lockfile not written)

## Rationale

_Explain why this task exists or the business driver behind it._

## Goal

_Describe the concrete result this task must produce._

`rp resolve` must not claim success when it fails to write a lockfile, and must validate inputs before reporting success.

## Scope

_State what is in scope and what is out of scope._

- **RP-06** (high): `rp resolve` with `uses: {}` prints "Resolved successfully. Wrote compose.lock.yaml" but no lockfile is written. Exit code 0.
- **RP-22** (high): Incomplete compose.yaml (missing url/branch) resolves "successfully" instead of failing validation.
- **RP-35** (medium): Same false success with nonexistent project URL; no URL validation.

## Implementation Path

_Outline the expected implementation route or affected surface._

## Validation

_List the checks required before this task can close._

- `rp resolve` on project with `uses: {}` does NOT print success; either writes a valid lockfile or errors.
- `rp resolve` with incomplete entries (missing url, branch, kind) fails with validation error.
- Lockfile is confirmed on disk after resolve claims to have written it.

## Done When

_Name the observable condition that makes the task complete._
