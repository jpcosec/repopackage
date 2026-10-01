---
references:
- desk/tasks/Board.md
- repopackage
files:
- src/repopackage/cli/handlers.py
- src/repopackage/git/client.py
- src/repopackage/core/models.py
- tests/test_cli_integration.py
pills:
- desk/contexts/pill-001-rp-cli-control-plane.md
- desk/contexts/pill-001-current-desk-execution-gates.md
- desk/contexts/pill-002-modular-task-boundaries.md
id: '016'
domain: workspace/operations
status: open
priority: p1
depends_on:
- '015'
created: ''
---

# Add multi-repo branch, commit, push, and worktree operations

## Rationale

_Explain why this task exists or the business driver behind it._

## Goal

_Describe the concrete result this task must produce._

Use `rp` to orchestrate routine multi-repo development operations that are currently done by hand, while leaving underlying git execution to git-aware tooling.

## Scope

_State what is in scope and what is out of scope._

- There is no coherent workflow for branch creation, worktree management, commit inspection, or coordinated push across resolved repos.
- Manual repo-by-repo work is still required even when `rp` already knows the composition graph.
- Operations should act on explicit target sets and surface partial failure clearly.

## Implementation Path

_Outline the expected implementation route or affected surface._

- Add orchestration commands for inventory-driven branch creation, worktree creation, commit staging summaries, and push planning.
- Use explicit selectors so operations can target one package, a dependency slice, or the whole workspace.
- Keep destructive operations gated behind clear preflight output.

## Validation

_List the checks required before this task can close._

- `rp` can show and execute multi-repo operations from the resolved workspace model.
- Failures identify the exact repo and operation that broke.
- Worktree and branch commands do not depend on hardcoded repo paths.

## Done When

_Name the observable condition that makes the task complete._
