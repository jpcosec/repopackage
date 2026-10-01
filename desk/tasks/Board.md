# Repopackage Tasks Board

## Current State Summary

- Objective: redesign `rp` into the control plane for local multi-repo development, command installation, and repairable workspace evolution
- Current blocker: `rp` still mixes composition policy with ad hoc manifest git state and lacks a canonical workspace command/control model
- Immediate focus: hand ownership of materialization to `git-repo`, centralize exported commands, and define a repair path for moves and renames
- Constraint: no legacy-preservation work unless it directly serves the new target

## Delivery Phases

### Phase 1 - Reset the control plane boundary
- `desk/tasks/011-redefine-rp-ownership-boundaries.md`
- `desk/tasks/012-replace-ad-hoc-manifest-repo-flow.md`

### Phase 2 - Centralize command ownership
- `desk/tasks/013-build-command-registry.md`
- `desk/tasks/014-install-command-entrypoints.md`

### Phase 3 - Own workspace orchestration
- `desk/tasks/015-add-workspace-inventory-and-status.md`
- `desk/tasks/016-add-multi-repo-operations.md`

### Phase 4 - Make structural change repairable
- `desk/tasks/017-index-cross-repo-references.md`
- `desk/tasks/018-implement-move-and-rename-repair-flow.md`

### Phase 5 - Stress-test corrections (Round 01 findings)
- `desk/tasks/001-fix-rp-init-silent-overwrite-and-permission-errors.md`
- `desk/tasks/002-fix-rp-resolve-false-success.md`
- `desk/tasks/003-fix-rp-sync-crash-and-error-messages.md`
- `desk/tasks/004-add-help-descriptions-to-all-commands.md`
- `desk/tasks/005-add-version-flag-and-format-json-support.md`
- `desk/tasks/006-fix-rp-generate-and-rp-exports-producing-no-output.md`
- `desk/tasks/007-fix-error-messages-tracebacks-to-user-friendly.md`
- `desk/tasks/008-fix-rp-graph-for-standalone-projects-and-add-flags.md`
- `desk/tasks/009-add-input-validation-for-compose-yaml.md`
- `desk/tasks/010-fix-rp-status-exit-code-and-output-consistency.md`
- `desk/tasks/011-fix-test-suite-1-failing-test.md`

## Active

| ID | Domain | Task | Priority | Depends On |
|----|--------|------|----------|------------|
| 011 | architecture/ownership | Redefine `rp` ownership boundaries | p0 | none |
| 012 | manifest/repo | Replace ad hoc manifest repo flow with `git-repo` ownership | p0 | 011 |
| 013 | commands/registry | Build canonical command registry | p0 | 011 |
| 014 | commands/entrypoints | Install resolved commands as entrypoints | p1 | 013 |
| 015 | workspace/status | Add workspace inventory and status model | p0 | 012 |
| 016 | workspace/operations | Add multi-repo branch, commit, push, and worktree operations | p1 | 015 |
| 017 | repair/index | Index cross-repo references for structural repair | p0 | 011, 015 |
| 018 | repair/moves | Implement move and rename repair flow | p1 | 017 |
| 001 | repopackage/cli | Fix rp init silent overwrite and permission errors | p0 | none |
| 002 | repopackage/resolve | Fix rp resolve false success (lockfile not written) | p0 | none |
| 003 | repopackage/sync | Fix rp sync crash and error messages | p0 | none |
| 004 | repopackage/cli | Add --help descriptions to all commands | p1 | none |
| 005 | repopackage/cli | Add --version flag and --format json support | p1 | none |
| 006 | repopackage/generate | Fix rp generate and rp exports producing no output | p1 | none |
| 007 | repopackage/cli | Fix error messages (tracebacks → user-friendly) | p1 | none |
| 008 | repopackage/graph | Fix rp graph for standalone projects and add flags | p2 | none |
| 009 | repopackage/validation | Add input validation for compose.yaml | p1 | none |
| 010 | repopackage/cli | Fix rp status exit code and output consistency | p2 | none |
| 011 | repopackage/tests | Fix test suite (1 failing test) | p1 | 002 |

## Blocked

| ID | Domain | Task | Priority | Depends On |
|----|--------|------|----------|------------|
| - | - | none | - | - |

## Working Rules

1. Keep all redesign planning in `desk/tasks/` until the new control-plane target stabilizes.
2. Do not preserve legacy workflow or compatibility shims unless a current task explicitly requires them.
3. Make `git-repo` the owner of workspace materialization; `rp` should own policy, registries, and orchestration.
4. Do not add command-installation behavior without a collision policy, provenance model, and verification path.
5. Structural move or rename automation must ship with diagnosis and repair output, not just best-effort rewriting.
