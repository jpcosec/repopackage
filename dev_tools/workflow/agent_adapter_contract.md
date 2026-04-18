# Agent Adapter Contract

## Purpose
- Defines per-tool normalization strategy.
- Transforms raw tool output into the normalized run package format.

## Normalized Run Package Layout

```text
runs/RUN-XXX/
  normalized/
    prompt.md
    context_snapshot.md
    journal.md
    result_manifest.json
    tool_metadata.json
  raw/
    tool_stdout.log
    tool_stderr.log
    native_transcript.*
  adapters/
    capture_report.json
```

## Per-Tool Adapter Strategy

### Claude

| Artifact | Source | Normalized To |
|----------|--------|---------------|
| prompt | transcript.json → prompt | normalized/prompt.md |
| output | transcript.json → response | normalized/result_manifest.json |
| steps | transcript.json → tool_use | normalized/journal.md |
| files | transcript.json → tool → source | normalized/tool_metadata.json |

**Normalization**:
- Extract from `transcript.json` the `prompt`, `response`, `tool_use` array
- Map each tool invocation to a journal entry
- Preserve file paths from `source_context`

### Gemini

| Artifact | Source | Normalized To |
|----------|--------|---------------|
| prompt | CLI argument or -p flag | normalized/prompt.md |
| output | stdout | normalized/result_manifest.json |
| steps | --verbose or log file | normalized/journal.md |
| metadata | model, temperature from CLI | normalized/tool_metadata.json |

**Normalization**:
- Parse CLI invocation for prompt
- Extract structured output from stdout
- Build journal from any available step logs

### OpenCode

| Artifact | Source | Normalized To |
|----------|--------|---------------|
| prompt | input message | normalized/prompt.md |
| output | tool results | normalized/result_manifest.json |
| steps | tool_calls observable | normalized/journal.md |
| files | file operations | normalized/tool_metadata.json |

**Normalization**:
- Capture input message as prompt
- Extract tool call sequence as journal
- Map file paths from read/write operations

### pi

| Artifact | Source | Normalized To |
|----------|--------|---------------|
| prompt | CLI argument | normalized/prompt.md |
| output | stdout | normalized/result_manifest.json |
| steps | log output | normalized/journal.md |
| context | passed files | normalized/context_snapshot.md |

**Normalization**:
- Parse `pi -p "..."` for prompt
- Extract stdout as result
- Build journal from log lines

## Adapter Output (capture_report.json)

```json
{
  "adapter_version": "1.0",
  "tool": "gemini",
  "run_id": "RUN-XXX",
  "normalization_status": "success",
  "normalized_files": [
    "normalized/prompt.md",
    "normalized/journal.md",
    "normalized/result_manifest.json",
    "normalized/tool_metadata.json"
  ],
  "raw_files_preserved": [
    "raw/stdout.log",
    "raw/stderr.log"
  ],
  "gaps_filled": [
    "context_snapshot inferred from task description"
  ],
  "unrecoverable": []
}
```

## Rules
- Each tool MUST have a documented adapter strategy.
- Adapters MUST preserve raw artifacts before normalization.
- Normalized files MUST follow agent_run_contract layout.
- If normalization fails, preserve raw and log gap in capture_report.json.