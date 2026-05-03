---
id: 008
domain: fixtures/e2e
status: done
priority: p1
depends_on:
- '001'
- '002'
- '004'
- '006'
created: ''
---

# Create real use case fixture

## Objective

CLI-managed task materialized from the desk board source of truth.

## Reference

- Board: `repopackage/desk/tasks/Board.md`
- Desk: `repopackage`

## What to Fix

- Domain: `fixtures/e2e`
- Priority: `p1`
- Status: `done`

## How to Do It

Use the repo tests, changelog, and board workflow managed by the CLI.

## Validation

Run the relevant repo tests and keep the board plus changelog in sync.
