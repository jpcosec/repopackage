# PILL-01 - CLI Command Structure

- Type: pattern
- Scope: project
- Domain: cli
- Language: python
- Nature: context
- Status: active
- Reusable: yes
- Applies To:
  - `talk_extractor/cli.py`
  - `talk_extractor/cli_pkg/`
- Why:
  - Establish a unified command hierarchy for the workflow.
- Constraints:
  - Follow the structure: `talk-extractor <category> <command>`.
- Contract:
  - Commands must support `--help`, `--verbose`, and `--dry-run`.
- Evidence:
  - `desk/design/cli-extension-spec.md`

## Pattern Shape
- `talk-extractor`
  - `extract`
  - `standardize`
  - `drawers`
  - `desk`
  - `exec`
  - `capture`
  - `eval`
  - `integrate`

## Allowed Variants
- Category names must be lowercase.

## Forbidden Variants
- Flat command names like `extract-turns` as primary commands (must be `extract turns`).
