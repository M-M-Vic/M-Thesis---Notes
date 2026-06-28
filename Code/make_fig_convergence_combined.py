#!/usr/bin/env python3
"""
make_fig_convergence_combined.py
================================

Standalone generator for the single combined convergence figure used in the
Results section (Subsection "Convergence to the baseline"):

    figures/results/fig_conv_combined.pdf  (+ .png)

It overlays all four specialised models -- B2, C2 and their head-of-line
variants B2^H, C2^H -- on ONE log-log axis of the L1 distance to Model A
against the distinguishing mechanism parameter (gamma1 for the jockeying
pair, theta1 for the abandonment pair), and adds a second panel tracking the
empty-state descriptors pi0 and pi(0,0).

Why two panels:
  (a) L1 distance ||pi - pi_A||_1 vs mechanism parameter, log-log, with
      first-order (slope ~ 1) fitted lines over parameter < 1. All four
      collapse onto Model A at first order.
  (b) pi0 and pi(0,0) vs mechanism parameter. The conserving jockeying models
      B2, B2^H sit IDENTICALLY on the Model-A lines pi0 = 1-rho and
      pi(0,0) = rho(1-rho) for every gamma1 > 0 (jockeying conserves N), so
      their approach is carried entirely by interior redistribution. The
      abandonment models C2, C2^H drift above both lines and relax back only
      as theta1 -> 0, so they approach via BOTH the idle state and interior
      mass.

Exact CTMC ground truth via Code/model_master.solve_exact -- the same solver
used by the validation and exhaustive notebooks. The L1 convention mirrors
build_nb_exhaustive.L1_distance (over the busy joint array pi_joint, idle
excluded) so the fitted slopes coincide with Table tab:conv:rates.

Stability: rho = (lam1+lam2)/mu = 0.70 < 1 (no abandonment for A, B2, B2^H);
the abandonment models C2, C2^H are positive recurrent for every theta1 > 0.

Run:  python3 make_fig_convergence_combined.py
"""
from __future__ import annotations

import os
import numpy as np
import matplotlib.pyplot as plt

from model_master import Params, model_B21, model_C21, solve_exact, mean_queue_lengths

# ----------------------------------------------------------------------------
# Canonical parameters (match the rest of the Results pipeline)
# ----------------------------------------------------------------------------
LAM1, LAM2, MU = 0.30, 0.40, 1.0
RHO = (LAM1 + LAM2) / MU                      # 0.70
PI0_A = 1.0 - RHO                             # 0.30  (Model-A idle prob)
PI00_A = RHO * (1.0 - RHO)                    # 0.21  (Model-A busy-empty prob)
N_MAX = 70                                    # tail 0.7^70 ~ 1e-11 at rho=0.70

# Colours consistent with the per-model figures of build_nb_exhaustive.py
C_B2, C_C2 = "#1f77b4", "#d62728"
C_B2H, C_C2H = "#17a2a2", "#b000b0"

SAVE_DIR = os.path.join(os.path.dirname(__file__), "..", "figures", "results")


def L1_to_A(pi_joint, piA):
    """||pi - pi_A||_1 over the busy joint array (idle excluded), zero-padded.
    Mirrors build_nb_exhaustive.L1_distance so slopes match tab:conv:rates."""
    Ma, Mb = pi_joint.shape[0], piA.shape[0]
    M = max(Ma, Mb)
    A = np.zeros((M, M)); A[:Mb, :Mb] = piA
    B = np.zeros((M, M)); B[:Ma, :Ma] = pi_joint
    return float(np.abs(A - B).sum())


def loglog_slope(x, y, xmax=1.0):
    """Least-squares slope of log10(y) vs log10(x) over the regime x < xmax."""
    x, y = np.asarray(x), np.asarray(y)
    m = (x < xmax) & (y > 0) & np.isfinite(y)
    if m.sum() < 2:
        return np.nan, (np.nan, np.nan)
    s, b = np.polyfit(np.log10(x[m]), np.log10(y[m]), 1)
    return s, (s, b)


def sweep(build, grid, piA):
    """Solve each truncated CTMC on the grid; return (L1, pi0, pi00) arrays."""
    L1, pi0, pi00 = [], [], []
    for v in grid:
        r = solve_exact(build(v), N_max=N_MAX)
        L1.append(L1_to_A(r["pi_joint"], piA))
        pi0.append(r["pi_idle"])
        pi00.append(r["pi_joint"][0, 0])
    return np.array(L1), np.array(pi0), np.array(pi00)


