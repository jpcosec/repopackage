---
references:
- desk/tasks/Board.md
- repopackage
files:
- src/repopackage/cli/handlers.py
- src/repopackage/core/models.py
- src/repopackage/repo/
- tests/test_cli_integration.py
- tests/test_exports_handler.py
pills:
- desk/contexts/pill-001-rp-cli-control-plane.md
- desk/contexts/pill-001-current-desk-execution-gates.md
- desk/contexts/pill-002-modular-task-boundaries.md
id: '014'
domain: commands/entrypoints
status: open
priority: p1
depends_on:
- '013'
created: ''
---

# Install resolved commands as entrypoints

## Rationale

_Explain why this task exists or the business driver behind it._

## Goal

_Describe the concrete result this task must produce._

Generate and install executable launchers from the resolved command registry so local commands can be listed, verified, and invoked through one `rp`-managed surface.

## Scope

_State what is in scope and what is out of scope._

- `rp exports` reports commands but does not install or verify them.
- There is no workspace bin directory or launcher materialization contract.
- Entry point installation must work for Python and non-Python commands without mutating package-local `pyproject.toml` files.

## Implementation Path

_Outline the expected implementation route or affected surface._

- Add a command that materializes launchers from the canonical registry into a managed workspace bin.
- Generate wrappers with provenance comments or metadata so ownership is inspectable.
- Add listing and verification commands that show what is installed and whether the launcher still matches the resolved state.

## Validation

_List the checks required before this task can close._

- `rp` can list installed local commands from the managed registry.
- Installed launchers are reproducible from resolved state.
- Conflicting commands fail with a useful diagnosis instead of silent overwrite.

## Done When

_Name the observable condition that makes the task complete._
