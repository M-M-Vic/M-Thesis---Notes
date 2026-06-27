# Repository Map & Build Baseline

> Generated baseline so later sessions can read this instead of re-exploring.
> Snapshot date: 2026-06-27. Regenerate after large structural changes.

Thesis: *Two-class non-preemptive priority M/M/1 queues with jockeying and
abandonment* (Victor Dominguez Sainz). Compiled file: `main.tex` (`article` class).

---

## 1. Repository structure

### Main file & assembly
- [main.tex](../main.tex) — root document. `\input`s the chapter files and runs
  `\bibliography{references}`. Build artifacts (`main.aux/.bbl/.log/...`) are git-ignored.

> ⚠️ **File number ≠ PDF section number, and three files are special.**
> - `05_model_x.tex` was **deleted** (2026-06-19): the standalone *Analysis of Model-X*
>   section is gone, demoted to **Remark~`rem:B:modelX`** inside Model-B
>   (`07_model_b.tex`). Model-X now survives only as the *model description* in
>   `04_model_description.tex` and as that remark.
> - `12_comparison.tex` **no longer exists** as a separate file (2026-06-27 results
>   restructure): the comparison is now an inline `\subsection{Structural comparison of the
>   solved models}` (`sec:comparison`) **inside** `13_results.tex` (line 57).
> - `15_appendix_numerics.tex` still exists but is **excluded** from the compiled PDF
>   (commented out at `main.tex:93`, 2026-06-27).
> Always reference by `\label`, never by hardcoded number.

### Rendered section order (PDF)
`§1` Introduction · `§2` Literature · `§3` Preliminaries · `§4` Model description (Model-X)
· `§5` Model-A · `§6` Model-B · `§7` Model-B₂ · `§8` Model-C₂ · `§9` Model-B₂ᴴ (`\BH`)
· `§10` Model-C₂ᴴ (`\CH`) · `§11` Results (with `§11.x` Comparison + Convergence)
· `§12` Conclusion & Future Work. **Appendix A** (extended numerical validation) lives in
`chapters/15_appendix_numerics.tex` but is **not** compiled (re-enable by uncommenting
`main.tex:93`).

### Bibliography
- [references.bib](../references.bib) — single BibTeX database (e.g. `adan2002queueing`).
  **16 entries; all 16 cited** (the formerly-uncited `abate2000asymptotic` /
  `tian2006vacation` were removed).

### Chapters (`chapters/`, `\input` order from `main.tex`)

| File | Section in thesis | `\label` |
|---|---|---|
| [01_introduction.tex](../chapters/01_introduction.tex) | Introduction | — |
| [02_literature.tex](../chapters/02_literature.tex) | Literature | `sec:literature` |
| [03_preliminaries.tex](../chapters/03_preliminaries.tex) | Preliminaries | `sec:prelim` |
| [04_model_description.tex](../chapters/04_model_description.tex) | Model description: Model-$X$ | `sec:model_x` |
| [06_model_a.tex](../chapters/06_model_a.tex) | Analysis of Model-$A$ ($\gamma=\theta=0$) | `sec:model_a` |
| [07_model_b.tex](../chapters/07_model_b.tex) | Analysis of Model-$B$ (two-way jockeying; open) | `sec:model_b` |
| [08_model_b2.tex](../chapters/08_model_b2.tex) | Analysis of Model-$B_2$ ($\gamma_2=0$) | `sec:model_b2` |
| [09_model_c2.tex](../chapters/09_model_c2.tex) | Analysis of Model-$C_2$ ($\theta_1>0$) | `sec:model_c2` |
| [10_model_b21.tex](../chapters/10_model_b21.tex) | Analysis of Model-$\BH$ (head-of-line jockeying) | `sec:model_b21` |
| [11_model_c21.tex](../chapters/11_model_c21.tex) | Analysis of Model-$\CH$ (head-of-line abandonment) | `sec:model_c21` |
| [13_results.tex](../chapters/13_results.tex) | Results — validation + comparison (`sec:comparison`) + convergence | `sec:results` |
| [14_conclusion.tex](../chapters/14_conclusion.tex) | Conclusion and Future Work | `sec:conclusion` |
| [15_appendix_numerics.tex](../chapters/15_appendix_numerics.tex) | Appendix A: extended numerical validation (**excluded from PDF**, `main.tex:93`) | `app:numerics` |

> `05_model_x.tex` and `12_comparison.tex` no longer exist. File numbers 05 and 12 are gaps
> in the top-level `\input` sequence; the appendix (15) exists but is not `\input` in the
> compiled build.

### Other tex
- [drafts/dumpster.tex](../drafts/dumpster.tex) — scratch/draft dump, **not** `\input`.
- [mean_queue_and_waiting_times.tex](../mean_queue_and_waiting_times.tex) — repo-root archive
  of the per-model mean-queue/waiting-time subsections removed 2026-06-27; **not** `\input`.
- `figures/results/tab_*.tex` — 4 auto-generated result tables (see §3).
- [results/derived_metrics.tex](../results/derived_metrics.tex) — auto-generated metric
  macros, `\input` at `main.tex:57`. Do not edit by hand.

