# Execution Journal Contract

## Purpose
- Persist a durable, reviewable trace of how an agent executed a task.

## Base Journal

```markdown
# JOURNAL-XXX - <task title>

- Task: T-XXX
- Agent: <agent id or role>
- Start Time: <timestamp>
- End Time: <timestamp>
- Outcome: success | partial | blocked | failed

## Steps
- <step>

## Files Touched
- `path`

## Commands Run
- `<command>`

## Validations Run
- tests: <result>
- lint: <result>

## Reasoning Summary
- <reasoning>

## Decisions During Execution
- <decision>

## Blockers
- <blocker>

## Evidence
- `path`
- commit: `<hash or message>`
```

## Rules
- This is not raw hidden chain-of-thought.
- It is a structured execution trace.
- Every closed task should have a journal or equivalent structured trace.
