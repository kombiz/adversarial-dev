# agents/ — first-class agent manifests

> **New as of 2026-05-12 (Phase 1 of the agent-first rewrite).** This directory is the canonical home for agent.yaml manifests per the 6-field Agent Definition Contract (see https://greywiki.onlyarag.com/architecture/agents). Sister to the existing claude-harness/ and codex-harness/ directories which contain the Python/TypeScript harness code today.

## Why this exists

adversarial-dev today has three discrete agent roles (planner / generator / evaluator) defined as system prompts in shared/prompts.ts. The framework principle #10 ("agents are first-class") asks each role to be its own entity with a manifest, memory contract, and eval bindings. This directory is where that promotion lands.

See docs/agent-first-rewrite-plan.md for the full plan. For the workbench-side parent plan, see https://github.com/kombiz/workbench/blob/main/docs/agent-first-rewrite-plan-2026-05-12.md.

## Layout

- agents/README.md           — this file
- agents/planner/agent.yaml  — 6-field manifest for planner role
- agents/generator/agent.yaml — 6-field manifest for generator role
- agents/evaluator/agent.yaml — 6-field manifest for evaluator role

## Status

These manifests are draft 0.1.0 documentation-only. Existing claude-harness/ and codex-harness/ continue to read prompts from shared/prompts.ts. Phase 2 of the workbench rewrite will produce a manifest loader that makes these files load-bearing.

NEEDS-DECISION markers in the manifests are valid in drafts. They block promotion to 1.0.0 but not commit.
