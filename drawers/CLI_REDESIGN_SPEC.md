# Spec: Workflow CLI Redesign

## Goal
Implement a rational, drift-proof CLI for managing the Supervisor/Executor development lifecycle.

## Context
- **Philosophy**: Kill the God-Agent by externalizing all rationale into durable Context Pills.
- **Language**: Python 3.
- **State Storage**: Move from Markdown tables to YAML for internal logic (algorithmic ease).
- **Templates**: Enforce usage of base templates for all workflow artifacts.

## Implementation Roadmap

### 1. Data Layer (YAML Schemas)
- Define `task_schema.yaml` and `pill_schema.yaml`.
- Tasks and Pills will be stored as individual YAML files for machine-readability.
- Generate `Board.md` from YAML state for human visibility.

### 2. Core Mechanics (System Area)
- **`workflow init`**: 
    - Scaffold folders: `desk/{tasks,pills,drawers,design}`, `modules/`, `runs/`.
    - Deploy base templates from `workflow/contracts/`.

### 3. Design Distillation (Distill Area)
- Re-implement `extract-turns` and `extract-artifacts` using logic from `legacy/`.
- **`workflow distill scaffold-workspace`**: Create the evidence index for agent passes.

### 4. Backlog Management (Drawers Area)
- **`workflow drawers defer-spec`**: Move ambiguous inputs to backlog.
- **`workflow drawers promote-spec`**: Algorithmic conversion of Spec -> Task using YAML templates.

### 5. Execution & Verification (Exec/Capture/Eval Areas)
- **`workflow exec run-agent`**: The "Cage" builder. Automate context injection.
- **`workflow capture normalize-trace`**: Convert raw logs to `evidence.json` via Adapters.
- **`workflow eval lint-laws`**: Enforce the Laws of Physics (line limits, SRP).

### 6. Integration Area
- **`workflow integrate merge-verified`**: Move code from Run to Source and update Changelog.

## Next Immediate Steps
1. Atomize this spec into `T-01`, `T-02`, etc.
2. Draft the YAML templates for Tasks and Pills.