def main():
    grid = np.logspace(-3, 2, 40)          # mechanism parameter, matches pipeline

    # Model-A reference
    rA = solve_exact(Params(LAM1, LAM2, MU), N_max=N_MAX)
    piA = rA["pi_joint"]
    en1A, en2A = mean_queue_lengths(piA)
    assert abs(rA["pi_idle"] - PI0_A) < 1e-3 and abs(piA[0, 0] - PI00_A) < 1e-3
    assert abs((en1A + en2A) - 1.6333) < 1e-3

    # The four specialisations
    L1_B2,  pi0_B2,  pi00_B2  = sweep(lambda g: Params(LAM1, LAM2, MU, gamma1=g), grid, piA)
    L1_B2H, pi0_B2H, pi00_B2H = sweep(lambda g: model_B21(LAM1, LAM2, MU, g),      grid, piA)
    L1_C2,  pi0_C2,  pi00_C2  = sweep(lambda t: Params(LAM1, LAM2, MU, theta1=t),  grid, piA)
    L1_C2H, pi0_C2H, pi00_C2H = sweep(lambda t: model_C21(LAM1, LAM2, MU, t),      grid, piA)

    # ---- validate the canonical (param = 0.5) column against derived_metrics ----
    i05 = int(np.argmin(np.abs(grid - 0.5)))
    checks = {
        "B2  pi0":  (pi0_B2[i05],  0.3000), "B2  pi00":  (pi00_B2[i05],  0.2100),
        "B2H pi0":  (pi0_B2H[i05], 0.3000), "B2H pi00":  (pi00_B2H[i05], 0.2100),
        "C2  pi0":  (pi0_C2[i05],  0.3696), "C2  pi00":  (pi00_C2[i05],  0.2587),
        "C2H pi0":  (pi0_C2H[i05], 0.3636), "C2H pi00":  (pi00_C2H[i05], 0.2545),
    }
    print(f"grid point nearest 0.5: {grid[i05]:.4f}")
    for k, (got, exp) in checks.items():
        flag = "OK" if abs(got - exp) < 2e-3 else "**MISMATCH**"
        print(f"  {k:10s} got {got:.4f}  expect {exp:.4f}  {flag}")

    # ---- fitted log-log slopes (param < 1) ----
    s_B2,  f_B2  = loglog_slope(grid, L1_B2)
    s_B2H, f_B2H = loglog_slope(grid, L1_B2H)
    s_C2,  f_C2  = loglog_slope(grid, L1_C2)
    s_C2H, f_C2H = loglog_slope(grid, L1_C2H)
    print(f"slopes  B2={s_B2:.3f}  B2H={s_B2H:.3f}  C2={s_C2:.3f}  C2H={s_C2H:.3f}")

    # ========================================================================
    # Figure: 2 panels
    # ========================================================================
    fig, ax = plt.subplots(1, 2, figsize=(13.0, 5.0))

    # ---- panel (a): combined L1 convergence, log-log ----
    series = [
        (grid, L1_B2,  s_B2,  f_B2,  C_B2,  "o", r"$B_2$"),
        (grid, L1_B2H, s_B2H, f_B2H, C_B2H, "^", r"$B_2^{\mathrm{H}}$"),
        (grid, L1_C2,  s_C2,  f_C2,  C_C2,  "s", r"$C_2$"),
        (grid, L1_C2H, s_C2H, f_C2H, C_C2H, "v", r"$C_2^{\mathrm{H}}$"),
    ]
    for x, y, s, (ss, bb), col, mk, lab in series:
        m = y > 0
        ax[0].loglog(x[m], y[m], mk, color=col, ms=5, alpha=0.9,
                     label=rf"{lab}  (slope $\approx{s:.2f}$)")
        xs = x[(x < 1) & m]
        ax[0].loglog(xs, 10 ** bb * xs ** ss, "-", color=col, lw=1.2, alpha=0.7)
    ax[0].set_xlabel(r"mechanism parameter $\gamma_1$ (jockeying) or $\theta_1$ (abandonment)")
    ax[0].set_ylabel(r"$\|\pi-\pi_A\|_1$")
    ax[0].set_title(r"(a) First-order $L_1$ convergence to Model $A$")
    ax[0].legend(loc="lower right", fontsize=9, framealpha=0.95)
    ax[0].grid(alpha=0.3, which="both")

    # ---- panel (b): empty-state descriptors pi0, pi(0,0) ----
    ax[1].axhline(PI0_A, color="black", ls="--", lw=1.1,
                  label=rf"$1-\rho={PI0_A:.2f}$  ($B_2,B_2^{{\mathrm{{H}}}}$)")
    ax[1].axhline(PI00_A, color="grey", ls="--", lw=1.1,
                  label=rf"$\rho(1-\rho)={PI00_A:.2f}$  ($B_2,B_2^{{\mathrm{{H}}}}$)")
    ax[1].semilogx(grid, pi0_C2,  "-",  color=C_C2,  lw=2.0, label=r"$\pi_0$:  $C_2$")
    ax[1].semilogx(grid, pi0_C2H, "--", color=C_C2H, lw=2.0, label=r"$\pi_0$:  $C_2^{\mathrm{H}}$")
    ax[1].semilogx(grid, pi00_C2,  "-",  color="#7b1f1f", lw=2.0, label=r"$\pi(0,0)$:  $C_2$")
    ax[1].semilogx(grid, pi00_C2H, "--", color="#5a005a", lw=2.0, label=r"$\pi(0,0)$:  $C_2^{\mathrm{H}}$")
    ax[1].set_xlabel(r"mechanism parameter $\gamma_1$ or $\theta_1$")
    ax[1].set_ylabel("probability")
    ax[1].set_title(r"(b) Empty-state descriptors $\pi_0,\ \pi(0,0)$")
    ax[1].legend(loc="upper left", fontsize=8, framealpha=0.95, ncol=1)
    ax[1].grid(alpha=0.3, which="both")
    ax[1].annotate(r"jockeying conserves $N$:" "\n" r"$\pi_0,\pi(0,0)\equiv$ Model $A$",
                   xy=(1e-2, PI0_A), xytext=(3e-3, 0.40), fontsize=8.5,
                   arrowprops=dict(arrowstyle="->", color="black", lw=0.8))

    fig.suptitle(r"Convergence of the four specialisations to Model $A$ "
                 r"($\lambda_1=0.3,\ \lambda_2=0.4,\ \mu=1,\ \rho=0.70$)", fontsize=12)
    fig.tight_layout(rect=(0, 0, 1, 0.96))

    os.makedirs(SAVE_DIR, exist_ok=True)
    for ext in ("pdf", "png"):
        path = os.path.join(SAVE_DIR, f"fig_conv_combined.{ext}")
        fig.savefig(path, dpi=150, bbox_inches="tight")
        print("saved:", os.path.abspath(path))


if __name__ == "__main__":
    main()
