# adversarial-dev — Agent-First Rewrite Plan

**Drafted:** 2026-05-12 by an AFK agent per the workbench-side prep packet at https://github.com/kombiz/workbench/blob/main/docs/agent-first-prep-packets/adversarial-dev-2026-05-12.md.

**Companion to:** /architecture/now §2 on greywiki, and workbench/docs/agent-first-rewrite-plan-2026-05-12.md (the parent plan).

## What this plan does

Promotes the 3 prompt-based agent roles in adversarial-dev (planner, generator, evaluator) into first-class entities with agent.yaml manifests per the 6-field Agent Definition Contract. The harness orchestration (the planner -> contract -> build -> evaluate -> retry-or-advance loop) stays as-is until Phase 4 of the workbench rewrite makes workflow-as-orchestration land.

## Phases (mirrors workbench rewrite)

1. **Phase 1 (this PR):** scaffold agents/{planner,generator,evaluator}/agent.yaml + this plan + evals/adversarial-quality/README.md. No runtime change.
2. **Phase 2 (after workbench Phase 2):** wire the harness to read prompts/policies from agent.yaml instead of shared/prompts.ts. Schema validation against workbench's agents/schema.json.
3. **Phase 3:** author the adversarial-quality eval suite fixtures (spec-shape, contract-roundtrip, honest-scoring).
4. **Phase 4:** dual-SDK consolidation — confirm one manifest per role works for both claude-harness/ and codex-harness/; harness chooses the model at dispatch.

## Non-goals

- UI rewrite. The harness has no UI.
- New agent roles. Stays at 3 roles.
- Runtime changes in Phase 1.

## Blockers

- Workbench agents/schema.json not yet authored (Phase 1 of workbench rewrite). Manifests here are unvalidated drafts until that lands.
- NEEDS-DECISION policy fields (on_tool_failure, on_max_context) need design conversation.
