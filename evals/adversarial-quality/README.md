# adversarial-quality eval suite

Eval suite gating the promotion of the 3 adversarial-dev manifests (planner / generator / evaluator) from draft 0.1.0 to 1.0.0.

## Evals

| Name | Targets | What it asserts | Status |
|---|---|---|---|
| spec-shape | planner | spec.md has required sections + sprint count in [3,6] + no implementation-detail leak outside Tech Stack | draft fixtures landed 2026-05-13 |
| contract-roundtrip | contract-proposer + contract-reviewer | contract has ≥3 unique criteria, well-formed thresholds, no vague language survives the review | draft fixtures landed 2026-05-13 |
| honest-scoring | evaluator | given a deliberately-broken app, evaluator returns passed=false, scores the failing criterion below threshold, and names the defect | draft fixtures landed 2026-05-13 |

## Fixtures

Draft fixtures live under `fixtures/<eval-name>/`. The assumed runner contract (input.json / expected.json shape, assertion kinds) is documented in `SCHEMA.md`. These are **shape-illustrative, not runner-ready** — no runner consumes them yet. When workbench Phase 2 publishes its eval-runner contract, the fixtures will either satisfy it or get retrofitted.

Each fixture directory contains:

- `README.md` — design notes for that eval
- `input.json` — what the runner feeds the agent (or describes how to construct it)
- `expected.json` — list of assertions per `SCHEMA.md`
- Auxiliary files (a spec, a broken app, a contract) referenced from `input.json`

## Running (future)

Once the agent.yaml manifests are load-bearing (workbench Phase 2), an eval runner will load these fixtures, materialize their inputs into a workspace, invoke the target agent, and check the agent's output against `expected.json`. Until then, the fixtures are reference material.
