# T-01 - Refactor CLI for categories

- Type: refactor
- Domain: cli
- Language: python
- Module: talk_extractor
- Phase: A
- Status: open
- Priority: high
- Depends On:
- Pills:
  - PILL-01
  - PILL-03

## Goal
- Update `CliApp` to support the hierarchical command structure: `talk-extractor <category> <command>`.

## Requested Artifacts
- `talk_extractor/cli_pkg/app.py`

## Constraints
- Support nested subparsers for categories (`extract`, `standardize`, `design`, `eval`, `desk`, `exec`, `capture`, `integrate`).
- Maintain legacy top-level commands as aliases (e.g., `extract-turns`).

## Validation Contract
- Tests:
  - Verify `talk-extractor extract turns --help` and `talk-extractor extract-turns --help`.
- Lint:
  - `python -m talk_extractor lint-constraints`
- Additional Checks:
  - Verify `--help` output shows categories.

## Completion Evidence
- `talk_extractor/cli_pkg/app.py`
- commit: `refactor: #01 support hierarchical CLI categories and aliases`