### Figures (`figures/`)
- TikZ sources (hand-authored, `\input` directly): `model-a-queue.tikz`,
  `model-b-queue.tikz`, `model-b2-queue.tikz`, `model-c2-queue.tikz`,
  `model_c-diagram.tikz`, `models-queue-overview.tikz`,
  `diagram_jockeying_and_abandonments.tikz`.
- `figures/results/` — generated `.pdf`/`.png` plots + the 4 `tab_*.tex` tables (from `nb_exhaustive`).
- `figures/validation/` — generated validation `.pdf`/`.png` plots (from `nb_validation`).
- `figures/archive/` — old figures.
- The `.tex` includes figures as **`.pdf`**; matching `.png` are also emitted but unused by the build.

---

## 2. Figure-generation / simulation code (`Code/`)

**No CSV/JSON data files exist.** Notebooks compute closed forms + numerical CTMC
solutions in-memory and emit `.pdf`/`.png`/`.tex` directly into `figures/`.

### Core library
- [model_master.py](../Code/model_master.py) — master module on state space
  `S = {(0)} ∪ {(n1,n2)}`; interior balance equation with optional `gamma_i`/`theta_i`.
- [model_master_tilde.py](../Code/model_master_tilde.py) — variant on `S~` (total-count coords).

### Notebook builders (`build_*.py` → `*.ipynb`)
| Builder script | Produces | Outputs when executed |
|---|---|---|
| [build_notebooks.py](../Code/build_notebooks.py) | `nb_model_{A,B,B2,C2,X}.ipynb` (on `S~`) | per-model checks |
| [build_nb_validation.py](../Code/build_nb_validation.py) | `nb_validation.ipynb` | `figures/validation/val_*.pdf/png` |
| [build_nb_results.py](../Code/build_nb_results.py) | `nb_results.ipynb` | comparative performance figures |
| [build_nb_exhaustive.py](../Code/build_nb_exhaustive.py) | `nb_exhaustive.ipynb` | **`figures/results/*.pdf/png` + the 4 `tab_*.tex` tables** |
| [compute_derived_metrics.py](../Code/compute_derived_metrics.py) | `results/derived_metrics.tex` | the `\loss*`/`\throughput*`/… macros |

### Data files consumed by the tex (current locations)
- **`tab_comparison_main.tex`** → `\input` in `13_results.tex:321` (`tab:comp:main`) — the
  only generated table currently in the compiled PDF.
- **`tab_EN_sweep.tex`**, **`tab_priority_benefit.tex`**, **`tab_convergence_rates.tex`** →
  `\input` in `15_appendix_numerics.tex` (`tab:comp:EN_sweep`, `tab:prio:benefit`,
  `tab:conv:rates`) — currently **dark** (the appendix is excluded from the PDF).
- All four are generated by `nb_exhaustive.ipynb` (built from `build_nb_exhaustive.py`).

### Build entry points ([Makefile](../Makefile))
- `make pdf` → `latexmk -pdf main.tex`
- `make clean` → `latexmk -C` + remove `main.bbl`
- `make notebooks` / `make results` / `make validation` → regenerate+execute notebooks.

---

## 3. Build baseline (latexmk -pdf, clean rebuild)

- **Result: PASS.** Exit 0. `main.pdf` = **67 pages** (was 98 pp at the 2026-06-19
  baseline; the drop is the appendix being excluded from the PDF, `main.tex:93`, plus the
  removal of the per-model mean-queue/waiting subsections — archived to
  `mean_queue_and_waiting_times.tex`). Snapshot date: 2026-06-27.
- **0 errors, 0 LaTeX/hyperref/package warnings.** No undefined refs, no undefined
  citations.
- **244 unique labels** (chapters + `main.tex`; all unique, no duplicates); **518**
  `\ref`/`\eqref`/`\Cref` targets, all resolve. No literal `??`.
- **1 cosmetic pdfTeX** `destination with the same identifier` warning (`equation.3.6`;
  harmless hyperref duplicate-anchor note; down from 3).

### Overfull / underfull boxes
- Overfull `\hbox`: **10**; Underfull `\hbox`: **7**; vbox: 0. All cosmetic. Worst:

| too wide | file:lines |
|---|---|
| 36.86 pt | `chapters/02_literature.tex:51-69` |
| 14.85 pt | `chapters/06_model_a.tex:200` |
| 14.85 pt | `chapters/06_model_a.tex:270` |
| 13.48 pt | `chapters/08_model_b2.tex:181` |
| 11.15 pt | `chapters/09_model_c2.tex:203` |

Remaining boxes are < 5 pt.

---

## 4. In-source markers (AUTHOR / TODO / FIXME / XXX / ??)

Grep over `chapters/ main.tex`. **0 hits** as of 2026-06-27: the four markers recorded at
the 2026-06-19 baseline have all been resolved in source —

- the working title is committed (`main.tex:59`, no `TODO-confirm`);
- the Model-A `[AUTHOR]` ordering note is gone (the section now runs
  Analytical → Probabilistic, matching CLAUDE.md §6 step 5);
- the Kernel-Method `TODO: cite` now carries `\cite{cohen1956delay}` (`06_model_a.tex:122`).

The only residual citation question is the Hadamard finite-part reading at
`07_model_b.tex:375`, now framed as the open analytical obstruction rather than a `TODO`
(author item — see `docs/REVIEW_2026-06-27.md`). No `FIXME`, `XXX`, or stray `??`.
