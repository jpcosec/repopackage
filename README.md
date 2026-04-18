# Repopackage

A sophisticated Python toolkit for distilling AI conversations into structured engineering artifacts and managing a high-fidelity **Supervisor/Executor** development workflow.

## 🚀 Unified CLI

The `workflow` CLI provides a hierarchical command structure to manage the entire development lifecycle:

- **`system`**: Initialize project structure (`workflow init`).
- **`distill`**: Ingest AI transcripts and extract turns/artifacts (formerly talk-extractor).
- **`standardize`**: Scaffold reusable or normed modules.
- **`drawers`**: Manage deferred specifications and design documents.
- **`desk`**: Orchestrate active work with automated boards and pills.
- **`exec`**: Execute agents on tasks with bound context.
- **`capture`**: Rescue and normalize agent run logs.
- **`eval`**: Run quality gates (test, lint, constraints).
- **`integrate`**: Merge verified artifacts and manage rollbacks.

## 🛠 Getting Started

1. **Initialize Project**:
   ```bash
   ./workflow init
   ```
2. **Check Board Status**:
   ```bash
   ./workflow desk board sync && cat desk/tasks/Board.md
   ```
3. **Run Constraint Linter**:
   ```bash
   ./workflow eval constraints
   ```
