# Test Contract

## Purpose
- Define required verification for tasks, modules, and phases.

## Required Fields

```markdown
# TEST-XXX - <title>

- Mode: unit | integration | e2e | semantic
- Scope: file | module | project | phase
- Command: `<command>`
- Pass Condition:
  - <condition>
- Failure Policy:
  - fix | block | invalidate old tests
- Evidence:
  - log
  - report path
```

## Rules
- Every executable task must reference at least one test contract unless explicitly exempted.
- Invalidated tests must be updated or deleted before completion.
