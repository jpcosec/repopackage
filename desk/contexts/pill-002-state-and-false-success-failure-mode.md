---
id: pill-002-state-and-false-success-failure-mode
title: 'Failure Mode: repopackage false success and stale state'
tags:
- system:repopackage
- topic:failure-mode
- topic:state
---

# Failure Mode: repopackage false success and stale state

ID: pill-002

## What

_Define the context or guardrail this pill carries._

Repackage commands must not report success unless the expected manifest, lockfile, workspace, or output state was actually produced and verified.

## Why

_Explain why this context matters for safe execution._

Stress-test tasks found commands that returned success while writing no lockfile, producing no output, or failing underneath with tool-specific tracebacks. This creates unsafe context for later subagents.

## When

_Describe when an agent should apply this pill._

Apply to tasks involving `rp resolve`, `sync`, `generate`, `exports`, `status`, graph output, compose validation, and any command with filesystem or lockfile side effects.

## Where

_Name the files, surfaces, or scope this pill applies to._

Primary owner surfaces:

- `tools/repopackage/src/repopackage/cli/`
- resolver/sync/generate/status handlers
- manifest, compose, and lockfile model code
- `tools/repopackage/tests/`

## How

_Describe the correct way to apply this guidance._

**Required Reads**

- Read the task file.
- Read this pill and `pill-001-rp-cli-control-plane.md`.
- Read the handler and state model named by the task.
- Read tests around expected state creation or command exit codes.

**Execution Boundary**

Fix the assigned command's state verification. Do not change the workspace ownership model unless the task is one of the redesign tasks and names that boundary.

**Validation Contract**

Run the command with a temp project. Verify exit code, user message, expected files, parseable JSON if requested, and absence of raw tracebacks. For false-success tasks, assert the command fails when expected state is missing.

**Drift Signals**

- Success message appears but expected file is missing.
- Status says clean when required inputs are absent.
- A command catches third-party tracebacks but loses actionable diagnostics.
- Tests assert text only and not resulting state.

## How Not

_Describe the shortcut or failure mode to avoid._

Do not turn failures into warnings with exit 0. Do not create empty placeholder outputs to satisfy existence checks. Do not hide missing external tools until mid-operation.
