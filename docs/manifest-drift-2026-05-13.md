# Manifest ↔ Runtime Drift Report — 2026-05-13

**Scope:** cross-check the three Phase 1 manifests under `agents/` against the runtime they document (`claude-harness/`, `codex-harness/`, `shared/prompts.ts`, `shared/config.ts`).
**Audience:** whoever wires the manifests in workbench Phase 2.
**Status:** advisory. The manifests are documentation-only today; nothing breaks if drift exists, but each row below is a decision Phase 2 must make.

## Conventions

- **AGREES** — manifest matches runtime exactly.
- **DRIFT** — manifest disagrees with runtime; one side must move.
- **PROMPT-ENFORCED** — manifest claims a constraint that the runtime does not enforce; the only thing keeping it true is wording in the system prompt.
- **UNENFORCED** — manifest claims a constraint that nothing enforces (neither runtime nor prompt).

The claude-harness uses the Anthropic Agent SDK `tools:` allowlist, which is enforced. The codex-harness uses `sandboxMode: "danger-full-access"` with `approvalPolicy: "never"` — it has **no per-tool allowlist**, so every `allowed_tools` row below is enforced in claude-harness only.

---

## Planner (`agents/planner/agent.yaml`)

| Manifest field | Manifest value | Runtime (claude-harness/planner.ts, shared/prompts.ts) | Verdict |
|---|---|---|---|
| `capability_surface.allowed_tools` | `[Write]` | `tools: ["Read", "Write"]` (planner.ts:16) | **DRIFT** |
| `capability_surface.max_turns` | `1` (comment: "planner is one-shot") | `CLAUDE_MAX_TURNS = 50` (config.ts:12 → planner.ts:18) | **DRIFT (load-bearing)** |
| `capability_surface.max_context` | `16000` | Not set in runtime; defers to SDK/model default | UNENFORCED |
| `memory_contract.retains` | `[spec.md]` | `writeSpec()` is the only persisted artifact path for planner (harness.ts:62) | AGREES |
| `prompts.system` | `shared/prompts.ts::PLANNER_SYSTEM_PROMPT` | Imported at planner.ts:4, codex-harness/planner.ts:2 | AGREES |
| `subagents` | `[]` | Planner dispatches no subagents | AGREES |

### Findings

1. **`allowed_tools` should include Read.** The runtime grants Read; the prompt doesn't use it, but the harness doesn't strip it either. Either tighten runtime to `["Write"]` (safe — the prompt never reads anything) or expand manifest to `[Read, Write]`. **Recommendation:** tighten runtime; the planner spec is "expand a sentence into a spec," nothing it could legitimately need to read.
2. **`max_turns: 1` is a lie today.** The harness grants 50 turns. The planner usually terminates in 1–2 turns by virtue of the prompt, but the manifest's claim is not enforced anywhere. Two ways to reconcile:
   - **Fix manifest → 50**, with a comment noting "logically one-shot but runtime grants slack for tool retries."
   - **Treat manifest as truth and add Phase 2 enforcement** — pass `maxTurns: agent.capability_surface.max_turns` when the loader wires this up.
   **Recommendation:** the second option. The point of first-class manifests is that they constrain the runtime. Document it as a Phase 2 to-enforce item.

---

## Generator (`agents/generator/agent.yaml`)

| Manifest field | Manifest value | Runtime | Verdict |
|---|---|---|---|
| `capability_surface.allowed_tools` | `[Read, Write, Edit, Bash, Glob, Grep]` | `tools: ["Read", "Write", "Edit", "Bash", "Glob", "Grep"]` (generator.ts:31) | AGREES |
| `capability_surface.max_turns` | `50` (comment: CLAUDE_MAX_TURNS) | `CLAUDE_MAX_TURNS = 50` | AGREES |
| `capability_surface.max_context` | `200000` | Not set in runtime; defers to SDK/model default | UNENFORCED (documented intent) |
| `memory_contract.retains` | `[git-history-of-app, contract.json, spec.md, feedback.md]` | Actual paths: `contracts/sprint-N.json` (not `contract.json`), `feedback/sprint-N-round-R.json` (not `feedback.md`), `spec.md`, and `app/.git/` history. See `shared/files.ts:48-71`. | **DRIFT (filenames)** |
| `prompts.system` | `shared/prompts.ts::GENERATOR_SYSTEM_PROMPT` | Imported at generator.ts:2 | AGREES |
| `subagents` | `[]` | Generator dispatches no subagents | AGREES |

### Findings

Generator is otherwise clean; `max_context` is a documented-intent number, not a runtime constraint. The `retains` filename drift is shared with the evaluator and consolidated in finding 3 below.

---

## Evaluator (`agents/evaluator/agent.yaml`)

| Manifest field | Manifest value | Runtime | Verdict |
|---|---|---|---|
| `capability_surface.allowed_tools` | `[Read, Bash, Glob, Grep]` ("NO Write") | claude-harness `tools: ["Read", "Bash", "Glob", "Grep"]` (evaluator.ts:34) | AGREES (claude-harness) |
| same | same | codex-harness has **no allowlist** — `sandboxMode: "danger-full-access"`, evaluator can Write | **DRIFT (codex-harness)** |
| `capability_surface.max_turns` | `50` | `CLAUDE_MAX_TURNS = 50` | AGREES |
| `memory_contract.retains` | `[eval-result.json, feedback.md]` | Actual: only `feedback/sprint-N-round-R.json` (shared/files.ts:69). Neither `eval-result.json` nor `feedback.md` exists. | **DRIFT (filenames)** |
| `memory_contract.forgets` | `[background-processes]` | Enforced by prompt only (EVALUATOR_SYSTEM_PROMPT lines about `kill %1`, `pkill -f uvicorn`, etc.). Runtime does not kill processes after the turn. | **PROMPT-ENFORCED** |
| `eval_bindings.must_pass` | `[meta-eval/honest-scoring, meta-eval/no-write-tool-use]` | No eval runner exists yet (Phase 2/3) | UNENFORCED (intentional) |
| `prompts.system` | `shared/prompts.ts::EVALUATOR_SYSTEM_PROMPT` | Imported at evaluator.ts:2 | AGREES |
| `subagents` | `[]` | Evaluator dispatches no subagents | AGREES |

