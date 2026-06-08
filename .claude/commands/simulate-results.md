# /simulate-results — Exhaustive Thesis Simulation & Validation Notebook

You are an expert numerical analyst, queueing theorist, and Python notebook architect
working on Victor's two-class non-preemptive priority M/M/1 thesis. Your task is to
generate a publication-quality Jupyter notebook that exhaustively validates every
theorem and produces every comparative plot needed for the thesis.

---

## 0. Before You Begin — Read Existing Infrastructure

**You MUST read these files before writing a single line of code:**

1. `Code/model_master.py` — the CTMC solver. Understand `Params`, `solve_exact`,
   `simulate`, `diagnostics`, `mean_queue_lengths`. You will import from it, never
   reimplement it.
2. `Code/model_master_tilde.py` — the S̃-space solver. Understand `solve_exact_tilde`,
   `P_tilde`, `P_tilde_approx_modelA`.
3. `Code/build_nb_validation.py` — the existing validation notebook builder. Read it
   completely. The new notebook must NOT duplicate its theorem validation cells; instead
   it must IMPORT those results or cross-reference them. The new notebook is exclusively
   about **comparative analysis, convergence, and publishable figures**.
4. `Code/build_nb_results.py` — read it and understand what is already done in
   `nb_results.ipynb`. Do not duplicate those plots; only complement or supersede them.
5. `figures/` — note which figures already exist so you never overwrite them.

After reading, write a short comment at the top of your build script listing what
exists and what is NEW in this notebook.

---

## 1. Deliverable

Create a Python build script `Code/build_nb_exhaustive.py` that, when run with
`python Code/build_nb_exhaustive.py`, produces `Code/nb_exhaustive.ipynb`.

Then execute the notebook by running:
```
cd Code && jupyter nbconvert --to notebook --execute --inplace nb_exhaustive.ipynb
```
Fix any execution errors before reporting done.

All figures must be saved to `figures/results/` (create the directory if absent).
Naming convention: `fig_<model>_<metric>_<variant>.pdf` and `.png` (always both).

---

## 2. Critical Notation — Non-Negotiable

Every docstring, markdown cell, comment, and variable name must respect:

- `N1`, `N2` = customers **waiting in queues**, **excluding** the in-service customer.
  `N = N1 + N2` (total in-queue, not in-system).
- `pi_idle` = π₀ = P(server idle). `pi_joint[0,0]` = π(0,0) = P(server busy, both
  queues empty). **These are always different.** Assert `pi_idle != pi_joint[0,0]` (to
  machine precision, they differ whenever ρ > 0).
- Tuple state (n1, n2) **always implies the server is busy**. The idle state is
  separate and denoted `(0)` in the thesis.
- `rho = (lam1 + lam2) / mu`, `rho_i = lam_i / mu`.
- Stability: without abandonments, require `rho < 1`. With `theta1 > 0`, the chain is
  positive recurrent for all loads; state this explicitly in the relevant markdown cells.

---

## 3. Canonical Parameters

Use these exact values for consistency with the existing notebooks and for
cross-referencing in the thesis:

```python
MU            = 1.0          # always normalised
LAM1_SYM      = 0.35         # symmetric: lam1=lam2=0.35, rho=0.70
LAM2_SYM      = 0.35
LAM1_ASYM     = 0.50         # asymmetric: heavy prio class, rho=0.70
LAM2_ASYM     = 0.20
LAM1_STD      = 0.30         # standard: matches existing notebooks
LAM2_STD      = 0.40         # rho=0.70
GAMMA1_CANON  = 0.50         # canonical jockeying rate (Model B2)
THETA1_CANON  = 0.50         # canonical abandonment rate (Model C2)
N_MAX_DEFAULT = 50           # CTMC truncation; raise to 80 near rho=0.95
RHO_SWEEP     = [0.10, 0.20, 0.30, 0.40, 0.50, 0.60, 0.70, 0.75,
                 0.80, 0.85, 0.90, 0.95]
```

Adaptive truncation: after solving, assert `pi_joint[N_MAX-5:, :].sum() < 1e-8` and
`pi_joint[:, N_MAX-5:].sum() < 1e-8`. If either fails, re-solve with `N_MAX *= 2`.

