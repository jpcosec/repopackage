# Pill Contract

## Purpose
- Define the canonical schema for all pill types.

## Base Pill

```markdown
# PILL-XXX - <title>

- Type: guardrail | decision | pattern | model | code | test | lint | workflow | domain-rule | business-rule
- Scope: global | project | module | file | component | phase
- Domain: <domain>
- Language: <language>
- Nature: context | implementation
- Status: active | stale | superseded | final
- Reusable: yes | no
- Applies To:
  - `path`
- Why:
  - <reason>
- Constraints:
  - <constraint>
- Contract:
  - <guarantee>
- Evidence:
  - `path`
```

## Pattern Pill Additions
- Pattern Shape
- Allowed Variants
- Forbidden Variants

## Code Pill Additions
- Artifact Kind
- Required Interfaces
- Output Shape

## Decision Pill Additions
- Chosen Option
- Rejected Options

## Test Pill Additions
- Verification Mode
- Pass Condition

## Lint Pill Additions
- Rule Set
- Enforcement

## Rules
- Pills are context, not source of truth.
- Type-specific fields are mandatory when the type applies.
