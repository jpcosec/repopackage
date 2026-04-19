# PILL-03 - CLI Category Refactoring

- Type: guardrail
- Scope: module
- Domain: cli
- Language: python
- Nature: context
- Status: active
- Reusable: yes
- Applies To:
  - `talk_extractor/cli_pkg/app.py`
- Why:
  - Moving from flat to hierarchical CLI requires refactoring `CliApp`.
- Constraints:
  - Support nested subparsers for categories.
  - Maintain legacy top-level commands as aliases.
- Contract:
  - `talk-extractor extract turns` must be equivalent to `talk-extractor extract-turns`.
- Evidence:
  - `desk/design/cli-extension-spec.md`
