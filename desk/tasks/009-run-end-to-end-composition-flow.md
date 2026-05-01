---
id: 9
domain: e2e
status: open
priority: p1

created: "2026-05-01"
---

# Run end-to-end composition flow

## Objective

Prove the first real delivery slice from compose definition through validation.

## Reference

- `desk/SPEC.md`
- `desk/tasks/008-create-real-use-case-fixture.md`

## What to Fix

The architecture is only credible once the intended flow works on a real multi-repo fixture.

## How to Do It

1. resolve the fixture project
2. inspect the lockfile
3. materialize the workspace
4. validate it
5. inspect status output

## Validation

- the whole flow works on the canonical fixture
- the result is auditable through lockfile, workspace, validation, and status output
