---
id: 1
domain: git-adapter
status: done
priority: p0

created: "2026-05-01"
---

# Fix git adapter for real repo inspection

## Objective

Make the git adapter capable of resolving commits and reading contract files from real repositories, including nested paths.

## Reference

- `docs/DIAGNOSIS.md`
- `src/repopackage/adapters/git.py`
- `tests/test_git_adapter.py`

## What to Fix

Current failures include:

- no clone/fetch behavior for repos not already on disk
- broken nested tree traversal
- incorrect blob access in `read_file`

## How to Do It

1. define the cache/clone strategy
2. fix tree walking and blob resolution
3. update tests to cover missing-repo and nested-contract reads

## Validation

- a non-precloned repo can be resolved into a commit hash
- `contracts/integration.contract.yaml` can be read from nested tree paths
- failures are explicit instead of misleading
