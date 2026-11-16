---
name: test-audit
description: "Writing/changing/reviewing/sweeping tests: reject duplicate or implementation-coupled proof; remove test-only production seams."
---

# Test Audit

- Authoring gates every new/changed test.
- Audits: remove low-value proof in coherent owner batches; never chase deletion counts.
- Whole-subsystem campaign: read [CAMPAIGN.md](CAMPAIGN.md) first.

## Authoring gate

Before adding test, answer:

1. Protected observable behavior, invariant, or independent contract?
2. Credible regression that makes it fail?
3. Expected value from an independent oracle (spec, known example, external
   caller, protocol fixture), not the code under test or a copy of its algorithm?
4. Why existing proof misses it? Each contract: one primary owner at strongest
   boundary. Another layer needs distinct transport/lifecycle risk. Extend
   tables/shared fixtures; consolidate repeated setup.
5. Export, flag, wrapper, injection hook with no production caller needed?
   Move proof to real boundary instead.

- Pick the cheapest boundary that can still fail for the real regression: pure
  logic at unit level, wiring/transport/lifecycle at the real boundary with a
  fake network or store, not a mock of the collaborator under test. Slow tests
  need a reason the cheaper layer cannot catch the bug.
- Regressions must fail pre-fix for intended reason, pass after repair; report
  unavailable baseline proof.
- One owner regression covers bug; never replay at every crossed layer.
- Behavior-preserving refactors should not break test.

## Junk patterns

- Reject self-comparisons, copied inventories, source greps,
  implementation/call-shape assertions, duplicate contracts, test-only seams,
  subject-generated expected values, mocks supplying asserted behavior.
- Fixtures must not fabricate owner receipts/order or claim persistence path
  never writes.
- Negative controls must fail at intended guard; names must match exercised behavior.
- Reject correction pile-ups, same-branch parameter permutations, assertions
  dominated by a stronger one, fixture-tautological tests, coverage-owned tests.
- Mutual-support clusters (checksum, validator, receipt, fallback plus the tests
  that only exist for them): trace to an
  [independent root](references/audit.md#closed-justification-loops); none
  found, delete seam and tests together.
- Duplicate only under [dominance](references/audit.md#dominance): same owner,
  branch, result, failure domain, equal or stronger oracle.
- Auditing candidates: use [full checklist](references/audit.md#junk-patterns).

## Retention bar

- Keep independent API, SDK, protocol, config, migration, storage, security,
  platform, default, prompt-byte, generated-language, package, release,
  architecture, observable-ordering contracts. Static/slow ≠ disposable.
- Source inspection must survive identifier-only refactors and guard independent
  user-facing contract.
- Baseline failures may be bugs to repair, not tests to delete.

## Audit and validation

- Before audit edit: read [candidate evidence and workflow](references/audit.md#candidate-evidence);
  inspect full owners/callers/history; record remaining proof before deletion.
- Delete obsolete production seams with tests; never optimize for deletion,
  test, assertion, or coverage counts.
- Adding a test during an audit is not the default; see
  [when to add](references/audit.md#adding-tests-during-an-audit).
- Compare collected-test counts, skips, and deselections before and after.
- Proof policy: run owner + sibling tests and the project's changed-file checks,
  using the narrowest command that can fail for the intended reason; never edit
  the checkout during an active test run; then self-review the diff.
- Report causes, retained contracts, proof/cost, production versus test LOC,
  follow-ups. Commit/push/land only with task authority.
