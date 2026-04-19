# Workflow System

A high-fidelity **Supervisor/Executor** framework for managing complex AI-driven development.

## 🏛 Foundation

The core logic and philosophy are defined in the `workflow/` directory:

- **[Philosophy](./workflow/philosophy.md)**: Kill the God-Agent by externalizing all reason.
- **[Ontology](./workflow/ontology.md)**: Taxonomy of Specs, Tasks, Pills, and Runs.
- **[Rituals](./workflow/rituals.md)**: Step-by-step algorithms for initialization, execution, and verification.
- **[Contracts](./workflow/contracts/)**: Canonical schemas for all workflow data.

## 🚀 The Redesign Phase

We are currently in a **Phase 0 Redesign**. The previous implementation has been moved to `legacy/`.

### Active Roadmap
1. **Define YAML Schemas**: Move state management to YAML for algorithmic consistency.
2. **Implement Bootstrapper**: A new `workflow init` command to deploy base templates.
3. **Purpose-Specific Hierarchy**: Refactor CLI logic into strictly isolated areas (Distill, Eval, Desk, etc.).

## 🛠 Project Map

- `workflow/`: Foundational documentation and contracts.
- `desk/`: Active work surface (Drawers, Tasks, Pills).
- `legacy/`: Previous implementation (reference only).
- `Raw/`: Input source material.
