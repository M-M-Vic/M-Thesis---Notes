"""
Generates five per-model notebooks, all on state space S_tilde:

    nb_model_A.ipynb   — pure non-preemptive priority (gamma=theta=0)
    nb_model_B.ipynb   — jockeying both directions (theta=0)
    nb_model_B2.ipynb  — jockeying class-1 only (gamma2=theta=0)
    nb_model_C2.ipynb  — class-1 abandonments only (gamma=theta2=0)
    nb_model_X.ipynb   — full model (gamma and theta both non-zero)

Run:
    python3 build_notebooks.py
"""

import nbformat as nbf


# ---------------------------------------------------------------------------
# Notebook builder helpers
# ---------------------------------------------------------------------------

def new_nb():
    nb = nbf.v4.new_notebook()
    nb["cells"] = []
    return nb

def md(nb, text):
    nb["cells"].append(nbf.v4.new_markdown_cell(text.strip()))

def code(nb, text):
    nb["cells"].append(nbf.v4.new_code_cell(text.strip()))

def save(nb, path):
    with open(path, "w") as f:
        nbf.write(nb, f)
    print(f"  wrote {path}  ({len(nb['cells'])} cells)")


# ---------------------------------------------------------------------------
# Shared setup block (identical first two cells in every notebook)
# ---------------------------------------------------------------------------

SETUP_CODE = r"""
%matplotlib inline
import sys, os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
from matplotlib.gridspec import GridSpec

from model_master import Params, solve_exact, diagnostics
from model_master_tilde import (
    solve_exact_tilde, simulate_tilde,
    convert_S_to_Stilde,
    P_tilde, marginals_tilde, diagnostics_tilde,
    P_tilde_approx_modelA, y_star,
)

plt.rcParams.update({
    "font.family": "DejaVu Serif", "mathtext.fontset": "cm",
    "axes.titlesize": 11, "axes.labelsize": 10,
    "legend.fontsize": 9, "xtick.labelsize": 9, "ytick.labelsize": 9,
    "figure.dpi": 110, "savefig.dpi": 140, "savefig.bbox": "tight",
})

# ── shared plotting helpers ───────────────────────────────────────────────────

def tilde_heatmap(ax, pi_tilde, title, nmax=12, log=False, vmin=None, vmax=None):
    grid = pi_tilde[:nmax+1, :nmax+1].copy()
    n2i, ni = np.indices(grid.shape)
    grid[n2i > ni] = np.nan
    if log:
        grid = np.where(grid > 0, grid, np.nan)
        vm  = vmin or 1e-6
        vM  = vmax or float(np.nanmax(grid))
        im  = ax.imshow(grid, origin="lower", cmap="viridis",
                        norm=LogNorm(vmin=vm, vmax=vM))
    else:
        im = ax.imshow(grid, origin="lower", cmap="viridis",
                       vmin=vmin or 0, vmax=vmax or float(np.nanmax(grid)))
    ax.set_xlabel(r"$n$"); ax.set_ylabel(r"$n_2$")
    ax.set_title(title)
    ax.plot([0, nmax], [0, nmax], "w--", lw=0.8, alpha=0.6)
    return im

def ppgf_panel(ax, pi_tilde, p, ns=(1,2,3,5,8), show_approx=False, label_suffix=""):
    y = np.linspace(0.0, 1.0, 201)
    cols = plt.cm.viridis(np.linspace(0.15, 0.9, len(ns)))
    for n, c in zip(ns, cols):
        ax.plot(y, P_tilde(y, n, pi_tilde), color=c, lw=2.0,
                label=rf"$n={n}${label_suffix}")
        if show_approx:
            ax.plot(y, P_tilde_approx_modelA(y, n, p), color=c,
                    lw=1.3, ls="--", alpha=0.7)
    ax.set_xlabel(r"$y$"); ax.set_ylabel(r"$\widetilde{P}(y,n)$")
    ax.grid(alpha=0.3); ax.legend(fontsize=8)

def marginals_panel(ax, pi_tilde, kmax=14):
    m = marginals_tilde(pi_tilde)
    k = np.arange(min(kmax+1, len(m["pi_n1"])))
    ax.bar(k - 0.2, m["pi_n1"][:len(k)], 0.4, label=r"$\pi(n_1)$",
           color="#1f3a93", alpha=0.85)
    ax.bar(k + 0.2, m["pi_n2"][:len(k)], 0.4, label=r"$\pi(n_2)$",
           color="#c0392b", alpha=0.85)
    ax.set_xlabel("queue count"); ax.set_ylabel("probability")
    ax.legend(); ax.grid(alpha=0.3)

def metrics_row(name, p, r):
    d = diagnostics_tilde(p, r["pi_idle"], r["pi_tilde"])
    print(f"  {name:<28} pi_0={r['pi_idle']:.4f}  P(busy)={d['P_busy']:.4f}"
          f"  E[N1]={d['E_n1']:.3f}  E[N2]={d['E_n2']:.3f}"
          f"  E[N]={d['E_n']:.3f}  throughput={d['throughput']:.4f}")
""".strip()


# ===========================================================================
# MODEL A
# ===========================================================================

