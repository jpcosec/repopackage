---
references:
- desk/tasks/Board.md
- repopackage
files:
- src/repopackage/core/models.py
- src/repopackage/core/solver.py
- src/repopackage/contracts/integration.contract.yaml
- src/repopackage/cli/handlers.py
- tests/test_export_surface.py
pills:
- desk/contexts/pill-001-rp-cli-control-plane.md
- desk/contexts/pill-001-current-desk-execution-gates.md
- desk/contexts/pill-002-modular-task-boundaries.md
id: '013'
domain: commands/registry
status: open
priority: p0
depends_on:
- '011'
created: ''
---

# Build canonical command registry

## Rationale

_Explain why this task exists or the business driver behind it._

## Goal

_Describe the concrete result this task must produce._

Make `rp` the canonical registry for commands exported by resolved packages, regardless of whether those commands are Python entrypoints or other executable forms.

## Scope

_State what is in scope and what is out of scope._

- Command export data exists in contracts, but there is no canonical resolved registry.
- There is no collision policy for duplicate command names or aliases.
- There is no provenance model that explains which package owns an installed command.

## Implementation Path

_Outline the expected implementation route or affected surface._

- Define a resolved command-registry model in lock/workspace state.
- Merge command exports during resolution with explicit precedence and collision rules.
- Capture provenance, runtime type, launcher target, alias ownership, and verification metadata.

## Validation

_List the checks required before this task can close._

- The resolved graph emits one canonical command registry.
- Duplicate command ownership is detected deterministically.
- Tests cover Python and non-Python command descriptors.

## Done When

_Name the observable condition that makes the task complete._
