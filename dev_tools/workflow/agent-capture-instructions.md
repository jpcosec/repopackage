# Agent Capture Instructions

## Mission
- Reliably extract raw execution evidence from agent sessions and package it for normalization.

## Inputs
- Agent session transcript (native format)
- Execution logs (stdout/stderr)
- File system delta (touched files)
- Command history

## Procedure
1. Identify the session ID and target `run_id`.
2. Locate native tool transcripts (e.g., Claude's JSON, Gemini's CLI logs).
3. Export transcripts and logs to `runs/RUN-XXX/raw/`.
4. Enumerate all files modified or created during the run.
5. Record the exact invocation command used.
6. Verify all "Required Meanings" from `agent_capture_contract.md` are present.

## Outputs
- Raw capture package in `runs/RUN-XXX/raw/`
- Capture manifest conforming to `agent_capture_contract.md`

## Rules
- Do not filter or summarize at this stage.
- Do not capture hidden internal reasoning.
- Prioritize completeness over cleanliness in the raw layer.
- Ensure timestamps are in UTC.
