# Repopackage Tasks Board

## Current State Summary

- Objective: deliver a real, auditable multi-repo composition slice
- Current blocker: implementation lags behind the control-plane concept
- Real use case: resolve and materialize a project that reuses shared repos with contextual and central lines

## Delivery Phases

### Phase 1 - Make core resolution trustworthy
- `desk/tasks/001-fix-git-adapter.md`
- `desk/tasks/002-type-dependency-specs.md`
- `desk/tasks/003-stop-swallowing-contract-errors.md`

### Phase 2 - Make workspace state real
- `desk/tasks/004-define-lockfile-state.md`
- `desk/tasks/005-implement-rp-status.md`

### Phase 3 - Make materialization safe
- `desk/tasks/006-fix-manifest-generation.md`
- `desk/tasks/007-validate-materialized-workspace.md`

### Phase 4 - Prove the real use case
- `desk/tasks/008-create-real-use-case-fixture.md`
- `desk/tasks/009-run-end-to-end-composition-flow.md`

## Active

| ID | Domain | Task | Priority | Depends On |
|----|--------|------|----------|------------|
| 001 | git-adapter | Fix git adapter for real repo inspection | p0 | none |
| 002 | models/solver | Type dependency specs | p0 | none |
| 003 | solver/contracts | Stop swallowing contract errors | p0 | 001 |
| 004 | lockfile/workspace | Define lockfile state semantics | p1 | 002, 003 |
| 005 | cli/status | Implement `rp status` | p1 | 004 |
| 006 | manifest/sync | Fix manifest generation | p1 | 002 |
| 007 | validation | Validate materialized workspace | p1 | 004, 006 |
| 008 | fixtures/e2e | Create real use case fixture | p1 | 001, 002, 004, 006 |
| 009 | e2e | Run end-to-end composition flow | p1 | 005, 007, 008 |

## Blocked

| ID | Domain | Task | Priority | Depends On |
|----|--------|------|----------|------------|
| - | - | none | - | - |

## Working Rules

1. Start from `desk/SPEC.md`.
2. Prefer fixing core trust issues before adding new command surface.
3. Every completed task must leave tests or fixtures stronger than before.
4. Do not mark the control plane ready while `rp status`, git inspection, or lockfile semantics remain unclear.
