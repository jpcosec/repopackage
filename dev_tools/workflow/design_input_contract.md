# Design Input Contract

## Purpose
- Define the input package consumed by the Design Ritual.

## Base Design Input

```markdown
# DESIGN-INPUT-XXX - <title>

- Source Type: conversation | notes | transcript | issue-set | mixed
- Topic: <short topic>
- Domain: <domain>
- Language: <primary language(s)>
- Provenance:
  - <where it came from>
- Intent:
  - <what must be distilled>
- Evidence Files:
  - `path`
- Desired Outputs:
  - spec
  - decisions
  - artifacts
  - open questions
- Constraints:
  - <constraint>
- Ambiguities Known:
  - <ambiguity>
```

## Rules
- Input must reference concrete evidence files.
- Ambiguities must be explicit.
- No execution tasks are generated directly from raw input.
