# Repopackage

A sophisticated Python toolkit for distilling AI conversations into structured engineering artifacts and managing a high-fidelity **Supervisor/Executor** development workflow.

## 🚀 Unified CLI

The `talk-extractor` CLI provides a hierarchical command structure to manage the entire development lifecycle:

- **`extract`**: Ingest raw AI transcripts and extract turns or structured artifacts (UML, YAML, etc.).
- **`standardize`**: Scaffold reusable modules and domain-specific normed components.
- **`drawers`**: Manage deferred specifications and design documents.
- **`desk`**: Orchestrate active work using automated task boards and context pills.
- **`exec`**: Execute agents on specific tasks with bound context.
- **`capture`**: Rescue and normalize agent run logs into structured evidence.
- **`eval`**: Run automated quality gates including tests, linting, and constraint audits.
- **`integrate`**: Merge verified artifacts into the project and manage rollbacks.

## 🛠 Development Workflow

This project adheres to a strict **Supervisor/Executor** model to ensure traceability and quality:

1.  **Atomization Ritual**: The Supervisor breaks design specs into atomic, executable tasks (`desk/tasks/`).
2.  **Pill Binding**: Rationale and constraints are encapsulated in **Context Pills** (`desk/pills/`).
3.  **Automated Tracking**: Use `talk-extractor desk board sync` to automatically maintain the project's state in `desk/tasks/Board.md`.
4.  **Execution Ritual**: Executors solve exactly one task per commit, verified by the local constraint linter.

## 📏 Quality Standards

We enforce the "Laws of Physics" for code structural integrity:
- **Functions**: Maximum 10 lines of code.
- **Files**: Maximum 80 lines of code.
- **Classes**: Maximum 50 lines of code.
- **Responsibility**: One entity per file; one responsibility per entity.

## 📂 Project Map

- `dev_tools/talk_extractor`: Primary CLI and logic engine.
- `dev_tools/workflow`: Formal data contracts and role instructions.
- `desk/`: The active workspace (Tasks, Pills, Drawers, Design).
- `modules/`: Standardized and Normed system components.
- `Raw/`: Input source material for extraction.

---

## 🚦 Getting Started

1. **Setup Environment**:
   ```bash
   export PYTHONPATH=$PYTHONPATH:$(pwd)/dev_tools
   ```
2. **Check Board Status**:
   ```bash
   python -m talk_extractor desk board sync && cat desk/tasks/Board.md
   ```
3. **Run Constraint Linter**:
   ```bash
   python -m talk_extractor eval lint-constraints
   ```
