# PILL-05 - Execution Journal Pattern

- Type: pattern
- Scope: global
- Domain: execution
- Language: en
- Nature: context
- Status: active
- Reusable: yes
- Applies To:
  - `runs/RUN-XXX/normalized/journal.json`
- Why:
  - Track agent process fidelity and decision history.
- Constraints:
  - Must include Task ID, Agent ID, Steps, Files touched, Commands run.
- Contract:
  - Machine-readable JSON compliant with `execution_journal_contract.md`.
- Evidence:
  - `desk/design/workflow-system-spec.md`

## Pattern Shape
- `journal`:
  - `meta`: {task_id, agent_id}
  - `steps`: []
  - `verifications`: []
  - `decisions`: []
