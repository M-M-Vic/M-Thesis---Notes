# Committee-Review Checklist

> Final integration audit (task G1), 2026-06-11. Maps every task in
> `Prompts for claude - Review/claude_code_prompts_thesis_edits.md` to the commit
> that addressed it, and records the residual findings of the audit itself.

## 2026-06-27 full audit — autonomous fixes executed

> Source: `docs/REVIEW_2026-06-27.md` (full whole-thesis audit, `/thesis-review`). Run on the
> post-restructure document: appendix now excluded from the PDF (`main.tex:93`), the
> comparison inlined into `13_results.tex` (no `12_comparison.tex`), per-model
> mean-queue/waiting subsections archived to `mean_queue_and_waiting_times.tex`.

- **Build**: PASS, 0 errors / 0 LaTeX warnings. **67 pages** (was 98 pp; appendix excluded +
  mean-queue removal). 244 unique labels (chapters + `main.tex`), no duplicates; 518
  `\ref`/`\eqref`/`\Cref` targets, all resolve. 10 overfull + 7 underfull hboxes (cosmetic);
  1 cosmetic pdfTeX duplicate-anchor warning (`equation.3.6`).
- **Citations**: 16 cited / 16 defined, perfect 1:1; no orphans, no undefined keys.
- **Autonomous fixes** (branch `thesis-review-2026-06-27`, tasks C1–C5):
  - **C1** Stability strictness: `$\rho\le1$` → `$\rho<1$` in `06_model_a.tex`
    (Theorem~`thm:A:PGF` hypothesis :55, Corollary~`cor:A:pi0` :72) and `08_model_b2.tex:161`,
    matching each model's own `eq:*:stability` definition and CLAUDE.md §2 (the chain is
    null-recurrent at `\rho=1`, so the non-strict bound was wrong).
  - **C2** Eight prose typos: `anysuch`→`any such` (`06:122`), `signifficantly`→`significantly`
    (`10:6`), `theis`→`this` (`10:4`), doubled "through the" (`09:144`), `ans`→`and` /
    `brievity`→`brevity` (`09:147`), doubled "the the" (`08:80`), `As in for`→`As in`
    (`08:78`, `08:69`).
  - **C3** Bare cross-ref `\ref{apx:A:PPGF_Stilde}` → `Approximation~\ref{...}` (`06:7`).
  - **C4** `docs/REPO_MAP.md` refreshed to the current layout (67 pp, no `12_comparison`,
    appendix excluded, 16/16 citations, 0 in-source markers).
  - **C5** This entry.
- **Resolved since 2026-06-19** (cleared carry-forwards): working-title `TODO-confirm`;
  Kernel-Method `TODO: cite` (now `\cite{cohen1956delay}`); Model-A `[AUTHOR]` ordering flag;
  `abate2000asymptotic` / `tian2006vacation` orphan bib entries (removed).
- **Open items for the author (2026-06-27)**:
  1. Hadamard finite-part citation (`07_model_b.tex:375`) — supply source, or leave as the
     framed open obstruction.
  2. (optional) Kernel Method could additionally cite `fayolle1999random` (`06_model_a.tex:122`).
  3. (optional) Whether the appendix `15_appendix_numerics.tex` stays excluded from the PDF.
  4. (optional, cosmetic) 36.86 pt overfull box at `02_literature.tex:51–69` (content-touching).

## 2026-06-19 full audit — Phase 1 & 2 executed

> Source: `docs/REVIEW_2026-06-19.md` (full whole-thesis audit). This entry supersedes the
> structural facts of the 2026-06-12/G1 sections (the document was restructured in the
> interim: Model-X analysis deleted → `rem:B:modelX`; `12_comparison.tex` nested inside
> `13_results.tex`; new `15_appendix_numerics.tex`). See `docs/REPO_MAP.md` (refreshed
> 2026-06-19) for the current layout.

- **Build**: still PASS, 0 errors / 0 LaTeX warnings. **98 pages** (was 105 pp). 275
  unique labels (no duplicates); 636 `\ref`/`\eqref`/`\Cref` targets, all resolve. 16
  overfull + 4 underfull hboxes (cosmetic, no regression); 3 cosmetic pdfTeX
  duplicate-anchor warnings.
