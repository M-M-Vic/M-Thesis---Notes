"""
Generates nb_results.ipynb — comparative performance analysis for the results section.

Sections
--------
0. Setup
1. Cross-model performance table  (A, B₂, C₂ at base parameters)
2. Priority benefit: E[N₁] vs E[N₂] across load ρ
3. Effect of jockeying γ₁ on Model B₂
4. Effect of abandonment θ₁ on Model C₂
5. Cross-model joint distribution heatmaps
6. Cross-model total queue distribution  P(N=n)

Run:
    python3 build_nb_results.py
then execute:
    jupyter nbconvert --to notebook --execute nb_results.ipynb --output nb_results.ipynb
"""

import os
import nbformat as nbf

nb = nbf.v4.new_notebook()
cells = []

# ─────────────────────────────────────────────────────────────────────────────
# §0  Setup
# ─────────────────────────────────────────────────────────────────────────────

cells.append(nbf.v4.new_markdown_cell(
    "# Results — comparative performance analysis\n\n"
    "Base parameters throughout: $\\lambda_1=0.3$, $\\lambda_2=0.4$, $\\mu=1.0$  "
    "($\\rho=0.7$, $\\rho_1=0.3$, $\\rho_2=0.4$).\n\n"
    "Mechanism parameters are varied per section.\n\n"
    "**Notation reminder:** $N_1, N_2, N$ count customers *waiting in the queues*; "
    "the customer in service is implicit."
))

cells.append(nbf.v4.new_code_cell(
    "%matplotlib inline\n"
    "import sys, os\n"
    "import numpy as np\n"
    "import matplotlib.pyplot as plt\n"
    "from matplotlib.colors import LogNorm\n\n"
    "from model_master import Params, solve_exact, diagnostics\n"
    "from model_master_tilde import (\n"
    "    solve_exact_tilde, convert_S_to_Stilde,\n"
    "    marginals_tilde, diagnostics_tilde,\n"
    ")\n\n"
    "plt.rcParams.update({\n"
    '    "font.family": "DejaVu Serif", "mathtext.fontset": "cm",\n'
    '    "axes.titlesize": 11, "axes.labelsize": 10,\n'
    '    "legend.fontsize": 9, "xtick.labelsize": 9, "ytick.labelsize": 9,\n'
    '    "figure.dpi": 110, "savefig.dpi": 140, "savefig.bbox": "tight",\n'
    "})\n\n"
    "LAM1, LAM2, MU = 0.3, 0.4, 1.0\n"
    "RHO = (LAM1 + LAM2) / MU\n\n"
    "# Convenience: exact solve + diagnostics in one call\n"
    "def solve_diag(p, n_max=60):\n"
    "    r = solve_exact_tilde(p, n_max=n_max)\n"
    "    d = diagnostics_tilde(p, r['pi_idle'], r['pi_tilde'])\n"
    "    return r, d\n"
))

# ─────────────────────────────────────────────────────────────────────────────
# §1  Cross-model performance table
# ─────────────────────────────────────────────────────────────────────────────

cells.append(nbf.v4.new_markdown_cell(
    "## 1. Cross-model performance table\n\n"
    "Mechanism parameters: $\\gamma_1=0.5$ (Model B₂), $\\theta_1=0.5$ (Model C₂)."
))

cells.append(nbf.v4.new_code_cell(
    "from scipy.special import hyp1f1\n\n"
    "def E_BC(lam1, mu, theta1):\n"
    "    if theta1 == 0:\n"
    "        return 1.0 / (mu - lam1)\n"
    "    return hyp1f1(1, mu/theta1 + 1, lam1/theta1) / mu\n\n"
    "models = [\n"
    "    ('Model A',  Params(LAM1, LAM2, MU)),\n"
    "    ('Model B₂ (γ₁=0.5)', Params(LAM1, LAM2, MU, gamma1=0.5)),\n"
    "    ('Model C₂ (θ₁=0.5)', Params(LAM1, LAM2, MU, theta1=0.5)),\n"
    "]\n\n"
    "print(f\"{'Model':<22} {'π₀':>8} {'P(busy)':>9} \"\n"
    "      f\"{'E[N₁]':>8} {'E[N₂]':>8} {'E[N]':>8} {'throughput':>12}\")\n"
    "print('─' * 80)\n"
    "for name, p in models:\n"
    "    r, d = solve_diag(p)\n"
    "    print(f\"{name:<22} {r['pi_idle']:>8.4f} {d['P_busy']:>9.4f} \"\n"
    "          f\"{d['E_n1']:>8.4f} {d['E_n2']:>8.4f} {d['E_n']:>8.4f} \"\n"
    "          f\"{d['throughput']:>12.4f}\")\n"
))

