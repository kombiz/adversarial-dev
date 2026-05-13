# spec-shape

**Target agent:** planner (`agents/planner/agent.yaml`, system prompt `PLANNER_SYSTEM_PROMPT` in `shared/prompts.ts`).

## What this eval asserts

The planner is given a 1-4 sentence user prompt and must produce a `spec.md` that:

1. **Has all five required sections** the system prompt demands: Product Overview, Tech Stack, Design Language, Feature List, Sprint Plan.
2. **Organizes work into 3-6 sprints**, per the prompt's `Organize features into sprints (3-6 sprints)` instruction.
3. **Does not leak implementation detail** in narrative sections — i.e., no function signatures, file paths, API route lines, or SQL DDL outside the Tech Stack section. (Tech Stack is excluded because a planner may legitimately list directory layout or sample paths there.)

## What this eval does NOT assert

- That the spec is "good" — taste is out of scope. We can only mechanically check shape.
- That sprints have balanced effort. Subjective.
- That every claimed feature is actually buildable. The harness will discover that the hard way at evaluate-time.

## Failure modes this catches

- Planner skips a section (e.g., omits "Design Language" because the user prompt didn't mention design).
- Planner produces a 1- or 2-sprint spec, breaking the harness's assumed sprint cadence.
- Planner over-specifies, dictating function signatures and file paths the generator should be deciding.

## Failure modes this misses

- Subtle bad design — e.g., five sprints that don't build on each other.
- A spec that's technically valid but fails Phase 2's schema-stricter checks.
- Planner "writes code" using prose instead of regex-detectable syntax.

## Quirk: the planner writes via the Write tool

`PLANNER_SYSTEM_PROMPT` instructs the planner to write `spec.md` directly using the Write tool. The runner reads `<workDir>/spec.md` after the planner returns, not the planner's text output.
