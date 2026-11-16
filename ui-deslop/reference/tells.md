# The tells: catalog and review checklist

Each entry is `Tell → why it reads AI → fix (and "fine when" if it has a legitimate use)`.
Read every entry through the core principle: the problem is reflexive, meaningless use, not
the element itself. Keep all generated copy em-dash-free.

## Tier 1: almost always slop

The reflex itself is the problem. These are very hard to justify.

### Chrome and components

- **Single-side accent bar.** A colored left or top border on cards *and on list rows* (the
  status-page incident-row look). Reads as a lazy stand-in for hierarchy that almost never
  looks intentional. Fix: convey state or category with a status dot, a label, or a
  full-surface tint. Earn a border only when it is part of a real, consistent system.
- **Blinking / pulsing status indicator.** The green "Live" dot with a pulse animation.
  Decorative motion masquerading as signal; on everything it is just noise. Fix: a static dot
  plus a clear label. Reserve a pulse for genuinely live, real-time state, used sparingly.
- **All-caps letter-spaced microtext** used as a reflexive eyebrow/label default. Fine when
  it is a deliberate, consistent part of a real established brand type system. Slop when it is
  sprinkled on every eyebrow. Fix: normal case, with hierarchy from weight, size, and color.
- **Dots as filler separators.** `Tier ∞ • All Access`, `Kiosk · Station 2` as decorative
  punctuation. Fine when separating genuinely peer metadata compactly. Slop when standing in
  for layout. Fix: spacing or stacking instead.
- **Excessive rounded corners.** Large radius on every surface, pills for everything. Uniform
  softness erases hierarchy and reads templated. Fix: commit to a radius scale tied to the
  aesthetic. Some things should be square.
- **Obvious nested containers.** Card inside card inside card. Every border adds a box the
  eye must parse and none of them adds meaning. Fix: flatten; group with space and type, not
  more borders.
- **Glowing gradient orb / sphere "mascot."** The abstract consciousness blob. Fix: if a
  brand mark is needed, design a real one; otherwise drop it.
- **`∞` and gratuitous emoji flourishes** (`Tier ∞`, 😇, ✨) used as a substitute for real
  personality. Fix: let voice and content carry personality, not symbols.
- **⌘K / shortcut hint pills as pure decoration** (`Ask anything… ⌘K`, `EXECUTE ⌘↵`). Fine
  when the shortcut actually exists and is discoverable. Slop when it is chrome.
- **Pill-shaped gradient CTA buttons** as the default button style. Fix: a button style that
  fits the system; reserve emphasis for the one primary action.

- **Icon chip on every card.** A small icon inside a tinted rounded square at the top left of
  each card, each chip a different pastel. Reads as the stock feature-card recipe. Fix: drop the
  chip, or use an icon only where it distinguishes one item from its neighbors.
- **Fake window chrome.** Three traffic-light dots and a title bar drawn around a screenshot,
  code block, or terminal to make it "look like an app." Fix: show the real product in its real
  frame, or show the content with no frame.
- **Floating mock notification cards.** Tilted mini-cards drifting around the hero
  (`+$4,200 revenue`, `New signup`) that correspond to nothing in the product. Fix: one honest
  screenshot or a working example.
- **Perspective-tilted hero screenshot with a glow.** The dashboard image rotated in 3D with a
  colored halo. Fix: show the product flat and legible at a size where its text can be read.
- **Chips and badges as texture.** `New`, `Beta`, `Pro`, `AI` labels scattered across nav
  items and cards with no release state behind them. Fix: badge only real, current state.
- **Gradient-fill avatar circles.** Initials on a random gradient for every user row, used to
  add color. Fine when it is the product's real fallback avatar. Slop as decoration.
- **Border, ring, and shadow stacked on one surface.** Three kinds of edge on the same card.
  Fix: pick one way to separate a surface and use it consistently.
- **Everything is a card.** Page sections, single sentences, and lone buttons each wrapped in
  a bordered, padded box. Fix: use a card only for a discrete object a user can act on or
  compare.
- **Tooltip on everything.** Hover text repeating the visible label. Fix: tooltips only for
  icon-only controls and truncated text.

### Color and background