# ─────────────────────────────────────────────────────────────────────────────
# §2  Priority benefit across load ρ
# ─────────────────────────────────────────────────────────────────────────────

cells.append(nbf.v4.new_markdown_cell(
    "## 2. Priority benefit: $E[N_1]$ vs $E[N_2]$ across load $\\rho$\n\n"
    "We fix the load split $\\lambda_1 / \\lambda_2 = 3/4$ and vary $\\mu$ "
    "to sweep $\\rho \\in [0.2, 0.92]$. "
    "Class-1 has priority; class-2 bears the congestion cost."
))

cells.append(nbf.v4.new_code_cell(
    "rho_vals = np.linspace(0.20, 0.92, 40)\n"
    "En1_A, En2_A = [], []\n"
    "En1_B2, En2_B2 = [], []\n"
    "En1_C2, En2_C2 = [], []\n\n"
    "for rho in rho_vals:\n"
    "    mu = (LAM1 + LAM2) / rho\n"
    "    pA  = Params(LAM1, LAM2, mu)\n"
    "    pB2 = Params(LAM1, LAM2, mu, gamma1=0.5)\n"
    "    pC2 = Params(LAM1, LAM2, mu, theta1=0.5)\n"
    "    for p, en1_list, en2_list in [\n"
    "        (pA, En1_A, En2_A), (pB2, En1_B2, En2_B2), (pC2, En1_C2, En2_C2)\n"
    "    ]:\n"
    "        r, d = solve_diag(p)\n"
    "        en1_list.append(d['E_n1'])\n"
    "        en2_list.append(d['E_n2'])\n\n"
    "fig, axes = plt.subplots(1, 2, figsize=(13, 4.5))\n"
    "COLORS = {'A': '#1f3a93', 'B2': '#27ae60', 'C2': '#c0392b'}\n\n"
    "for ax, (en1_vals, en2_vals, label, color) in zip(\n"
    "    [axes[0], axes[0], axes[0]],\n"
    "    [(En1_A, None, 'Model A', COLORS['A']),\n"
    "     (En1_B2, None, r'Model B₂ ($\\gamma_1=0.5$)', COLORS['B2']),\n"
    "     (En1_C2, None, r'Model C₂ ($\\theta_1=0.5$)', COLORS['C2'])]\n"
    "):\n"
    "    axes[0].plot(rho_vals, en1_vals, '-', color=color, lw=2, label=label)\n\n"
    "for en2_vals, label, color in [\n"
    "    (En2_A, 'Model A', COLORS['A']),\n"
    "    (En2_B2, r'Model B₂ ($\\gamma_1=0.5$)', COLORS['B2']),\n"
    "    (En2_C2, r'Model C₂ ($\\theta_1=0.5$)', COLORS['C2'])\n"
    "]:\n"
    "    axes[1].plot(rho_vals, en2_vals, '-', color=color, lw=2, label=label)\n\n"
    "axes[0].set_xlabel(r'$\\rho$'); axes[0].set_ylabel(r'$E[N_1]$')\n"
    "axes[0].set_title('Class-1 mean queue (priority class)')\n"
    "axes[0].legend(); axes[0].grid(alpha=0.3)\n\n"
    "axes[1].set_xlabel(r'$\\rho$'); axes[1].set_ylabel(r'$E[N_2]$')\n"
    "axes[1].set_title('Class-2 mean queue (non-priority class)')\n"
    "axes[1].legend(); axes[1].grid(alpha=0.3)\n\n"
    "fig.suptitle(r'Priority benefit: class-1 is shielded; class-2 absorbs congestion', fontsize=11)\n"
    "fig.tight_layout()\n"
))

# ─────────────────────────────────────────────────────────────────────────────
# §3  Effect of jockeying γ₁ — Model B₂
# ─────────────────────────────────────────────────────────────────────────────

cells.append(nbf.v4.new_markdown_cell(
    "## 3. Effect of jockeying $\\gamma_1$ — Model B₂\n\n"
    "Model B₂ has one-way jockeying: class-1 customers may move to the class-2 queue "
    "at per-customer rate $\\gamma_1$. Jockeying is queue-length-preserving ($N$ is unchanged), "
    "so it cannot improve throughput — but it redistributes $N_1$ and $N_2$."
))

