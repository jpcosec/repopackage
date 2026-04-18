# Normed Module Contract

## Purpose
- Define modules that are not fully standardized but must remain stylistically and architecturally uniform.

## Required Fields

```markdown
# NORM-MODULE-XXX - <module>

- Domain: <domain>
- Language: <language>
- Guardrails:
  - <guardrail>
- Dependency Rules:
  - <rule>
- Style/Lint Contract:
  - LINT-XXX
- Test Contract:
  - TEST-XXX
```

## Rules
- Normed modules may vary in internals.
- They must still satisfy shared guardrails, linting, and validation.
