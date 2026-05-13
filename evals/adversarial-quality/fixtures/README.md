# fixtures/

> **Status — 2026-05-13:** drafts. **Shape-illustrative, not runner-ready.** No eval runner consumes these yet. They exist to make the test design legible and to give workbench Phase 2 a concrete target. If Phase 2 publishes an incompatible runner contract, fixtures get retrofitted; the test design stays.

See `../SCHEMA.md` for the assumed `input.json` / `expected.json` shape.

## Fixtures in this directory

| Fixture | Target agent | What it asserts |
|---|---|---|
| `spec-shape/` | planner | spec.md has required sections, sprint count in [3,6], no implementation-detail leak in narrative sections |
| `contract-roundtrip/` | contract-proposer + contract-reviewer | negotiated contract has ≥3 unique criteria, well-formed thresholds, and vague proposal criteria are revised away |
| `honest-scoring/` | evaluator | given a deliberately broken app, evaluator returns `passed: false` and names the defect |

## Authoring conventions

- Every fixture has a `README.md` explaining its intent and any quirks.
- `input.json` is what the runner feeds the agent (or instructions for materializing the inputs).
- `expected.json` is a list of assertions per `../SCHEMA.md`.
- Auxiliary files (a fixture `spec.md`, a broken `app/`, etc.) sit alongside `input.json` and are referenced from it by relative path.
