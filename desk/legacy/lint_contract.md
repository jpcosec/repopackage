# Lint Contract

## Purpose
- Define style, structure, and quality enforcement as workflow data.

## Required Fields

```markdown
# LINT-XXX - <title>

- Scope: file | module | project | phase
- Rule Set:
  - <rules>
- Command: `<command>`
- Enforcement: blocking | warning
- Exception Policy:
  - <policy>
- Evidence:
  - log
  - report path
```

## Rules
- Linting is first-class validation.
- Blocking lint contracts must pass before task or phase closure.
