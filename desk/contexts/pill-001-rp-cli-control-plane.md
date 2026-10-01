---
id: pill-001-rp-cli-control-plane
title: 'Pattern: keep rp fixes inside the control-plane boundary'
tags:
- system:repopackage
- topic:cli
- topic:control-plane
---

# Pattern: keep rp fixes inside the control-plane boundary

ID: pill-001

## What

_Define the context or guardrail this pill carries._

This pill gives a fresh subagent the minimum context needed to execute a repopackage task without drifting into broad workspace redesign.

## Why

_Explain why this context matters for safe execution._

The active redesign separates policy, registry, orchestration, and repair from low-level checkout/materialization. Stress-test fixes can accidentally reintroduce ad hoc manifest or repo state handling.

## When

_Describe when an agent should apply this pill._

Apply to tasks that touch `rp init`, `resolve`, `sync`, `generate`, `exports`, `graph`, `status`, compose validation, or CLI help/version/error behavior.

## Where

_Name the files, surfaces, or scope this pill applies to._

Primary owner files:

- `tools/repopackage/src/repopackage/cli/`
- `tools/repopackage/src/repopackage/` command handlers and models named by the task
- manifest, lockfile, compose, and command registry files named by the task
- `tools/repopackage/tests/`

## How

_Describe the correct way to apply this guidance._

Validate command behavior at the CLI boundary. Keep errors actionable, avoid silent success, and make filesystem writes explicit and recoverable.

**Required Reads**

- Read the assigned task file.
- Read this pill.
- Read `tools/repopackage/desk/tasks/Board.md` only for dependency and active redesign boundary.
- Read the command handler/model files named by the task.

**Execution Boundary**

Keep `rp` responsible for policy, registries, orchestration, status, and repair. Do not make it silently own low-level checkout/materialization if the task is only about CLI correctness. For redesign tasks, preserve the control-plane boundary before adding behavior.

**Validation Contract**

Run the command named by the task. Verify exit code, stdout/stderr, generated files, lockfile/manifest changes, and no false success. For JSON support, parse the output.

**Drift Signals**

- The executor starts changing workspace architecture while fixing a CLI traceback.
- `rp resolve` or `rp status` reports success without writing or verifying the expected state.
- Error handling catches everything and hides actionable failure causes.
- A repair/index task changes command installation behavior without a dependency task.

## How Not

_Describe the shortcut or failure mode to avoid._

Do not hide failures behind zero exit codes. Do not duplicate materialization ownership or preserve legacy flow unless an active task explicitly requires it. Do not add compatibility shims for obsolete manifests unless the task names them.
