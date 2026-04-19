# Project AGENTS Contract

This workspace operates under a strict **Supervisor / Executor** split.

## Roles & Protocols

### 1. Supervisor (Orchestrator)
- **Mission:** Protect the "laws of physics" of the project and manage atomization.
- **Rules:** 
  - Never implement `src/` code directly.
  - Audit all tasks (Phase A/B) before dispatch.
  - Verify that each commit maps 1:1 to an atomic task.
- **Reference:** `workflow/docs/supervisor_instructions.md`

### 2. Executor (Worker)
- **Mission:** Solve exactly ONE task from `desk/tasks/`.
- **Rules:**
  - Follow the context pills and the task description strictly.
  - Add unit tests for every change.
  - Document all `Induced Changes` in the task file.
- **Reference:** `workflow/docs/executor_instructions.md`

## Workflow Authority
The documentation under `workflow/` is the absolute source of truth for all agents in this repository.
