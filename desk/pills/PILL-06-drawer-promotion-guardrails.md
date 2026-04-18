# PILL-06 - Drawer Promotion Guardrails

- Type: guardrail
- Scope: global
- Domain: workflow
- Language: en
- Nature: context
- Status: active
- Reusable: yes
- Applies To:
  - `desk/drawers/`
- Why:
  - Ensure drawer items are mature before becoming tasks.
- Constraints:
  - No ambiguity allowed in promoted items.
  - Must identify target module and phase.
- Contract:
  - Promotion fails if target location is not defined.
- Evidence:
  - `desk/design/workflow-system-spec.md`
