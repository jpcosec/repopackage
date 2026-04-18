# T-05 - Implement Execution and Capture commands

- Type: implementation
- Domain: workflow
- Language: python
- Module: talk_extractor
- Phase: A
- Status: open
- Priority: high
- Depends On:
  - T-01
  - T-04
- Pills:
  - PILL-01
  - PILL-05
  - PILL-07

## Goal
- Implement `exec run`, `exec dispatch`, `capture rescue`, and `capture normalize`.

## Requested Artifacts
- `talk_extractor/cli_pkg/exec_command.py`
- `talk_extractor/cli_pkg/capture_command.py`

## Constraints
- `capture rescue` must pull raw logs into `runs/RUN-XXX/raw/`.
- `capture normalize` must use adapters to generate `evidence.json`.

## Validation Contract
- Tests:
  - Verify directory structure of a captured run.
- Lint:
  - `python -m talk_extractor lint-constraints`

## Completion Evidence
- `talk_extractor/cli_pkg/exec_command.py`
- commit: `feat: #05 implement execution and capture commands`
