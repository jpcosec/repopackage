---
id: 8
domain: fixtures/e2e
status: open
priority: p1

created: "2026-05-01"
---

# Create real use case fixture

## Objective

Create a realistic multi-repo fixture that proves the intended composition model better than toy one-dependency examples.

## Reference

- `desk/SPEC.md`
- `compose.yaml`
- `tests/`

## What to Fix

The repo currently has examples, but not yet a clearly defined real delivery fixture for the core story.

## How to Do It

1. define a fixture project with at least two reusable repos
2. include one contextual branch case and one central-line case
3. make the fixture usable from tests

## Validation

- there is one canonical delivery fixture
- it exercises the control-plane story more realistically than the current dummy setup
