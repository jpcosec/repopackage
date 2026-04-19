# Agent Capture Contract

## Purpose
- Defines how a tool delivers raw evidence of its execution.
- The "raw" layer before normalization.

## Capture Levels

| Level | Description | Examples |
|-------|-------------|----------|
| capturable | Directly accessible output | prompt, output, logs, command trace, touched files, timestamps |
| semi-capturable | Requires extraction | intermediate summaries, tool call traces, visible reasoning artifacts |
| non-capturable | Should not require | hidden chain-of-thought, internal tool state |

## Raw Artifact Types

- `tool_stdout.log` - standard output
- `tool_stderr.log` - standard error
- `native_transcript.*` - tool-specific transcript format (html, md, json)
- `native_metadata.*` - tool-specific metadata (json, yaml)
- `command_trace.log` - exact commands executed
- `file_touch_log.txt` - files read/written during run

## Capture Requirements

Each tool MUST provide:
1. Invocation command used
2. Timestamps (start, end)
3. Exit status
4. stdout/stderr capture
5. Files accessed during execution

## Tool-Specific Raw Locations

| Tool | Raw Location | Format |
|------|--------------|--------|
| Claude | ~/.claude/sessions/*/transcript.json | json, html |
| Gemini | gemini CLI logs | md, json |
| OpenCode | tool output streams | md, json |
| pi | pi CLI output | md, txt |

## Contract

```json
{
  "run_id": "RUN-XXX",
  "tool": "gemini",
  "mode": "cli",
  "invocation": "gemini -p '...' --model 2.5-flash",
  "timestamp_start": "2026-04-18T10:00:00Z",
  "timestamp_end": "2026-04-18T10:05:00Z",
  "exit_status": "success",
  "raw_artifacts": [
    "runs/RUN-XXX/raw/gemini/stdout.log",
    "runs/RUN-XXX/raw/gemini/stderr.log",
    "runs/RUN-XXX/raw/gemini/command.log"
  ],
  "capture_gaps": [
    "no native step trace available"
  ]
}
```

## Rules
- Never attempt to capture hidden internal reasoning.
- Always capture observable artifacts: logs, transcripts, command traces.
- If a tool provides visible intermediate summaries, capture those as semi-capturable.
- Store raw artifacts before normalization.