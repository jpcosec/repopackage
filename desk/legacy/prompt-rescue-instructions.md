# Prompt Rescue Instructions

## Purpose
- Capture observable evidence from an agent execution.
- Do NOT capture hidden chain-of-thought; capture only observable artifacts.

## When to Run
- After any agent run (Claude, Gemini, OpenCode, pi)
- Before evaluation phase
- As part of execution trace ritual

## Rescue Ritual Steps

### 1. Snapshot Phase
Before running the agent:
```bash
mkdir -p runs/RUN-XXX/raw/[TOOL]
```
Capture:
- Prompt to be sent → `raw/prompt_input.txt`
- Active instructions in scope → `raw/active_instructions.md`
- Context pills loaded → `raw/context_snapshot.md`
- Command to be executed → `raw/command.sh`

### 2. Execution Phase
Run agent with capture:
```bash
# Example for Gemini
gemini -p "$(cat prompt.txt)" 2>&1 | tee runs/RUN-XXX/raw/gemini/stdout.log
```

### 3. Rescue Phase
After execution, capture:
- `raw/tool_stdout.log` - stdout captured during run
- `raw/tool_stderr.log` - stderr captured during run
- `raw/exit_status.txt` - exit code
- `raw/timestamp_start.txt` - start time
- `raw/timestamp_end.txt` - end time
- Any native transcript files

### 4. Normalize Phase
Transform to normalized format:
```
runs/RUN-XXX/normalized/
  prompt.md        # cleaned prompt
  context_snapshot.md  # instructions + pills
  journal.md       # observable execution steps
  result_manifest.json  # outputs and status
  tool_metadata.json    # tool, version, mode
```

### 5. Report Phase
Create adapter report:
```json
// runs/RUN-XXX/adapters/capture_report.json
{
  "run_id": "RUN-XXX",
  "tool": "gemini",
  "status": "complete",
  "normalized": [...],
  "raw_preserved": [...],
  "gaps": [...]
}
```

## What NOT to Capture
- Internal tool reasoning
- Hidden chain-of-thought
- Tool-specific internal state

## What TO Capture
- Prompt sent
- Output received
- Commands executed
- Files touched
- Logs generated
- Timestamps
- Exit status
- Observable tool call sequences

## Contract Reference
- `contracts/agent_run_contract.md` - normalized format
- `contracts/agent_capture_contract.md` - raw capture
- `contracts/agent_adapter_contract.md` - per-tool normalization