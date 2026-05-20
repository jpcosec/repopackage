---
id: '015'
domain: workspace/status
status: open
priority: p0
depends_on:
- '012'
created: ''
---

# Add workspace inventory and status model

## Objective

Give `rp` a real model of the local workspace so it can report which repos, branches, worktrees, commands, and resolved artifacts are currently materialized.

## Reference

- Board: `repopackage/desk/tasks/Board.md`
- Desk: `repopackage`

## What to Fix

- `rp` has no canonical inventory of the materialized workspace beyond a lockfile and minimal validation.
- There is no durable model for repo location, branch state, worktree membership, or installed command set.
- Status reporting needs to compare desired, resolved, and actual workspace state.

## Files Likely Involved

- `src/repopackage/core/models.py`
- `src/repopackage/cli/handlers.py`
- `src/repopackage/git/client.py`
- `tests/test_git_adapter.py`
- `tests/test_handlers.py`

## How to Do It

- Define workspace inventory models for repos, branches, worktrees, manifests, and managed commands.
- Make `rp status` and related commands read from that model instead of ad hoc checks.
- Ensure inventory can be rebuilt from local filesystem and git/repo state without manual bookkeeping.

## Validation

- `rp status` reports desired vs materialized state with concrete per-repo facts.
- Worktree, branch, and command inventory are visible in one canonical view.
- Tests cover drift between lockfile, manifest source, and workspace checkout.