cells.append(nbf.v4.new_code_cell(
    "gamma1_vals = np.concatenate([np.linspace(0.0, 0.3, 10), np.linspace(0.3, 5.0, 25)])\n"
    "metrics_B2 = {'pi0': [], 'E_n1': [], 'E_n2': [], 'E_n': [], 'throughput': []}\n\n"
    "for g1 in gamma1_vals:\n"
    "    p = Params(LAM1, LAM2, MU, gamma1=float(g1))\n"
    "    r, d = solve_diag(p)\n"
    "    metrics_B2['pi0'].append(r['pi_idle'])\n"
    "    metrics_B2['E_n1'].append(d['E_n1'])\n"
    "    metrics_B2['E_n2'].append(d['E_n2'])\n"
    "    metrics_B2['E_n'].append(d['E_n'])\n"
    "    metrics_B2['throughput'].append(d['throughput'])\n\n"
    "# Model A reference\n"
    "r_A, d_A = solve_diag(Params(LAM1, LAM2, MU))\n\n"
    "fig, axes = plt.subplots(1, 3, figsize=(14, 4.2))\n\n"
    "ax = axes[0]\n"
    "ax.semilogx(gamma1_vals + 1e-4, metrics_B2['E_n1'], 'o-', color='#1f3a93', ms=3, lw=1.8,\n"
    "            label=r'$E[N_1]$  (B₂)')\n"
    "ax.semilogx(gamma1_vals + 1e-4, metrics_B2['E_n2'], 's-', color='#c0392b', ms=3, lw=1.8,\n"
    "            label=r'$E[N_2]$  (B₂)')\n"
    "ax.axhline(d_A['E_n1'], color='#1f3a93', ls='--', lw=1.3, alpha=0.6,\n"
    "           label=f\"Model A: {d_A['E_n1']:.3f}\")\n"
    "ax.axhline(d_A['E_n2'], color='#c0392b', ls='--', lw=1.3, alpha=0.6,\n"
    "           label=f\"Model A: {d_A['E_n2']:.3f}\")\n"
    "ax.set_xlabel(r'$\\gamma_1$'); ax.set_ylabel('mean queue length')\n"
    "ax.set_title(r'$E[N_1]$ and $E[N_2]$ vs $\\gamma_1$')\n"
    "ax.legend(fontsize=8); ax.grid(alpha=0.3, which='both')\n\n"
    "ax = axes[1]\n"
    "ax.semilogx(gamma1_vals + 1e-4, metrics_B2['E_n'], 'o-', color='#8e44ad', ms=3, lw=1.8)\n"
    "ax.axhline(d_A['E_n'], color='#8e44ad', ls='--', lw=1.3, alpha=0.6,\n"
    "           label=f\"Model A: {d_A['E_n']:.3f}\")\n"
    "ax.set_xlabel(r'$\\gamma_1$'); ax.set_ylabel(r'$E[N]$')\n"
    "ax.set_title(r'Total queue $E[N]$ vs $\\gamma_1$  (N conserved by jockeying)')\n"
    "ax.legend(fontsize=8); ax.grid(alpha=0.3, which='both')\n\n"
    "ax = axes[2]\n"
    "ax.semilogx(gamma1_vals + 1e-4, metrics_B2['pi0'], 'o-', color='#27ae60', ms=3, lw=1.8)\n"
    "ax.axhline(r_A['pi_idle'], color='#27ae60', ls='--', lw=1.3, alpha=0.6,\n"
    "           label=f\"Model A: {r_A['pi_idle']:.3f}\")\n"
    "ax.set_xlabel(r'$\\gamma_1$'); ax.set_ylabel(r'$\\pi_0$')\n"
    "ax.set_title(r'Idle probability $\\pi_0$ vs $\\gamma_1$  (unchanged — jockeying is internal)')\n"
    "ax.legend(fontsize=8); ax.grid(alpha=0.3, which='both')\n\n"
    "fig.suptitle(r'Model B₂: one-way jockeying $1\\to2$ reshuffles queues without changing $N$ or $\\pi_0$',\n"
    "             fontsize=10)\n"
    "fig.tight_layout()\n"
))

# ─────────────────────────────────────────────────────────────────────────────
# §4  Effect of abandonment θ₁ — Model C₂
# ─────────────────────────────────────────────────────────────────────────────

