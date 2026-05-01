# turn-001

## Summary
- The user introduces the concept of a recursive composition system for Git repositories called "repopackage". The core idea is the "Composable Unit", which can act as a reusable module (Repopackage) or an assembler (Project).

## Intent
- Present the initial architectural vision and core components of the library to verify understanding and feasibility.

## Conversation Role
- proposal

## Semantic Contribution
- Defines the fundamental ontology: Composable Unit, Repopackage, Project.
- Introduces typed composition via Integration Contracts (exports/consumes).
- Distinguishes between Integration Contracts and Local Traits (internal vs external rules).
- Proposes a non-static versioning model using Central Lines (canonical) and Development Lines (contextual).
- Replaces static lockfiles with a dynamic Composition Index.
- Proposes Focus Worktrees for isolated unit development/testing.
- Establishes a recursive graph-based composition model.

## Artifacts
- `arctifacts/mermaid_turn001_diagrama-minimo.mmd` - CU/RP/PR relationships, draft
- `arctifacts/mermaid_turn001_grafo-composicional.mmd` - Sample ecosystem graph, draft
- `arctifacts/yaml_turn001_define-lo-que-el-paquete-promete-hacia-afuera.yaml` - Repopackage contract schema, draft
- `arctifacts/yaml_turn001_define-que-puede-conectarse-dentro-del-proyecto.yaml` - Project contract schema, draft
- `arctifacts/yaml_turn001_local-traits.yaml` - Contrast between integration and local traits, draft
- `arctifacts/yaml_turn001_necesitas-una-relacion-explicita.yaml` - Development lines mapping, draft
- `arctifacts/yaml_turn001_contextual-versions.yaml` - Central vs contextual versioning record, draft
- `arctifacts/yaml_turn001_composition-index.yaml` - Composition Index structure, draft
- `arctifacts/yaml_turn001_para-desarrollar-testear-un-repopackage-sin-contaminar-el-proyecto-real.yaml` - Focus worktree concept, draft
- `arctifacts/yaml_turn001_contrato.yaml` - Focus worktree example, draft
- `arctifacts/mermaid_turn001_composable-unit-composable-unit.mmd` - Recursive composition visualization, draft
- `arctifacts/yaml_turn001_por-eso-el-modelo-base-deberia-ser.yaml` - Composable Unit base model, draft
- `arctifacts/mermaid_turn001_diagrama-final-mas-limpio.mmd` - Comprehensive conceptual map, draft

## Decisions
- DEC-001 - Recursive Composition: The system is built on "Composable Units" that can be both Project and Repopackage. Status: proposed.
- DEC-002 - Typed Integration: Use contracts (exports/consumes) instead of just versions. Status: proposed.
- DEC-003 - Contextual Branching: Support parallel development lines per project. Status: proposed.

## Resulting State
- The system is defined as a recursive, typed composition framework for Git repositories using explicit contracts and contextual versioning.

## Evidence
- turn-001
- `arctifacts/mermaid_turn001_diagrama-minimo.mmd`
- `arctifacts/mermaid_turn001_grafo-composicional.mmd`
- `arctifacts/yaml_turn001_define-lo-que-el-paquete-promete-hacia-afuera.yaml`
- `arctifacts/yaml_turn001_define-que-puede-conectarse-dentro-del-proyecto.yaml`
- `arctifacts/yaml_turn001_local-traits.yaml`
- `arctifacts/yaml_turn001_necesitas-una-relacion-explicita.yaml`
- `arctifacts/yaml_turn001_contextual-versions.yaml`
- `arctifacts/yaml_turn001_composition-index.yaml`
- `arctifacts/yaml_turn001_para-desarrollar-testear-un-repopackage-sin-contaminar-el-proyecto-real.yaml`
- `arctifacts/yaml_turn001_contrato.yaml`
- `arctifacts/mermaid_turn001_composable-unit-composable-unit.mmd`
- `arctifacts/yaml_turn001_por-eso-el-modelo-base-deberia-ser.yaml`
- `arctifacts/mermaid_turn001_diagrama-final-mas-limpio.mmd`
