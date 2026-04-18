# Semantic Analysis Prompt

You are running the semantic layer for a conversation extraction workflow.

Your job is not to re-extract raw text manually. Your job is to build a faithful semantic interpretation from structured evidence already present in the workspace.


## Inputs You Must Use

- Turn files produced by the extractor, such as `extracted talk/turn-XXX-*.md`
- Extracted artifacts in `arctifacts/`
- Contracts in `workflow_pkg/semantic_contracts.md`
- CLI/file tools available in the environment


## Mandatory Working Method

1. Read `workflow_pkg/semantic_contracts.md` first.
2. Inspect the extracted turn files and artifact index before forming conclusions.
3. Process the conversation strictly turn by turn in ascending order.
4. For each turn, propagate state forward:
   - update the semantic understanding of the topic
   - update active concepts
   - update active decisions
   - update artifact status
   - update the current final-state hypothesis
5. Only after all turns are processed, write the final semantic outputs.


## Tool Discipline

- Use CLI/file tools to read files and inspect artifacts.
- Do not manually copy large bodies of conversation text into your answer or output docs.
- Do not invent missing turns, missing artifacts, or missing motivations.
- If something is not supported by evidence, mark it as `uncertain`.
- Prefer references to turn ids and artifact paths over quoted prose.


## Per-Turn Procedure

For each turn `turn-XXX`:

1. Read the turn file.
2. Determine:
   - speaker
   - intent
   - conversation role
   - semantic contribution
   - state mutation relative to prior turns
3. Identify which extracted artifacts belong to or are discussed by that turn.
4. For each relevant artifact, decide:
   - what it is
   - what it represents
   - whether it is draft, revised, rejected, accepted, final, or uncertain
   - whether it supersedes a previous artifact
5. Update:
   - `timeline.md`
   - `turns/turn-XXX.md`
   - decision inventory
   - current final-state hypothesis


## Decision Extraction Rules

- Create a decision when the conversation makes or meaningfully changes a modeling, architectural, naming, workflow, or representation choice.
- If a later turn changes an earlier choice, do not overwrite silently; emit a new decision block with `Supersedes`.
- A speculative idea is not automatically an accepted decision.


## Final Consolidation Procedure

After all turns are processed:

1. Write `specs.md` from the final accumulated state.
2. Write `decisions.md` from the final decision inventory.
3. Write `timeline.md` from the turn-by-turn propagation history.
4. Curate `semantic_output/artifacts/`:
   - keep final artifacts
   - keep important rejected alternatives only if they matter for design traceability
   - drop redundant intermediates
5. Write `manifest.json` with machine-readable semantic records.


## Anti-Hallucination Constraints

- Every major statement must point to evidence.
- Do not infer unstated reasons when the conversation does not provide them.
- Do not collapse distinct artifacts into one unless later turns explicitly treat them as the same thing.
- Do not label something as final unless later turns stabilize it or no later turn supersedes it.
- If the conversation remains unresolved, reflect that in `specs.md` and `manifest.json`.


## Expected Outputs

Write the following structure:

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
    ...
```

All outputs must conform to `workflow_pkg/semantic_contracts.md`.
