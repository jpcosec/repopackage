# T-04 - Implement `desk` mechanics commands

- Type: implementation
- Domain: workflow
- Language: python
- Module: talk_extractor
- Phase: A
- Status: open
- Priority: high
- Depends On:
  - T-01
- Pills:
  - PILL-01
  - PILL-04

## Goal
- Implement `tasks atomize`, `pills inject`, `board sync`, and `board status`.

## Requested Artifacts
- `talk_extractor/cli_pkg/desk_command.py`

## Constraints
- `board sync` must regenerate `Board.md` from file metadata in `desk/tasks/`.

## Validation Contract
- Tests:
  - Verify `board sync` updates `Board.md` correctly.
- Lint:
  - `python -m talk_extractor lint-constraints`

## Completion Evidence
- `talk_extractor/cli_pkg/desk_command.py`
- commit: `feat: #04 implement desk mechanics commands`
