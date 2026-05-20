---
id: '012'
domain: manifest/repo
status: open
priority: p0
depends_on:
- '011'
created: ''
---

# Replace ad hoc manifest repo flow with `git-repo` ownership

## Objective

Stop fabricating manifest git state inside `rp` and move workspace materialization to an explicit `git-repo`-managed manifest source.

## Reference

- Board: `repopackage/desk/tasks/Board.md`
- Desk: `repopackage`

## What to Fix

- `src/repopackage/repo/manifest.py` currently initializes, commits, and resets a local manifest repo as an implementation detail.
- Branch assumptions such as forced `master` ownership should be removed.
- Manifest rendering, manifest publication, and workspace sync need separate responsibilities.

## Files Likely Involved

- `src/repopackage/repo/manifest.py`
- `src/repopackage/cli/handlers.py`
- `src/repopackage/core/models.py`
- `tests/test_cli_integration.py`
- `tests/test_handlers.py`

## How to Do It

- Split manifest rendering from manifest publication and workspace sync.
- Introduce explicit manifest-source configuration instead of hidden local git bootstrapping.
- Make `rp sync` consume a declared manifest source through `repo init` and `repo sync` without branch hardcoding.

## Validation

- No path in `rp sync` requires `git init`, fake local commits, or forced branch resets for manifest generation.
- Manifest source configuration is explicit and test-covered.
- A rendered manifest can be published and consumed by `git-repo` without hidden state.