- **Purple / neon gradients on dark.** The default AI palette family: purple-to-blue,
  cyan-on-dark, neon glow. Fix: commit to a context-driven palette. Dark themes are fine when
  the product calls for them; pick restrained accents and skip the glow.
- **Gradient text headline.** `background-clip: text` on the hero H1. Currently the single
  most recognizable tell in generated UI. Fix: solid color; let typeface, size, and weight
  carry the impact.
- **Blurred gradient blobs.** Oversized `blur-3xl` color circles absolutely positioned behind
  the hero. Fix: a background either reinforces the brand or stays plain.
- **Dot-grid or grid-line background** with a radial fade mask. The default "technical"
  texture. Same test: brand reinforcement or nothing.
- **Spotlight hero.** Radial glow from top center on a dark page. Same family as the blobs.
- **Colored glow shadow under the primary CTA.** Fix: emphasis through contrast, size, and
  placement, not luminescence.
- **Default-dark with glassmorphism.** Dark by reflex, frosted-glass layers everywhere. Fix:
  choose light or dark from the product's context; reserve blur and translucency for UI that
  genuinely layers over content (overlays, sticky headers over scrolling media).
- **Sparklines and mini-charts as decoration.** Charts that measure nothing. Fix: if it is
  not visualizing real data a user needs, remove it.

- **Animated or conic gradient border.** A moving "beam" tracing the edge of a card or input.
  Fix: a static border, or a focus state that only appears on focus.
- **A different tint per card.** Blue, green, purple, amber, and pink cards in one grid, the
  colors encoding nothing. Fix: one surface color; use color only where it carries a category
  or state the user needs.
- **Opacity as the whole color system.** Every surface `white/5`, every border `white/10`,
  every label `white/60`. It produces a uniform haze with no hierarchy. Fix: a small set of
  named, opaque surface and text colors.
- **Low-contrast gray text.** Light gray body or secondary text on white, or mid-gray on dark,
  chosen because it looks refined. It fails contrast checks and reads as timid. Fix: meet WCAG
  AA and get hierarchy from size and weight.
- **The default accent.** The generator's or framework's stock indigo, violet, or blue used as
  the brand color because nothing else was chosen. Fix: derive the accent from the product.
- **Noise or grain overlay** applied to add "texture" over an otherwise default layout. Same
  test as the grid background: brand reinforcement or nothing.

### House defaults and unmade decisions

Every generator has a house style, and slop points in two opposite directions: loud defaults
(the gradient maximalism above) and quiet ones. The quiet tells:

- **The unmodified component-library look.** Stock component-kit output shipped as the
  design: neutral gray palette (zinc/slate), muted gray secondary text, thin borders on every
  surface, the library's default font, no color commitment anywhere. The tell is the absence
  of decisions. A component library is a starting point; fix by making the decisions it
  deferred: palette, type, radius, density, one distinctive move.
