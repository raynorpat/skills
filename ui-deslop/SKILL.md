---
name: ui-deslop
description: Context-aware catalog of the visual "tells" that make a UI read as AI-generated,
  with fixes. Use when the user says "deslop" about any interface, or when generating, styling,
  or reviewing any web or app interface (landing pages, dashboards, components, forms, chat
  UIs, artifacts) to avoid generic AI design cliches such as gradient text headlines,
  announcement badge pills, purple gradients, blurred background blobs, accent bars, pulsing
  status dots, all-caps microtext, nested containers, icon chips, KPI card rows, fake window
  chrome, placeholder data, dead controls, unmodified component-library defaults, templated
  landing-page and dashboard layouts, and reflexive animations, and to audit existing UI for
  them. Flags reflexive decoration, not meaningful affordances.
---

# UI Slop Review

A focused catalog of the specific visual "tells" that make an interface read instantly as
AI-generated, plus how to fix them. Use it both when **generating** UI and when **reviewing**
UI (code or screenshots).

## Core principle: intentionality, not prohibition

**The slop is never the element. It is the reflexive, meaningless use of the element.**

The single test for anything on screen is: **"Does this convey real information or serve the
context here?"**

- If yes, it is craft. Keep it. A nav icon that encodes a real category, a chevron that
  signals "expandable," a status pill that maps to a distinct state, a relative-time feed in
  an activity log, a dark-mode toggle: all good.
- If it is there because it "looks like a dashboard" or "looks technical," it is slop. Cut it
  or replace it with something that earns its place.

Do not strip meaningful affordances in the name of avoiding tells. Over-correction (a flat
banned-list applied blindly) is its own failure mode. The catalog reflects this: Tier 1 items
are almost always reflex; Tier 2 items are good when meaningful and slop only when decorative.

When generating, your own house style is the highest-risk slop source. Counter your defaults
by making context-driven decisions, not by imitating a different generator's defaults; slop
points both loud (gradient maximalism) and quiet (unmade decisions). The catalog covers both
directions.

## When generating

Make the decisions before writing markup, so the defaults do not make them for you:

1. **Context.** Who uses this, for what, on what device, how often? A tool used all day and a
   page read once want opposite densities.
2. **Palette.** One or two committed colors drawn from the product or brand, plus neutrals
   with a deliberate temperature. Not the generator's default accent.
3. **Type.** A typeface and a short scale chosen for this product. State it; do not inherit it.
4. **Shape and density.** A radius scale, a border and shadow policy, spacing per surface.
5. **One distinctive move.** A single thing this interface does that a template would not.
6. **Real content.** Use the content, data, and names the user gave you. Where none exists,
   use clearly marked placeholders; never invent metrics, customers, or testimonials.
7. **Every state.** Empty, loading, error, disabled, focus, and long-content cases for
   whatever you build, not only the populated happy path.

Then build, then run Review mode from the catalog against your own output before returning it.

## Working with other skills

This skill stands alone; no other skill is required.

- If a broader design-direction skill is installed, it owns aesthetic direction: font choice,
  palette strategy, layout philosophy. Follow its fuller treatment and use this catalog as the
  review checklist.
- For interface copy beyond the short Copy tells section (long marketing text, docs, onboarding
  prose), use `writing-deslop` if installed.
- A project's design system or brand guide outranks this catalog. If the system specifies
  all-caps eyebrows or a purple accent, that is a decision, not a tell.

## The catalog and review checklist

The full Tier 1 / Tier 2 catalog, code tells, copy tells, and the review checklist live in
[reference/tells.md](reference/tells.md). Consult it whenever generating or reviewing UI.

Note: keep all output em-dash-free. The em dash used as clause punctuation is itself the most
recognizable AI writing tell.

Derived from [deslop-ui](https://github.com/kmaida/deslop-skills/tree/main/deslop-ui) by
Kim Maida. Entries added here are listed at the end of `reference/tells.md`.
