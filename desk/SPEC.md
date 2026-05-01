# Repopackage Delivery Spec

This file defines the implementation target that current desk tasks should serve.

---

## Product Goal

`repopackage` should act as a deterministic control plane on top of Git and `google repo` for multi-repo workspaces.

It should not replace Git.
It should not replace `google repo`.
It should add the missing composition logic above them.

---

## Real Use Case

We want to assemble a real project workspace from reusable repos where:

- one shared UI repo is reused by multiple projects
- one diagnostics repo is reused by multiple projects
- each reusable repo keeps a canonical central line
- a project may pin a contextual development line for one dependency without affecting other projects
- the final workspace can be materialized deterministically
- the resulting state can be validated and inspected

### Example

Project `main-project` uses:

- `ui-kit` on a contextual line `feat/project-a-nav`
- `code-quality-auditor` on its central line

Another project may use the same `ui-kit` from central or from a different contextual line.

The system must:

1. resolve those choices explicitly
2. record them in `compose.lock.yaml`
3. materialize a workspace from that resolved state
4. validate compatibility and physical integrity
5. expose enough status to understand whether the workspace matches the resolved state

---

## Minimal Feature Slice To Deliver

The minimum credible slice is:

1. `rp resolve` works on actual repos without pre-cloning assumptions
2. dependency specs are typed enough to represent `url`, `branch`, `version`, and `line`
3. `compose.lock.yaml` records selected packages, branches, commits, and compatibility status
4. `rp validate` checks the materialized workspace against the lockfile and contracts
5. `rp status` is no longer a stub and can report desired vs resolved vs materialized state

`rp generate` and `rp graph` may remain simpler than their eventual vision, but they should not be fake commands if advertised.

---

## What Is Currently Missing

The current implementation still has known gaps:

- git adapter does not implement reliable clone/fetch and nested tree reads
- solver fabricates transitive URLs
- malformed contracts are swallowed silently
- dependency specs are under-typed
- several `rp` commands are still stubs
- manifest generation has unsafe assumptions
- workspace tracking semantics are not yet documented cleanly in code

These are implementation blockers, not polish items.

---

## Non-Goals For This Delivery

Do not try to solve everything at once.

Out of scope for the first delivery slice:

- full ecosystem-wide `rp` command aggregation
- generalized `config_store` extraction
- advanced promotion/merge automation across contextual lines
- complete graph visualization sophistication

The first delivery should prove that `repopackage` can resolve, lock, materialize, validate, and report on a real multi-repo workspace.

---

## Acceptance Criteria

The first delivery is good enough when:

1. a real `compose.yaml` with at least two dependencies resolves cleanly
2. the lockfile contains exact commits and meaningful compatibility results
3. workspace materialization uses a reproducible manifest flow
4. validation can detect missing packages or missing contracts
5. status can explain the current workspace state without placeholder output

---

## Subagent Guidance

If this work is delegated to a subagent, the subagent should:

- prefer small, verifiable implementation steps
- treat `docs/DIAGNOSIS.md` as real backlog input
- avoid introducing hidden fallback behavior
- make failures explicit when contract or resolution data is incomplete
- update tests with every behavior change
