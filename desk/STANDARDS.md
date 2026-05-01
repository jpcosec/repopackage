# Repopackage Desk Standards

This `desk/` is the execution surface for `repopackage` work.

It exists to turn architectural intent into auditable implementation tasks.

---

## Purpose

Use this desk to:

- keep the current implementation roadmap explicit
- assign implementation tasks that a subagent can execute safely
- separate durable package docs from active work planning

Durable package knowledge belongs in `docs/`.
Execution planning belongs in `desk/`.

---

## Task Rules

1. Every active task must be listed in `desk/tasks/Board.md`.
2. Every task must point to a real file, command, or workflow in this repo.
3. Every task must define a concrete validation step.
4. If a task depends on another task, the dependency must be explicit.
5. If a behavior is still speculative, it belongs in a spec or RFC before implementation.

---

## What Counts As A Good Task

A good task for a subagent:

- has a narrow scope
- changes a real user-visible or system-visible behavior
- names the files likely involved
- defines how success is checked
- avoids mixing architecture design and code changes in one step

---

## Current Priority

The current priority is to make `repopackage` usable for a real multi-repo composition flow, not just architecturally attractive.

That means the desk should focus first on:

- reliable git inspection
- typed dependency specs
- real lockfile/workspace tracking
- non-stub `rp` commands
- a minimal real use case that proves the control-plane story
