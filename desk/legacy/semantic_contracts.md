# Semantic Contracts

This file defines the required output contracts for the semantic layer built on top of turn and artifact extraction.

The goal is to make the semantic pass:
- turn-aware
- evidence-based
- incremental
- reproducible
- resistant to hallucination


## Global Rules

- Every semantic claim must be grounded in at least one turn id, artifact file, or both.
- Do not copy large conversation spans manually into the semantic docs unless quoting is necessary.
- Prefer references to paths and turn ids over duplicated content.
- Mark uncertainty explicitly with `Status: uncertain`.
- Distinguish between:
  - `proposed`
  - `revised`
  - `rejected`
  - `accepted`
  - `final`
- Treat the conversation as a stateful evolution, not as a bag of unrelated messages.
- Later turns may supersede earlier artifacts or decisions; preserve that lineage explicitly.


## Output Folder Contract

The semantic layer writes into a separate folder, recommended name: `semantic_output/`.

Required structure:

```text
semantic_output/
  specs.md
  decisions.md
  timeline.md
  manifest.json
  turns/
    turn-001.md
    turn-002.md
    ...
  artifacts/
    <curated final artifacts>
```


## `specs.md` Contract

Purpose: consolidated final state of the conversation.

Required sections, in this exact order:

```markdown
# Spec

## Topic
- One sentence describing what the conversation is about.

## Work Type
- One or more of: design, feature, architecture, refactor, research, debugging, extraction, documentation.

## Problem Statement
- What problem the conversation is trying to solve.

## Final State
- What the final model/design/proposal is by the end of the conversation.

## Core Concepts
- Bullet list of the final domain concepts.

## Final Architecture
- Bullet list describing the final architecture.

## Final Artifacts
- Bullet list of artifact paths that represent the final state.

## Accepted Decisions
- Bullet list of decision ids from `decisions.md` that ended accepted/final.

## Open Questions
- Items still unresolved by the conversation.

## Explicitly Rejected Or Not Chosen
- Alternatives that were discussed and not selected, with short reason.

## Evidence
- Bullet list of turn ids and artifact paths supporting the spec.
```

Rules:
- `Final State` must describe the end state, not the whole exploration.
- `Final Artifacts` should list only curated artifacts, not every extracted artifact.
- `Explicitly Rejected Or Not Chosen` must mention why, if the reason is present.


## `decisions.md` Contract

Purpose: architectural and semantic decision log.

Each decision must use this exact block format:

```markdown
## DEC-XXX - <short title>
- Status: proposed | revised | rejected | accepted | final | uncertain
- Category: domain-model | architecture | artifact-shape | workflow | naming | tooling | other
- Summary: <one sentence>
- Context: <why the decision came up>
- Options Considered:
  - <option A>
  - <option B>
- Chosen Option: <chosen option or `none`>
- Why: <reason>
- Consequences:
  - <impact 1>
  - <impact 2>
- Supersedes: DEC-XXX | none
- Supported By:
  - turn-XXX
  - `path/to/artifact`
```

Rules:
- If a later turn changes a previous decision, create a new decision block and set `Supersedes`.
- Do not collapse multiple materially different decisions into one block.
- If the conversation explores but never settles, keep the status as `proposed` or `uncertain`.


## `timeline.md` Contract

Purpose: explain what happened over time.

Each turn entry must use this exact block format:

```markdown
## turn-XXX
- Speaker: user | assistant | unknown
- Intent: <what this turn is trying to do>
- What Happened:
  - <event 1>
  - <event 2>
- State Change:
  - Added: <concepts/artifacts/decisions>
  - Revised: <concepts/artifacts/decisions>
  - Rejected: <concepts/artifacts/decisions>
  - Finalized: <concepts/artifacts/decisions>
- Artifacts Mentioned:
  - `path/to/artifact`
- Decisions Touched:
  - DEC-XXX
- Evidence:
  - turn-XXX
  - `path/to/artifact`
```

Rules:
- `timeline.md` must cover every extracted turn in order.
- `State Change` must describe mutation relative to previous turns.
- Empty categories are allowed, but the keys must still appear.


## `turns/turn-XXX.md` Contract

Purpose: semantic interpretation of a single turn.

Each file must use this exact structure:

```markdown
# turn-XXX

## Summary
- One short paragraph.

## Intent
- What this turn is trying to achieve.

## Conversation Role
- One of: exploration, clarification, proposal, revision, correction, consolidation, finalization.

## Semantic Contribution
- Bullet list of what this turn adds or changes.

## Artifacts
- `path/to/artifact` - what it is, what it represents, status

## Decisions
- DEC-XXX - how this turn affects that decision

## Resulting State
- What is true after this turn that was not true before.

## Evidence
- turn-XXX
- `path/to/artifact`
```

Rules:
- The `Artifacts` section must explain meaning, not just list file names.
- `Resulting State` must be incremental.


## Artifact Semantic Record Contract

Every curated artifact in `semantic_output/artifacts/` must have a semantic record in `manifest.json`.

Each record must contain these fields:

```json
{
  "artifact_id": "ART-XXX",
  "path": "semantic_output/artifacts/...",
  "source_path": "arctifacts/...",
  "turn": "turn-XXX",
  "kind": "plantuml|mermaid|yaml|python|json|typescript|csv|...",
  "title": "short human label",
  "represents": "what this artifact is",
  "role": "diagram|contract|implementation-sketch|data-model|example|other",
  "status": "draft|intermediate|final_candidate|final|rejected|uncertain",
  "supersedes": ["ART-XXX"],
  "decision_ids": ["DEC-XXX"],
  "evidence": ["turn-XXX", "arctifacts/..."]
}
```

Rules:
- `status` is mandatory and must reflect semantic position in the conversation.
- `represents` must describe meaning, not syntax.
- Use `supersedes` when a later artifact replaces an earlier one.


## `manifest.json` Contract

Purpose: machine-readable summary of the semantic pass.

Required top-level structure:

```json
{
  "topic": "string",
  "work_type": ["design", "architecture"],
  "source": {
    "conversation": "Talk.md",
    "turn_count": 0,
    "artifact_count": 0,
    "curated_artifact_count": 0
  },
  "final_state": {
    "summary": "string",
    "accepted_decisions": ["DEC-001"],
    "final_artifacts": ["semantic_output/artifacts/..."],
    "open_questions": ["string"]
  },
  "decisions": [],
  "artifacts": [],
  "turns": []
}
```

Rules:
- `decisions` must list all decision ids with status.
- `turns` must list all turn ids with role and one-line summary.
- `final_artifacts` must be a strict subset of curated artifacts.


## Curated Artifact Selection Contract

Only copy an artifact into `semantic_output/artifacts/` if at least one of these is true:

- it represents the final accepted design
- it represents a major discarded alternative worth preserving
- it is explicitly discussed as important in later turns
- it supersedes earlier versions and should be the canonical retained artifact

Do not copy an artifact just because it exists.


## Evidence Reference Contract

Use these identifiers consistently:

- turn ids: `turn-001`, `turn-002`, ...
- decision ids: `DEC-001`, `DEC-002`, ...
- artifact ids: `ART-001`, `ART-002`, ...

Paths must be repo-relative and clickable where possible.