def build_model_A():
    nb = new_nb()
    md(nb, r"""
# Model A — Pure non-preemptive priority on $\widetilde{S}$
### $\gamma_1 = \gamma_2 = \theta_1 = \theta_2 = 0$

State space $\widetilde{S} = \{(0)\}\cup\{(n_2, n) : 0 \le n_2 \le n\}$, where
$n = n_1 + n_2$ is the total queue count and $n_2$ is the class-2 queue count.

This notebook covers:
1. Exact stationary distribution and cross-validation
2. Joint distribution $\widetilde{\pi}(n_2, n)$
3. Partial PGF $\widetilde{P}(y,n)$ and the Cohen-trick approximation
4. Marginal distributions and performance metrics
5. **Approximation error analysis** — how good is $\widetilde{P}_{\rm app}(y,n) = (1-\rho)\rho[\widetilde{y}^*(y)]^n$?
""")
    code(nb, SETUP_CODE)

    # ── Section 1: solve and validate ──
    md(nb, r"""
## 1. Solving and cross-validation

We solve the CTMC on both $S$ and $\widetilde{S}$ and verify they agree.
""")
    code(nb, r"""
p = Params(0.3, 0.4, 1.0)
r = solve_exact_tilde(p, n_max=60)
r_S = solve_exact(p, N_max=40)

# cross-check
pi_t_from_S = convert_S_to_Stilde(r_S["pi_joint"])
sh = (max(pi_t_from_S.shape[0], r["pi_tilde"].shape[0]),
      max(pi_t_from_S.shape[1], r["pi_tilde"].shape[1]))
A, B = np.zeros(sh), np.zeros(sh)
A[:pi_t_from_S.shape[0], :pi_t_from_S.shape[1]] = pi_t_from_S
B[:r["pi_tilde"].shape[0], :r["pi_tilde"].shape[1]] = r["pi_tilde"]
max_diff = np.max(np.abs(A - B))

print(f"{p.label()}")
print(f"  rho = {p.rho:.3f}   pi_0 = {r['pi_idle']:.5f}  (theory 1-rho = {1-p.rho:.5f})")
print(f"  pi(0,0) = {r['pi_tilde'][0,0]:.5f}  (theory rho(1-rho) = {p.rho*(1-p.rho):.5f})")
print(f"  max|S - Stilde| = {max_diff:.2e}  (should be < 1e-8)")
metrics_row("Model A", p, r)
""")

    # ── Section 2: joint distribution ──
    md(nb, r"""
## 2. Joint distribution $\widetilde{\pi}(n_2, n)$

The heatmap is triangular: the diagonal $n_2 = n$ (white dashed) represents states
where all queue customers are class-2 ($N_1 = 0$). The lower-left concentration near
$(n_2, n) = (0, \text{small})$ reflects the priority service: whenever any class-1
customer is waiting, it is served first, so the probability of many class-2 customers
while class-1 is also present is low.
""")
    code(nb, r"""
fig, axes = plt.subplots(1, 3, figsize=(14, 4.4))

im = tilde_heatmap(axes[0], r["pi_tilde"], r"$\widetilde{\pi}(n_2, n)$  (linear scale)")
plt.colorbar(im, ax=axes[0], fraction=0.046)

im2 = tilde_heatmap(axes[1], r["pi_tilde"],
                    r"$\widetilde{\pi}(n_2, n)$  (log scale)", log=True)
plt.colorbar(im2, ax=axes[1], fraction=0.046)

# diagonal probabilities pi_tilde(n, n) vs n
nmax_diag = 20
ns_d = np.arange(nmax_diag + 1)
diag = np.array([r["pi_tilde"][n, n] for n in ns_d])
axes[2].semilogy(ns_d, diag, "o-", color="steelblue", lw=2, label=r"$\widetilde{\pi}(n,n)$")
# overlay geometric fit
from scipy.optimize import curve_fit
valid = diag > 0
def geom(x, a, b): return a * b**x
popt, _ = curve_fit(geom, ns_d[valid], diag[valid], p0=[diag[0], p.rho])
axes[2].plot(ns_d, geom(ns_d, *popt), "k--", lw=1.3,
             label=rf"fit: {popt[0]:.3f} $\times$ {popt[1]:.3f}$^n$")
axes[2].set_xlabel(r"$n$"); axes[2].set_ylabel(r"$\widetilde{\pi}(n, n)$")
axes[2].set_title("Diagonal probabilities (all-class-2 states)")
axes[2].legend(); axes[2].grid(alpha=0.3, which="both")

fig.suptitle(f"Model A joint distribution  |  {p.label()}", fontsize=10)
fig.tight_layout()
""")

    # ── Section 3: PPGF ──
    md(nb, r"""
## 3. Partial PGF $\widetilde{P}(y, n)$ and Cohen-trick approximation

The exact recurrence is
$$(\lambda_1+\lambda_2+\mu)\widetilde{P}(y,n)
  = (\lambda_1+\lambda_2 y)\widetilde{P}(y,n{-}1)+\mu\widetilde{P}(y,n{+}1)
  + \mu y^n(1{-}y)\,\widetilde{\pi}(n{+}1,n{+}1).$$

Dropping the non-homogeneous term and applying Cohen's trick yields
$$\widetilde{P}_{\rm app}(y,n) = (1{-}\rho)\rho\,[\widetilde{y}^*(y)]^n, \qquad
\widetilde{y}^*(y) = \frac{(\lambda_1+\lambda_2+\mu)-\sqrt{(\lambda_1+\lambda_2+\mu)^2-4\mu(\lambda_1+\lambda_2 y)}}{2\mu}.$$
""")
    code(nb, r"""
fig, axes = plt.subplots(1, 2, figsize=(12, 4.4))

ppgf_panel(axes[0], r["pi_tilde"], p, show_approx=True)
axes[0].set_title("PPGF: exact (solid) vs approximation (dashed)")

# residual: exact - approx
y_g = np.linspace(0.0, 0.99, 200)
cols = plt.cm.viridis(np.linspace(0.15, 0.9, 5))
for n, c in zip([1, 2, 3, 5, 8], cols):
    exact  = P_tilde(y_g, n, r["pi_tilde"])
    approx = P_tilde_approx_modelA(y_g, n, p)
    axes[1].plot(y_g, exact - approx, color=c, lw=1.8, label=rf"$n={n}$")
axes[1].axhline(0, color="k", lw=0.8, ls="--")
axes[1].set_xlabel(r"$y$")
axes[1].set_ylabel(r"$\widetilde{P}_{\rm exact}(y,n) - \widetilde{P}_{\rm app}(y,n)$")
axes[1].set_title("Signed residual (approximation underestimates for $y<1$)")
axes[1].legend(fontsize=8); axes[1].grid(alpha=0.3)

fig.tight_layout()
""")

    # ── Section 4: marginals ──
    md(nb, r"""
## 4. Marginal distributions and performance metrics
""")
    code(nb, r"""
fig, axes = plt.subplots(1, 2, figsize=(11, 4.0))

marginals_panel(axes[0], r["pi_tilde"])
axes[0].set_title("Class marginals $\\pi(n_1)$ and $\\pi(n_2)$")

# total queue marginal vs M/M/1
m = marginals_tilde(r["pi_tilde"])
ns_tot = np.arange(len(m["pi_n"]))
axes[1].semilogy(ns_tot[:20], m["pi_n"][:20], "o-", color="steelblue",
                 lw=2, label=r"$\pi(N=n)$ from $\widetilde{S}$ solver")
axes[1].semilogy(ns_tot[:20], (1-p.rho)*p.rho**(ns_tot[:20]+1),
                 "k--", lw=1.5, label=r"M/M/1: $(1-\rho)\rho^{n+1}$")
axes[1].set_xlabel(r"$n$"); axes[1].set_ylabel(r"$\mathbb{P}(N=n,\;\text{busy})$")
axes[1].set_title("Total queue marginal")
axes[1].legend(); axes[1].grid(alpha=0.3, which="both")

fig.tight_layout()

d = diagnostics_tilde(p, r["pi_idle"], r["pi_tilde"])
print(f"Performance metrics for {p.label()}")
for k, v in d.items():
    print(f"  {k:<25} {v:.6f}")
""")

    # ── Section 5: approximation error ──
    md(nb, r"""
## 5. Approximation error analysis

We quantify how well $\widetilde{P}_{\rm app}(y,n)$ approximates the exact PPGF:
$$\varepsilon_{\rm rel}(y,n) = \frac{|\widetilde{P}_{\rm app}(y,n)-\widetilde{P}(y,n)|}{\widetilde{P}(y,n)}, \qquad
\varepsilon_\infty = \max_{y,n}\varepsilon_{\rm rel},\qquad
\varepsilon_{L_2} = \text{RMS}(\varepsilon_{\rm rel}).$$

The approximation is valid only for **Model A** (the dropped term requires $\gamma=\theta=0$).
""")
    code(nb, r"""
# ── error metric helper ───────────────────────────────────────────────────────

def approx_errors(p, n_max=50, y_grid=None, n_values=None):
    if y_grid  is None: y_grid  = np.linspace(0.0, 0.98, 100)
    if n_values is None: n_values = np.arange(1, 16)
    r = solve_exact_tilde(p, n_max=n_max)
    pi_t = r["pi_tilde"]
    eps_rel = np.zeros((len(n_values), len(y_grid)))
    for i, n in enumerate(n_values):
        exact  = P_tilde(y_grid, n, pi_t)
        approx = P_tilde_approx_modelA(y_grid, n, p)
        mask = exact > 1e-14
        eps_rel[i, mask] = np.abs(approx[mask] - exact[mask]) / exact[mask]
    return dict(
        eps_rel=eps_rel,
        eps_inf=float(eps_rel.max()),
        eps_L2=float(np.sqrt((eps_rel**2).mean())),
        n_values=n_values, y_grid=y_grid,
    )

print("Helper defined.")
""")
    code(nb, r"""
# 5a. Pointwise error field for the default parameters
ns_err  = np.arange(1, 16)
y_err   = np.linspace(0.0, 0.98, 120)
err0    = approx_errors(p, n_max=60, y_grid=y_err, n_values=ns_err)

fig, axes = plt.subplots(1, 3, figsize=(14, 4.2))

im = axes[0].imshow(
    err0["eps_rel"], origin="lower", aspect="auto",
    extent=[y_err[0], y_err[-1], ns_err[0]-0.5, ns_err[-1]+0.5],
    norm=LogNorm(vmin=1e-5, vmax=1.0), cmap="plasma",
)
plt.colorbar(im, ax=axes[0], label=r"$\varepsilon_{\rm rel}(y,n)$")
axes[0].set_xlabel(r"$y$"); axes[0].set_ylabel(r"$n$")
axes[0].set_title(rf"Error field  ($\rho_1/\rho={p.rho1/p.rho:.2f}$, $\rho={p.rho:.1f}$)")

cols = plt.cm.viridis(np.linspace(0.15, 0.9, 6))
for n, c in zip([1, 2, 3, 5, 8, 12], cols):
    idx = np.where(ns_err == n)[0]
    if len(idx): axes[1].plot(y_err, err0["eps_rel"][idx[0]], color=c, lw=1.8, label=rf"$n={n}$")
axes[1].set_yscale("log"); axes[1].set_xlabel(r"$y$")
axes[1].set_ylabel(r"$\varepsilon_{\rm rel}$"); axes[1].grid(alpha=0.3, which="both")
axes[1].set_title(r"$\varepsilon_{\rm rel}(y,n)$ vs $y$ for fixed $n$")
axes[1].legend(fontsize=8)

axes[2].semilogy(ns_err, err0["eps_rel"].max(axis=1), "o-", color="steelblue", lw=2)
axes[2].axhline(err0["eps_inf"], color="red", ls="--", lw=1.2,
                label=rf"$\varepsilon_\infty={err0['eps_inf']:.3f}$")
axes[2].set_xlabel(r"$n$"); axes[2].set_ylabel(r"$\max_y\varepsilon_{\rm rel}$")
axes[2].set_title("Max error decays geometrically in $n$")
axes[2].legend(); axes[2].grid(alpha=0.3, which="both")

fig.suptitle(
    rf"Approximation error  |  {p.label()}  "
    rf"|  $\varepsilon_\infty={err0['eps_inf']:.3f}$,  $\varepsilon_{{L_2}}={err0['eps_L2']:.3f}$",
    fontsize=10,
)
fig.tight_layout()
print(f"eps_inf = {err0['eps_inf']:.4f},   eps_L2 = {err0['eps_L2']:.4f}")
""")
    code(nb, r"""
# 5b. Sweep rho1/rho (keep rho=0.7) and sweep rho (keep rho1/rho=0.4)
mu = 1.0
rho_fix, split_fix = 0.7, 0.4
splits = np.linspace(0.05, 0.95, 19)
rhos   = np.linspace(0.10, 0.95, 20)

ei_split, eL_split = [], []
for s in splits:
    e = approx_errors(Params(s*rho_fix*mu, (1-s)*rho_fix*mu, mu), n_max=50)
    ei_split.append(e["eps_inf"]); eL_split.append(e["eps_L2"])

ei_rho, eL_rho = [], []
for rho in rhos:
    e = approx_errors(Params(split_fix*rho*mu, (1-split_fix)*rho*mu, mu), n_max=50)
    ei_rho.append(e["eps_inf"]); eL_rho.append(e["eps_L2"])

fig, axes = plt.subplots(1, 2, figsize=(11, 4.0))
for ax, xs, eis, eLs, xl, tit in [
    (axes[0], splits, ei_split, eL_split,
     r"$\rho_1/\rho$", rf"Error vs load split  ($\rho={rho_fix}$ fixed)"),
    (axes[1], rhos,   ei_rho,   eL_rho,
     r"$\rho$", rf"Error vs total load  ($\rho_1/\rho={split_fix}$ fixed)"),
]:
    ax.plot(xs, eis, "o-", color="darkblue", lw=2, label=r"$\varepsilon_\infty$")
    ax.plot(xs, eLs, "s--", color="firebrick", lw=2, label=r"$\varepsilon_{L_2}$")
    ax.set_xlabel(xl); ax.set_ylabel("error"); ax.set_title(tit)
    ax.legend(); ax.grid(alpha=0.3)
fig.tight_layout()
""")
    code(nb, r"""
# 5c. 2D heat-map over (rho1, rho2)
mu = 1.0
rho1_v = np.linspace(0.04, 0.58, 16)
rho2_v = np.linspace(0.04, 0.58, 16)
ei_2D  = np.full((len(rho1_v), len(rho2_v)), np.nan)

for i, r1 in enumerate(rho1_v):
    for j, r2 in enumerate(rho2_v):
        if r1 + r2 >= 0.97: continue
        e = approx_errors(Params(r1*mu, r2*mu, mu), n_max=40,
                          y_grid=np.linspace(0.0, 0.95, 60),
                          n_values=np.arange(1, 13))
        ei_2D[i, j] = e["eps_inf"]

fig, ax = plt.subplots(figsize=(6.5, 5.5))
ext = [rho2_v[0], rho2_v[-1], rho1_v[0], rho1_v[-1]]
im = ax.imshow(ei_2D, origin="lower", extent=ext, aspect="auto",
               cmap="RdYlGn_r", norm=LogNorm(vmin=1e-3, vmax=1.0))
plt.colorbar(im, ax=ax, label=r"$\varepsilon_\infty$")
r1_line = np.linspace(rho2_v[0], 0.95, 100)
ax.plot(r1_line, 0.95 - r1_line, "k--", lw=1.5, label=r"$\rho=0.95$")
ax.set_xlabel(r"$\rho_2$"); ax.set_ylabel(r"$\rho_1$")
ax.set_title(r"$\varepsilon_\infty$ over $(\rho_1, \rho_2)$ — green = accurate, red = poor")
ax.legend(fontsize=8); fig.tight_layout()
""")
    code(nb, r"""
# 5d. Summary table
configs = [
    ("Light, balanced",        Params(0.20, 0.20, 1.0)),
    ("Light, prio heavy",      Params(0.30, 0.10, 1.0)),
    ("Light, prio light",      Params(0.10, 0.30, 1.0)),
    ("Medium, balanced",       Params(0.30, 0.35, 1.0)),
    ("Medium, prio heavy",     Params(0.45, 0.20, 1.0)),
    ("Medium, prio light",     Params(0.15, 0.50, 1.0)),
    ("Heavy, balanced",        Params(0.40, 0.45, 1.0)),
    ("Heavy, prio heavy",      Params(0.60, 0.25, 1.0)),
    ("Heavy, prio light",      Params(0.20, 0.70, 1.0)),
]
print(f"{'Configuration':<26} {'rho':>5} {'r1/r':>6} {'eps_inf':>9} {'eps_L2':>9}")
print("─" * 60)
for name, pm in configs:
    e = approx_errors(pm, n_max=50,
                      y_grid=np.linspace(0.0, 0.95, 80),
                      n_values=np.arange(1, 14))
    print(f"{name:<26} {pm.rho:>5.2f} {pm.rho1/pm.rho:>6.2f} "
          f"{e['eps_inf']:>9.4f} {e['eps_L2']:>9.4f}")
print()
print("Rule of thumb: eps_inf < 5 % when rho1/rho > 0.4 and rho < 0.8.")
""")
    md(nb, r"""
### Conclusions for Model A approximation

| Regime | $\varepsilon_\infty$ | Assessment |
|---|---|---|
| $\rho\le0.6$, $\rho_1/\rho\ge0.4$ | $<2\%$ | excellent |
| $\rho\le0.8$, $\rho_1/\rho\ge0.4$ | $<5\%$ | good |
| $\rho_1/\rho<0.2$ | $>15\%$ | poor — class-2 diagonal states dominate |
| near stability boundary | diverges | inapplicable |

The approximation *systematically underestimates* $\widetilde{P}(y,n)$ for $y<1$,
and is **exact at $y=1$** (both sides equal $(1-\rho)\rho^{n+1}$, the M/M/1 marginal).
""")
    save(nb, "nb_model_A.ipynb")