- **Phase 1 + Phase 2 fixes** (branch `phase1-2-review-fixes`) — autonomous tasks C1–C9:
  - **C1** `docs/REPO_MAP.md` + this file refreshed to the post-restructure layout (98 pp,
    no `05_model_x`, `12`→nested in `13`, `15_appendix_numerics` added).
  - **C2** Hardcoded "Lemma~2" → `Lemma~\ref{lem:gen:PPGF_dynamics}` (`15_appendix:27`).
  - **C3** Added `\label{thm:C2:PGF}` to the C₂ theorem; renamed `thm:B2`→`thm:B2:PGF`;
    validation-table T-A/T-B₂/T-C₂ rows now `\ref` the theorems (`13_results.tex`).
  - **C4** "Reading the fundamental equation" paragraph promoted to
    `\begin{remark}\label{rem:gen:reading}` (`04_model_description.tex`); the 4 "remark
    following Lemma 1" citations (B₂, C₂, C₂ᴴ, conclusion) now `\ref{rem:gen:reading}`.
  - **C5** Loss-fraction symbol unified to `L_1` (was `P_{\mathrm{loss}}^{(1)}` in the
    appendix loss-accounting table + conclusion).
  - **C6** Abstract uses `\BH`/`\CH` macros (was literal `$B_2^H$`/`$C_2^H$`) and
    "head-of-line" (was "head-of-the-line").
  - **C7** Orphaned `tab:comp:loss_acct` now cross-referenced in prose (`15_appendix`).
  - **C8** `eq:results:EN_A` → `eq:comp:EN_A` (namespace consistency, `12_comparison`).
  - **C9** Trailing blank lines trimmed from `09_model_c2.tex`. (The 36.86 pt literature
    box was left as-is — content-touching, deferred.)
- **Open items for the author (as of 2026-06-19)** — unchanged carry-forwards:
  1. Confirm working title (`main.tex:59`, 3 candidates).
  2. Kernel-Method citation (`06_model_a.tex:121`).
  3. Hadamard finite-part citation (`07_model_b.tex:483`).
  4. `[AUTHOR]` Probabilistic/Analytical ordering in Model-A (`06_model_a.tex:52`).
  5. S̃ state-space policy (half-applied: general in `04`, used only in Model-A).
  6. Cite or remove `abate2000asymptotic` / `tian2006vacation` from `references.bib`.
  7. Whether to macro-ise the inline hardcoded CTMC sweep numbers (drift risk).

## Phase 1 follow-up (2026-06-12)

> Source: `docs/REVIEW_2026-06-12.md` (full audit) → Phase 1 of its "Recommended
> Execution Order" (tasks C1–C4, all independent, no author input required).

- **Build**: still PASS, 0 errors / 0 LaTeX warnings. **105 pages** (was 99pp at
  G1; growth is the head-of-line experiment chapters 10/11 plus narrative additions
  since G1). 10 cosmetic pdfTeX `destination with the same identifier` warnings
  remain (unchanged, harmless — see G1 notes).
- **Overfull/underfull hboxes**: down from 24 (20 overfull + 4 underfull, per the
  2026-06-12 audit) to **21** (17 overfull + 4 underfull). The four largest boxes
  flagged by the audit were addressed (task C3):
  - 61.97pt `chapters/13_results.tex:27` (validation-summary table) → fixed with
    `\footnotesize`.
  - 57.85pt `chapters/06_model_a.tex:208` (single-line `align*` chain) → broken
    into 4 `\\`-separated rows.
  - 43.37pt `chapters/09_model_c2.tex:265` and a duplicate 43.37pt instance in
    `chapters/11_model_c21.tex:265` (same derivation pattern, copied into the
    head-of-line $C_2^1$ section) → both `align*` blocks re-broken across rows.
  - 41.57pt `chapters/09_model_c2.tex:74` (`eq:C2:fundamental`, single-line
    `equation`) → converted to `multline` (now 1.99pt, under threshold).
  - Remaining 21 boxes are all <15pt and left alone, per the no-content-change rule.
- **Cross-reference added** (task C2): `chapters/10_model_b21.tex` "Limits and
  sanity checks" now points forward to the $k$-ladder discussion in
  `chapters/14_conclusion.tex` (`sec:future_work`), tying $\BH$ to the $k=1$ rung
  and Model-$B_2$ to the $k\to\infty$ limit.
