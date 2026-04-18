# T-09 - Final Workflow Enhancements

- Type: implementation
- Domain: workflow
- Language: python
- Module: talk_extractor
- Phase: B
- Status: closed
- Priority: medium
- Depends On:
  - T-06
  - T-07
- Pills:
  - PILL-01

## Goal
- Implement `integrate promote` command.
- Expand `agent_run_contract.md` with prompt provenance fields.
- Implement `CAPTURE-01` (agent-capture-instructions) and `AGENT-CAPTURE-01`.

## Requested Artifacts
- `talk_extractor/cli_pkg/integrate_promote_command.py`
- `dev_tools/workflow/agent_run_contract.md`
- `dev_tools/workflow/agent-capture-instructions.md`

## Constraints
- Follow the established hierarchical CLI structure.

## Validation Contract
- Tests:
  - Verify `talk-extractor integrate promote` command stub.
- Lint:
  - `python -m talk_extractor lint-constraints`

## Completion Evidence
- `talk_extractor/cli_pkg/integrate_promote_command.py`
- commit: `e8f527a`
