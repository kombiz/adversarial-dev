# adversarial-quality eval suite

Eval suite gating the promotion of the 3 adversarial-dev manifests (planner / generator / evaluator) from draft 0.1.0 to 1.0.0.

## Evals

| Name | Targets | What it asserts | Status |
|---|---|---|---|
| spec-shape | planner | spec.md has required sections + sprint count in [3,6] + no implementation-detail leak | scaffolded, fixtures TBD |
| contract-roundtrip | generator + evaluator | contract negotiation has at least 1 round, at least 3 final criteria, no duplicates | scaffolded, fixtures TBD |
| honest-scoring | evaluator | given a deliberately-broken app, evaluator returns passed=false and identifies the specific defect | scaffolded, fixtures TBD |

## Fixtures

To author per Phase 3 of docs/agent-first-rewrite-plan.md. Each eval gets:

- evals/adversarial-quality/fixtures/<eval-name>/input.json — the input the agent processes
- evals/adversarial-quality/fixtures/<eval-name>/expected.json — the output the agent should produce (or constraints it should satisfy)

## Running (future)

Once the agent.yaml manifests are load-bearing (workbench Phase 2), the harness will load these eval files and run them against each agent before promotion.
