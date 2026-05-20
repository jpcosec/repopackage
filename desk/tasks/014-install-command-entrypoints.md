---
id: '014'
domain: commands/entrypoints
status: open
priority: p1
depends_on:
- '013'
created: ''
---

# Install resolved commands as entrypoints

## Objective

Generate and install executable launchers from the resolved command registry so local commands can be listed, verified, and invoked through one `rp`-managed surface.

## Reference

- Board: `repopackage/desk/tasks/Board.md`
- Desk: `repopackage`

## What to Fix

- `rp exports` reports commands but does not install or verify them.
- There is no workspace bin directory or launcher materialization contract.
- Entry point installation must work for Python and non-Python commands without mutating package-local `pyproject.toml` files.

## Files Likely Involved

- `src/repopackage/cli/handlers.py`
- `src/repopackage/core/models.py`
- `src/repopackage/repo/`
- `tests/test_cli_integration.py`
- `tests/test_exports_handler.py`

## How to Do It

- Add a command that materializes launchers from the canonical registry into a managed workspace bin.
- Generate wrappers with provenance comments or metadata so ownership is inspectable.
- Add listing and verification commands that show what is installed and whether the launcher still matches the resolved state.

## Validation

- `rp` can list installed local commands from the managed registry.
- Installed launchers are reproducible from resolved state.
- Conflicting commands fail with a useful diagnosis instead of silent overwrite.
