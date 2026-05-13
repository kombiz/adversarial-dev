# contract-roundtrip

**Target agents:** contract-proposer + contract-reviewer (currently the two `CONTRACT_NEGOTIATION_*_PROMPT` prompts in `shared/prompts.ts`; **not yet manifested** — see `docs/manifest-drift-2026-05-13.md` finding 6).

## What this eval asserts

Given a `spec.md` and a sprint number, the negotiation round must produce a `SprintContract` (shape per `shared/types.ts::SprintContract`) where:

1. The contract has **at least 3 criteria** and at most 15 (matches the proposer prompt's stated range).
2. Criterion names are **unique** within the contract.
3. Each criterion has well-formed `name`, `description`, and `threshold` (1-10).
4. **No vague criteria survive.** If the proposer emits a criterion like `works_well`, `user_friendly`, or `looks_good`, the reviewer's revision must replace it. The final contract must not contain any criterion whose `name` or `description` matches the vague-language patterns.

Assertion 4 is the bit the advisor flagged: it discriminates a real reviewer from a rubber-stamp.

## What this eval does NOT assert

- That the criteria are *substantively* good — only that they're not lexically vague.
- That negotiation iterates more than once. The current harness does exactly one proposal+review pass; iterating would require runtime changes.
- That the proposer's first draft was good. We test the *final* contract; the proposer may emit garbage as long as the reviewer fixes it.

## Failure modes this catches

- Reviewer "APPROVED"s a contract full of vague criteria.
- Proposer emits 1-2 criteria and reviewer doesn't add coverage.
- Duplicate criterion names (which silently confuse the evaluator's score lookup).

## Failure modes this misses

- Both proposer and reviewer agreeing on plausible-sounding but unverifiable criteria.
- Threshold values that are technically in [1,10] but uniformly trivial (e.g., everything set to 1).
- The "all happy paths" failure where coverage of error handling is absent — testing this would need a semantic check beyond regex.

## How the runner constructs the input

The proposer is invoked with `CONTRACT_NEGOTIATION_GENERATOR_PROMPT` against the spec.md in this fixture directory, sprint number 1. Its proposal is then handed to the reviewer (`CONTRACT_NEGOTIATION_EVALUATOR_PROMPT`) and the final contract is whichever the reviewer returns ("APPROVED" → proposal verbatim; otherwise → the reviewer's revision).
