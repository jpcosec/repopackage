---
id: '016'
domain: workspace/operations
status: open
priority: p1
depends_on:
- '015'
created: ''
---

# Add multi-repo branch, commit, push, and worktree operations

## Objective

Use `rp` to orchestrate routine multi-repo development operations that are currently done by hand, while leaving underlying git execution to git-aware tooling.

## Reference

- Board: `repopackage/desk/tasks/Board.md`
- Desk: `repopackage`

## What to Fix

- There is no coherent workflow for branch creation, worktree management, commit inspection, or coordinated push across resolved repos.
- Manual repo-by-repo work is still required even when `rp` already knows the composition graph.
- Operations should act on explicit target sets and surface partial failure clearly.

## Files Likely Involved

- `src/repopackage/cli/handlers.py`
- `src/repopackage/git/client.py`
- `src/repopackage/core/models.py`
- `tests/test_cli_integration.py`

## How to Do It

- Add orchestration commands for inventory-driven branch creation, worktree creation, commit staging summaries, and push planning.
- Use explicit selectors so operations can target one package, a dependency slice, or the whole workspace.
- Keep destructive operations gated behind clear preflight output.

## Validation

- `rp` can show and execute multi-repo operations from the resolved workspace model.
- Failures identify the exact repo and operation that broke.
- Worktree and branch commands do not depend on hardcoded repo paths.
