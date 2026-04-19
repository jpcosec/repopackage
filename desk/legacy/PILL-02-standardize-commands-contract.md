# PILL-02 - Standardize Commands Contract

- Type: code
- Scope: module
- Domain: standardization
- Language: python
- Nature: implementation
- Status: active
- Reusable: yes
- Applies To:
  - `talk_extractor/cli_pkg/standardize_command.py`
- Why:
  - Define the interface for creating standardized and normed modules.
- Constraints:
  - `standardize create --standardized <name>`
  - `standardize create --normed <name>`
- Contract:
  - Support `--name`, `--domain`, `--language`, `--template`, `--rules`.
- Evidence:
  - `desk/design/cli-extension-spec.md`

## Code Pill Additions
- Artifact Kind: cli
- Required Interfaces: `talk_extractor.cli_pkg.command_types.CommandBase`
- Output Shape: Creates `modules/<kind>/<name>/module.yaml`.
