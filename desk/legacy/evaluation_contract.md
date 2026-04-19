# Evaluation Contract

## Purpose
- Define how completed work is judged before integration.

## Required Fields

```markdown
# EVAL-XXX - <title>

- Scope: task | phase | project
- Target: <id>
- Requested Outcome:
  - <outcome>
- Observed Outcome:
  - <outcome>
- Validation Evidence:
  - `path`
- Gaps:
  - <gap>
- Decision: pass | partial | fail | reopen
```

## Rules
- Evaluation happens after execution and before integration.
- Reopen work when observed outcome diverges materially from requested outcome.
