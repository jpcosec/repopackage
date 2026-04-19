# Task Contract

## Purpose
- Define the canonical shape of one executable task.

## Required Structure

```markdown
# T-XXX - <title>

- Type: design | standardization | implementation | refactor | test | lint | integration | audit
- Domain: <domain>
- Language: <language>
- Module: <module name>
- Phase: <phase id>
- Status: open | in_progress | blocked | done
- Priority: low | medium | high | critical
- Depends On:
  - T-XXX
- Pills:
  - PILL-XXX

## Goal
- <clear executable goal>

## Requested Artifacts
- `path`

## Constraints
- <constraint>

## Validation Contract
- Tests:
  - <test contract reference>
- Lint:
  - <lint contract reference>
- Additional Checks:
  - <check>

## Completion Evidence
- `path`
- commit: `<hash or expected message>`
```

## Rules
- One task maps to one resolving commit.
- A task must belong to exactly one phase.
- A task cannot be executable if required pills are missing.