- **Borrowed design-language bleed.** The UI reads as another company's design system
  (a corporate design language's shadows, shapes, and signature color) rather than this
  product's. Fine when the product genuinely lives inside that ecosystem and must match it.
  Slop when it is just what the generator absorbed. Fix: derive the visual language from this
  product's brand and context.
- **Stock-photo hero reflex.** Generic lifestyle or workspace photography (or an AI-generated
  equivalent) filling space where the product itself should be. Fix: show the actual product,
  real output, or nothing.

Swapping one house style for another is not deslopping; it trades a loud provenance tell for
a quiet one. When generating, counter your own defaults by making context-driven decisions,
not by imitating a different generator's defaults.

- **Placeholder identity shipped as content.** `Acme Inc`, `John Doe`, `jane@example.com`,
  `Lorem ipsum`, placeholder-image services, and suspiciously round numbers left in a deliverable.
  Fix: use the user's real content; where it does not exist, mark placeholders visibly as
  placeholders so nobody mistakes them for data.
- **One typeface doing nothing.** The framework default at two weights, with an oversized,
  tightly tracked headline as the only typographic idea. Fix: choose the face and build a
  scale with real contrast between levels.
- **Monospace as "technical" seasoning.** Mono type on labels, stats, and eyebrows in a
  product that is not about code. Fine for code, IDs, and tabular figures. Slop as mood.
- **One icon set at one size and stroke** applied to every label, straight from the library.
  Fix: icons where they add recognition, sized and weighted to the type beside them.

### The templated landing page

The tell here is the assembly. Each piece below can be individually defended, but together
they form the page every generator produces, recognizable at a glance:

- announcement badge pill above the hero headline (`✨ New: v2.0 →`) with nothing to announce
- centered hero heading, centered gray subtitle, two side-by-side buttons
- identical section rhythm throughout: colored eyebrow, big centered headline, gray subhead,
  content grid
- three-up feature card grid: icon on top, title, two-line description, all equal weight
- numbered step circles with a connecting line ("How it works")
- stats band (`99.9% uptime / 10M+ requests / 150+ countries`), often with scroll-triggered
  count-up animation
- pricing table with a highlighted middle tier and "Most Popular" badge
- logo marquee and other manufactured social proof: overlapping avatar stacks, five-star
  rows, invented testimonials with names and job titles (inventing proof is a data-honesty
  violation on top of a style problem; never present fabricated data, people, or endorsements
  as real)
- bento grid where every card has the same visual weight regardless of importance
- FAQ accordion and a four-column footer link farm as filler

Fix: structure the page around the product's actual argument. Vary alignment, section
anatomy, and card weight by importance. Ship only sections with real content behind them.

### The templated dashboard

The app-side equivalent. Flag the assembly, not the pieces:

- greeting header (`Welcome back, John 👋`) with a date-range picker that does nothing
- a row of four KPI cards, each with an icon, a big number, and `+12.5% from last month` in green
- one area chart with a gradient fill beside a "Recent activity" list
- a left sidebar with an icon beside every item and an "Upgrade to Pro" card pinned to the bottom
- a table that uses zebra rows, borders, hover highlight, avatars, status pills, and a kebab
  menu all at once
- a user menu with a gradient avatar and a fictional name

Fix: lead with the one thing this user came to do or check. Show numbers only when they are
real and a decision depends on them. Give the primary task most of the screen.

### The templated chat and auth screens

- **Chat.** "How can I help you today?" centered above a two-by-two grid of prompt-starter
  chips, a gradient assistant avatar, and a sparkle on the send button. Fix: starters only when
  they reflect what this product can actually do; otherwise an input and nothing else.
- **Auth.** A centered card with a logo, a row of social sign-in buttons for providers that are
  not wired up, an "or continue with" divider, and a testimonial panel on the other half. Fix:
  only the sign-in methods that exist.

### Dead and fake interface

Controls that imply function they do not have. These are worse than decoration because they
mislead:

- buttons, tabs, filters, and search fields that do nothing
- links that point to `#`
- a command palette, notification bell, or settings gear with nothing behind it
- pagination and counts over data that is not there
- only the first tab or first nav item implemented

Fix: build it, visibly disable it with a reason, or remove it. In a mockup, say which parts
are inert.

### Iconography

- **The benefit icon triad: Zap = fast, Shield = secure, Sparkles = AI.** As a set, an
  instant tell (any one alone is Tier 2). Fix: icons that encode something specific to this
  product, or no icons at all.
- **Sparkles as the universal AI signifier.** Fix: name the capability instead of badging it.
- **Emoji standing in for an icon system** (🚀 🎯 💡 atop feature cards). Distinct from emoji
  flourishes above; this one is structural. Fix: a real icon set, or none.

### Motion

- **Scroll-triggered fade-in-up on everything, staggered.** Fix: default to static; animate
  the one or two moments that earn it.
- **`transition-all` as a reflex.** Fix: transition the specific properties that change.

- **Cursor-following effects.** Spotlight that tracks the pointer across cards, 3D tilt on
  hover, magnetic buttons. Fix: a plain hover state.
- **Typewriter and text-reveal headlines.** The hero sentence typed out or cycling through
  words. It delays the one thing the visitor came to read. Fix: static text.
- **Looping ambient motion.** Drifting gradient backgrounds, floating shapes, an endless
  marquee, a bouncing "scroll down" arrow. Fix: remove; motion should answer an action.
- **Skeleton shimmer for content that is already there**, or a spinner on an instant action.
  Fix: loading states only where there is real latency.
- **Orchestrated page-load entrance** on a tool people open many times a day. Fix: appear
  immediately.
- **Confetti and celebration** for routine actions. Fine for a real, rare milestone.
- **Motion with no reduced-motion fallback.** Fix: honor `prefers-reduced-motion`.

### Density

- **Uniform airiness.** Maximum padding between every section, oversized card padding, low
  information density on every surface. Real products vary density with purpose: dense where
  users work, spacious where they decide. Fix: set density per surface, not globally.

- **Everything centered in one narrow column.** Every section the same max width and
  alignment, so nothing has more weight than anything else. Fix: let important content take
  more room and vary alignment with purpose.
- **Full-viewport hero on a tool.** A screen-tall banner before the user reaches anything
  usable. Fix: put the working surface first.
- **Equal-height, equal-width grids for unequal things.** Fix: size by importance and content.

### States and resilience

Generated UI is usually a single screenshot of the best case. The missing states are the tell:

- **Happy path only.** No empty, loading, error, or disabled state anywhere. Fix: design each
  state for every data-backed surface.
- **Perfectly uniform sample data.** Every name the same length, every title one line, no
  missing fields, no long numbers. Fix: test with long, short, missing, and awkward content,
  and decide how each truncates or wraps.
- **Fixed-width desktop layout only.** Nothing changes below a laptop width. Fix: decide the
  small-screen behavior of each region.
- **Focus rings removed** and hover as the only interaction feedback. Fix: visible focus on
  every interactive element; keyboard operation for every control.
- **Tap targets sized for a cursor.** Fix: at least 44 by 44 CSS pixels for touch.
- **Web habits in a native app.** Web-style cards, custom toggles, and hamburger menus where
  the platform has its own navigation and controls. Fix: use platform conventions unless the
  brand requires otherwise.

## Tier 2: fine when meaningful, slop only when reflexive

This tier is the point of the skill. These are NOT prohibitions. They are "earn it" checks.
Keep them when they carry information; cut them only when they are decoration.

- **Icon beside a nav item.** Good when the icon encodes a real category (for example an
  incident-type icon). Slop when it is a decorative icon next to every label for sameness.
- **Chevron `>` on a row.** Good when it signals expandable or navigates somewhere. Slop when
  it is a default affordance on rows that do nothing.
- **Status pills.** Good when they map to real, distinct states (`Resolved`, `Monitoring`).
  Slop when everything gets a colored pill for visual texture.
- **Relative-time feed with leading dots** (`2s ago`). Good and appropriate in many real
  contexts (activity logs, notifications). Use it when it genuinely helps.
- **Radial progress rings, labeled meter bars, green delta percentages.** Good when they
  visualize a real, meaningful measurement. Slop when they are decorative gauges visualizing
  nothing (a "98.7% coherence" dial). Note: this is about the *decorative* use of data-viz.
  *Fabricating* the underlying numbers is a separate data-honesty problem; never present fake
  data as real.
- **Green checkmark bullets.** Good in a genuine comparison (plans, before/after, supported
  vs. unsupported). Slop as decoration on every feature list.
- **Arrow in a CTA** (`Get Started →`). Fine on the single primary action. Slop when every
  button grows one.
- **Hover scale and shadow lift on cards.** Fine as a consistent system on genuinely
  clickable cards. Slop when every surface inflates on hover.
- **Dark-mode toggle.** Fine. It is a normal convention. Listed only to say: do not flag it.

- **Icon inside an input.** Good for search and for fields whose type is otherwise unclear.
  Slop when every field gets a leading icon.
- **Empty-state illustration.** Good when the empty state is a real first-run moment and the
  illustration explains what goes here. Slop as a stock drawing above "Nothing here yet."
- **Modal dialog.** Good for a decision that must block. Slop when every create, edit, and
  detail view opens in one.
- **Tabs.** Good for peer views of the same object. Slop when used to hide a short page.
- **Sidebar navigation.** Good for an app with many destinations. Slop on a three-page site.
- **Avatar.** Good where identity matters (authorship, assignment, presence). Slop as a
  colored circle beside every row.
- **Shadow.** Good for something that floats above the page (menus, dialogs, dragged items).
  Slop as a soft blur under every card.
- **Card.** Good for a discrete, comparable object. Slop as a wrapper for layout.
- **Skeleton loader.** Good for slow, layout-stable content. Slop everywhere else.
- **Toast.** Good to confirm a background result. Slop to announce what the screen already
  shows.

## Code tells

Visible when reviewing source. Most point at a visual tell above.

- **Utility-class soup repeated verbatim** across elements instead of a component or token.
- **Hardcoded hex values and magic-number spacing** beside an existing token system.
- **`div` with a click handler** where a `button` or `a` belongs; missing labels and `alt`
  text; headings chosen by size instead of structure.
- **`outline: none`** with no replacement focus style.
- **Arbitrary z-index escalation** (`z-50`, `z-[9999]`) in place of a stacking plan.
- **`cursor: pointer` and hover styles** on elements that do nothing.
- **Inline SVG icons duplicated** in every file, or three icon libraries imported at once.
- **Animation libraries imported** to fade one section in.
- **Dark mode half-implemented.** Some surfaces themed, others hardcoded light.
- **Remote placeholder images and fonts** loaded from third-party services in a deliverable.
- **Comments narrating the markup** (`<!-- Hero Section -->` above every block) and emoji in
  class names, logs, or commit text.

Fix: report these with the visual tell they produce; the remedy is the same decision made once
and reused.

## Copy tells

- **Em dashes** (the `—` character) in UI copy. Never use it as clause or parenthetical
  punctuation. Use commas, parentheses, colons, or split the sentence.
- **Slop vocabulary:** supercharge, unleash, effortlessly, seamlessly, blazing fast,
  empower, elevate, "10x your." Fix: say what the product does in concrete terms.
- **The imperative verb-pair headline formula** ("Ship faster. Build smarter."). Tolerable
  once; a tell when it is every heading on the page.
- **Generic button labels.** `Get started`, `Learn more`, `Submit`, `Click here` on every
  action. Fix: name what happens (`Create invoice`, `Compare plans`).
- **Stock microcopy.** `Oops! Something went wrong`, `No items yet. Create your first one to
  get started!`, `Welcome back`, `You're all set!`. Fix: say what happened and what to do next,
  in the product's own voice.
- **Hero formulas.** "The all-in-one platform for X", "Your X, reimagined", "X, but better",
  "Built for developers, by developers", "Trusted by teams at". Fix: state what it does and
  for whom in plain words.
- **Exclamation marks and emoji** in system messages and buttons.
- **Footer filler.** "Made with ❤️", an outdated or invented copyright line, link columns to
  pages that do not exist.
- **Casing inconsistency.** Title Case buttons next to sentence-case headings and back again.
  Pick one convention (sentence case unless the brand system says otherwise) and hold it.

## Review mode

Run this against existing or just-built UI. Works on both code and screenshots.

- Code (HTML/JSX/CSS): report each finding as `file:line - tell - suggested fix`.
- Image / screenshot: report each finding as `region or element - tell - suggested fix` (no
  line numbers).

For Tier 1, flag any occurrence. For Tier 2, the check is conditional: name the element, then
ask whether it carries real meaning here or is decorative, and only flag the decorative case.
Example: "status pill present: does it map to a real distinct state, or is it texture?"

For the templated landing page, dashboard, chat, and auth layouts, flag the *pattern* when
three or more of its pieces co-occur, then list the pieces; do not file ten separate findings
for one templated page.

Report dead and fake interface, fabricated data, and failed contrast or focus first: they
mislead or exclude users, which is worse than looking generic. Then the style tells.

If a design system or brand guide is present, check it before flagging. A tell that the
system specifies is a decision; report it only if the system is applied inconsistently.

### The AI Slop Test

Finish every review with the gut-check:

> Shown this interface and told "AI made it," would they believe you instantly?

If yes, that is the problem. A distinctive interface makes someone ask "how was this made?",
not "which AI made this?"

## Provenance

The base catalog is from deslop-ui by Kim Maida. Added here: icon chips, fake window chrome,
floating mock cards, tilted hero screenshots, badge texture, gradient avatars, stacked edges,
card-wrapping, tooltip overuse; gradient borders, per-card tints, opacity color systems,
low-contrast text, default accents, grain; placeholder identity, single-typeface and monospace
defaults, single icon set; the templated dashboard, chat, and auth layouts; dead and fake
interface; the extra motion entries; the layout entries under Density; States and resilience;
the extra Tier 2 entries; Code tells; the extra copy tells; and the review ordering.