# ===========================================================================
# MODEL B  (jockeying, both directions)
# ===========================================================================

def build_model_B():
    nb = new_nb()
    md(nb, r"""
# Model B — Jockeying (both directions) on $\widetilde{S}$
### $\gamma_1, \gamma_2 > 0$,  $\theta_1 = \theta_2 = 0$

Jockeying moves customers between queues *without removing them*. In state space
$\widetilde{S}$ this means transitions that change $n_2$ at **fixed $n$**: a
class-1 customer who jockeys increases $n_2 \to n_2{+}1$ (and $n_1 \to n_1{-}1$),
keeping the total $n$ constant. Consequently:

* The **total queue marginal** $\widetilde{P}(1,n)=(1-\rho)\rho^{n+1}$ is
  **invariant** under any $(\gamma_1, \gamma_2)$ — jockeying cannot change $\rho$.
* The **within-column redistribution** of $\widetilde{\pi}(n_2,n)$ over $n_2$
  *does* change with $\gamma_i$.
""")
    code(nb, SETUP_CODE)
    code(nb, r"""
p_A  = Params(0.3, 0.4, 1.0)                        # reference
p_B  = Params(0.3, 0.4, 1.0, gamma1=0.5, gamma2=0.3)

r_A  = solve_exact_tilde(p_A, n_max=60)
r_B  = solve_exact_tilde(p_B, n_max=60)

print("Cross-validate (jockeying preserves pi_0, pi(0,0), E[N]):")
for name, pm, r in [("Model A", p_A, r_A), ("Model B", p_B, r_B)]:
    metrics_row(name, pm, r)
""")

    md(nb, r"""
## 1. Joint distribution: Model A vs Model B

Jockeying redistributes mass *within each column* $n=\text{const}$ of the triangle.
$\gamma_1>0$ pushes mass toward larger $n_2$ (class-1 moves to class-2 queue).
$\gamma_2>0$ pushes it back.
""")
    code(nb, r"""
fig, axes = plt.subplots(1, 2, figsize=(11, 4.4))
vmax = max(np.nanmax(r_A["pi_tilde"][:13,:13]),
           np.nanmax(r_B["pi_tilde"][:13,:13]))
for ax, (r, name) in zip(axes, [(r_A, "Model A  (no jockeying)"),
                                 (r_B, rf"Model B  $\gamma_1=0.5,\gamma_2=0.3$")]):
    im = tilde_heatmap(ax, r["pi_tilde"], name, vmax=vmax)
    plt.colorbar(im, ax=ax, fraction=0.046)
fig.suptitle(f"{p_A.label()}")
fig.tight_layout()
""")

    md(nb, r"""
## 2. Within-column profile: $\widetilde{\pi}(n_2, n)$ for fixed $n$

For each total queue length $n$, how is the mass spread over $n_2 \in [0,n]$?
""")
    code(nb, r"""
fig, axes = plt.subplots(1, 3, figsize=(14, 4.0))
for ax, n in zip(axes, [2, 4, 8]):
    n2vals = np.arange(n + 1)
    col_A = np.array([r_A["pi_tilde"][n2, n] for n2 in n2vals])
    col_B = np.array([r_B["pi_tilde"][n2, n] for n2 in n2vals])
    ax.bar(n2vals - 0.2, col_A, 0.38, label="Model A", color="#1f3a93", alpha=0.85)
    ax.bar(n2vals + 0.2, col_B, 0.38, label="Model B", color="#c0392b", alpha=0.85)
    ax.set_xlabel(r"$n_2$"); ax.set_ylabel(r"$\widetilde{\pi}(n_2, n)$")
    ax.set_title(rf"$n = {n}$ column"); ax.legend(fontsize=8); ax.grid(alpha=0.3)
fig.suptitle("Within-column redistribution under jockeying", fontsize=10)
fig.tight_layout()
""")

    md(nb, r"""
## 3. Invariance of the total queue marginal

The marginal $\widetilde{P}(1,n) = \mathbb{P}(N=n,\text{busy})$ must equal
$(1-\rho)\rho^{n+1}$ for **any** choice of $\gamma_i$.
""")
    code(nb, r"""
gammas = [(0.0, 0.0), (0.5, 0.3), (1.0, 0.0), (0.0, 1.0), (2.0, 2.0)]
fig, ax = plt.subplots(figsize=(7.5, 3.6))
ns = np.arange(16)
for g1, g2 in gammas:
    pg = Params(0.3, 0.4, 1.0, gamma1=g1, gamma2=g2)
    rg = solve_exact_tilde(pg, n_max=60)
    Pn = [float(P_tilde(1.0, n, rg["pi_tilde"])) for n in ns]
    ax.plot(ns, Pn, "o-", ms=5, lw=1.6,
            label=rf"$\gamma_1={g1},\gamma_2={g2}$")
ax.plot(ns, (1-p_A.rho)*p_A.rho**(ns+1), "k--", lw=2.0,
        label=r"M/M/1: $(1-\rho)\rho^{n+1}$")
ax.set_xlabel(r"$n$"); ax.set_ylabel(r"$\widetilde{P}(1, n)$")
ax.set_yscale("log"); ax.set_title("Total queue marginal (all curves must overlap)")
ax.legend(fontsize=8, ncol=2); ax.grid(alpha=0.3, which="both")
fig.tight_layout()
""")

    md(nb, r"""
## 4. PPGF $\widetilde{P}(y,n)$ curves
""")
    code(nb, r"""
fig, axes = plt.subplots(1, 2, figsize=(12, 4.2))
ppgf_panel(axes[0], r_A["pi_tilde"], p_A, label_suffix="  A")
ppgf_panel(axes[1], r_B["pi_tilde"], p_B, label_suffix="  B")
axes[0].set_title("Model A PPGF"); axes[1].set_title("Model B PPGF")
fig.tight_layout()
""")

    md(nb, r"""
## 5. Effect of $\gamma_1$ and $\gamma_2$ on mean queue lengths

Because $E[N] = E[N_1]+E[N_2]$ is invariant, increasing $\gamma_1$
(class-1 → class-2 migration) lowers $E[N_1]$ and raises $E[N_2]$ by the same amount.
""")
    code(nb, r"""
g_vals = np.linspace(0.0, 3.0, 25)
mu_b = 1.0

# sweep gamma1, keep gamma2=0
En1_g1, En2_g1 = [], []
for g in g_vals:
    r_g = solve_exact_tilde(Params(0.3, 0.4, mu_b, gamma1=g), n_max=60)
    d   = diagnostics_tilde(Params(0.3, 0.4, mu_b, gamma1=g), r_g["pi_idle"], r_g["pi_tilde"])
    En1_g1.append(d["E_n1"]); En2_g1.append(d["E_n2"])

# sweep gamma2, keep gamma1=0
En1_g2, En2_g2 = [], []
for g in g_vals:
    r_g = solve_exact_tilde(Params(0.3, 0.4, mu_b, gamma2=g), n_max=60)
    d   = diagnostics_tilde(Params(0.3, 0.4, mu_b, gamma2=g), r_g["pi_idle"], r_g["pi_tilde"])
    En1_g2.append(d["E_n1"]); En2_g2.append(d["E_n2"])

fig, axes = plt.subplots(1, 2, figsize=(12, 4.0))
for ax, (En1, En2, g_lbl) in zip(axes, [
    (En1_g1, En2_g1, r"$\gamma_1$ (class-1 $\to$ class-2)"),
    (En1_g2, En2_g2, r"$\gamma_2$ (class-2 $\to$ class-1)"),
]):
    ax.plot(g_vals, En1, "b-o", ms=4, lw=2, label=r"$E[N_1]$")
    ax.plot(g_vals, En2, "r-s", ms=4, lw=2, label=r"$E[N_2]$")
    ax.plot(g_vals, np.array(En1)+np.array(En2), "k--", lw=1.5, label=r"$E[N]$")
    ax.set_xlabel(g_lbl); ax.set_ylabel("mean queue length")
    ax.set_title(f"Varying {g_lbl}"); ax.legend(); ax.grid(alpha=0.3)
fig.tight_layout()
""")
    save(nb, "nb_model_B.ipynb")