cells.append(nbf.v4.new_markdown_cell(
    "## 4. Effect of abandonment $\\theta_1$ — Model C₂\n\n"
    "Class-1 customers abandon at per-customer rate $\\theta_1$. Unlike jockeying, "
    "abandonment is a true departure: $N$ decreases, throughput drops, and "
    "$\\pi_0$ rises above $1-\\rho$."
))

cells.append(nbf.v4.new_code_cell(
    "theta1_vals = np.concatenate([np.linspace(0.01, 0.3, 12), np.linspace(0.3, 5.0, 25)])\n"
    "metrics_C2 = {'pi0': [], 'E_n1': [], 'E_n2': [], 'E_n': [], 'throughput': [], 'aban_rate': []}\n\n"
    "for th in theta1_vals:\n"
    "    p = Params(LAM1, LAM2, MU, theta1=float(th))\n"
    "    r, d = solve_diag(p)\n"
    "    metrics_C2['pi0'].append(r['pi_idle'])\n"
    "    metrics_C2['E_n1'].append(d['E_n1'])\n"
    "    metrics_C2['E_n2'].append(d['E_n2'])\n"
    "    metrics_C2['E_n'].append(d['E_n'])\n"
    "    metrics_C2['throughput'].append(d['throughput'])\n"
    "    metrics_C2['aban_rate'].append(d['abandonment_rate'])\n\n"
    "fig, axes = plt.subplots(2, 2, figsize=(12, 8))\n\n"
    "specs = [\n"
    "    ('E_n1', r'$E[N_1]$', '#1f3a93', d_A['E_n1'], r'$E[N_1]$ vs $\\theta_1$'),\n"
    "    ('E_n2', r'$E[N_2]$', '#c0392b', d_A['E_n2'], r'$E[N_2]$ vs $\\theta_1$'),\n"
    "    ('throughput', 'throughput', '#27ae60', d_A['throughput'],\n"
    "     r'Throughput vs $\\theta_1$  (decreases as class-1 abandons)'),\n"
    "    ('pi0', r'$\\pi_0$', '#8e44ad', r_A['pi_idle'],\n"
    "     r'$\\pi_0$ vs $\\theta_1$  (rises above $1-\\rho$)'),\n"
    "]\n\n"
    "for ax, (key, ylabel, color, ref_val, title) in zip(axes.flat, specs):\n"
    "    ax.semilogx(theta1_vals, metrics_C2[key], 'o-', color=color, ms=3, lw=1.8)\n"
    "    ax.axhline(ref_val, color=color, ls='--', lw=1.3, alpha=0.55,\n"
    "               label=f'Model A: {ref_val:.4f}')\n"
    "    ax.set_xlabel(r'$\\theta_1$'); ax.set_ylabel(ylabel)\n"
    "    ax.set_title(title); ax.legend(fontsize=8); ax.grid(alpha=0.3, which='both')\n\n"
    "fig.suptitle(r'Model C₂: class-1 abandonment reduces queue lengths and throughput', fontsize=11)\n"
    "fig.tight_layout()\n"
))

# ─────────────────────────────────────────────────────────────────────────────
# §5  Cross-model joint distribution heatmaps
# ─────────────────────────────────────────────────────────────────────────────

cells.append(nbf.v4.new_markdown_cell(
    "## 5. Cross-model joint distributions $\\widetilde{\\pi}(n_2, n)$\n\n"
    "Heatmaps on $\\widetilde{S}$. The white dashed diagonal is $n_2 = n$ "
    "(the constraint boundary, i.e. $n_1 = 0$). "
    "Jockeying pushes mass toward the diagonal; abandonment drains the upper-left "
    "(large $n_1$) toward the diagonal from the right."
))