### Findings

3. **`eval-result.json` and `feedback.md` are fictitious.** The harness emits `EvalResult` objects (shared/types.ts:27) through `writeFeedback()` which writes JSON to `feedback/sprint-<n>-round-<r>.json` (shared/files.ts:69). The generator manifest's `retains: [..., contract.json, ..., feedback.md]` and the evaluator manifest's `retains: [eval-result.json, feedback.md]` both reference filenames that don't exist. Phase 2 must reconcile the manifests to the real paths: `contracts/sprint-<n>.json` and `feedback/sprint-<n>-round-<r>.json`.
4. **The "NO Write" rule for evaluator is unenforced in codex-harness.** Codex SDK doesn't expose a per-tool allowlist on `startThread()`. If the no-Write invariant matters (and it should — the evaluator must not edit the app it's judging), Phase 2 must either (a) wrap the codex thread in a sandbox that blocks file writes outside `/tmp`, or (b) accept that the invariant is prompt-enforced for codex and document that fact in the manifest.
5. **`forgets: [background-processes]` relies entirely on the prompt.** The runtime does not enumerate or kill spawned processes. If the prompt is ever softened, this invariant evaporates silently. Worth a Phase 2 wrapper that scans for orphaned child processes after the evaluator returns.

---

## Implicit roles not yet manifested

The harness has **two contract-negotiation prompts** in `shared/prompts.ts` that don't correspond to any manifest:

- `CONTRACT_NEGOTIATION_GENERATOR_PROMPT` (proposes a SprintContract)
- `CONTRACT_NEGOTIATION_EVALUATOR_PROMPT` (reviews and approves or revises)

Both are invoked from `claude-harness/harness.ts::negotiateContract()` with `tools: ["Read"]` and `maxTurns: 10` — a **different capability surface** than the main generator/evaluator roles. Codex-harness has equivalent logic (TODO: confirm path).

**Phase 2 decision needed:** are these (a) sub-prompts of the main generator/evaluator manifests with a runtime-selectable role, or (b) two additional manifests (`agents/contract-proposer/agent.yaml` and `agents/contract-reviewer/agent.yaml`)?

**Recommendation:** option (b). The capability surface is different (`tools: ["Read"]` vs. full Bash for the main roles), the prompts are structurally distinct, and `subagents: []` would no longer be honest for the main generator/evaluator if their negotiation behavior is part of their role.

---

## Cross-SDK consolidation (Phase 4 preview)

The current SDK split is:

| Concern | claude-harness | codex-harness |
|---|---|---|
| Per-tool allowlist | yes (`tools: [...]`) | no (sandbox-based, full access) |
| Max turns | `CLAUDE_MAX_TURNS = 50` | unbounded per call (uses `thread.run()`) |
| Network access | implicit (SDK default) | explicit `CODEX_NETWORK_ACCESS = true` |
| Permission mode | `"bypassPermissions"` | `"never"` approval policy |
| Background process cleanup | not enforced | not enforced |

A single `agent.yaml` must either:
1. Be the **least common denominator** (every constraint the manifest declares must be enforceable on both SDKs), or
2. Carry **SDK-specific overrides** (e.g. `capability_surface.codex.sandbox_writeable_paths: [/tmp]` for the codex evaluator).

Phase 4 will need to choose. Today the manifests assume option 1 implicitly, which means the evaluator's `allowed_tools` exclusion of Write is honest for claude-harness and aspirational for codex-harness.

---

## Summary — what blocks promotion to 1.0.0

| # | Finding | Action | Owner |
|---|---|---|---|
| 1 | Planner `allowed_tools` missing Read | Tighten runtime to `["Write"]` (preferred) or expand manifest | Phase 2 |
| 2 | Planner `max_turns: 1` not enforced | Enforce in Phase 2 loader, or fix manifest to 50 | Phase 2 (decision needed) |
| 3 | Generator + evaluator `retains` reference fictitious filenames (`contract.json`, `feedback.md`, `eval-result.json`) | Reconcile to actual `contracts/sprint-N.json` and `feedback/sprint-N-round-R.json` | Phase 2 |
| 4 | Evaluator no-Write rule unenforced in codex-harness | Sandbox or prompt-only acceptance | Phase 4 |
| 5 | `forgets: [background-processes]` is prompt-only | Add post-turn process scan or accept prompt-only | Phase 2 |
| 6 | Contract-negotiation prompts have no manifest | Author two new manifests (`contract-proposer`, `contract-reviewer`) | Phase 1.5 / Phase 2 |
| 7 | `max_context` numbers are aspirational | Decide whether manifests carry SDK-enforceable context limits | Phase 4 |

Findings 1, 2, 3, 6 are cheap and can land before Phase 2 starts. Findings 4, 5, 7 need SDK-level decisions.