# ===========================================================================
# MODEL B2  (jockeying class-1 only)
# ===========================================================================

def build_model_B2():
    nb = new_nb()
    md(nb, r"""
# Model B₂ — Jockeying from class-1 only on $\widetilde{S}$
### $\gamma_1 > 0$,  $\gamma_2 = \theta_1 = \theta_2 = 0$

Class-1 customers jockey to class-2 at per-customer rate $\gamma_1$, but class-2
customers never move back. In state space $\widetilde{S}$, jockeying increases $n_2$
at fixed $n$, so mass flows *up* within each column toward the diagonal $n_2=n$.

The fundamental equation reduces to a **first-order linear ODE in $x$** (thesis §6.1.2),
which admits a closed-form integral solution. Here we analyse it numerically.
""")
    code(nb, SETUP_CODE)
    code(nb, r"""
p_A  = Params(0.3, 0.4, 1.0)
p_B2 = Params(0.3, 0.4, 1.0, gamma1=0.8)

r_A  = solve_exact_tilde(p_A,  n_max=60)
r_B2 = solve_exact_tilde(p_B2, n_max=60)

print("Cross-validate (jockeying preserves total load):")
for name, pm, r in [("Model A", p_A, r_A), ("Model B2", p_B2, r_B2)]:
    metrics_row(name, pm, r)
""")

    md(nb, r"""
## 1. Joint distribution — mass migration toward the diagonal

$\gamma_1>0$ moves class-1 customers into the class-2 queue (increasing $n_2$ at
fixed $n$). The mass in each column shifts *up* toward $n_2=n$, making the diagonal
more prominent and the lower triangle sparser.
""")
    code(nb, r"""
fig, axes = plt.subplots(1, 3, figsize=(14.5, 4.4))
g_vals_plot = [0.0, 0.8, 3.0]
for ax, g1 in zip(axes, g_vals_plot):
    p_g = Params(0.3, 0.4, 1.0, gamma1=g1)
    r_g = solve_exact_tilde(p_g, n_max=60)
    im  = tilde_heatmap(ax, r_g["pi_tilde"], rf"$\gamma_1={g1}$", log=True)
    plt.colorbar(im, ax=ax, fraction=0.046)
fig.suptitle(r"B₂ joint $\widetilde{\pi}(n_2, n)$ — increasing $\gamma_1$ moves mass up each column")
fig.tight_layout()
""")

    md(nb, r"""
## 2. Within-column profile evolution
""")
    code(nb, r"""
g_sweep = [0.0, 0.3, 0.8, 2.0, 5.0]
fig, axes = plt.subplots(1, 3, figsize=(14, 4.0))
for ax, n in zip(axes, [2, 4, 8]):
    n2vals = np.arange(n + 1)
    cols = plt.cm.Blues(np.linspace(0.3, 0.9, len(g_sweep)))
    for g1, c in zip(g_sweep, cols):
        r_g = solve_exact_tilde(Params(0.3, 0.4, 1.0, gamma1=g1), n_max=60)
        col = np.array([r_g["pi_tilde"][n2, n] for n2 in n2vals])
        ax.plot(n2vals, col, "o-", color=c, lw=1.8, ms=5,
                label=rf"$\gamma_1={g1}$")
    ax.set_xlabel(r"$n_2$"); ax.set_ylabel(r"$\widetilde{\pi}(n_2, n)$")
    ax.set_title(rf"Column $n={n}$"); ax.legend(fontsize=7); ax.grid(alpha=0.3)
fig.suptitle(r"B₂: within-column redistribution as $\gamma_1$ increases")
fig.tight_layout()
""")

    md(nb, r"""
## 3. PPGF and mean queue lengths vs $\gamma_1$
""")
    code(nb, r"""
fig, axes = plt.subplots(1, 2, figsize=(12, 4.2))
ppgf_panel(axes[0], r_A["pi_tilde"],  p_A,  label_suffix=" (A)")
ppgf_panel(axes[1], r_B2["pi_tilde"], p_B2, label_suffix=" (B2)")
axes[0].set_title("Model A  PPGF"); axes[1].set_title(r"Model B₂  PPGF  ($\gamma_1=0.8$)")
fig.tight_layout()

g_vals = np.linspace(0.0, 4.0, 30)
En1, En2 = [], []
for g in g_vals:
    r_g = solve_exact_tilde(Params(0.3, 0.4, 1.0, gamma1=g), n_max=60)
    d   = diagnostics_tilde(Params(0.3, 0.4, 1.0, gamma1=g), r_g["pi_idle"], r_g["pi_tilde"])
    En1.append(d["E_n1"]); En2.append(d["E_n2"])

fig2, ax = plt.subplots(figsize=(7, 3.6))
ax.plot(g_vals, En1, "b-o", ms=4, lw=2, label=r"$E[N_1]$")
ax.plot(g_vals, En2, "r-s", ms=4, lw=2, label=r"$E[N_2]$")
ax.plot(g_vals, np.array(En1)+np.array(En2), "k--", lw=1.5, label=r"$E[N]$ (invariant)")
ax.set_xlabel(r"$\gamma_1$"); ax.set_ylabel("mean queue length")
ax.set_title(r"B₂: mean queue lengths vs $\gamma_1$")
ax.legend(); ax.grid(alpha=0.3)
fig2.tight_layout()
""")
    save(nb, "nb_model_B2.ipynb")


