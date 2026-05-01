# Timeline

## turn-001
- Speaker: user
- Intent: Introduce the vision for "repopackage".
- What Happened:
  - User presented the core concept of recursive Composable Units.
- State Change:
  - Added: Concepts of Repopackage, Project, Central/Development Lines, Composition Index.
- Artifacts Mentioned:
  - `arctifacts/mermaid_turn001_diagrama-minimo.mmd`
  - `arctifacts/yaml_turn001_composition-index.yaml`
- Decisions Touched:
  - DEC-001, DEC-002, DEC-003
- Evidence:
  - turn-001

## turn-002
- Speaker: assistant
- Intent: Synthesize and formalize the vision.
- What Happened:
  - Assistant organized the concepts into four architectural pillars.
- State Change:
  - Finalized: Initial ontology and system purpose.
- Artifacts Mentioned:
  - none
- Decisions Touched:
  - DEC-001, DEC-002
- Evidence:
  - turn-002

## turn-003 to turn-008
- Speaker: user & assistant
- Intent: Visualize the hierarchy.
- What Happened:
  - Exploration of how to draw nested components in PlantUML.
- State Change:
  - Revised: Representation of "Projects containing packages" vs "Units interacting via interfaces".
- Artifacts Mentioned:
  - `arctifacts/plantuml_turn006_01.puml`
  - `arctifacts/plantuml_turn008_01.puml`
- Evidence:
  - turn-008

## turn-009 to turn-017
- Speaker: user & assistant
- Intent: Refine and consolidate the object model.
- What Happened:
  - The user requested merging "Composable Unit" into "Repopackage".
- State Change:
  - Finalized: Object model where Project is a specialized Repopackage.
- Artifacts Mentioned:
  - `arctifacts/plantuml_turn017_01.puml`
- Decisions Touched:
  - DEC-004
- Evidence:
  - turn-017

## turn-018 to turn-021
- Speaker: assistant
- Intent: Define the operational model.
- What Happened:
  - Assistant defined the CLI commands (`init`, `sync`, `resolve`, `validate`) and the physical file names.
- State Change:
  - Added: Operational lifecycle (Pre-sync vs Post-sync validation).
- Artifacts Mentioned:
  - none (inline YAML definitions)
- Decisions Touched:
  - DEC-002
- Evidence:
  - turn-021

## turn-022 to turn-025
- Speaker: assistant
- Intent: Detail the implementation of the Solver.
- What Happened:
  - Discussion of GitAdapters and the recursive DFS algorithm for version/contract unificator.
- State Change:
  - Added: Technical strategy for reading contracts without full checkouts.
- Evidence:
  - turn-023

## turn-026 to turn-029
- Speaker: user & assistant
- Intent: Bridge the gap to actual source code.
- What Happened:
  - User requested "contract interpretation" tools (Pydantic/Zod).
- State Change:
  - Added: "Contract-First" workflow via Codegen.
- Decisions Touched:
  - DEC-005, DEC-006
- Evidence:
  - turn-029

## turn-030 to turn-041
- Speaker: user & assistant
- Intent: Finalize complex scenarios (Pipelines, E2E).
- What Happened:
  - Clarified that E2E tests belong to the Project node. Finalized the Solver logic using `networkx`.
- State Change:
  - Finalized: Recursive E2E verification model and DAG-based resolution.
- Decisions Touched:
  - DEC-005
- Evidence:
  - turn-035, turn-039, turn-041

## turn-042
- Speaker: user
- Intent: Conclusion.
- What Happened:
  - User states the system is ready for development.
- State Change:
  - Finalized: Whole system specification.
- Evidence:
  - turn-042
