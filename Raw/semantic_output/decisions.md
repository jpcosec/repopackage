# Decisions

## DEC-001 - Recursive Composition Model
- Status: accepted
- Category: domain-model
- Summary: Treat every unit as a "Composable Unit" that can act as both an exporter and an assembler.
- Context: Traditional systems separate "projects" from "libraries" too strictly, preventing nested repository graphs.
- Options Considered:
  - Flat dependency list (npm style)
  - Recursive nodes (The chosen model)
- Chosen Option: Recursive nodes.
- Why: Allows infinite nesting where a project can be consumed as a module by a higher-level project.
- Consequences:
  - Requires a Graph-based solver (DAG).
  - Simplifies the object model to a single base type.
- Supersedes: none
- Supported By:
  - turn-001
  - `arctifacts/mermaid_turn001_composable-unit-composable-unit.mmd`

## DEC-002 - Typed Integration via YAML Contracts
- Status: accepted
- Category: architecture
- Summary: Use explicit Exports/Consumes contracts with path-based schemas instead of just version strings.
- Context: Version numbers don't guarantee interface compatibility, especially across different languages.
- Options Considered:
  - SemVer only
  - JSON/YAML Schema contracts
- Chosen Option: YAML contracts defining integration surfaces.
- Why: Provides mathematical certainty of compatibility before code is even downloaded.
- Consequences:
  - Enables pre-sync validation.
  - Requires a schema-aware matcher in the solver.
- Supersedes: none
- Supported By:
  - turn-002
  - turn-021
  - `arctifacts/yaml_turn001_define-lo-que-el-paquete-promete-hacia-afuera.yaml`

## DEC-003 - Contextual Development Lines
- Status: accepted
- Category: workflow
- Summary: Support project-specific branches ("Development Lines") that track back to a "Central Line".
- Context: Projects often need a custom version of a package that hasn't been merged to main yet.
- Options Considered:
  - Hard forks
  - Contextual branches in the same repo
- Chosen Option: Contextual branches managed via the Composition Index.
- Why: Maintains traceability and allows parallel evolution without the overhead of forks.
- Consequences:
  - The solver must prioritize contextual branches over canonical ones.
- Supersedes: none
- Supported By:
  - turn-001
  - turn-017
  - `arctifacts/yaml_turn001_necesitas-una-relacion-explicita.yaml`

## DEC-004 - Object Model Consolidation
- Status: accepted
- Category: domain-model
- Summary: Merge "Composable Unit" into "Repopackage" and make "Project" a specialized instance/subclass.
- Context: The initial CU/RP/PR hierarchy was redundant; every node is essentially a package.
- Options Considered:
  - 3-tier hierarchy (CU -> RP -> PR)
  - Unified base (Everything is a Repopackage)
- Chosen Option: Unified base.
- Why: Simplifies code implementation and aligns with the reality that "Projects" are just packages that own an assembly index.
- Consequences:
  - Reduced boilerplate in the Python implementation.
- Supersedes: none
- Supported By:
  - turn-015
  - turn-017
  - `arctifacts/plantuml_turn017_01.puml`

## DEC-005 - Implementation Stack (Python + NetworkX)
- Status: accepted
- Category: tooling
- Summary: Use Python for the CLI and `networkx` for the core graph logic.
- Context: The system is a Control Plane where I/O and graph theory are more important than execution speed.
- Options Considered:
  - Python
  - TypeScript
- Chosen Option: Python.
- Why: Better libraries for complex graph manipulation and YAML parsing with comment preservation.
- Consequences:
  - CLI performance is limited by Git/Network I/O.
- Supersedes: none
- Supported By:
  - turn-027
  - turn-035

## DEC-006 - Contract-First Workflow with Codegen
- Status: accepted
- Category: architecture
- Summary: Automatically generate runtime types (Pydantic/Zod) from the YAML contracts.
- Context: There is a risk of the abstract contract drifting from the actual source code.
- Options Considered:
  - Manual mapping
  - Automated Codegen
- Chosen Option: Automated Codegen via `compose generate`.
- Why: Forces the developer to satisfy the contract in their code, closing the gap between design and reality.
- Consequences:
  - Introduces a build step for the developer.
- Supersedes: none
- Supported By:
  - turn-029
