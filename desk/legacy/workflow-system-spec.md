# Workflow System Spec

## Topic
- Unified development workflow from design distillation to phased execution.

## Problem Statement
- The system must convert ambiguous input material into durable specs, standardize reusable modules and rules, atomize execution safely, verify work through tests and linting, and preserve traceability across design, tasks, commits, and evaluation.

## Final State
- The workflow is a staged pipeline: `design input -> distillation -> standardization -> drawers -> promotion -> tasks/pills -> phased execution -> phase closure -> evaluation -> integration`.

## Core Concepts
- `desk` is the active top-level workspace and replaces legacy `plan` terminology.
- `drawers` stores deferred work and concrete specs/spec that are not yet executable tasks.
- `pills` are typed context units with explicit contracts and reuse semantics.
- `tasks` are executable units derived from promoted drawer material plus pills.
- `design distillation` is a formal ritual that transforms text inputs into specs.
- `projects` contain modules; modules contain files; files are implemented across phases.
- `standardized modules` are reusable patterns with stronger contracts.
- `normed modules` follow shared style/linting but remain domain-specific.

## Hierarchy
- Project
  - Spec package
  - Modules
    - Files
    - Phases
- Module kinds
  - standardized: CLI, IO adapters, Alpine UI patterns, agent frameworks, etc.
  - normed: domain-specific modules constrained by style, linting, and architecture rules

## Workflow Stages
- Design
  - Input can be a conversation, note set, transcript, or other text source.
  - A design ritual distills input into structured specs.
- Standardization
  - Identify reusable module patterns, guardrails, and contracts.
- Drawers
  - Persist concrete specs, spec, and deferred work until promoted.
- Promotion
  - Supervisor checks ambiguity, coverage, dependencies, and reusable pills.
- Task/Pill Generation
  - Convert promoted material into typed tasks and typed pills.
- Execution By Phases
  - Executor implements module/file work in explicit phases.
- Phase Closure
  - Verify tests, linting, artifacts, changelog, and context freshness.
- Evaluation
  - Confirm requested outcome, actual outcome, and traceability.
- Integration
  - Merge knowledge into code/docs/design; clean stale pills.

## Rituals

### 1. Initialization Ritual
- Atomize candidate work.
- Dedupe overlaps.
- Audit existing code, history, and artifacts.
- Bind pills.
- Refresh boards.

### 2. Design Ritual
- Accept raw design input.
- Distill it into specs, decisions, timelines, and curated artifacts.
- Rehouse durable outputs into `desk/drawers/specs/`.
- Identify reusable pills and promotion candidates.
- Reject ambiguity before execution starts.

### 3. Execution Ritual
- Validate test inventory.
- add/update tests.
- run required tests and lint gates.
- update changelog and boards.
- audit pills.
- commit atomically.

### 4. Phase Completion Ritual
- Run full quality gate.
- fix regressions.
- collapse redundant pills into code/docs.
- advance to next phase.

## Testing And Linting
- No task is complete without testing.
- Linting is a first-class verification mode, not an optional style pass.
- Every task and phase must declare required validation:
  - unit
  - integration
  - e2e
  - semantic
  - lint
- Standardized modules should define reusable validation recipes.
- Normed modules must at least satisfy project linting, style, and architectural checks.

## Typed Task Ontology
- Task types:
  - design
  - standardization
  - implementation
  - refactor
  - test
  - lint
  - integration
  - audit
- Required task fields:
  - id
  - type
  - domain
  - language
  - module
  - phase
  - dependencies
  - pills
  - requested artifacts
  - validation contract

## Agent Verification
- The system must verify not only output, but process fidelity.
- Desired evidence layers:
  - artifact existence
  - tests/lint logs
  - git traceability
  - reasoning trace or execution journal
- Agent reasoning storage should be handled as an execution journal, not raw hidden chain-of-thought.
- The preferred durable artifact is a structured trace:
  - task id
  - steps taken
  - files touched
  - tests/lints run
  - decisions made during execution
  - blockers encountered

## Transition Invariants
- No ambiguity may survive from design into execution.
- Drawer content must be promoted before it becomes executable work.
- Pills must be typed and contract-valid before binding to tasks.
- Tasks must belong to phases.
- Phase closure requires testing and linting.
- Evaluation must happen before integration.
- Integration must push durable knowledge into code/docs/design and remove stale context.

## Suggested Output Mapping For Conversation Distillation
- `semantic_output/specs.md` -> `desk/drawers/specs/<topic>/spec.md`
- `semantic_output/decisions.md` -> `desk/drawers/specs/<topic>/decisions.md`
- curated artifacts -> `desk/drawers/specs/<topic>/artifacts/`
- open questions -> `desk/drawers/Board.md` or candidate tasks

## Open Questions
- Exact durable format for execution journals.
- Whether reasoning traces are stored per task, per phase, or per agent run.
- Which module families qualify as standardized by default.
