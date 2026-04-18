# Agent Brief

Use `talk_extractor/prompts/semantic_analysis.md` and `talk_extractor/semantic_contracts.md` as the operating contract.
Use `talk_extractor/CONSTRAINTS.md` as the code-structure constraint contract.

## Workspace
- Conversation source: `Talk.md`
- Extracted turns: `extracted talk`
- Extracted artifacts: `arctifacts`
- Semantic output target: `semantic_output`

## Required Process
1. Read `talk_extractor/semantic_contracts.md`.
2. Read `talk_extractor/prompts/semantic_analysis.md`.
3. Process turn files in `extracted talk` in ascending order.
4. Use `arctifacts/index.md` plus individual artifacts as evidence.
5. Fill `semantic_output/specs.md`, `semantic_output/decisions.md`, `semantic_output/timeline.md`, `semantic_output/turns/`, and curate `semantic_output/artifacts/`.
6. Update `semantic_output/manifest.json` with the final semantic state.
