# Thesis Talk Design System

A presentation design system for **Victor Dominguez Sainz's** MSc Mathematics
master-thesis defence at the **Vrije Universiteit Amsterdam**:

> *Exact Generating-Function Analysis of a Two-Class Non-Preemptive Priority
> M/M/1 Queue with Jockeying and Abandonment*
> Supervisor: René Bekker · Second reader: Wouter Kager

The talk (~40 minutes) walks through a family of queueing models — a single
server shared by a **priority (class 1)** and a **non-priority (class 2)**
stream — augmented with two waiting-room mechanisms: **jockeying** (a waiting
customer switches queue) and **abandonment** (a waiting customer leaves). The
central object is the bivariate Probability Generating Function *P(x,y)*; the
deck's job is to make a dense analytical argument legible and paced.

This system exists so any slide, figure, or handout for the defence is built
from one coherent, blue-free "mathematics" look, with LaTeX set natively.

## Sources
- **Codebase (read-only):** `M-Thesis---Notes/` — LaTeX thesis (`main.tex`,
  `chapters/*.tex`), Python analysis (`Code/*.py`, notebooks), result figures
  (`figures/results/*.png`), and derived metrics (`results/derived_metrics.json`).
  All headline numbers in the sample slides are lifted from that JSON.
- **Logo:** `uploads/VU-logo-RGB.png` → `assets/vu-logo.png`.
- No brand typeface or component library was provided; the visual system below
  is an original, deliberate design for this talk (see Visual Foundations).

---

## CONTENT FUNDAMENTALS — how copy is written

