---
references:
- desk/tasks/Board.md
- repopackage
files:
- src/repopackage/core/models.py
- src/repopackage/cli/handlers.py
- src/repopackage/git/client.py
- tests/test_git_adapter.py
- tests/test_handlers.py
pills:
- desk/contexts/pill-001-rp-cli-control-plane.md
- desk/contexts/pill-002-state-and-false-success-failure-mode.md
- desk/contexts/pill-001-current-desk-execution-gates.md
- desk/contexts/pill-002-modular-task-boundaries.md
id: '015'
domain: workspace/status
status: open
priority: p0
depends_on:
- '012'
created: ''
---

# Add workspace inventory and status model

## Rationale

_Explain why this task exists or the business driver behind it._

## Goal

_Describe the concrete result this task must produce._

Give `rp` a real model of the local workspace so it can report which repos, branches, worktrees, commands, and resolved artifacts are currently materialized.

## Scope

_State what is in scope and what is out of scope._

- `rp` has no canonical inventory of the materialized workspace beyond a lockfile and minimal validation.
- There is no durable model for repo location, branch state, worktree membership, or installed command set.
- Status reporting needs to compare desired, resolved, and actual workspace state.

## Implementation Path

_Outline the expected implementation route or affected surface._

- Define workspace inventory models for repos, branches, worktrees, manifests, and managed commands.
- Make `rp status` and related commands read from that model instead of ad hoc checks.
- Ensure inventory can be rebuilt from local filesystem and git/repo state without manual bookkeeping.

## Validation

_List the checks required before this task can close._

- `rp status` reports desired vs materialized state with concrete per-repo facts.
- Worktree, branch, and command inventory are visible in one canonical view.
- Tests cover drift between lockfile, manifest source, and workspace checkout.

## Done When

_Name the observable condition that makes the task complete._