cells.append(nbf.v4.new_code_cell(
    "NMAX_PLOT = 14\n"
    "configs = [\n"
    "    ('Model A',                    Params(LAM1, LAM2, MU)),\n"
    "    (r'Model B₂  ($\\gamma_1=0.5$)', Params(LAM1, LAM2, MU, gamma1=0.5)),\n"
    "    (r'Model C₂  ($\\theta_1=0.5$)', Params(LAM1, LAM2, MU, theta1=0.5)),\n"
    "    (r'Model C₂  ($\\theta_1=2.0$)', Params(LAM1, LAM2, MU, theta1=2.0)),\n"
    "]\n\n"
    "# common colour scale across all panels\n"
    "pi_maxes = []\n"
    "results_list = []\n"
    "for _, p in configs:\n"
    "    r, _ = solve_diag(p)\n"
    "    results_list.append(r)\n"
    "    pi_maxes.append(r['pi_tilde'][:NMAX_PLOT+1, :NMAX_PLOT+1].max())\n"
    "vmax_shared = max(pi_maxes)\n\n"
    "fig, axes = plt.subplots(1, 4, figsize=(16, 4.2))\n"
    "for ax, (title, _), r in zip(axes, configs, results_list):\n"
    "    grid = r['pi_tilde'][:NMAX_PLOT+1, :NMAX_PLOT+1].copy()\n"
    "    n2i, ni = np.indices(grid.shape)\n"
    "    grid[n2i > ni] = np.nan\n"
    "    grid = np.where(grid > 0, grid, np.nan)\n"
    "    im = ax.imshow(grid, origin='lower', cmap='viridis',\n"
    "                   norm=LogNorm(vmin=1e-6, vmax=vmax_shared))\n"
    "    ax.plot([0, NMAX_PLOT], [0, NMAX_PLOT], 'w--', lw=0.8, alpha=0.6)\n"
    "    ax.set_xlabel(r'$n$'); ax.set_ylabel(r'$n_2$')\n"
    "    ax.set_title(title)\n"
    "    plt.colorbar(im, ax=ax, fraction=0.046)\n\n"
    "fig.suptitle(r'Joint distribution $\\widetilde{\\pi}(n_2,n)$: shared log colour scale',\n"
    "             fontsize=11)\n"
    "fig.tight_layout()\n"
))

# ─────────────────────────────────────────────────────────────────────────────
# §6  Total queue distribution P(N=n)
# ─────────────────────────────────────────────────────────────────────────────

cells.append(nbf.v4.new_markdown_cell(
    "## 6. Total queue distribution $\\mathbb{P}(N=n)$ across models\n\n"
    "$\\mathbb{P}(N=n) = \\sum_{n_2=0}^{n} \\widetilde{\\pi}(n_2, n)$ "
    "for $n \\geq 1$, plus $\\pi_0$ at $n=0$ (idle). "
    "Jockeying leaves this distribution unchanged relative to Model A; "
    "abandonment shifts mass toward small $n$."
))

cells.append(nbf.v4.new_code_cell(
    "NMAX_DIST = 18\n"
    "ns = np.arange(NMAX_DIST + 1)\n\n"
    "model_specs = [\n"
    "    ('Model A',                    Params(LAM1, LAM2, MU),              '#1f3a93'),\n"
    "    (r'B₂ ($\\gamma_1=0.5$)',      Params(LAM1, LAM2, MU, gamma1=0.5), '#27ae60'),\n"
    "    (r'B₂ ($\\gamma_1=2.0$)',      Params(LAM1, LAM2, MU, gamma1=2.0), '#a8e6a3'),\n"
    "    (r'C₂ ($\\theta_1=0.5$)',      Params(LAM1, LAM2, MU, theta1=0.5), '#c0392b'),\n"
    "    (r'C₂ ($\\theta_1=2.0$)',      Params(LAM1, LAM2, MU, theta1=2.0), '#f1948a'),\n"
    "]\n\n"
    "fig, ax = plt.subplots(figsize=(10, 4.5))\n\n"
    "for label, p, color in model_specs:\n"
    "    r, _ = solve_diag(p)\n"
    "    m = marginals_tilde(r['pi_tilde'])\n"
    "    # P(N=n) for n>=1 is the marginal of total-in-queue n; n=0 is pi_idle\n"
    "    pn = np.zeros(NMAX_DIST + 1)\n"
    "    pn[0] = r['pi_idle']\n"
    "    for n in range(1, NMAX_DIST + 1):\n"
    "        if n < len(m['pi_n']):\n"
    "            pn[n] = m['pi_n'][n]\n"
    "    ax.semilogy(ns, pn, 'o-', color=color, ms=4, lw=1.8, label=label)\n\n"
    "ax.set_xlabel(r'$n$ (total in queues)')\n"
    "ax.set_ylabel(r'$\\mathbb{P}(N=n)$  (log scale)')\n"
    "ax.set_title(r'Total queue distribution: jockeying is neutral, abandonment lightens the tail')\n"
    "ax.legend(ncol=2); ax.grid(alpha=0.3, which='both')\n"
    "fig.tight_layout()\n"
))

# ─────────────────────────────────────────────────────────────────────────────
# Assemble and write
# ─────────────────────────────────────────────────────────────────────────────

nb.cells = cells
out_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "nb_results.ipynb")
with open(out_path, "w", encoding="utf-8") as f:
    nbf.write(nb, f)
print(f"Written: {out_path}")
