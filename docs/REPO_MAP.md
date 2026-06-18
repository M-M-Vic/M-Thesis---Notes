# Repository Map & Build Baseline

> Generated baseline so later sessions can read this instead of re-exploring.
> Snapshot date: 2026-06-19. Regenerate after large structural changes.

Thesis: *Two-class non-preemptive priority M/M/1 queues with jockeying and
abandonment* (Victor Dominguez Sainz). Compiled file: `main.tex` (`article` class).

---

## 1. Repository structure

### Main file & assembly
- [main.tex](../main.tex) — root document. `\input`s the chapter files and runs
  `\bibliography{references}`. Build artifacts (`main.aux/.bbl/.log/...`) are git-ignored.

> ⚠️ **File number ≠ PDF section number, and two files are special.**
> - `05_model_x.tex` was **deleted** (2026-06-19): the standalone *Analysis of Model-X*
>   section is gone, demoted to **Remark~`rem:B:modelX`** inside Model-B
>   (`07_model_b.tex`). Model-X now survives only as the *model description* in
>   `04_model_description.tex` and as that remark.
> - `12_comparison.tex` is **not** a top-level `\input`; it is nested inside
>   `13_results.tex` (line 73) as the `\subsection{Comparison of the solved models}`
>   (`sec:comparison`).
> Always reference by `\label`, never by hardcoded number.

### Rendered section order (PDF)
`§1` Introduction · `§2` Literature · `§3` Preliminaries · `§4` Model description (Model-X)
· `§5` Model-A · `§6` Model-B · `§7` Model-B₂ · `§8` Model-C₂ · `§9` Model-B₂ᴴ (`\BH`)
· `§10` Model-C₂ᴴ (`\CH`) · `§11` Results (with `§11.x` Comparison + Convergence)
· `§12` Conclusion & Future Work · **Appendix A** Extended numerical validation & comparison.

### Bibliography
- [references.bib](../references.bib) — single BibTeX database (e.g. `adan2002queueing`).
  18 entries; 16 cited (`abate2000asymptotic`, `tian2006vacation` defined-but-uncited).

### Chapters (`chapters/`, `\input` order from `main.tex` lines 83–96)

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
| [13_results.tex](../chapters/13_results.tex) | Results — validation + comparison + convergence | `sec:results` |
| [12_comparison.tex](../chapters/12_comparison.tex) | Comparison subsection (`\input` by `13_results.tex:73`) | `sec:comparison` |
| [14_conclusion.tex](../chapters/14_conclusion.tex) | Conclusion and Future Work | `sec:conclusion` |
| [15_appendix_numerics.tex](../chapters/15_appendix_numerics.tex) | Appendix A: extended numerical validation & comparison | `app:numerics` |

> `05_model_x.tex` no longer exists. File numbers 05 (deleted) and 12 (nested) are gaps in
> the top-level `\input` sequence.

### Other tex
- [drafts/dumpster.tex](../drafts/dumpster.tex) — scratch/draft dump, **not** `\input`.
- `figures/results/tab_*.tex` — 4 auto-generated result tables (see §3).
- [results/derived_metrics.tex](../results/derived_metrics.tex) — 93 auto-generated metric
  macros, `\input` at `main.tex:57`. All 93 are used; do not edit by hand.

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
| [compute_derived_metrics.py](../Code/compute_derived_metrics.py) | `results/derived_metrics.tex` | the 93 `\loss*`/`\throughput*`/… macros |

### Data files consumed by the tex (current locations)
- **`tab_comparison_main.tex`** → `\input` in `12_comparison.tex:305` (`tab:comp:main`).
- **`tab_EN_sweep.tex`** → `\input` in `15_appendix_numerics.tex:315` (`tab:comp:EN_sweep`).
- **`tab_priority_benefit.tex`** → `\input` in `15_appendix_numerics.tex:527` (`tab:prio:benefit`).
- **`tab_convergence_rates.tex`** → `\input` in `15_appendix_numerics.tex:761` (`tab:conv:rates`).
- All four are generated by `nb_exhaustive.ipynb` (built from `build_nb_exhaustive.py`).

### Build entry points ([Makefile](../Makefile))
- `make pdf` → `latexmk -pdf main.tex`
- `make clean` → `latexmk -C` + remove `main.bbl`
- `make notebooks` / `make results` / `make validation` → regenerate+execute notebooks.

---

## 3. Build baseline (latexmk -pdf, clean rebuild)

- **Result: PASS.** Exit 0. `main.pdf` = **98 pages** (was 105 pp before the Model-X
  analysis deletion + the Results/Comparison consolidation of 2026-06-19). Snapshot date:
  2026-06-19.
- **0 errors, 0 LaTeX/hyperref/package warnings.** No undefined refs, no undefined
  citations.
- **275 unique labels** (all unique, no duplicates); **636** `\ref`/`\eqref`/`\Cref`
  targets, all resolve. No literal `??`.
- **3 cosmetic pdfTeX** `destination with the same identifier` warnings (harmless
  hyperref duplicate-anchor notes; down from 10).

### Overfull / underfull boxes
- Overfull `\hbox`: **16**; Underfull `\hbox`: **4**; vbox: 0. All cosmetic. Worst:

| too wide | file:lines |
|---|---|
| 36.86 pt | `chapters/02_literature.tex:51-59` |
| 14.85 pt | `chapters/06_model_a.tex:240` |
| 14.85 pt | `chapters/06_model_a.tex:311` |
| 13.48 pt | `chapters/08_model_b2.tex:297-304` |
| 13.48 pt | `chapters/09_model_c2.tex:273` |

Remaining 15 are < 8 pt.

---

## 4. In-source markers (AUTHOR / TODO / FIXME / XXX / ??)

Grep over `chapters/ figures/ main.tex references.bib Code/`. **4 hits**, all deliberate
author notes (commented-out, prefixed `%`), none blocking:

| File:line | Marker | Note |
|---|---|---|
| [main.tex:59](../main.tex#L59) | `TODO-confirm:` | working title (1 of 3 candidates) |
| [06_model_a.tex:52](../chapters/06_model_a.tex#L52) | `[AUTHOR:` | Probabilistic/Analytical ordering vs canonical spine (§6 step 5) |
| [06_model_a.tex:121](../chapters/06_model_a.tex#L121) | `TODO:` | cite the Kernel Method (Bayer & Boxma, or Cohen) |
| [07_model_b.tex:483](../chapters/07_model_b.tex#L483) | `TODO(citation):` | Hadamard finite-part integrals reference |

No `FIXME`, `XXX`, or stray `??`.
