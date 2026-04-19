<!-- we must review the contracts, i don't really know if they are ok. -->
# Workflow Philosophy

> **Kill the God-Agent. Externalize the Reason. Audit the Trace.**

## 1. Externalized Rationale (Pills)
Reasoning must never stay in an agent's head. Every architectural decision, every naming convention, and every guardrail must be captured in a **Context Pill**.  <!-- very architectural decision, every naming convention, and every guardrail must be captured in THE BLUEPRINT, context pills are just abstractions of the design made for subagents in order to make them do EXACTLY WHAT ASKED; NOT MORE, NOT LESS -->
*   **DNA, not Memory:** Pills are the DNA of the project. If it's not in a pill, it doesn't exist for the subagent.
*   **Orthogonality:** Every Pill must be unique and non-overlapping. Orthogonal context ensures stable, clear, and non-contradictory context composition.

## 2. Caged Execution (Isolation)
Subagents (Executors) are "caged." They are given exactly one task and the specific pills required to solve it. <!-- they must not touch anything outside of it without giving a good reason for it. -->
*   **Zero-Invention Rule:** Subagents are strictly forbidden from "inventing" logic or "guessing" intent. If a subagent finds an ambiguity, it MUST stop and request a new Context Pill.
*   **The Law of Separation:** Test generation and Code implementation **must never** be performed by the same subagent run. Using the same agent leads to "Test Mutilation"—where the agent modifies tests to hide flawed implementation.

## 3. Failure Mechanics (Out-Failure)
An agent run is a binary state: **Success (0) or Failure (1+).**
*   **Automated Rejection:** "Out-failure" is determined by the Quality Gate (`eval`). If `ruff`, `mypy`, or `pytest` return a non-zero exit code, the implementation is physically rejected. 
*   **The Self-Loop:** Every failure is an opportunity for system iteration. After every step (success or failure), a **Failure Report** must be generated, analyzing why the drift or error occurred to refine the Pills or Rituals.

## 4. Mandatory CLI Automation (Integrity)

*   **Programmatic Mandate:** Everything that does not absolutely require an LLM **must** be done programmatically. No manual "stubs" or "placeholders" in logic.

## 5. The Clarification Mandate (Alignment)
*   **The 100% Clarity Rule:** Before starting any design or implementation, the agent must ask the user about every aspect that is not 100% clear. Redesign is the default response to ambiguity.


<!--
- Everything from the agent/subagent rationale to the changes and results of testing must be traced where it belongs
- There are clear contracts for each passed signal in this workflow, respect them
- The finality of transparency is being able to correct the flow
 -->