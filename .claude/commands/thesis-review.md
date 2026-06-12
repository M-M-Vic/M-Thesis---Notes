# Thesis Review & Action Plan

You are conducting a **whole-thesis audit** of this repository — a graduate-level
mathematics thesis in queueing theory (two-class non-preemptive priority $M/M/1$
queues with jockeying and abandonment; Models A, B, B₂, C₂, X). Entry point: `main.tex`.

**This is a read-only diagnostic pass.** Do not edit any files. Your deliverable is a
written **report + action plan**, not a set of fixes. The user (Victor) will decide
which Claude-Code tasks to dispatch and in what order.

Optional argument: `$ARGUMENTS`
- empty → **full audit** of the entire thesis.
- `since <git-ref-or-date>` → **incremental audit**: scope the review to files
  changed since that point (`git log --since=... --name-only` /
  `git diff <ref> --name-only`), but still run the build-cleanliness and
  cross-reference checks globally (those can't be scoped — a stale ref anywhere
  breaks the whole document).

---

## 0. Before You Begin — Context Gathering

Read, in this order:
1. **`CLAUDE.md`** in full — every convention in it is binding and is the rubric for
   this review.
2. **`docs/REPO_MAP.md`** — current file structure, section ↔ file mapping, build
   pipeline. Note the file-number ≠ PDF-section-number caveat.
3. **`docs/REVIEW_CHECKLIST.md`** — history of prior audits and their "Open items for
   the author". **Do not re-flag items already marked done** unless you find a
   regression (the thing was fixed, then reintroduced). Carry forward any open author
   items that are still unresolved.
4. **`Prompts for claude - Review/claude_code_prompts_thesis_edits.md`** (if present) —
   prior task framing/conventions, for continuity of voice and task numbering style.

---

## 1. Build Cleanliness

- Run `latexmk -pdf main.tex` (TeX Live). Capture `main.log`.
- Report: errors (must be zero), warnings (LaTeX + hyperref + float), overfull/underfull
  hbox count and the worst offenders (file:line + magnitude), page count vs. last
  recorded baseline in `docs/REPO_MAP.md`/`docs/REVIEW_CHECKLIST.md`.
- `grep -rn '\\ref{\|\\eqref{\|\\label{'` to confirm: no duplicate labels, every
  `\ref`/`\eqref` target resolves, no literal `??` survives in the PDF/log.

## 2. Notation & Convention Audit (CLAUDE.md §1–§3)

Across every chapter:
- `π₀` vs `π(0,0)` kept distinct everywhere they appear (prose and equations).
- `N1, N2, N` consistently described as **in-queue, excluding the customer in
  service**.
