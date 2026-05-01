# Spec

## Topic
- **Repopackage**: A recursive, contract-based composition system for Git repositories that manages complex dependency graphs through typed interfaces and contextual development lines.

## Work Type
- Design, Architecture, Documentation.

## Problem Statement
- Traditional package managers and monorepos fail to handle systems where independent repositories must evolve in parallel across different project contexts. 
- Static lockfiles lack the semantic depth to manage project-specific branches ("Development Lines") without losing traceability to the canonical source ("Central Line").
- Cross-language dependencies often lack a unified, mathematical way to validate interface compatibility before runtime.

## Final State
- A Control Plane (CLI/Solver) that orchestrates a Directed Acyclic Graph (DAG) of **Composable Units**. 
- Each unit declares what it **Exports** and **Consumes** via YAML contracts. 
- The system manages physical materialization (VCS Sync) and static validation of I/O schemas (JSON Schema) to ensure that every project composition is "RESOLVED" and "COMPATIBLE" across all layers of recursion.

## Core Concepts
- **Composable Unit**: The atomic building block; acts as a **Repopackage** (exporter) or a **Project** (assembler).
- **Integration Contract**: A formal YAML definition of a unit's input/output surface (Exports/Consumes).
- **Local Traits**: Operational rules (linters, test runners) specific to a repo that are ignored by the integration solver.
- **Central Line**: The canonical branch (e.g., `main`) of a repository.
- **Development Line**: A contextual branch created for a specific project, allowing parallel evolution without breaking the global ecosystem.
- **Composition Index**: A dynamic replacement for lockfiles that tracks exact commits, branches, and contract versions for the entire graph.
- **Focus Worktree**: An ephemeral, isolated workspace for developing a single unit against mocked dependencies.

## Final Architecture
- **Language**: Python 3.x (chosen for I/O agility and rich graph/YAML libraries).
- **Graph Engine**: `networkx` for DAG construction, cycle detection, and topological sorting.
- **VCS Adapters**: Abstracted `GitAdapter` and `RepoAdapter` (for Google Repo integration) to handle remote/local history inspection.
- **Type System**: JSON Schema (Draft 7/2020-12) used as the language-neutral interface bridge.
- **Codegen Bridge**: `compose generate` command to produce Pydantic models (Python) or Zod schemas (TypeScript) directly from contracts.
- **Solver**: A top-down DFS resolver with constraint unificator for version ranges and schema compatibility.

## Final Artifacts
- `Raw/arctifacts/mermaid_turn001_diagrama-final-mas-limpio.mmd` - Comprehensive conceptual map.
- `Raw/arctifacts/plantuml_turn017_01.puml` - Final class/component model.
- `Raw/arctifacts/yaml_turn001_define-lo-que-el-paquete-promete-hacia-afuera.yaml` - Repopackage contract schema.
- `Raw/arctifacts/yaml_turn001_composition-index.yaml` - Logical structure of the resolved lockfile.

## Accepted Decisions
- **DEC-001 - Recursive Composition**: Everything is a "Composable Unit"; projects can be packages. (turn-001)
- **DEC-002 - Typed Integration Surface**: Use explicit Exports/Consumes instead of simple version numbers. (turn-002)
- **DEC-003 - Contextual Development Lines**: Support parallel branching tied to project contexts. (turn-001, turn-021)
- **DEC-004 - Control Plane Isolation**: The solver operates on metadata (Git hashes/YAML) before materializing code. (turn-021, turn-033)
- **DEC-005 - Contract-First Workflow**: Codegen (Pydantic/Zod) from YAML contracts to close the runtime gap. (turn-029)
- **DEC-006 - Project-Owned E2E**: End-to-End tests are the responsibility of the assembler node, not the modules. (turn-039)

## Open Questions
- **Circular Dependency Resolution**: MVP strictly forbids cycles (FAILED_CYCLE); future versions may allow runtime plugins.
- **URL Discovery**: Standardizing how transitive dependencies find their remote URLs (convention vs organization registry).

## Explicitly Rejected Or Not Chosen
- **Flat Monorepo**: Rejected because it forces tight coupling of lifecycles and history.
- **Standard SemVer-only Resolution**: Rejected because it lacks interface awareness across language boundaries.
- **Pure JSON Schemas**: Schemas are authored in YAML for better human legibility/comments but evaluated as JSON Schema internally. (turn-028)

## Evidence
- turns: 001, 002, 017, 021, 023, 027, 029, 033, 035, 037, 039, 041.
- artifacts: `mermaid_turn001_diagrama-final-mas-limpio.mmd`, `plantuml_turn017_01.puml`, `yaml_turn001_composition-index.yaml`, `yaml_turn001_define-lo-que-el-paquete-promete-hacia-afuera.yaml`.