# ===========================================================================
# MODEL C2  (theta1 only)
# ===========================================================================

def build_model_C2():
    nb = new_nb()
    md(nb, r"""
# Model C₂ — Class-1 abandonments only on $\widetilde{S}$
### $\theta_1 > 0$,  $\gamma_1 = \gamma_2 = \theta_2 = 0$

Class-1 customers abandon the queue at per-customer rate $\theta_1$. In state
space $\widetilde{S}$, abandonment of a class-1 customer reduces $n$ by 1 while
keeping $n_2$ fixed: the transition is $(n_2, n) \to (n_2, n-1)$ at rate
$\theta_1(n-n_2) = \theta_1 n_1$.

Key consequences (from the thesis Corollary 7):
$$\pi_0 = \frac{1-\lambda_2\mathbb{E}[B_C]}{1+\lambda_1\mathbb{E}[B_C]}, \qquad
\pi(0,0) = (\rho_1+\rho_2)\,\pi_0,$$
where $\mathbb{E}[B_C] = {}_1F_1(1;\mu/\theta_1{+}1;\lambda_1/\theta_1)/\mu$
is the mean busy period of the $M/M/1{+}M$ subsystem.
As $\theta_1\to0$, these recover $\pi_0=1-\rho$ and $\pi(0,0)=\rho(1-\rho)$.
""")
    code(nb, SETUP_CODE)
    code(nb, r"""
from scipy.special import hyp1f1

def E_BC(lam1, mu, theta1):
    if theta1 == 0: return 1.0 / (mu - lam1)
    return hyp1f1(1, mu/theta1 + 1, lam1/theta1) / mu

def pi0_C2(lam1, lam2, mu, theta1):
    eb = E_BC(lam1, mu, theta1)
    return (1 - lam2*eb) / (1 + lam1*eb)

def pi00_C2(lam1, lam2, mu, theta1):
    return (lam1+lam2)/mu * pi0_C2(lam1, lam2, mu, theta1)

lam1, lam2, mu = 0.3, 0.4, 1.0
theta1_vals = [0.0, 0.2, 0.5, 1.0, 2.0]

print(f"{'theta1':>8} {'pi0 formula':>14} {'pi0 numeric':>14} "
      f"{'pi(0,0) formula':>17} {'pi(0,0) numeric':>17}")
print("─" * 75)
for th in theta1_vals:
    if th == 0.0:
        pm = Params(lam1, lam2, mu)
    else:
        pm = Params(lam1, lam2, mu, theta1=th)
    r  = solve_exact_tilde(pm, n_max=60)
    pi0_f  = pi0_C2(lam1, lam2, mu, th) if th > 0 else 1-(lam1+lam2)/mu
    pi00_f = pi00_C2(lam1, lam2, mu, th) if th > 0 else (lam1+lam2)/mu*(1-(lam1+lam2)/mu)
    print(f"{th:>8.2f} {pi0_f:>14.6f} {r['pi_idle']:>14.6f} "
          f"{pi00_f:>17.6f} {r['pi_tilde'][0,0]:>17.6f}")
""")

    md(nb, r"""
## 1. Joint distribution: abandonments pull mass toward the diagonal

A class-1 customer who abandons removes a count from $n_1=n-n_2$, moving the
state from $(n_2,n)$ to $(n_2,n-1)$. This *drains the strictly-upper-triangular*
region (large $n_1$) toward the diagonal ($n_1=0$, $n_2=n$).
""")
    code(nb, r"""
fig, axes = plt.subplots(1, 4, figsize=(15, 4.0))
for ax, th in zip(axes, [0.0, 0.3, 1.0, 3.0]):
    pm = Params(lam1, lam2, mu, theta1=th)
    r  = solve_exact_tilde(pm, n_max=60)
    im = tilde_heatmap(ax, r["pi_tilde"], rf"$\theta_1={th}$", log=True,
                       vmin=1e-6, vmax=r["pi_tilde"][:13,:13].max())
    plt.colorbar(im, ax=ax, fraction=0.046)
fig.suptitle(r"Model C₂: increasing $\theta_1$ drains the interior toward the diagonal")
fig.tight_layout()
""")

    md(nb, r"""
## 2. PPGF $\widetilde{P}(y,n)$: redistribution under $\theta_1$
""")
    code(nb, r"""
fig, axes = plt.subplots(1, 2, figsize=(12, 4.2))
r_A = solve_exact_tilde(Params(lam1, lam2, mu), n_max=60)

ppgf_panel(axes[0], r_A["pi_tilde"], Params(lam1, lam2, mu), label_suffix="  (A)")
axes[0].set_title(r"Model A  ($\theta_1=0$)")

th_show = 0.8
r_C = solve_exact_tilde(Params(lam1, lam2, mu, theta1=th_show), n_max=60)
ppgf_panel(axes[1], r_C["pi_tilde"], Params(lam1, lam2, mu, theta1=th_show),
           label_suffix=rf"  ($\theta_1={th_show}$)")
axes[1].set_title(rf"Model C₂  ($\theta_1={th_show}$)")
fig.tight_layout()
""")

    md(nb, r"""
## 3. Convergence to Model A as $\theta_1 \to 0$

All metrics ($\pi_0$, $E[N_1]$, $E[N_2]$, throughput) must recover their Model A
values in the limit $\theta_1\to0$.
""")
    code(nb, r"""
th_range = np.concatenate([np.linspace(0.01, 0.2, 10), np.linspace(0.2, 3.0, 20)])
pi0_list, En1_list, En2_list, thru_list = [], [], [], []
for th in th_range:
    pm = Params(lam1, lam2, mu, theta1=th)
    r  = solve_exact_tilde(pm, n_max=60)
    d  = diagnostics_tilde(pm, r["pi_idle"], r["pi_tilde"])
    pi0_list.append(r["pi_idle"]); En1_list.append(d["E_n1"])
    En2_list.append(d["E_n2"]);   thru_list.append(d["throughput"])

# Model A reference values
r_ref = solve_exact_tilde(Params(lam1, lam2, mu), n_max=60)
d_ref = diagnostics_tilde(Params(lam1, lam2, mu), r_ref["pi_idle"], r_ref["pi_tilde"])

fig, axes = plt.subplots(2, 2, figsize=(11, 7.0))
for ax, vals, ref, ylabel, title in zip(
    axes.flat,
    [pi0_list, En1_list, En2_list, thru_list],
    [r_ref["pi_idle"], d_ref["E_n1"], d_ref["E_n2"], d_ref["throughput"]],
    [r"$\pi_0$", r"$E[N_1]$", r"$E[N_2]$", r"throughput"],
    [r"Idle probability $\pi_0$", r"Mean class-1 queue $E[N_1]$",
     r"Mean class-2 queue $E[N_2]$", "Throughput"],
):
    ax.semilogx(th_range, vals, "o-", color="steelblue", ms=4, lw=2)
    ax.axhline(ref, color="red", ls="--", lw=1.5,
               label=f"Model A: {ref:.4f}")
    ax.set_xlabel(r"$\theta_1$"); ax.set_ylabel(ylabel); ax.set_title(title)
    ax.legend(fontsize=9); ax.grid(alpha=0.3, which="both")
fig.suptitle(r"Model C₂ $\to$ Model A as $\theta_1\to0$", fontsize=11)
fig.tight_layout()
""")

    md(nb, r"""
## 4. Total queue marginal: abandonments lower $\mathbb{P}(\text{busy})$

Unlike jockeying, abandonments *do* change the total queue marginal: the sum
$\sum_n\widetilde{P}(1,n)=\mathbb{P}(\text{busy})<\rho$ because some customers
leave before service.
""")
    code(nb, r"""
fig, ax = plt.subplots(figsize=(7.5, 3.6))
ns = np.arange(16)
for th in [0.0, 0.1, 0.3, 0.6, 1.0, 2.0]:
    pm = Params(lam1, lam2, mu, theta1=th) if th > 0 else Params(lam1, lam2, mu)
    r  = solve_exact_tilde(pm, n_max=60)
    Pn = [float(P_tilde(1.0, n, r["pi_tilde"])) for n in ns]
    ax.plot(ns, Pn, "o-", ms=4, lw=1.6,
            label=rf"$\theta_1={th}$  (sum={sum(Pn):.3f})")
ax.set_xlabel(r"$n$"); ax.set_yscale("log")
ax.set_ylabel(r"$\widetilde{P}(1, n) = \mathbb{P}(N=n, \mathrm{busy})$")
ax.set_title(r"Abandonments lower $\mathbb{P}(\text{busy})$ and shift the total distribution")
ax.legend(fontsize=8, ncol=2); ax.grid(alpha=0.3, which="both")
fig.tight_layout()
""")
    save(nb, "nb_model_C2.ipynb")


