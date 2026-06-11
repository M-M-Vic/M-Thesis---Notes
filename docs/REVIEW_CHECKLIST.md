# Committee-Review Checklist

> Final integration audit (task G1), 2026-06-11. Maps every task in
> `Prompts for claude - Review/claude_code_prompts_thesis_edits.md` to the commit
> that addressed it, and records the residual findings of the audit itself.

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
| C3 | Promote γ₁→0⁺ singular-limit discussion to a Remark (Model-B₂) | — | ❌ **not addressed** — the discussion still sits inside the proof of the theorem in `chapters/08_model_b2.tex` (after `eq:B2:Pxy_proof`); no `remark` environment is declared in the preamble |
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
1. **C3 is the only unaddressed playbook task** (singular-limit Remark in B₂).
2. Confirm the working title (`main.tex:49`).
3. Supply the two missing citations (Kernel Method; Hadamard finite part).
4. Resolve the remaining `[AUTHOR]`/`[Discuss]` comment flags listed above.
5. Optionally extend the metrics script with system-wide loss macros ($L$) and a
   percent-form macro so no loss number is hardcoded anywhere.
