---
id: '013'
domain: commands/registry
status: open
priority: p0
depends_on:
- '011'
created: ''
---

# Build canonical command registry

## Objective

Make `rp` the canonical registry for commands exported by resolved packages, regardless of whether those commands are Python entrypoints or other executable forms.

## Reference

- Board: `repopackage/desk/tasks/Board.md`
- Desk: `repopackage`

## What to Fix

- Command export data exists in contracts, but there is no canonical resolved registry.
- There is no collision policy for duplicate command names or aliases.
- There is no provenance model that explains which package owns an installed command.

## Files Likely Involved

- `src/repopackage/core/models.py`
- `src/repopackage/core/solver.py`
- `src/repopackage/contracts/integration.contract.yaml`
- `src/repopackage/cli/handlers.py`
- `tests/test_export_surface.py`

## How to Do It

- Define a resolved command-registry model in lock/workspace state.
- Merge command exports during resolution with explicit precedence and collision rules.
- Capture provenance, runtime type, launcher target, alias ownership, and verification metadata.

## Validation

- The resolved graph emits one canonical command registry.
- Duplicate command ownership is detected deterministically.
- Tests cover Python and non-Python command descriptors.
