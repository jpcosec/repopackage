# Workflow Schema Audit

## Purpose
- Audit whether the current workflow documents define the contracts needed for each workflow data type.

## Present Schemas Or Partial Schemas

### 1. Agent Instructions
- Present in:
  - `dev_tools/workflow/AGENTS.md`
  - `dev_tools/workflow/instructions/*.md`
- Status:
  - partial
- Notes:
  - role behavior is described
  - no strict machine-readable contract for required sections/fields per instruction file

### 2. Context Pill
- Present in:
  - `dev_tools/WORKFLOW.md`
  - `dev_tools/workflow/desk/pills/README.md`
- Status:
  - strong partial
- Notes:
  - dimensions and shared contract exist
  - type-specific additions exist
  - still missing a canonical filename/id/location convention and a validation schema for all mandatory headings

### 3. Task Board
- Present in:
  - `dev_tools/WORKFLOW.md`
  - `dev_tools/workflow/desk/tasks/Board.md`
- Status:
  - present
- Notes:
  - board columns exist
  - still missing rules for row lifecycle, sorting, and exact status enum beyond section placement

### 4. Drawers Board
- Present in:
  - `dev_tools/WORKFLOW.md`
  - `dev_tools/workflow/desk/drawers/Board.md`
- Status:
  - present
- Notes:
  - enough for a first board contract
  - still missing promotion criteria schema and stale-review workflow in structured form

### 5. Semantic Spec
- Present in:
  - `dev_tools/talk_extractor/semantic_contracts.md`
  - `dev_tools/workflow/desk/drawers/specs/workflow-system-spec.md`
- Status:
  - present
- Notes:
  - `specs.md` contract is explicit
  - mapping into drawer/spec packages is defined conceptually, not yet as a canonical drawer spec contract

### 6. Decisions Log
- Present in:
  - `dev_tools/talk_extractor/semantic_contracts.md`
- Status:
  - present

### 7. Timeline
- Present in:
  - `dev_tools/talk_extractor/semantic_contracts.md`
- Status:
  - present

### 8. Per-Turn Semantic Record
- Present in:
  - `dev_tools/talk_extractor/semantic_contracts.md`
- Status:
  - present

### 9. Artifact Semantic Record
- Present in:
  - `dev_tools/talk_extractor/semantic_contracts.md`
- Status:
  - present

### 10. Manifest
- Present in:
  - `dev_tools/talk_extractor/semantic_contracts.md`
- Status:
  - present

## Missing Or Weak Schemas

### 1. Executable Task File Contract
- Missing
- Needed because:
  - tasks are central to execution but only the board schema is explicit
- Should define:
  - id
  - type
  - domain
  - language
  - module
  - phase
  - goal
  - dependencies
  - bound pills
  - requested artifacts
  - validation contract
  - completion evidence
  - commit expectation

### 2. Drawer Spec Package Contract
- Missing
- Needed because:
  - drawers now hold concrete specs and spec
- Should define package contents such as:
  - `spec.md`
  - `decisions.md`
  - `artifacts/`
  - `promotion.md`
  - `open_questions.md`
  - `source_manifest.json`

### 3. Design Input Contract
- Missing
- Needed because:
  - design ritual can accept conversations, notes, transcripts, and future inputs
- Should define:
  - source type
  - provenance
  - language
  - evidence files
  - distillation target

### 4. Standardized Module Contract
- Missing
- Needed because:
  - workflow distinguishes standardized vs normed modules
- Should define:
  - module family
  - required interfaces
  - approved variants
  - test recipe
  - lint recipe
  - example implementation shape

### 5. Normed Module Contract
- Missing
- Needed because:
  - many modules are not fully standardized but still require uniform outputs
- Should define:
  - applicable guardrails
  - style/lint requirements
  - architectural dependency rules

### 6. Phase Contract
- Missing
- Needed because:
  - tasks execute in phases and phases close with rituals
- Should define:
  - phase id
  - target modules/files
  - entry criteria
  - exit criteria
  - mandatory validations
  - commit policy

### 7. Test Contract
- Weak
- Current state:
  - workflow says tests are mandatory
  - no explicit schema for test obligations per task/module/phase
- Needed fields:
  - verification mode
  - command
  - scope
  - pass condition
  - invalidation policy

### 8. Lint Contract
- Weak
- Current state:
  - linting is mentioned in standards/specs but not formalized as workflow data
- Needed fields:
  - rule set
  - enforcement mode
  - command
  - exceptions policy
  - ownership scope

### 9. Execution Journal Contract
- Missing
- Needed because:
  - workflow wants to verify what the agent did and how it did it
- Should define:
  - task id
  - agent id
  - start/end time
  - steps executed
  - files touched
  - commands run
  - tests/lints run
  - blockers
  - reasoning summary
  - final evidence links

### 10. Promotion Contract
- Missing
- Needed because:
  - design -> standardization -> drawers -> tasks/pills must be unambiguous
- Should define:
  - source drawer item
  - promotion reason
  - generated tasks
  - generated pills
  - unresolved ambiguities
  - approving agent

## Recommended Next Contracts To Add
- Implemented in `contracts/`:
  - `task_contract.md`
  - `drawer_spec_contract.md`
  - `execution_journal_contract.md`
  - `phase_contract.md`
  - `test_contract.md`
  - `lint_contract.md`
  - `standardized_module_contract.md`
  - `design_input_contract.md`
  - `pill_contract.md`
  - `agent_run_contract.md`
  - `evaluation_contract.md`
  - `integration_contract.md`
  - `tasks_board_contract.md`
  - `drawers_board_contract.md`
  - `ontology.md`

## Summary
- The workflow now has explicit contracts for major workflow artifacts.
- Remaining work is mostly integration into `WORKFLOW.md`, `README.md`, role instructions, and eventual CLI support for validation and scaffolding.
