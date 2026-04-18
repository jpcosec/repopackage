# T-08 - Implement Agent Capture Adapters

- Type: implementation
- Domain: capture
- Language: python
- Module: talk_extractor
- Phase: A
- Status: closed
- Priority: medium
- Depends On:
  - T-05
- Pills:
  - PILL-07

## Goal
- Implement the normalization adapters for different agents.

## Requested Artifacts
- `talk_extractor/semantic/adapters/claude_adapter.py`
- `talk_extractor/semantic/adapters/gemini_adapter.py`

## Constraints
- Must transform raw transcripts into the common `evidence.json` format.

## Validation Contract
- Tests:
  - Run adapters against sample transcripts and verify JSON output.
- Lint:
  - `python -m talk_extractor lint-constraints`

## Completion Evidence
- Adapter files in `talk_extractor/semantic/adapters/`
- commit: `ee16ffa`
