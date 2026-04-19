# Workflow Ontology

## Purpose
- Provide a shared vocabulary for typed workflow artifacts.

## Core Axes
- Domain: problem space or bounded context
- Business Rule: invariant behavior within a domain
- Language: implementation or naming language
- Module Kind: standardized or normed
- Task Type: design | standardization | implementation | refactor | test | lint | integration | audit
- Pill Type: guardrail | decision | pattern | model | code | test | lint | workflow | domain-rule | business-rule
- Validation Type: unit | integration | e2e | semantic | lint

## Agent Tool Types
- claude
- gemini
- opencode
- pi

## Capture Mode
- cli: command-line execution
- api: programmatic execution
- interactive: interactive session

## Run Package
- normalized: standardized format (prompt.md, journal.md, result_manifest.json, tool_metadata.json)
- raw: tool-native output (stdout, stderr, transcripts)
- adapter: tool-specific normalization report

## Trace Types
- raw trace: uncaptured tool output
- normalized trace: standardized run package
- observable reasoning: visible tool summaries (not hidden CoT)

## Module Kinds
- standardized
  - reusable family with stronger contracts
- normed
  - domain-specific module with shared style and validation rules

## Hierarchy
- project
  - spec package
  - modules
    - files
    - phases

## Rules
- Use ontology terms consistently across contracts, boards, tasks, and pills.
- If a new type is introduced, this file must be updated.
