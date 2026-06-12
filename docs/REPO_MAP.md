# Repository Map & Build Baseline

> Generated baseline so later sessions can read this instead of re-exploring.
> Snapshot date: 2026-06-10. Regenerate after large structural changes.

Thesis: *Two-class non-preemptive priority M/M/1 queues with jockeying and
abandonment* (Victor Dominguez Sainz). Compiled file: `main.tex` (`article` class).

---

## 1. Repository structure

### Main file & assembly
- [main.tex](../main.tex) — root document. `\input`s the 13 chapter files and runs
  `\bibliography{references}`. Build artifacts (`main.aux/.bbl/.log/...`) are git-ignored.

> ⚠️ **File number ≠ PDF section number.** As of the Model-X reorder, `main.tex` `\input`s
> the analysis of Model-$X$ (`05_model_x.tex`) **after** Model-$B$ (`07_model_b.tex`), so the
> rendered order is A→B→X→B₂→C₂. PDF section numbers: 4 = model description, **5 = Model-A
> (`06_`), 6 = Model-B (`07_`), 7 = Model-X (`05_`)**, 8 = B₂, 9 = C₂, 10/11 = head-of-line,
> 12 = comparison, 13 = results. Always reference by `\label`, never by hardcoded number.

### Bibliography
- [references.bib](../references.bib) — single BibTeX database (e.g. `adan2002queueing`).

### Chapters (`chapters/`, all `\input` from `main.tex` lines 57–69)

| File | Section in thesis |
|---|---|
| [01_introduction.tex](../chapters/01_introduction.tex) | Introduction |
| [02_literature.tex](../chapters/02_literature.tex) | Literature (`sec:literature`) |
| [03_preliminaries.tex](../chapters/03_preliminaries.tex) | Preliminaries (`sec:prelim`) |
| [04_model_description.tex](../chapters/04_model_description.tex) | Model description: Model-$X$ (`sec:model_x`) |
| [05_model_x.tex](../chapters/05_model_x.tex) | Analysis of Model-$X$, full model $\gamma_i,\theta_i>0$ (`sec:model_x_anal`) |
| [06_model_a.tex](../chapters/06_model_a.tex) | Analysis of Model-$A$, baseline $\gamma=\theta=0$ (`sec:model_a`) |
| [07_model_b.tex](../chapters/07_model_b.tex) | Analysis of Model-$B$, two-way jockeying (`sec:model_b`) |
| [08_model_b2.tex](../chapters/08_model_b2.tex) | Analysis of Model-$B_2$, one-way jockeying $\gamma_2=0$ (`sec:model_b2`) |
| [09_model_c2.tex](../chapters/09_model_c2.tex) | Analysis of Model-$C_2$, class-1 abandonment $\theta_1>0$ (`sec:model_c2`) |
| [10_model_b21.tex](../chapters/10_model_b21.tex) | Analysis of Model-$B_2^1$, head-of-line jockeying (experiment) |
| [11_model_c21.tex](../chapters/11_model_c21.tex) | Analysis of Model-$C_2^1$, head-of-line abandonment (experiment) |
| [12_comparison.tex](../chapters/12_comparison.tex) | Comparison of Models $A$, $B_2$, $C_2$ (figures + 3 result tables) |
| [13_results.tex](../chapters/13_results.tex) | Results — validation & simulation figures (`sec:results`) |

> Note: file numbering was renumbered vs. earlier memory notes (Model-A is now `06_`,
> not `05_`; the two experiment models are now `10_`/`11_`; comparison is `12_`).

### Other tex
- [drafts/dumpster.tex](../drafts/dumpster.tex) — scratch/draft dump, **not** `\input` by `main.tex`.
- `figures/results/tab_*.tex` — 4 auto-generated result tables (see §3).

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
| [build_nb_validation.py](../Code/build_nb_validation.py) | `nb_validation.ipynb` | `figures/validation/val_*.pdf/png` (one section per lemma/theorem/corollary) |
| [build_nb_results.py](../Code/build_nb_results.py) | `nb_results.ipynb` | comparative performance figures |
| [build_nb_exhaustive.py](../Code/build_nb_exhaustive.py) | `nb_exhaustive.ipynb` | **`figures/results/*.pdf/png` + the 4 `figures/results/tab_*.tex` tables** |
| [build_notebook.py](../Code/build_notebook.py), [build_notebook_tilde.py](../Code/build_notebook_tilde.py) | legacy single-notebook builders | — |