---

## 4. Traceability Protocol — Mandatory for Every Computation

Every code cell that produces a numerical result or figure MUST be immediately preceded
by a markdown cell with this exact structure:

```markdown
### [<Model Name> — <Theorem / Lemma / Corollary label>]
**Statement (verbatim from thesis):** <one-sentence statement of the result>
**Formula:** $<LaTeX>$
**Validation method:** CTMC exact solver / closed-form formula / PGF extraction / Little's Law / ...
**Parameters:** mu=..., lam1=..., lam2=..., gamma1=..., theta1=...
```

If a cell is purely comparative (no specific theorem), use:
```markdown
### [Comparative Analysis — <topic>]
**Purpose:** <what insight this plot reveals>
**Models contrasted:** <list>
**Expected behaviour:** <what the math predicts>
```

---

## 5. Notebook Sections

Build the notebook in exactly this order. Each section heading maps to one `md()` call
at the section level in the build script.

### Section 0 — Shared Setup (one cell)

Import from `model_master` and `model_master_tilde`. Define:
- `pgf_series(pi_joint, x, y)` — evaluate P(x,y) by direct summation.
- `L1_distance(pi_a, pi_b)` — L1 norm of the difference of two `pi_joint` arrays
  (zero-padded to the larger size).
- `EN1_EN2(pi_joint)` — returns (E[N1], E[N2]) using `mean_queue_lengths`.
- `EW1_EW2(p, pi_joint)` — returns (E[W1], E[W2]) via Little's Law:
  E[Wi] = E[Ni] / lami (state Little's Law explicitly in a comment).
- `make_P_A(lam1, lam2, mu)` — closed-form PGF for Model A (copy from
  `build_nb_validation.py`; keep it here for self-containment).
- `make_P_B2(lam1, lam2, mu, gamma1)` — closed-form PGF for Model B2.
- `make_P_C2(lam1, lam2, mu, theta1)` — closed-form PGF for Model C2.
- A global `SAVE_DIR = "../figures/results/"` and a helper `savefig(name)` that saves
  both `.pdf` and `.png` (dpi=150) and prints the path.
- A global `plt.rcParams` block matching the style in `build_nb_validation.py`:
  `font.family=DejaVu Serif`, `mathtext.fontset=cm`, appropriate size settings.

### Section 1 — Sanity Check Suite (run first, fail fast)

Before doing any analysis, verify the four baseline identities hold for all three
canonical parameter sets (standard, symmetric, asymmetric):

| Check | Formula | Tolerance |
|---|---|---|
| π₀ = 1−ρ | for Models A, B, B2 only | 1e-5 |
| π(0,0) = ρ(1−ρ) | for Models A, B, B2 only | 1e-5 |
| P(1,1) = 1−π₀ | all models | 1e-4 |
| P(z,z) = π(0,0)/(1−ρz) | all models, z ∈ {0.3,0.5,0.7,0.9} | 1e-4 |
| Normalisation: π₀ + Σπ(n1,n2) = 1 | all models | 1e-6 |
| Little's Law: E[N] = (lam1+lam2)·E[W] | all models | 1e-4 |

Format as a table with PASS/FAIL per row. Raise `AssertionError` on any FAIL so the
notebook stops immediately rather than silently propagating wrong numbers.

### Section 2 — Traffic Intensity Sweep (all models)

**Theorem reference:** Corollary A (π₀=1−ρ, π(0,0)=ρ(1−ρ)), Theorem B2, Corollary C2.

For each ρ in `RHO_SWEEP`, compute for Models A, B2 (gamma1=GAMMA1_CANON),
and C2 (theta1=THETA1_CANON), using LAM1_STD/LAM2_STD split (rho = lam1+lam2 so
scale lam1, lam2 proportionally keeping their ratio fixed):
- E[N1], E[N2], E[N]
- E[W1] = E[N1]/lam1, E[W2] = E[N2]/lam2 (cite Little's Law)
- π₀, π(0,0)
- Throughput (mu × P_busy)

**Figure 2a** (`fig_sweep_EN_vs_rho.pdf`): 4-panel figure.
- Panel 1: E[N] vs ρ for all three models. Model A in black solid (reference baseline),
  B2 in blue dashed, C2 in red dash-dot. Add a vertical line at ρ=0.70 (canonical).
  Title: "Mean queue length E[N] vs traffic intensity ρ".
- Panel 2: E[N1] vs ρ (same colour scheme).
- Panel 3: E[W1] vs ρ (waiting time, priority class). Add annotation: at ρ=0.9, show
  numerical values for each model to illustrate the magnitude of the improvement.
- Panel 4: π₀ vs ρ. For Model C2, π₀ > 1−ρ: annotate this region explicitly with
  "abandonment increases idle probability".

**Figure 2b** (`fig_sweep_pi00_vs_rho.pdf`): π(0,0) vs ρ for all models.
Show that for Models A and B2, π(0,0)=ρ(1−ρ) (parabola, draw the formula on the plot);
for Model C2, π(0,0) deviates above this parabola at high ρ.

**Table 2** (LaTeX output): Print a booktabs LaTeX table string to stdout with columns:
ρ | E[N1] A | E[N1] B2 | E[N1] C2 | E[W1] A | E[W1] B2 | E[W1] C2
for ρ ∈ {0.50, 0.70, 0.90}. Format floats to 4 decimal places. Label: `tab:comp:EN_sweep`.

### Section 3 — Jockeying Effect Analysis (Model B2)

**Theorem reference:** Theorem B2 (integral-form P(x,y)), Corollary A (π(0,0)=ρ(1−ρ)
remains true for all γ₁ — jockeying conserves customer count).

Fix lam1=LAM1_STD, lam2=LAM2_STD, mu=MU, rho=0.70.
Sweep gamma1 ∈ {0.001, 0.01, 0.05, 0.1, 0.2, 0.5, 1.0, 2.0, 5.0, 10.0, 50.0}.
For gamma1=0.001 treat as Model A (serves as the γ₁→0 reference point).

Compute E[N1], E[N2], E[N], π₀, π(0,0), E[W1], E[W2] at each gamma1.

**Figure 3a** (`fig_B2_jockeying_EN_vs_gamma1.pdf`): 3-panel.
- Panel 1: E[N1] and E[N2] vs log₁₀(γ₁) on the same axes (blue=N1, orange=N2).
  Add horizontal dashed lines at Model A values (γ₁=0 limit, annotate as "Model A").
  Caption must note: "E[N1] is monotone decreasing in γ₁ because class-1 customers
  jockey into the class-2 queue; E[N2] increases correspondingly."
- Panel 2: E[N] vs log₁₀(γ₁). Should be flat (jockeying conserves total count N).
  Add a horizontal line at the Model A value and annotate the conservation law explicitly.
- Panel 3: π(0,0) vs log₁₀(γ₁). Should be identically ρ(1−ρ). Add horizontal line.
  This verifies Corollary A is jockeying-invariant.

**Figure 3b** (`fig_B2_priority_ratio_vs_gamma1.pdf`):
Plot E[W1]/E[W2] (priority advantage ratio) vs log₁₀(γ₁). As γ₁ increases:
- High γ₁ erodes the class-1 advantage (class-1 customers leave the priority queue).
- Annotate the λ₁/λ₂ ratio as a lower bound for E[W1]/E[W2] (load-balance limit).
- Title: "Priority advantage ratio E[W₁]/E[W₂] vs jockeying rate γ₁".

**Figure 3c** (`fig_B2_class_asymmetry_gamma1.pdf`):
At three values γ₁ ∈ {0.1, 1.0, 10.0}, plot E[N1] and E[N2] as a function of
α = λ₁/(λ₁+λ₂) ∈ {0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9} (fix ρ=0.70, vary
the split). This shows how the class asymmetry interacts with the jockeying rate.

### Section 4 — Abandonment Effect Analysis (Model C2)

**Theorem reference:** Theorem C2 (integral-form P(x,y)), Corollary C2 (π₀ and π(0,0)
via E[B_C]), Kummer identity underlying the 1F1 formula.

Fix lam1=LAM1_STD, lam2=LAM2_STD, mu=MU, rho=0.70.
Sweep theta1 ∈ {0.001, 0.01, 0.05, 0.1, 0.2, 0.5, 1.0, 2.0, 5.0, 10.0, 50.0}.

Compute E[N1], E[N2], E[N], π₀, π(0,0), E[W1], E[W2], throughput, abandonment_rate.

**Figure 4a** (`fig_C2_abandonment_EN_vs_theta1.pdf`): 4-panel.
- Panel 1: E[N1] vs log₁₀(θ₁). Should monotone decrease to 0. Annotate Model A limit
  at θ₁=0. Caption must explain: "Class-1 abandonments act as a self-regulating valve,
  bounding E[N1] below ρ₁/θ₁ for large θ₁."
- Panel 2: E[N2] vs log₁₀(θ₁). Note: E[N2] may initially increase then decrease as
  θ₁ grows (class-1 customers exit faster, freeing the server for class-2, but high
  abandonment also reduces system load). Flag this non-monotone behaviour if present.
- Panel 3: π₀ vs log₁₀(θ₁), with horizontal dashed line at 1−ρ (Model A value).
  Annotate: "π₀ > 1−ρ whenever θ₁ > 0 (Corollary C₂)".
- Panel 4: throughput and abandonment_rate vs log₁₀(θ₁) on the same axes. Show the
  throughput-quality tradeoff: as θ₁ grows, throughput falls and abandonment rate rises.

**Figure 4b** (`fig_C2_E_BC_vs_theta1.pdf`):
Plot E[B_C] (mean class-1 busy period) vs log₁₀(θ₁) using scipy.special.hyp1f1.
Add horizontal asymptote at (mu-lam1)^{-1} (the θ₁→0 limit — cite Corollary C2 limit).
Add annotation: "E[B_C] → (μ−λ₁)⁻¹ as θ₁→0 (Model A busy period)".

**Figure 4c** (`fig_C2_rho_theta_heatmap.pdf`):
2D heatmap over ρ ∈ {0.3,0.4,...,0.95} × θ₁ ∈ {0.05,0.1,0.2,0.5,1,2,5}:
colour = E[N1] / E[N1_ModelA] (the ratio of class-1 waiting under C2 vs A).
This shows where abandonment gives the most benefit relative to baseline.
Use a diverging colormap with 1.0 as centre.

### Section 5 — CONVERGENCE ANALYSIS (Mathematical Heart)

This is the most important section. It directly validates the limit theorems and
convergence claims in the thesis. Do not cut corners here.

#### 5a. C2 → A as θ₁ → 0

**Theorem reference:** Corollary C2 limit: "As θ₁→0⁺, E[B_C]→(μ−λ₁)⁻¹,
hence π₀→1−ρ and π(0,0)→ρ(1−ρ) (Model A values)."

Use lam1=LAM1_STD, lam2=LAM2_STD, mu=MU. Compute at:
theta1_vals = np.logspace(-3, 2, 40)   # from 0.001 to 100

For each theta1:
1. Solve C2 via CTMC. Solve Model A via CTMC (once, reuse).
2. Compute L1 distance: ||pi_C2(theta1) - pi_A||_1 (zero-pad arrays to same size).
3. Compute |pi0_C2 - pi0_A|, |pi00_C2 - pi00_A|, |E[N1]_C2 - E[N1]_A|.

**Figure 5a** (`fig_conv_C2_to_A_L1.pdf`): Two panels.
- Panel 1: log-log plot of ||pi_C2 - pi_A||_1 vs θ₁.
  Fit a linear regression on the log-log data for θ₁ < 1 and annotate the slope
  (should be ≈1 if convergence is first-order in θ₁). Add the fitted line.
  Title: "L1 convergence of Model C₂ to Model A as θ₁→0".
- Panel 2: π₀(θ₁) (red solid) and 1−ρ (dashed horizontal), both on the same axis.
  Also plot π(0,0)(θ₁) (blue solid) and ρ(1−ρ) (dashed horizontal).
  Use a log x-axis. At the rightmost theta1 value, annotate the current value;
  at the leftmost, show how close it is to the Model A limit.

**Figure 5b** (`fig_conv_C2_to_A_indiv.pdf`):
Three sub-panels: |E[N1]_C2 - E[N1]_A|, |pi0_C2 - pi0_A|, |pi00_C2 - pi00_A|
all vs log(θ₁). Fit log-log slopes and annotate each panel with its slope.

#### 5b. B2 → A as γ₁ → 0

**Theorem reference:** Corollary A and the B2 theorem reduce to Model A when γ₁=0.

Use lam1=LAM1_STD, lam2=LAM2_STD, mu=MU. Compute at:
gamma1_vals = np.logspace(-3, 2, 40)

For each gamma1:
1. Solve B2 via CTMC. Reuse Model A solution.
2. Compute L1 distance ||pi_B2 - pi_A||_1 and individual metric differences.

**Figure 5c** (`fig_conv_B2_to_A_L1.pdf`):
Same structure as Figure 5a (log-log L1 distance, slope annotation).
Note: expect approximately first-order convergence in γ₁.

#### 5c. B2 Load-Balancing Limit as γ₁ → ∞

**Theorem reference:** As γ₁→∞, every class-1 customer immediately jockeys to
class-2 (instant jockeying). In this limit, the queue behaves like a single-class
M/M/1, and E[N1]/E[N2] → λ₁/λ₂.

gamma1_inf_vals = [0.1, 0.5, 1.0, 2.0, 5.0, 10.0, 25.0, 50.0, 100.0, 500.0]

**Figure 5d** (`fig_conv_B2_inf_jockeying.pdf`): Two panels.
- Panel 1: E[N1]/E[N2] vs log₁₀(γ₁). Add horizontal asymptote at λ₁/λ₂.
  Annotate: "Instant-jockeying limit: E[N₁]/E[N₂] → λ₁/λ₂".
- Panel 2: E[W1] and E[W2] vs log₁₀(γ₁). Show convergence.

### Section 6 — Class Asymmetry Analysis

Fix rho=0.70, mu=MU. Vary α = λ₁/(λ₁+λ₂) ∈ {0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9}.
For each α: lam1 = α × rho × mu, lam2 = (1−α) × rho × mu.
Compute for Models A, B2 (gamma1=0.5), C2 (theta1=0.5).

**Figure 6** (`fig_class_asymmetry.pdf`): 4-panel figure.
- Panel 1: E[N1] vs α for all three models.
  Annotate: at α→0, class-1 barely uses its priority; at α→1, class-1 dominates.
- Panel 2: E[N2] vs α.
- Panel 3: E[W1]/E[W2] (priority advantage ratio) vs α for all three models.
  This is the central argument for priority queue design: identify the α* where the
  ratio is maximised for each model and annotate it on the plot.
- Panel 4: Priority benefit = (E[W2]−E[W1]) vs α. Show that jockeying (B2) reduces
  this gap, while abandonment (C2) can either increase or decrease it depending on α.

### Section 7 — Comprehensive Comparison Tables

This section generates LaTeX-formatted tables. Print each to stdout (the notebook
captures them) AND write them to `../figures/results/` as `.tex` files for direct
`\input{}` inclusion in the thesis.

**Table 7.1** (`tab_comparison_main.tex`): Main comparison table.
Rows: rho × model (3 rho values × 3 models = 9 rows).
Columns: Model | ρ | E[N₁] | E[N₂] | E[N] | E[W₁] | E[W₂] | π₀ | π(0,0)
Caption: "Comparison of Models A, B₂ (γ₁=0.5), and C₂ (θ₁=0.5) at three traffic
intensities with λ₁=0.3, λ₂=0.4, μ=1."
Label: `tab:comp:main`
Use booktabs (\toprule, \midrule, \bottomrule), midrules between rho groups,
and `\multirow` for the ρ column. Format floats to 4 decimal places.

**Table 7.2** (`tab_convergence_rates.tex`): Convergence rates table.
Columns: Limit | Parameter → | L1 slope | π₀ slope | π(0,0) slope | Valid range
Rows: C2→A (θ₁→0), B2→A (γ₁→0).
Compute slopes from the log-log regression in Section 5 and fill in here.
Caption: "Empirical convergence rates of Models C₂ and B₂ to Model A."
Label: `tab:conv:rates`

**Table 7.3** (`tab_priority_benefit.tex`): Priority benefit under each model.
Rows: ρ ∈ {0.5, 0.7, 0.9}.
Columns: Model A | Model B2 | Model C2, each with sub-columns E[W1] and E[W2]/E[W1].
Caption: "Mean class-1 waiting time and priority ratio under each model."
Label: `tab:prio:benefit`

### Section 8 — Simulation vs CTMC Cross-Validation

For three parameter configurations (Model A, B2, C2 canonical), run:
```python
sim = simulate(p, n_events=5_000_000, seed=42)
exact = solve_exact(p, N_max=50)
```
Compare `sim['pi_idle']` vs `exact['pi_idle']`, `sim['pi_joint']` vs `exact['pi_joint']`
(mean absolute error), and E[N1], E[N2] from both.

**Figure 8** (`fig_sim_vs_ctmc.pdf`): 3-panel figure (one per model).
Scatter plot: CTMC π(n1,n2) (x-axis) vs simulation frequency (y-axis) for all (n1,n2)
with π(n1,n2) > 1e-4. Should lie on y=x line. Annotate with max absolute error.

### Section 9 — Final Summary Dashboard

A single 2×3 grid figure (`fig_summary_dashboard.pdf`) showing the 6 most important
comparative plots at a glance:
1. E[N] vs ρ (all models) — from Section 2.
2. E[W1] vs ρ (all models) — from Section 2.
3. ||pi_C2 - pi_A||_1 vs θ₁ (convergence) — from Section 5a.
4. ||pi_B2 - pi_A||_1 vs γ₁ (convergence) — from Section 5b.
5. E[N1] vs γ₁ (B2 jockeying effect) — from Section 3.
6. E[N1]/E[N1_A] heatmap over (ρ, θ₁) — from Section 4c.

Title: "Exhaustive validation and comparative analysis — M/M/1 priority with
jockeying and abandonment".
This figure will be used as a thesis frontispiece for the numerical results chapter.

---

## 6. Error Handling and Robustness

- Wrap every `solve_exact` call in a try/except that catches `ValueError` (unstable
  configuration) and `RuntimeError` (truncation exceeded). Skip the configuration and
  print a warning; do not crash the notebook.
- For near-critical loads (rho > 0.92), double N_MAX automatically.
- For the `simulate()` calls in Section 8, use `n_events=5_000_000` (not 10M) to keep
  runtime reasonable; note the lower precision in the markdown cell.
- If `scipy.special.hyp1f1` returns NaN or Inf for a parameter combination, flag it in
  the output and skip that point; these indicate parameter ranges beyond valid expansion.

---

## 7. Style and Output Quality

- Use `matplotlib` style matching `build_nb_validation.py`:
  `font.family=DejaVu Serif`, `mathtext.fontset=cm`.
- All axis labels and titles must use LaTeX math mode via `r"$...$"`.
- Every figure must have a descriptive title that includes the model name and the
  key parameter values being varied.
- Legends must be placed to avoid data. Use `loc='best'` unless it obviously fails.
- Color scheme: Model A = black solid, Model B2 = steelblue dashed, Model C2 = crimson
  dash-dot. Use this consistently across ALL figures so the thesis reads coherently.
- Every figure is saved at 150 dpi (PNG) and vector (PDF). Print the save path.

---

## 8. Final Checklist Before Reporting Done

Run this mentally before reporting the notebook is complete:

- [ ] `pi_idle` and `pi_joint[0,0]` are always kept distinct?
- [ ] Every code cell preceded by a traceability markdown cell (Section 4 protocol)?
- [ ] All 9+ figures saved to `figures/results/` in both PDF and PNG?
- [ ] All 3 LaTeX tables printed to stdout AND saved as `.tex` files?
- [ ] Convergence slopes computed and annotated on log-log plots?
- [ ] Simulation vs CTMC cross-validation passed (max err < 1e-2)?
- [ ] Notebook executes clean with `jupyter nbconvert --execute --inplace`?
- [ ] No `NameError`, `ImportError`, or silent wrong values (all assertions pass)?
- [ ] `figures/results/` directory created; no existing files in `figures/` overwritten?

Report the path to the generated notebook and a one-line summary of each figure produced.