# ===========================================================================
# MODEL X  (full model)
# ===========================================================================

def build_model_X():
    nb = new_nb()
    md(nb, r"""
# Model X — Full model (jockeying + abandonments) on $\widetilde{S}$
### $\gamma_1, \gamma_2, \theta_1, \theta_2$ all non-zero

The most general variant. Since no closed-form PGF exists for the full model,
analysis is entirely numerical via the $\widetilde{S}$-native CTMC solver.

We study how jockeying and abandonments interact, and show that all previous
models are special cases of this one.
""")
    code(nb, SETUP_CODE)
    code(nb, r"""
base = dict(lam1=0.3, lam2=0.4, mu=1.0)
scenarios = {
    "Model A":              Params(**base),
    "Model B (jockey)":     Params(**base, gamma1=0.5, gamma2=0.3),
    r"Model C2 (theta1)":   Params(**base, theta1=0.4),
    "Full (gamma+theta)":   Params(**base, gamma1=0.4, gamma2=0.2, theta1=0.2, theta2=0.1),
}
results = {}
for name, p in scenarios.items():
    r = solve_exact_tilde(p, n_max=60)
    results[name] = (p, r)
    metrics_row(name, p, r)
""")

    md(nb, r"""
## 1. Cross-model joint distribution comparison
""")
    code(nb, r"""
fig, axes = plt.subplots(1, 4, figsize=(15.5, 4.0))
for ax, (name, (p, r)) in zip(axes, results.items()):
    im = tilde_heatmap(ax, r["pi_tilde"], name, log=True, vmin=1e-6)
    d  = diagnostics_tilde(p, r["pi_idle"], r["pi_tilde"])
    ax.text(0.05, 0.95,
            f"$\\pi_0$={r['pi_idle']:.2f}\n"
            f"$E[N_1]$={d['E_n1']:.2f}\n$E[N_2]$={d['E_n2']:.2f}\n"
            f"thru={d['throughput']:.3f}",
            transform=ax.transAxes, va="top", ha="left", color="white",
            fontsize=8, bbox=dict(boxstyle="round", fc="black", alpha=0.5))
    plt.colorbar(im, ax=ax, fraction=0.046)
fig.suptitle(r"Joint $\widetilde{\pi}(n_2, n)$ across models — same $\lambda_1,\lambda_2,\mu$")
fig.tight_layout()
""")

    md(nb, r"""
## 2. Combined effect: 2D sweep over $(\gamma_1, \theta_1)$

With $\gamma_2=\theta_2=0$ fixed, we vary both jockeying and abandonment rates
simultaneously. The contours show iso-performance curves for $E[N_1]$ and $E[N_2]$.
""")
    code(nb, r"""
g1_vals = np.linspace(0.0, 2.0, 14)
t1_vals = np.linspace(0.0, 2.0, 14)
lam1, lam2, mu_b = 0.3, 0.4, 1.0

En1_surf = np.zeros((len(g1_vals), len(t1_vals)))
En2_surf = np.zeros_like(En1_surf)

for i, g1 in enumerate(g1_vals):
    for j, t1 in enumerate(t1_vals):
        pm = Params(lam1, lam2, mu_b, gamma1=g1, theta1=t1)
        r  = solve_exact_tilde(pm, n_max=50)
        d  = diagnostics_tilde(pm, r["pi_idle"], r["pi_tilde"])
        En1_surf[i, j] = d["E_n1"]
        En2_surf[i, j] = d["E_n2"]

fig, axes = plt.subplots(1, 2, figsize=(12, 5.0))
ext = [t1_vals[0], t1_vals[-1], g1_vals[0], g1_vals[-1]]
for ax, surf, title in [
    (axes[0], En1_surf, r"$E[N_1]$ — class-1 mean queue"),
    (axes[1], En2_surf, r"$E[N_2]$ — class-2 mean queue"),
]:
    im = ax.imshow(surf, origin="lower", extent=ext, aspect="auto", cmap="plasma_r")
    cs = ax.contour(surf, levels=8, colors="white", linewidths=0.8,
                    extent=ext, origin="lower")
    ax.clabel(cs, fmt="%.2f", fontsize=7)
    plt.colorbar(im, ax=ax)
    ax.set_xlabel(r"$\theta_1$ (abandonment)"); ax.set_ylabel(r"$\gamma_1$ (jockeying)")
    ax.set_title(title)
fig.suptitle(r"Full model: performance surface over $(\gamma_1, \theta_1)$"
             "\n" r"($\lambda_1=0.3, \lambda_2=0.4, \mu=1, \gamma_2=\theta_2=0$)",
             fontsize=10)
fig.tight_layout()
""")

    md(nb, r"""
## 3. PPGF comparison across all four models
""")
    code(nb, r"""
fig, axes = plt.subplots(1, 4, figsize=(16, 4.2))
for ax, (name, (p, r)) in zip(axes, results.items()):
    ppgf_panel(ax, r["pi_tilde"], p)
    ax.set_title(name)
fig.tight_layout()
""")

    md(nb, r"""
## 4. Special case verification: full model reduces to each sub-model

Set each combination of extra parameters to zero and check that the result
numerically matches the dedicated per-model solution.
""")
    code(nb, r"""
lam1, lam2, mu_v = 0.3, 0.4, 1.0
g1, g2, t1, t2   = 0.5, 0.3, 0.4, 0.2

tests = [
    ("Model A (gamma=theta=0)",     Params(lam1, lam2, mu_v),
                                    Params(lam1, lam2, mu_v, gamma1=0, gamma2=0,
                                           theta1=0, theta2=0)),
    ("Model B (theta=0)",           Params(lam1, lam2, mu_v, gamma1=g1, gamma2=g2),
                                    Params(lam1, lam2, mu_v, gamma1=g1, gamma2=g2,
                                           theta1=0, theta2=0)),
    ("Model C2 (gamma=theta2=0)",   Params(lam1, lam2, mu_v, theta1=t1),
                                    Params(lam1, lam2, mu_v, gamma1=0, gamma2=0,
                                           theta1=t1, theta2=0)),
]
print(f"{'test':<35} {'max|pi_special - pi_full|':>28}")
print("─" * 65)
for name, p_special, p_full in tests:
    r_sp = solve_exact_tilde(p_special, n_max=50)
    r_fu = solve_exact_tilde(p_full,    n_max=50)
    sh   = min(r_sp["pi_tilde"].shape[0], r_fu["pi_tilde"].shape[0])
    diff = np.max(np.abs(r_sp["pi_tilde"][:sh,:sh] - r_fu["pi_tilde"][:sh,:sh]))
    print(f"{name:<35} {diff:>28.2e}")
""")
    save(nb, "nb_model_X.ipynb")


# ===========================================================================
# Main
# ===========================================================================

if __name__ == "__main__":
    import os
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    print("Building per-model notebooks …")
    build_model_A()
    build_model_B()
    build_model_B2()
    build_model_C2()
    build_model_X()
    print("Done.")
