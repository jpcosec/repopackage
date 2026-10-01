---
references:
- desk/tasks/Board.md
- repopackage
files:
- src/repopackage/core/
- src/repopackage/cli/
- src/repopackage/repo/
- tests/
pills:
- desk/contexts/pill-001-rp-cli-control-plane.md
- desk/contexts/pill-001-current-desk-execution-gates.md
- desk/contexts/pill-002-modular-task-boundaries.md
id: '017'
domain: repair/index
status: open
priority: p0
depends_on:
- '011'
- '015'
created: ''
---

# Index cross-repo references for structural repair

## Rationale

_Explain why this task exists or the business driver behind it._

## Goal

_Describe the concrete result this task must produce._

Build the reference index needed for `rp` to diagnose what breaks when files or directories move and to drive repair workflows across the workspace.

## Scope

_State what is in scope and what is out of scope._

- `rp` has no index of import paths, config paths, contract paths, docs references, or command targets that point at workspace files.
- File moves and renames currently rely on manual search and repair.
- Cross-repo references need to be queryable by path and by owning package.

## Implementation Path

_Outline the expected implementation route or affected surface._

- Define a reference-index model that records path-based relationships across repos.
- Start with deterministic reference classes: imports, manifest paths, contract/schema paths, docs links, and launcher targets.
- Add commands to scan, persist, and inspect the index for a resolved workspace.

## Validation

_List the checks required before this task can close._

- `rp` can answer which files or package contracts reference a given path.
- The index is reproducible from workspace state.
- Tests cover at least one cross-repo move scenario and one non-code reference type.

## Done When

_Name the observable condition that makes the task complete._
