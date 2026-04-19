# CLI vs Agent Boundary

## Purpose
- Separate workflow operations that can be safely standardized in CLI tooling from operations that require agent judgment.

## Good CLI Candidates

### Design Intake And Distillation
- ingest raw transcript or text input
- extract turns
- extract structured artifacts
- generate semantic scaffolds
- materialize `specs.md`, `decisions.md`, `timeline.md`, `manifest.json` shells
- relocate distilled outputs into `desk/drawers/specs/<topic>/`

### Desk Mechanics
- scaffold `desk/` structure
- create/update board templates
- validate task file shape
- validate pill file shape
- validate spec file shape
- promote drawer items into task/pill skeletons
- regenerate board indexes from task metadata

### Verification And Audit Support
- run tests
- run linting
- run semantic validators
- check artifact existence
- check clean tree status
- check commit-message shape
- check one-task/one-commit traceability heuristics

### Standardization Support
- scaffold standardized module templates
- scaffold phase folders/files
- scaffold execution journal files
- run schema/contract validation for all workflow data types

## Agent-Required Work

### Ambiguity Resolution
- deciding whether input is still ambiguous
- deciding what missing context must be created
- deciding whether a drawer item is mature enough for promotion

### Semantic Interpretation
- understanding what a conversation or note set is really about
- deciding what artifacts represent
- deciding which alternatives were truly rejected vs merely explored
- deciding final architectural state from evolving evidence

### Ontology And Modeling
- deciding task types, pill types, and domain boundaries in unclear cases
- deciding whether a module is standardized or only normed
- deciding business-rule boundaries across domains/languages

### Atomization
- breaking specs into the smallest useful executable tasks
- merging overlapping tasks and pills
- deciding which pills are reusable vs task-local

### Architecture And Standards
- deciding architectural guardrails
- deciding reusable patterns for CLI, IO, UI, agents, etc.
- deciding when to relax atomization in a future merging phase

### Evaluation
- deciding whether the delivered result satisfies the original intent
- deciding whether a task should be reopened, split, or integrated
- auditing whether an agent's execution journal is sufficient and truthful

## Hybrid Zone
- CLI can propose; agent must approve:
  - task promotion from drawers
  - pill generation from specs
  - candidate final artifacts
  - standardized module classification
  - missing-schema detection

## Boundary Rule
- If the operation is deterministic, repeatable, and contract-checkable, prefer CLI.
- If the operation requires interpreting meaning, resolving ambiguity, or making architectural tradeoffs, require agent judgment.
