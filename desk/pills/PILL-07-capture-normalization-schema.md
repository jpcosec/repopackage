# PILL-07 - Capture Normalization Schema

- Type: model
- Scope: global
- Domain: capture
- Language: python
- Nature: implementation
- Status: active
- Reusable: yes
- Applies To:
  - `talk_extractor/semantic/evidence_artifact.py`
- Why:
  - Define a common format for agent traces.
- Constraints:
  - Unified JSON structure regardless of source agent.
- Contract:
  - Must capture timestamp, speaker, content, and tool use.
- Evidence:
  - `desk/design/workflow-system-spec.md`
