---
pills:
- desk/contexts/pill-001-rp-cli-control-plane.md
- desk/contexts/pill-001-current-desk-execution-gates.md
- desk/contexts/pill-002-modular-task-boundaries.md
- desk/contexts/pill-003-cli-stress-test-validation.md
files:
- src/repopackage/core/
id: '009'
domain: repopackage/validation
status: open
priority: p1
depends_on: []
created: '2026-06-07'
---

# Add input validation for compose.yaml

## Rationale

_Explain why this task exists or the business driver behind it._

## Goal

_Describe the concrete result this task must produce._

compose.yaml parsing must validate field types, warn about unknown fields, and reject dangerous or excessive inputs.

## Scope

_State what is in scope and what is out of scope._

- **RP-24** (medium): Unknown fields in compose.yaml silently ignored during resolve.
- **RP-25** (low): UTF-8 emoji names accepted but lockfile not written (silent failure).
- **RP-26** (medium): Path traversal URLs (e.g., `../../etc/passwd`) not validated.
- **RP-28** (low): 1000-character project name accepted without any warning.

## Implementation Path

_Outline the expected implementation route or affected surface._

## Validation

_List the checks required before this task can close._

- compose.yaml with unknown fields shows a warning during resolve.
- Suspicious URLs (path traversal, invalid schemes) trigger a warning or rejection.
- Excessively long names (>100 chars) show a warning.

## Done When

_Name the observable condition that makes the task complete._