- State spaces `S` / `S̃` used per the declared policy (currently `S~` appears only
  in Model A — flag if another section silently introduces `S̃` without the author's
  sign-off, per CLAUDE.md §6's open policy question).
- Generating-function / PPGF notation (`P(x,y)`, `P_x`, `P_y`, `\tP`, `\tilde P`, LST
  `\widetilde{B}_C(s)`) used consistently with the declared macros.
- Every principle invocation (Little's Law, PASTA, memorylessness, Poisson
  superposition/thinning, Pollaczek–Khinchine) is **named explicitly**, never silent.
- Stability/traffic-intensity statement present and correct wherever required
  (CLAUDE.md §2 — different conditions for non-abandonment vs. C₂-type models).

## 3. Section-Structure Conformance (CLAUDE.md §6)

For each model section (A, B, B₂, C₂, X, and the head-of-line experiment sections
B₂¹/C₂¹), check the canonical spine: Preamble → Stability → Reduced fundamental
equation → Theorem+Corollary (π₀, π(0,0)) → P_y(y) (Probabilistic then Analytical, or
explained absence) → Recovery of P(x,y) → Limits & sanity checks. Flag deviations,
but **do not re-litigate** the open `[AUTHOR]` flag on Model A's
Probabilistic/Analytical ordering (`chapters/06_model_a.tex:52`) — just confirm it's
still flagged and carry it forward.

## 4. Equation Labels, Macros, Known Cleanup Items (CLAUDE.md §5)

- All labels conform to `eq:<Model>:*` (`A`, `B`, `B2`, `C2`, `gen`, plus the
  head-of-line models' established prefixes). Flag any legacy/mixed prefix.
- `\mathcal{I}` clash (server idle/busy indicator vs. auxiliary integrals) — confirm
  it's resolved consistently across C₂ and B₂, or flag remaining instances.
- No editorial scaffolding (`[NEW]`, `[MINE]`, `[Discuss: …]`, `[Introduce: …]`)
  remains **unless** it's a deliberate open author flag already tracked in
  `docs/REVIEW_CHECKLIST.md` — list those by file:line so the author can triage.
- Section titles: no redundant trailing "M/M/1"; "Analysis of Model …" used
  uniformly.

## 5. Citations (CLAUDE.md §7)

- Every non-trivial claim (named theorem, classical result, formula from the
  literature) has a `\cite{}`.
- Every `\cite{}` key resolves in `references.bib`; list any bib entries that are
  **defined but never cited** (candidates for removal or for a future section).
- No invented keys. List any `% TODO: cite` / `% TODO(citation)` flags by file:line.

## 6. Prose, Grammar, British English

- Spot-check (don't exhaustively re-proofread already-reviewed sections per
  `docs/REVIEW_CHECKLIST.md`) for US spellings (`-ize`, `behavior`, `center`,
  `modeling` etc., excluding the documented LaTeX-command exemptions), passive-voice
  overuse, hedging, repetition.
- For an **incremental** audit (`since <ref>`), do a full line-by-line pass of the
  changed `.tex` regions instead — this mirrors the `daily-thesis-review` scheduled
  task but feeds into the structured output below.

## 7. Figures, Tables, Code Pipeline Consistency

- Every figure in `figures/` (and `figures/results/`, `figures/validation/`) that is
  `\input`/`\includegraphics`'d is referenced by `Figure~\ref{...}` in prose.
- `results/derived_metrics.tex` macros vs. any hardcoded numbers in
  `chapters/12_comparison.tex` / `13_results.tex` — flag new hardcoded values that
  should route through `\loss*`-style macros.
- If `Code/` was touched, confirm the corresponding `build_*.py` → notebook →
  `figures/` pipeline is still consistent (don't execute notebooks unless asked —
  just check for drift: referenced output files that don't exist, or generated files
  newer/older than their source script in a way that suggests staleness).

---

## 8. Deliverable

Write a single new report to `docs/REVIEW_<YYYY-MM-DD>.md` (use today's date) with
this structure, and print a concise version of it to the chat:

### A. Executive Summary
2–4 sentences: overall state, build status, headline risks.

### B. Findings by Category
One subsection per §1–7 above. Each finding: `file:line`, what's wrong, why it
matters (tie back to the specific CLAUDE.md rule). Carried-forward open items from
`docs/REVIEW_CHECKLIST.md` get their own clearly marked subsection ("Still open from
prior audits").

### C. Claude-Code Task List (ordered)
A numbered, dependency-ordered list of tasks Claude Code can execute autonomously —
no domain judgment required (label/ref fixes, build warnings, spelling, macro
unification, structure reordering, citation-key corrections, figure cross-ref
insertions, etc.). For each task give: a short title, the files it touches, and a
one-line rationale. Order by dependency (e.g., fix build errors before doing a
prose pass that requires a clean compile; fix label-scheme migrations before adding
new cross-references to those labels).

### D. Author-Only Task List
Items requiring Victor's judgment: title confirmation, citation *sourcing* (Claude
can flag a missing citation but not invent one), interpretive/structural decisions
flagged `[AUTHOR]`, content additions that need new mathematical derivation or
results, anything affecting the thesis's argument or scope.

### E. Recommended Execution Order
A short phased plan tying C and D together — e.g. "Phase 1: build/ref fixes (C1–C3,
no dependencies) → Phase 2: structure conformance (C4–C6, depends on Phase 1 clean
build) → Phase 3: author decisions needed before C7–C9 can proceed → Phase 4: final
audit re-run." Make explicit which author decisions block which Claude tasks.

---

## 9. Rules

- **No edits in this pass.** If something is trivially fixable and you're tempted to
  just do it, note it in the task list instead — the user reviews the plan first.
- Use exact file:line references throughout; verify every claim against the current
  file contents (don't rely on memory of past audits beyond what
  `docs/REVIEW_CHECKLIST.md` records).
- Don't invent citations, section content, or numeric results.
- If the user asks you to proceed with the plan immediately afterwards, convert
  section C into tracked tasks with `TaskCreate` before starting.
