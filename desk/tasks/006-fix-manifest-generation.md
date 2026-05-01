---
id: 6
domain: manifest/sync
status: open
priority: p1

created: "2026-05-01"
---

# Fix manifest generation

## Objective

Make lockfile-to-manifest translation safe enough for real workspace materialization.

## Reference

- `docs/DIAGNOSIS.md`
- `src/repopackage/adapters/repo.py`

## What to Fix

Current manifest assumptions are too simplistic for the intended system.

## How to Do It

1. define accepted remote URL handling
2. fix fetch-path derivation
3. document what part is delegated to `google repo` and what part is custom

## Validation

- manifest generation produces coherent remotes/projects for supported URL forms
- behavior is documented and testable
