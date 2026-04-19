# Phase Contract

## Purpose
- Define one execution phase for a project or module.

## Required Fields

```markdown
# PHASE-XXX - <title>

- Scope: project | module
- Target:
  - <module or project>
- Entry Criteria:
  - <criterion>
- Exit Criteria:
  - <criterion>
- Tasks:
  - T-XXX
- Required Validation:
  - test contract
  - lint contract
- Commit Policy:
  - <policy>
```

## Rules
- A phase closes only after validation passes.
- A phase may not advance with unresolved critical blockers.
