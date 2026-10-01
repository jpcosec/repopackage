---
references:
- desk/tasks/Board.md
- repopackage
files:
- desk/SPEC.md
- docs/ARCHITECTURE.md
- src/repopackage/core/
- src/repopackage/cli/
- src/repopackage/repo/
id: '011'
domain: architecture/ownership
status: open
priority: p0
depends_on: []
created: ''
---

# Redefine `rp` ownership boundaries

## Rationale

_Explain why this task exists or the business driver behind it._

## Goal

_Describe the concrete result this task must produce._

Redesign `rp` so it acts as the control plane for multi-repo development instead of a partial manifest helper with a narrow composition slice.

## Scope

_State what is in scope and what is out of scope._

- The current implementation does not clearly separate composition policy, command ownership, workspace orchestration, and structural repair.
- Manifest git lifecycle is owned implicitly by `rp` instead of explicitly by `git-repo` plus a declared manifest source.
- The new target should cover local command centralization, multi-repo workflow orchestration, and repairable workspace evolution.

## Implementation Path

_Outline the expected implementation route or affected surface._

- Rewrite the product boundary around four explicit surfaces: composition, manifest publication, command registry, and workspace orchestration.
- Remove legacy target language about the first delivery slice if it blocks the new control-plane direction.
- Define which capabilities belong to `rp`, which belong to `git-repo`, and which require a new repair/index subsystem.

## Validation

_List the checks required before this task can close._

- The architecture docs and task board agree on the new ownership boundary.
- No active task depends on preserving the old ad hoc manifest-repo workflow.
- The resulting target is specific enough to drive code tasks without fallback assumptions.

## Done When

_Name the observable condition that makes the task complete._
