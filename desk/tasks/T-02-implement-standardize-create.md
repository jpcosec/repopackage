# T-02 - Implement `standardize create` command

- Type: implementation
- Domain: standardization
- Language: python
- Module: talk_extractor
- Phase: A
- Status: open
- Priority: high
- Depends On:
  - T-01
- Pills:
  - PILL-01
  - PILL-02

## Goal
- Implement the `standardize create` command to scaffold standardized and normed modules.

## Requested Artifacts
- `talk_extractor/cli_pkg/standardize_command.py`

## Constraints
- `standardize create --standardized <name>` creates `modules/standardized/<name>/`.
- `standardize create --normed <name>` creates `modules/normed/<name>/`.
- Must initialize `module.yaml`.

## Validation Contract
- Tests:
  - Manual verification of directory creation and `module.yaml` content.
- Lint:
  - `python -m talk_extractor lint-constraints`

## Completion Evidence
- `talk_extractor/cli_pkg/standardize_command.py`
- commit: `feat: #02 implement standardize create command`