### Data files consumed by the tex
- **`figures/results/tab_comparison_main.tex`** → `\input` in `12_comparison.tex:313`
  (`tab:comp:main`).
- **`figures/results/tab_EN_sweep.tex`** → `\input` in `12_comparison.tex:317` (`tab:comp:EN_sweep`).
- **`figures/results/tab_priority_benefit.tex`** → `\input` in `12_comparison.tex:606` (`tab:prio:benefit`).
- **`figures/results/tab_convergence_rates.tex`** → `\input` in `13_results.tex:457` (`tab:conv:rates`).
- All four are generated by `nb_exhaustive.ipynb` (built from `build_nb_exhaustive.py`).

### Archive
- `Code/archive/thesis_models.ipynb`, `Code/archive/thesis_models_tilde.ipynb` — superseded.

### Build entry points ([Makefile](../Makefile))
- `make pdf` → `latexmk -pdf main.tex`
- `make clean` → `latexmk -C` + remove `main.bbl`
- `make notebooks` → regenerate ALL notebooks from builders, then `nbconvert --execute` each
- `make results` / `make validation` → regenerate+execute just that notebook

---

## 3. Build baseline (latexmk -pdf, clean rebuild)

- **Result: PASS.** Exit 0. `main.pdf` = **105 pages** (was 99pp at the G1 audit,
  93pp before that). Snapshot date for this baseline: 2026-06-12 (Phase 1 follow-up,
  see `docs/REVIEW_CHECKLIST.md`).
- Compile log: `main.log` from a clean `latexmk -pdf main.tex` rebuild.

### Undefined references / citations
- **None.** No `LaTeX Warning` / `Package ... Warning` lines at all → no undefined
  refs, no undefined citations. 297 labels (all unique), 285 `\ref`/`\eqref`/`\Cref`
  targets (all resolve).

### Multiply-defined labels
- **No true LaTeX multiply-defined labels.**
- **10 cosmetic pdfTeX warnings**: `destination with the same identifier
  (name{figure.N}/name{table.N}) has been already used` — hyperref duplicate-anchor
  warnings, not label clashes; harmless (down from 44 at G1 after the
  float-before-hyperref reorder).

### Overfull / underfull boxes
- Overfull `\hbox`: **17**; Underfull `\hbox`: **4**; vbox: 0. Total 21 (down from
  24 pre-Phase-1).
- The four worst boxes flagged by the 2026-06-12 audit (61.97pt, 57.85pt, 43.37pt,
  41.57pt) were fixed in Phase 1 (task C3, formatting-only). Remaining boxes are all
  <15pt. Current worst offenders:

| too wide | file:lines |
|---|---|
| 36.86 pt | `chapters/02_literature.tex:41-59` |
| 14.85 pt | `chapters/06_model_a.tex:240` |
| 14.85 pt | `chapters/06_model_a.tex:311` |
| 13.48 pt | `chapters/08_model_b2.tex:297-304` |
| 13.48 pt | `chapters/09_model_c2.tex:273` |

Remaining 16 are <8pt (negligible).

---

## 4. In-source markers (AUTHOR / TODO / FIXME / XXX / ??)

Grep over `chapters/ figures/ main.tex references.bib Code/`. **4 hits**, all are
deliberate author notes (commented-out, prefixed `%`), none are blocking:

| File:line | Marker | Note |
|---|---|---|
| [main.tex:59](../main.tex#L59) | `TODO-confirm:` | working title (1 of 3 candidates) |
| [06_model_a.tex:52](../chapters/06_model_a.tex#L52) | `[AUTHOR:` | canonical section spine (§6 step 5) — Probabilistic/Analytical ordering note |
| [06_model_a.tex:121](../chapters/06_model_a.tex#L121) | `TODO:` | add a citation for the Kernel Method (Bayer & Boxma, or Cohen's book) |
| [07_model_b.tex:479](../chapters/07_model_b.tex#L479) | `TODO(citation):` | Hadamard finite-part integrals reference |

The G1-era `[AUTHOR:` flags on `07_model_b.tex` (kernel regularisation) and
`05_model_x.tex` (Model-B-vs-X closure), plus the `13_results.tex`
`[Discuss:]`/`[Introduce:]` scaffolding, have since been resolved into narrative
(verified 2026-06-12) and no longer appear.

No `FIXME`, `XXX`, or stray `??` (no undefined-ref `??` in PDF, consistent with clean refs).
