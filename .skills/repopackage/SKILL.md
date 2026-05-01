# Repopackage Skill

Repopackage is a recursive, contract-based composition system for Git repositories. It manages complex dependency graphs through typed interfaces and contextual development lines.

## Core Ontology

- **Composable Unit**: The atomic building block; can be a **Repopackage** (exporter) or a **Project** (assembler).
- **Integration Contract**: Formal YAML defining input/output surfaces (`exports`/`consumes`).
- **Development Line**: A contextual project-specific branch.
- **Central Line**: The canonical "global" version of a repository.
- **Composition Index**: The `compose.lock.yaml` representing the resolved graph.

## Common Rituals

### 1. Initializing a Project
When starting a new assembler node:
1. Run `rp init`.
2. Edit `compose.yaml` to add dependencies under `uses`.
3. Run `rp resolve` to generate the lockfile.

### 2. Resolving & Syncing
To materialize the workspace:
1. Run `rp resolve` to ensure the graph is valid and versions are satisfied.
2. Run `rp sync` to use Google Repo to checkout the repositories.
3. Run `rp validate` to ensure physical integrity.

### 3. Modifying a Contract
When changing an interface:
1. Update `contracts/integration.contract.yaml` in the provider repo.
2. Run `rp generate` to update local Pydantic/Zod types.
3. Run `rp resolve` in the consumer project to detect breaking changes before syncing.

## Directory Structure Rituals

- `contracts/`: Must contain `integration.contract.yaml`.
- `schemas/`: Must contain `.json` or `.yaml` schemas referenced in the contract.
- `workspace/`: The location where `rp sync` materializes packages.
- `__generated__/`: Immutable folder managed by `rp generate`.
