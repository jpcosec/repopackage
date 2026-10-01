---
references:
- desk/tasks/Board.md
- repopackage
files:
- src/repopackage/repo/manifest.py
- src/repopackage/cli/handlers.py
- src/repopackage/core/models.py
- tests/test_cli_integration.py
- tests/test_handlers.py
pills:
- desk/contexts/pill-001-rp-cli-control-plane.md
- desk/contexts/pill-002-state-and-false-success-failure-mode.md
- desk/contexts/pill-001-current-desk-execution-gates.md
- desk/contexts/pill-002-modular-task-boundaries.md
id: '012'
domain: manifest/repo
status: open
priority: p0
depends_on:
- '011'
created: ''
---

# Replace ad hoc manifest repo flow with `git-repo` ownership

## Rationale

_Explain why this task exists or the business driver behind it._

## Goal

_Describe the concrete result this task must produce._

Stop fabricating manifest git state inside `rp` and move workspace materialization to an explicit `git-repo`-managed manifest source.

## Scope

_State what is in scope and what is out of scope._

- `src/repopackage/repo/manifest.py` currently initializes, commits, and resets a local manifest repo as an implementation detail.
- Branch assumptions such as forced `master` ownership should be removed.
- Manifest rendering, manifest publication, and workspace sync need separate responsibilities.

## Implementation Path

_Outline the expected implementation route or affected surface._

- Split manifest rendering from manifest publication and workspace sync.
- Introduce explicit manifest-source configuration instead of hidden local git bootstrapping.
- Make `rp sync` consume a declared manifest source through `repo init` and `repo sync` without branch hardcoding.

## Validation

_List the checks required before this task can close._

- No path in `rp sync` requires `git init`, fake local commits, or forced branch resets for manifest generation.
- Manifest source configuration is explicit and test-covered.
- A rendered manifest can be published and consumed by `git-repo` without hidden state.

## Done When

_Name the observable condition that makes the task complete._
