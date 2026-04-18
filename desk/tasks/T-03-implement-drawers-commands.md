# T-03 - Implement `drawers` commands

- Type: implementation
- Domain: workflow
- Language: python
- Module: talk_extractor
- Phase: A
- Status: closed
- Priority: high
- Depends On:
  - T-01
- Pills:
  - PILL-01
  - PILL-06

## Goal
- Implement `drawers add`, `drawers list`, `drawers promote`, and `drawers audit`.

## Requested Artifacts
- `talk_extractor/cli_pkg/drawers_command.py`

## Constraints
- `drawers add <spec>` registers specs in `desk/drawers/Board.md`.
- `drawers promote <id>` moves items to `tasks/` or `pills/` with skeletons.

## Validation Contract
- Tests:
  - Verify `drawers list` output matches `Board.md`.
- Lint:
  - `python -m talk_extractor lint-constraints`

## Completion Evidence
- `talk_extractor/cli_pkg/drawers_command.py`
- commit: `c330f66`