- **Derived-metrics pipeline extended** (task C4): `Code/compute_derived_metrics.py`
  now also emits (i) the system-wide loss fraction $L=(\pi_0-(1-\rho))/\rho$ for
  $C_2$/$\CH$ at all three grid loads (`\lossSysCtwo*`, `\lossSysCH*`,
  `\lossSysCtwoCanon`), and (ii) the off-grid $\theta_1\in\{0.05,5.0\}$ class-1 loss
  fraction at $\rho=0.70$ (`\lossCtwoThetaLow`, `\lossCtwoThetaHigh`). All three
  previously-hardcoded numbers in `chapters/12_comparison.tex` (lines ~600, ~601,
  ~629–630) and Table 9's (`tab:comp:loss`) system-wide $L$ column now route through
  these macros — closes item 5 below.
- **Citations**: still 16 cited keys, all resolve; `abate2000asymptotic` and
  `tian2006vacation` remain defined but unused in `references.bib`.
- **Labels/refs**: 297 labels, all unique; 285 `\ref`/`\eqref`/`\Cref` targets, all
  resolve. No duplicates, no `??`.

## Task → commit map

| Task | Description | Commit | Status |
|---|---|---|---|
| P0.1 | Repo map and build baseline | `2ed780a` (dup. `424097a`) | ✅ done |
| A1 | Typo and copy-edit sweep | `2db0160`, UK-spelling pass `490c9c1` | ✅ done |
| A2 | Cross-reference style and micro-corrections | `ad21641` | ✅ done |
| B1 | Head-of-line notation unification (`\BH`, `\CH`) + Table 1/3 reconciliation | `89acd7f` | ✅ done — audit grep finds no legacy `B_2^1`/`C_2^1` strings |
| B2 | Move Model-X analysis after Model-B; rewrite roadmap | `bc8e108`, repo-map note `5ef1807` | ✅ done — roadmap order verified against `main.tex` input order |
| C1 | Interpretive paragraph after Lemma 1 | `2169873` | ✅ done |
| C2 | Justify Hadamard finite part in Model-B | `6f7a0aa` | ✅ done |
| C3 | Promote γ₁→0⁺ singular-limit discussion to a Remark (Model-B₂) | `c81b0ee` | ✅ done — Remark 1 (`rem:B2:singular_limit`), `remark` environment added to preamble |
| C4 | Rigor patches (Foster–Lyapunov, C₂ necessity, P(N₁=0\|busy)) | `e9052e6` | ✅ done |
| C5 | Reframe §6.2 / demote Theorem 2 to characterised approximation | `26835e4` | ✅ done — audit grep confirms "Theorem 2" no longer appears |
| D1 | Derived metrics pipeline (`results/derived_metrics.tex`) | `51938ad` | ✅ done |
| D2 | Figure consistency pass | `6483a7b` (binaries `3c01858`) | ✅ done |
| E1 | Resolve the two [AUTHOR] placeholders | `290535e` | ✅ done |
| E2 | Insight paragraphs for §12–13 | `e2f4208` | ✅ done |
| E3 | Loss-fraction column in comparison table | `3ac898e` | ✅ done |
| F1 | Literature review | `e4217b9` | ✅ done |
| F2 | Conclusion & future work | `b7d69d5` | ✅ done |
| F3 | Abstract rewrite + working title | `e09b5cc` | ✅ done — title still flagged `TODO-confirm` (author's choice of 1 of 3 candidates) |
| G1 | Final integration audit | this commit | ✅ done |

## G1 audit findings

### Build (clean from scratch)
- **Zero errors, zero LaTeX warnings.** 99 pages.
- The blanket `pdfTeX warning: destination with the same identifier` (one per
  figure/table) was caused by `float` being loaded *after* `hyperref`; fixed by
  reordering in `main.tex`. No such warnings remain.
- 17 **overfull hboxes** remain (cosmetic; all pre-existing). Largest:
  61.97pt in `chapters/13_results.tex` (¶ at lines 29–46), 57.85pt in a
  `06_model_a.tex` display (line 209), 48.15pt in `02_literature.tex`,
  43.37pt / 41.57pt in `08_model_b2.tex` displays; the other 12 are < 15pt.

### Leftover greps
- "Theorem 2": none. Old head-of-line notation: none — all usages go through `\BH`/`\CH`.
- Literal "??": none in source; no undefined refs in the log.
- Remaining comment-only flags (invisible in the PDF; **author decisions, not fixed**):
  - `main.tex:49` — `TODO-confirm` working title (1 of 3 candidates).
  - `chapters/06_model_a.tex:52` — `[AUTHOR]` note on the Probabilistic/Analytical
    subsubsection ordering vs the canonical spine.
  - `chapters/06_model_a.tex:122` — `TODO: cite` Kernel Method reference (cannot
    invent a citation; needs the author's pick, e.g. Cohen or Bayer & Boxma).
  - `chapters/07_model_b.tex:391` — `TODO(citation)` Hadamard finite-part reference.
  - `chapters/07_model_b.tex:422` and `chapters/05_model_x.tex:420` — `[AUTHOR]`
    flags on the regularisation step and the Model-B-vs-X closure contrast.
  - `chapters/13_results.tex` — two `% [Discuss: …]` and one `% [Introduce: …]`
    scaffolding comments inside figure captions / before §"Experiment models"
    (same spirit as the above; left for the author).

### Reference audit
- All 271 `\ref`/`\eqref` targets resolve (4 live in generated
  `figures/results/tab_*.tex` files); **no duplicate labels**.
- All 21 cite keys exist in `references.bib`. Two bib entries are **never cited**
  and therefore do not print: `abate2000asymptotic`, `tian2006vacation`
  (left in place in case they are wanted for F1/F2 follow-ups).
- 8 figures were defined but never referenced in prose; **fixed** by adding
  `Figure~\ref{…}` sentences: the four model queue-layout figures (A, B, B₂, C₂),
  the `S~` transition diagram (`fig:diagram-gen-stilde`), the two head-of-line
  validation figures (`fig:val_experiment`, `fig:val_experiment_pi`), and the
  strong-jockeying figure (`fig:conv:b2_inf`).

### Consistency spot-checks
- **Roadmap vs section order:** matches (literature → prelim → Model-X description
  → A → B → X-analysis → B₂ → C₂ → \BH → \CH → comparison → results → conclusion).
- **Table 1 vs Table 3:** Table 1 omitted Model-X although its own following prose
  says "As one can see, … Model-X … left incomplete"; **fixed** by adding an X row
  (open, PDE with transcendental characteristics). Table 9 (`tab:comp:loss`) lists
  only C₂/\CH by design (only abandonment models lose customers) — consistent.
- **Abstract vs content:** all structural claims verified (hierarchy, pinning
  principles per model, named obstructions for B and X, heuristic-approximation
  framing for the `S~` recursion, "nearly one in four" ↔ L₁ = 0.232).
- **Loss fractions:** prose `$L_1=0.232$` and the six hardcoded L₁ cells of
  Table 9 **switched to the `\loss*` macros** from `results/derived_metrics.tex`
  (values verified identical first). Residuals that cannot come from macros today:
  the "23.2 %" restatement in the same sentence, and Table 9's system-wide $L$
  column (no `\L*` macros exist — $L = L_1\rho_1/\rho$; verified consistent by
  hand). Adding those macros would require extending
  `Code/compute_derived_metrics.py` and regenerating.

## Open items for the author
1. ~~C3~~ Done in `c81b0ee` — all playbook tasks are now addressed.
2. Confirm the working title (`main.tex:59`, three candidates listed inline).
3. Supply the two missing citations:
   - `chapters/06_model_a.tex:121` — Kernel Method (e.g. Bayer & Boxma, or Cohen's
     book).
   - `chapters/07_model_b.tex:479` — Hadamard finite-part integrals.
4. `chapters/06_model_a.tex:52` — `[AUTHOR]` flag on the Probabilistic/Analytical
   subsubsection ordering vs. the canonical spine (CLAUDE.md §6 step 5). The
   `07_model_b.tex`/`05_model_x.tex` regularisation/closure `[AUTHOR]` flags and the
   `13_results.tex` `[Discuss:]`/`[Introduce:]` scaffolding from G1 have since been
   resolved into narrative (verified in the 2026-06-12 audit) — only this one
   remains.
5. ~~Extend the metrics script with system-wide loss macros ($L$)~~ Done
   (Phase 1, C4, 2026-06-12) — see above.
