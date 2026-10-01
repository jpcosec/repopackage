# Repopackage — project brief

Legacy project brief from 2026-06-02. Its 5WH1+ sections were split into atoms
under `desk/atoms/`; what remains here is prose that does not answer a single
5WH1+ question and therefore is not atomizable as-is.

## Patterns

- **80/10 coding rule**: Every source file is capped at 80 lines, every function at 10 lines, enforced as a project standard.
- **Task-driven desk workflow**: Implementation is managed through `desk/tasks/Board.md` with concrete validation steps per task; changelog tracks resolved tasks by ID.
- **Contract-first integration**: Repos declare typed exports and compatibility requirements in `integration.contract.yaml`, validated at resolve time.
- **Lockfile-anchored composition**: `compose.lock.yaml` records the exact commit, branch, line, and compatibility status for every resolved dependency.
- **Dummy-repo fixture pattern**: Tests and examples use `/tmp/dummy_repos/` git fixtures for reproducible workspace scenarios.

## State of maturity

- `rp resolve`, `rp sync`, `rp validate`, and `rp status` commands exist with non-stub implementations.
- Lockfile generation and workspace validation produce real output against dummy-repo fixtures.
- Git adapter has URL hashing for cache paths and supports remote inspection.
- Solver has typed error hierarchy and semantic version constraint evaluation.
- Several hardened tasks completed through May 2026 (git adapter fix, dependency type specs, lockfile state, manifest generation, end-to-end composition flow, status command).
- Known gaps remain: git adapter does not yet implement reliable clone/fetch and nested tree reads; solver fabricates transitive URLs; malformed contracts are silently swallowed; several CLI commands are stubs under the surface; manifest generation has unsafe assumptions.

## Open questions

- Is there a real-world (non-fixture) multi-repo workspace being used to validate repopackage, or is it still exercised only against `/tmp/dummy_repos/`?
- The `compose.lock.yaml` shows both `packages:` and `repopackages:` top-level keys with identical entries — is this intentional duplication or a leftover from a schema migration?
- What is the relationship between `desk/atoms/` (new) and `desk/drawer/atoms/` (reference from deskops style) — should atoms live in both or is this the canonical location?
- When was the "redesign reset" triggered and what specifically changed in the architecture?
- Is there a plan to publish repopackage to PyPI, or is it intended only for internal hum-ecosystem use?

## References

- `desk/SPEC.md` — delivery specification with current gaps and acceptance criteria
- `desk/STANDARDS.md` — desk-level execution rules and priorities
- `STANDARDS.md` — project-wide 80/10 coding standards
- `pyproject.toml` — package metadata, dependencies, and build config
- `compose.yaml` / `compose.lock.yaml` — example project model and resolved lockfile
- `contracts/integration.contract.yaml` — contract schema for typed integration
- `src/repopackage/` — package source code
- `tests/` — pytest test suite (13 test files)
- `changelog.md` — task-resolution history
