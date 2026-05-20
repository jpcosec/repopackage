---
id: '018'
domain: repair/moves
status: open
priority: p1
depends_on:
- '017'
created: ''
---

# Implement move and rename repair flow

## Objective

Let `rp` plan and repair structural changes such as moving or renaming files and directories without leaving the workspace in a blind broken state.

## Reference

- Board: `repopackage/desk/tasks/Board.md`
- Desk: `repopackage`

## What to Fix

- There is no command that plans a move, reports blast radius, rewrites deterministic references, and leaves a diagnosis for unresolved breakage.
- Manual moves are risky because imports, docs, contracts, launcher targets, and path-bound config can drift independently.
- Repair output should distinguish rewritten references from unresolved references that need human action.

## Files Likely Involved

- `src/repopackage/cli/handlers.py`
- `src/repopackage/core/`
- `src/repopackage/repo/`
- `tests/`

## How to Do It

- Add a repair-planning command that computes the impact of a move or rename before mutation.
- Implement deterministic rewrites for supported reference classes and emit unresolved diagnostics for the rest.
- Make the repair flow update workspace inventory and command registry if entrypoint paths move.

## Validation

- A planned move reports affected packages and reference counts before applying changes.
- Supported references are rewritten automatically and verified afterward.
- Unsupported references are surfaced in a structured diagnosis instead of being ignored.
