# adversarial-quality fixture schema

**Status:** draft, not yet ratified by a runner. Until workbench Phase 2 publishes its eval-runner contract, the fixture layout below is **shape-illustrative** — it shows what we think the runner will need, but no runner consumes it today. Treat this file as a target the eventual runner must either satisfy or explicitly reject.

If workbench Phase 2 ships an incompatible contract, the fixtures get retrofitted; the test design (what is checked, against what input) stays the same.

## Directory layout

```
evals/adversarial-quality/
├── README.md                    # eval suite index
├── SCHEMA.md                    # this file
└── fixtures/
    ├── README.md                # fixture index, marks them illustrative
    ├── <eval-name>/
    │   ├── README.md            # per-eval design notes
    │   ├── input.json           # input the agent processes (or describes how to construct it)
    │   ├── expected.json        # constraints the output must satisfy
    │   └── (optional auxiliary files: spec.md, app/, contract.json, …)
```

## `input.json` contract

```jsonc
{
  "description": "Human-readable summary of what this fixture feeds to the agent.",
  "target_agent": "planner | generator | evaluator | contract-proposer | contract-reviewer",
  "inputs": {
    // Arbitrary keyed inputs. Conventions:
    //   userPrompt   — string passed to the planner
    //   spec_path    — path (relative to fixture dir) to a spec.md the agent reads
    //   contract     — inline SprintContract object
    //   app_path     — path to the broken app directory the evaluator inspects
    //   sprint_number — integer
  }
}
```

The runner is expected to:

1. Read `input.json`.
2. Materialize the inputs into the agent's working directory (copy `spec.md` into `workDir/`, copy `app/` into `workDir/app/`, etc.).
3. Invoke the `target_agent` against that working directory.
4. Read the agent's output (spec.md for planner, contract JSON for proposer/reviewer, EvalResult for evaluator).
5. Check the output against `expected.json`.

## `expected.json` contract

`expected.json` is a list of **assertions** the runner applies to the agent's output. We do not expect an exact-match output; the agents are non-deterministic.

```jsonc
{
  "description": "Human-readable summary of what these assertions enforce.",
  "assertions": [
    { "kind": "<assertion-kind>", "...": "kind-specific fields" },
    ...
  ]
}
```

### Assertion kinds (draft set)

- `output_contains_sections` — output (markdown) must contain top-level headings matching the supplied list.
  `{ "kind": "output_contains_sections", "headings": ["Product Overview", "Tech Stack", ...] }`
- `output_count_range` — a counted element (e.g., sprints, criteria) must fall within `[min, max]`.
  `{ "kind": "output_count_range", "what": "sprints", "min": 3, "max": 6 }`
- `output_pattern_absent` — none of the supplied regex patterns may match in the output (optionally scoped to certain sections).
  `{ "kind": "output_pattern_absent", "patterns": [...], "scope": "all" | { "exclude_sections": [...] } }`
- `output_pattern_present` — at least one of the patterns must match.
  `{ "kind": "output_pattern_present", "patterns": [...] }`
- `output_field_equals` — a named field in the output JSON must equal a value.
  `{ "kind": "output_field_equals", "path": "passed", "value": false }`
- `output_field_satisfies` — a named field must satisfy a JSON-schema-style constraint.
  `{ "kind": "output_field_satisfies", "path": "feedback[*].score", "constraint": { "type": "number", "minimum": 1, "maximum": 10 } }`
- `output_array_min_length` — a named array must have at least N items.
  `{ "kind": "output_array_min_length", "path": "criteria", "min": 3 }`
- `output_array_unique_by` — items in a named array must be unique by a key.
  `{ "kind": "output_array_unique_by", "path": "criteria", "key": "name" }`
- `output_mentions_defect` — for honest-scoring: the agent's free-text feedback must reference at least one of the supplied keywords (case-insensitive).
  `{ "kind": "output_mentions_defect", "path": "feedback[*].details", "any_of": ["minus", "subtract", "returns 0", ...] }`

This is a starter set, not exhaustive. Each fixture's `expected.json` is allowed to introduce a new `kind` — but should also propose it back to this schema in the same PR.

## What this schema deliberately does NOT define

- The runner's execution sandbox (Docker? bare process? workbench-supplied?).
- How the runner discovers fixtures (filesystem walk? manifest list? CLI args?).
- How the runner reports results (JUnit? JSON? both?).
- Whether agents are invoked via claude-harness or codex-harness (or either, parameterized).

These are workbench Phase 2's decisions. When that contract lands, this file is updated or replaced.
