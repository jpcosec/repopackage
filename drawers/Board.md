# Drawers Board

> **Deferred work surface.** Items here wait for prioritization. Stale after 6 months.

## Deferred Items

| ID | Domain | Task | Priority | Stale After |
|----|--------|------|----------|-------------|

## How to Defer Work
1. Document problem + proposed direction
2. Add `# TODO(future): <description>` at code location
3. Add entry here with stale_after date

## Stale Rule
Items untouched for 6 months → promote to desk or delete. No graveyard.

---

## Feature: Agent Trace Ingestion & Conversation Recovery

Capture observable artifacts and full transcripts from agent runs to feed the improvement loop.

| ID | Topic | Source | Status | Stale After |
|----|-------|--------|--------|-------------|
| AGENT-CAPTURE-01 | agent_run_contract expansion | design-ritual | pending | 2026-10-18 |
| ADAPTER-01 | agent_capture_contract | design-ritual | completed | - |
| ADAPTER-02 | agent_adapter_contract | design-ritual | completed | - |
| RESCUE-01 | prompt-rescue-instructions | design-ritual | completed | - |
| CAPTURE-01 | agent-capture-instructions | design-ritual | pending | 2026-10-18 |
| RECOVER-01 | conversation-recovery-ritual | feedback-loop | pending | 2026-10-18 |

### Enhancement Tools
| ID | Tool | Purpose | Priority | Stale After |
|----|------|---------|----------|-------------|
| TOOL-01 | capture-cli | Run rescue ritual per agent | high | 2026-10-18 |
| TOOL-02 | normalize-pipeline | Transform raw → normalized | high | 2026-10-18 |
| TOOL-03 | claude-adapter.py | Extract from Claude transcript | medium | 2026-10-18 |
| TOOL-04 | gemini-adapter.py | Extract from Gemini logs | medium | 2026-10-18 |
| TOOL-05 | opencode-adapter.py | Extract from OpenCode output | medium | 2026-10-18 |
| TOOL-06 | pi-adapter.py | Extract from pi output | medium | 2026-10-18 |
| TOOL-07 | run-indexer.sh | Index runs for evaluation | low | 2026-10-18 |
| TOOL-08 | transcript-rescuer | CLI to fetch and save full agent logs | high | 2026-10-18 |

---

## Feature: Workflow Meta-Iteration

Rituals for continuous improvement of the Supervisor/Executor system.

| ID | Ritual | Purpose | Status | Stale After |
|----|--------|---------|--------|-------------|
| META-01 | project-closure-ritual | Capture frictions and iterate on docs/rules | pending | 2026-10-18 |
| META-02 | feedback-loop-integration | Use recovered conversations to tune instructions | pending | 2026-10-18 |

---

## Feature: Unified CLI (Steps 2-8)

Extend talk_extractor CLI to cover full workflow.

| ID | Step | Command | Purpose | Status | Stale After |
|----|------|---------|---------|--------|-------------|
| CLI-01 | 2. Standardize | `standardize create` | create reusable/normed modules | pending | 2026-10-18 |
| CLI-02 | 3. Drawers | `drawers add/list/promote` | manage specs in drawers | pending | 2026-10-18 |
| CLI-03 | 4. Desk | `tasks atomize`, `pills inject` | organize tasks/pills | pending | 2026-10-18 |
| CLI-04 | 5. Execution | `exec run`, `exec dispatch` | run agents | pending | 2026-10-18 |
| CLI-05 | 6. Capture | `capture rescue/normalize` | rescue agent traces | pending | 2026-10-18 |
| CLI-06 | 7. Evaluation | `eval test/lint/audit` | validate results | pending | 2026-10-18 |
| CLI-07 | 8. Integration | `integrate merge/promote` | merge to project | pending | 2026-10-18 |

→ [CLI Extension Spec](./design/cli-extension-spec.md)

---

## Feature: Workflow Contracts

Standardized contracts for workflow artifacts.

| ID | Contract | Purpose | Status | Stale After |
|----|----------|---------|--------|-------------|
| CONTR-01 | agent_run_contract | prompt provenance | pending expansion | 2026-10-18 |
| CONTR-02 | task_contract | task file format | existing | - |
| CONTR-03 | pill_contract | context pill format | existing | - |
| CONTR-04 | phase_contract | execution phase | existing | - |
| CONTR-05 | test_contract | test requirements | existing | - |
| CONTR-06 | lint_contract | lint requirements | existing | - |

---

## Feature: Workflow Instructions

Detailed instructions for workflow roles and rituals.

| ID | Instruction | Purpose | Status | Stale After |
|----|-------------|---------|--------|-------------|
| INST-01 | supervisor-instructions | orchestrator role | existing | - |
| INST-02 | executor-instructions | worker role | existing | - |
| INST-03 | design-ritual-instructions | design ritual | existing | - |
| INST-04 | prompt-rescue-instructions | capture ritual | existing | - |
| INST-05 | pill-audit-instructions | audit pills | existing | - |

---

## Specs In Drawers

| ID | Topic | Source | Promotion Gate |
|----|-------|--------|----------------|