- **Register:** precise, academic, quietly confident. Third-person and passive
  where a result is stated ("Imposing boundedness at x = 1 determines the
  constant"); first-person plural for the argument's throughline ("We solve
  less complex models", "we introduce an alternative state space"). Never "you".
- **Vocabulary is exact.** *Customer* (not user/patient), *priority /
  non-priority class*, *jockeying*, *abandonment*, *kernel*, *closed form*,
  *tractable / intractable*, *PGF*, *CTMC*. Models are always named with their
  letter: *Model A*, *Model B₂*, *Model Cᴴ*, *Model X*.
- **Slide titles are claims, not labels.** Prefer "Jockeying redistributes;
  abandonment shortens" over "Results". Prefer "Class-1 customers jockey to
  Queue 2" over "Model B₂". The kicker carries the section/number; the title
  carries the finding.
- **Symbols stay in math.** Rates and variables (λ₁, λ₂, μ, γ₁, θ₁, ρ, N₁,
  P(x,y)) are set in mono inline or in KaTeX, never spelled out.
- **Casing:** sentence case for titles and captions; UPPERCASE only for the
  small tracked eyebrow/label. Em dashes for asides; "vs." for comparisons.
- **No emoji, no exclamation, no hype.** Findings are stated plainly and let
  the numbers carry weight. Captions name the model and parameter regime
  ("Model B₂ · ρ = 0.70 · truncated CTMC").

---

## VISUAL FOUNDATIONS

**Overall vibe.** Warm academic paper, not a corporate slide template. Flat
surfaces, generous margins, a scholarly serif for display, a clean technical
sans for labels, and mathematics rendered in Computer Modern via KaTeX. Clean
and rigorous, but the warm cream ground and terracotta accent keep it from
feeling severe.

**Colour.** Deliberately **blue-free** (a personal preference of the author,
and a clean break from the VU house blue). A warm neutral ramp (`--ink-900`
→ `--paper`) carries text and surfaces. Four saturated hues do semantic work:
- **Terracotta** `#C0563A` — primary accent **and** the priority class (class 1).
- **Pine** `#327B5B` — the non-priority class (class 2), and the "solved" status.
- **Ochre** `#CB9639` — the jockeying mechanism / highlights.
- **Plum** `#7E4A66` — the abandonment mechanism.
The two-class contrast (terracotta vs. pine) recurs everywhere: queue diagrams,
badges, stat callouts. "Open" problems are terracotta, "solved" ones pine.

**Type.** *Spectral* (serif) for hero, dividers, slide titles and math-adjacent
prose — warm, high-contrast, scholarly. *IBM Plex Sans* for eyebrows, captions,
UI and dense labels. *IBM Plex Mono* for rates, model names and state variables.
Math itself is **KaTeX** (Computer Modern), sized to sit inline with the serif.
Display sizes use tight tracking (−0.02em); the eyebrow is wide-tracked (0.14em)
uppercase. Slide body never drops below 20px.

**Backgrounds.** Two grounds only: warm cream `--paper` for content, and near-
black `--ink-900` for section dividers, the closing slide and occasional accent
moments. A faint dotted "grid-paper" texture (`.ds-gridpaper` / `.stage--paper`,
22–26px radial dots in `--line-200`) sits under the title and dividers — a nod
to squared maths paper. No photography, no gradients, no illustration.

**Cards & surfaces.** Flat `--surface` (white) panels on the cream ground, held
by a **1px warm hairline** (`--border-subtle`, `#E4DBCC`) — hairlines do most of
the structural work. Radii: 6px chips, 10px cards/callouts, 16px large panels.
Corners are soft, never pill-round except tags. We avoid the "rounded card with a
coloured left-border only" cliché: callouts use a full hairline plus a coloured
header tag; the one intentional left-rule is `StatCallout`, an accepted way to
anchor a single metric.

**Shadows.** Low, soft and **warm-tinted** (`rgba(56,40,24,·)`), never a cool
grey drop shadow. `--shadow-sm` for resting cards, `--shadow-md` for raised
panels, `--shadow-accent` (terracotta-tinted) to mark the current/active item.

**Borders & rules.** Table headers get a 1.5px ink underline; rows a 1px
hairline. Section-divider and title accents use a 72–80px × 4px terracotta rule.

**Motion.** Restrained. Fades and short rises on `--ease-out` (0.22,0.61,0.36,1)
over 140–480ms; entrance animations reveal from a hidden base and gate on the
active slide so print/PDF/reduced-motion always show content. No bounces, no
looping decoration — this is a formal defence.

**Hover / press** (for any interactive handout): hover lifts a card to
`--shadow-md` and deepens the hue one step (`-600` tokens); press settles back to
`--shadow-sm`. Focus uses the terracotta `--focus-ring`. No colour is used as the
sole signal — status always pairs a hue with a dot and a word.

**Layout.** Slides are a fixed **1280×720** canvas with 72px side / 56px top-
bottom safe margins and a 40px footer band (VU logo left, page number right).
Two-column content uses a 40px gutter. One rhythm across every slide type.

---

## ICONOGRAPHY

- **No icon set, by design.** A mathematics talk needs almost no UI icons; the
  system ships none and none should be invented. Where a mark would normally go,
  use type, a status **dot** (a small filled circle, the one recurring glyph),
  or a coloured tag.
- **The real "icons" are domain diagrams.** The recurring **queue schematic**
  (two hatched queues → one circular server) is provided as the `QueueDiagram`
  React component — pure SVG on the palette, with optional jockeying/abandonment
  arrows. Reuse it rather than drawing new diagrams. It is the single piece of
  bespoke vector art in the system and is a faithful recreation of the thesis's
  own TikZ figures (`figures/*.tikz`), not decoration.
- **Result figures are images, not redrawn.** The matplotlib plots from the
  thesis live in `assets/figures/` and are shown through the `Figure` component.
  Never re-draw a plot as SVG — embed the PNG.
- **Symbols over glyphs.** Arrows use unicode (↓ ↑ →); rates use their Greek
  letters. No emoji anywhere.
- **Logo:** the VU Amsterdam mark (`assets/vu-logo.png`) is the only logo. Use it
  full-colour on paper, or knocked out to white (`filter: brightness(0)
  invert(1)`) on ink. Do not recolour or reconstruct it.

---

## INDEX — what's in this system

**Global entry:** `styles.css` (link this one file) → imports the tokens below.

**Tokens** (`tokens/`)
- `colors.css` — neutral ramp, four brand hues, status, semantic aliases.
- `typography.css` — size / weight / line-height / tracking ramp + roles.
- `spacing.css` — 4px grid + slide-layout constants.
- `effects.css` — radii, borders, warm shadows, focus ring, motion.
- `fonts.css` — Google Fonts import + family tokens.
- `base.css` — light element defaults + `.ds-eyebrow`, `.ds-mono`, `.ds-gridpaper`.

**Components** — reusable React primitives (`window.ThesisTalkDesignSystem_e12f8a`):
- **`Equation`** (`components/math/`) — KaTeX display/inline equation, optional number.
- **`TheoremBox`** (`components/math/`) — amsthm-style theorem/lemma/definition/remark callout.
- **`QueueDiagram`** (`components/math/`) — the two-class one-server schematic, with jockey/abandon arrows (both directions).
- **`FlowDiagram`** (`components/math/`) — the state-transition diagrams on S ((n₁,n₂) grid) or S̃ ((n₂,n) with the diagonal n=n₂), per-mechanism rate arrows, faithful to the thesis TikZ.
- **`BirthDeathChain`** (`components/math/`) — a 1-D birth–death queue chain (M/M/1 constant μ, or M/M/1+M impatience μ+nθ); arrivals over the top, departures under the bottom.
- **`ModelBadge`** (`components/content/`) — model tag coloured by solved/open status.
- **`StatCallout`** (`components/content/`) — one headline metric with trend arrow.
- **`Chip`** (`components/content/`) — compact param/keyword/class tag.
- **`Figure`** (`components/content/`) — framed result image with numbered caption + source.

**Templates** (`templates/`)
- `thesis-talk/ThesisTalk.dc.html` — the defence deck starting point (title,
  taxonomy table, model, theorem and results slides). Built on `deck-stage.js`.

**Sample slides** (`slides/`) — standalone 1280×720 reference slides, one per
type (title, section divider, overview table, model, theorem, results, closing),
tagged as Design-System cards.

**Foundation cards** (`guidelines/`) — colour, type, spacing and brand specimen
cards for the Design System tab.

**Assets** (`assets/`) — `vu-logo.png` and the thesis result figures under
`assets/figures/`.

## Notes / substitutions
- **Fonts** are loaded from Google Fonts (Spectral, IBM Plex Sans, IBM Plex
  Mono) via `@import` in `tokens/fonts.css`, so the compiler reports 0 local
  `@font-face` webfonts. This is intentional — no brand font was supplied. If
  self-hosted or licensed faces are preferred, drop the files in and swap the
  import for `@font-face` rules.
- **KaTeX** is loaded per-slide from its CDN; it injects its own Computer-Modern
  webfonts at runtime.
