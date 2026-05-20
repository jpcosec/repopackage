---
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

## Objective

Build the reference index needed for `rp` to diagnose what breaks when files or directories move and to drive repair workflows across the workspace.

## Reference

- Board: `repopackage/desk/tasks/Board.md`
- Desk: `repopackage`

## What to Fix

- `rp` has no index of import paths, config paths, contract paths, docs references, or command targets that point at workspace files.
- File moves and renames currently rely on manual search and repair.
- Cross-repo references need to be queryable by path and by owning package.

## Files Likely Involved

- `src/repopackage/core/`
- `src/repopackage/cli/`
- `src/repopackage/repo/`
- `tests/`

## How to Do It

- Define a reference-index model that records path-based relationships across repos.
- Start with deterministic reference classes: imports, manifest paths, contract/schema paths, docs links, and launcher targets.
- Add commands to scan, persist, and inspect the index for a resolved workspace.

## Validation

- `rp` can answer which files or package contracts reference a given path.
- The index is reproducible from workspace state.
- Tests cover at least one cross-repo move scenario and one non-code reference type.
