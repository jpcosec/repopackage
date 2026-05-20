---
id: '011'
domain: architecture/ownership
status: open
priority: p0
depends_on: []
created: ''
---

# Redefine `rp` ownership boundaries

## Objective

Redesign `rp` so it acts as the control plane for multi-repo development instead of a partial manifest helper with a narrow composition slice.

## Reference

- Board: `repopackage/desk/tasks/Board.md`
- Desk: `repopackage`

## What to Fix

- The current implementation does not clearly separate composition policy, command ownership, workspace orchestration, and structural repair.
- Manifest git lifecycle is owned implicitly by `rp` instead of explicitly by `git-repo` plus a declared manifest source.
- The new target should cover local command centralization, multi-repo workflow orchestration, and repairable workspace evolution.

## Files Likely Involved

- `desk/SPEC.md`
- `docs/ARCHITECTURE.md`
- `src/repopackage/core/`
- `src/repopackage/cli/`
- `src/repopackage/repo/`

## How to Do It

- Rewrite the product boundary around four explicit surfaces: composition, manifest publication, command registry, and workspace orchestration.
- Remove legacy target language about the first delivery slice if it blocks the new control-plane direction.
- Define which capabilities belong to `rp`, which belong to `git-repo`, and which require a new repair/index subsystem.

## Validation

- The architecture docs and task board agree on the new ownership boundary.
- No active task depends on preserving the old ad hoc manifest-repo workflow.
- The resulting target is specific enough to drive code tasks without fallback assumptions.
