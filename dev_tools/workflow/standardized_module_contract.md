# Standardized Module Contract

## Purpose
- Define reusable module families with stronger constraints and repeatable implementation shape.

## Base Module

```markdown
# STD-MODULE-XXX - <family>

- Family: cli | io | ui | agent | schema | other
- Language: <language>
- Required Interfaces:
  - <interface>
- Required Files:
  - `path or pattern`
- Approved Variants:
  - <variant>
- Forbidden Variants:
  - <variant>
- Test Contract:
  - TEST-XXX
- Lint Contract:
  - LINT-XXX

## Example Shape
- <shape description or snippet>
```

## Rules
- Standardized modules are reusable and enforce a stable contract.
- Deviations must be explicit and justified.
