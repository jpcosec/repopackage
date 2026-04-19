# Context Pills

This directory contains context pills bound to tasks. Pills provide rationale and constraints for task execution.

## Pill Types

| Type | Purpose |
|------|---------|
| `guardrail` | Constraints that must not be violated |
| `decision` | Why this approach over alternatives |
| `pattern` | Architectural pattern to follow |
| `model` | Data model or schema to use |
| `code` | Implementation guidance |
| `test` | Test requirements |
| `lint` | Lint requirements |
| `workflow` | Workflow-specific guidance |
| `domain-rule` | Domain invariant behavior |
| `business-rule` | Business invariant behavior |
| `warning` | When to NOT do something |
| `tip` | Quick operational hints |
| `reference` | Links to docs |
| `example` | Concrete code snippets |

## Lifecycle

```
Drafted → Bound to task → Audited after step →
  → Still needed? Keep.
  → Redundant with code/docs? Delete.
  → Complete. Knowledge flows to code/docs. Delete.
```

## Pill Status

- `draft`: newly created, not yet reviewed
- `active`: bound to task, in use
- `stale`: not used in 6 months, needs review
- `superseded`: replaced by newer pill
- `final`: knowledge now in code/docs, reference only

## Core Rules

- Pills are context, not truth. Code is truth.
- Pills must not restate code or durable docs unnecessarily.
- Pills are reusable across tasks when their scope and language match.
- Pills are typed and must follow explicit contracts.

---

## Existing Pills

See individual .md files in this directory.

## Shared Fields

Every pill must define:

```markdown
# PILL-XXX - <title>

- Type: guardrail | decision | pattern | model | code | test | lint | workflow | domain-rule | business-rule
- Scope: global | project | module | file | component | phase
- Domain: <domain name>
- Language: <en|es|python|typescript|...>
- Nature: context | implementation
- Status: active | stale | superseded | final
- Reusable: yes | no
- Applies To:
  - `path/or/module`
- Why:
  - <reason>
- Constraints:
  - <guardrail>
- Contract:
  - <what this pill guarantees>
- Evidence:
  - `path`
  - turn-XXX
```

## Type-Specific Additions

### Pattern Pill

- Pattern Shape:
  - <structure>
- Allowed Variants:
  - <variant>
- Forbidden Variants:
  - <variant>

### Code Pill

- Artifact Kind:
  - cli | io | ui | agent | schema | test | lint | other
- Required Interfaces:
  - <interface>
- Output Shape:
  - <artifact contract>

### Decision Pill

- Chosen Option:
  - <option>
- Rejected Options:
  - <option>

### Test Pill

- Verification Mode:
  - unit | integration | e2e | semantic | lint
- Pass Condition:
  - <condition>

### Lint Pill

- Rule Set:
  - <rules>
- Enforcement:
  - blocking | warning

## Ontology Notes

- `Domain` identifies the problem space.
- `Business Rule` identifies invariant behavior of the domain.
- `Language` identifies implementation or naming language.
- `Scope` identifies where reuse is valid.
