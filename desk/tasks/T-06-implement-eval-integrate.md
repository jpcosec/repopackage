# T-06 - Implement Evaluation and Integration commands

- Type: implementation
- Domain: workflow
- Language: python
- Module: talk_extractor
- Phase: A
- Status: done
- Priority: high
- Depends On:
  - T-05
- Pills:
  - PILL-01
  - PILL-08

## Goal
- Implement `eval test/lint/audit` and `integrate merge/promote`.

## Requested Artifacts
- `talk_extractor/cli_pkg/eval_command.py`
- `talk_extractor/cli_pkg/integrate_command.py`

## Constraints
- `integrate rollback` must revert code and docs to pre-integration state.

## Validation Contract
- Tests:
  - Verify rollback functionality in a test branch.
- Lint:
  - `python -m talk_extractor lint-constraints`

## Completion Evidence
- `talk_extractor/cli_pkg/integrate_command.py`
- commit: `3abf65e`
