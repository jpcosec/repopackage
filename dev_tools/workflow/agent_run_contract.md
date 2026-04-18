# Agent Run Contract

## Purpose
- Preserve prompt provenance and execution context for an agent run.

## Required Layout

```text
runs/RUN-XXX/
  prompt.md
  context_snapshot.md
  journal.md
  result_manifest.json
```

## Required Meanings
- `prompt.md` - exact operator prompt given to the agent
- `context_snapshot.md` - instructions, pills, contracts, and task context used at start
- `journal.md` - structured execution trace, not hidden chain-of-thought
- `result_manifest.json` - outputs, validations, and completion status

## Required Fields
- run id
- agent id or role
- task id(s)
- prompt source
- prompt template id
- prompt version
- prompt hydration context
- prompt operator
- active instructions
- active contracts
- pills injected
- files touched
- commands run
- validations run
- outputs produced
- final status

## Rules
- Store prompt provenance, not raw hidden reasoning.
- Every executor run should be auditable through this package.
