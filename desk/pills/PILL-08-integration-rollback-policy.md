# PILL-08 - Integration Rollback Policy

- Type: guardrail
- Scope: project
- Domain: integration
- Language: en
- Nature: context
- Status: active
- Reusable: yes
- Applies To:
  - `integrate rollback` command
- Why:
  - Safely revert failed or incorrect integrations.
- Constraints:
  - Rollback must revert code, docs, and changelog.
- Contract:
  - Revert state to exactly before the integration commit.
- Evidence:
  - `desk/design/cli-extension-spec.md`
