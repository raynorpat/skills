# Slop Patterns

Use this checklist during cleanup.

## High-confidence removals

- Comments that narrate obvious code actions or restate the line below.
- Defensive checks and broad `try/catch` blocks that do not match trusted call-path conventions.
- `any`/unsafe casts added only to suppress type errors.
- Duplicate helper wrappers that only re-export existing behavior.
- Over-abstracted naming (`processDataHandlerManager`) where file style is simpler.

## Medium-confidence removals

- Logging that repeats values already returned or thrown.
- Generic helper functions used exactly once when inline style is the local norm.
- Redundant null/undefined guards after validated parsing layers.

## Keep (do not remove)

- Security boundaries, permission checks, input validation.
- Error handling required by subsystem contracts.
- Retries/timeouts/circuit breakers that are part of reliability policy.
- Observability hooks intentionally used by operations teams.

## TypeScript-specific guidance

- Replace `as any` with precise narrowing where feasible.
- Prefer existing project utility types over ad-hoc type escape hatches.
- Do not widen public API types for convenience.

## Scope discipline

- Edit only changed hunks unless a nearby fix is required for coherence.
- Avoid non-requested refactors and unrelated formatting churn.
- If uncertain whether a pattern is intentional, ask before changing behavior.

## C/C++-specific guidance

- Remove `NULL`/`nullptr` checks on pointers the local contract guarantees non-null; keep them at API boundaries and after allocation.
- Drop redundant C-style or `static_cast`/`reinterpret_cast` casts that only silence warnings; fix the type instead.
- Remove comments that restate the code or narrate ownership the types already show; keep comments on lifetime, locking, and ABI.
- Do not add `try/catch`, wrapper classes, or RAII shims where the codebase uses plain C idioms (`goto cleanup`, manual free).
- Match the local style for `const`, `auto`, `nullptr` vs `NULL`, `#define` vs `constexpr`, and header guards; do not modernize unprompted.
- Keep `assert`s, bounds checks, `volatile`, memory barriers, `#ifdef` platform branches, and error-code returns; they are rarely slop.
- Never touch macros, struct layout, or `extern "C"` blocks for style alone.
