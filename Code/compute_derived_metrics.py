"""
Derived metrics for the Results prose (task D1).

Computes, at the canonical parameters (lambda1=0.3, lambda2=0.4, mu=1, mechanism
parameter 0.5) and across the rho-sweep grid of Table 6 (rho in {0.50,0.70,0.90},
class split lambda1:lambda2 = 3:4):

  1. Class-1 loss fraction for C2 (full-rate) and the head-of-line C-variant CH,
     taken DIRECTLY from the CTMC as (class-1 abandonment flow)/lambda1.
       full-rate : theta1 * E[N1] / lambda1
       head-line : theta1 * P(N1>=1) / lambda1
  2. Conditional mean time-to-service of SERVED class-1 customers (Model-A baseline,
     C2, B2) via a per-customer tagged simulation, contrasted with the count-based
     unconditional E[W1] = E[N1]/lambda1.
  3. Maximiser alpha* of the priority ratio E[W1]/E[W2] over the class-split sweep
     of Figure 12 (rho=0.70), for each of the five models.
  4. B2-vs-head-of-line E[N1] gap at the three loads.
  5. P(N1>=2) for each model at the three loads.

Exports results/derived_metrics.json and results/derived_metrics.tex (\\newcommand
macros).  A conservation check carried+lost == offered is recorded for C2 at every
grid point.

The CTMC quantities are exact (sparse stationary solve of the truncated generator);
the conditional latency is the only simulation-based quantity (seeded, deterministic).
"""

from __future__ import annotations
import json, os
import numpy as np
from scipy.sparse import lil_matrix
from scipy.sparse.linalg import spsolve

import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from model_master import (Params, model_A, model_B2, model_C21, model_B21,
                          model_theta1_only, mean_queue_lengths, diagnostics)

MU = 1.0
MECH = 0.5                      # canonical mechanism parameter (gamma1 or theta1)
RHOS = [0.50, 0.70, 0.90]
SPLIT = (3, 4)                  # lambda1:lambda2, as in Table 6


def split_lams(rho, split=SPLIT):
    a, b = split
    return rho * a / (a + b), rho * b / (a + b)


# ---------------------------------------------------------------------------
# Sparse stationary solver (mirrors model_master.solve_exact but solves sparsely,
# so larger N_max is affordable for the heavier-tailed rho=0.9 no-abandonment cases)
# ---------------------------------------------------------------------------
def solve_stationary(p: Params, N_max: int):
    M = N_max + 1
    n = 1 + M * M

    def idx(n1, n2):
        return 1 + n1 * M + n2

    Q = lil_matrix((n, n))
    Q[0, 0] = -(p.lam1 + p.lam2)
    Q[0, idx(0, 0)] = p.lam1 + p.lam2
    for n1 in range(M):
        for n2 in range(M):
            i = idx(n1, n2); out = 0.0
            if n1 + 1 < M:
                Q[i, idx(n1 + 1, n2)] += p.lam1; out += p.lam1
            if n2 + 1 < M:
                Q[i, idx(n1, n2 + 1)] += p.lam2; out += p.lam2
            if n1 == 0 and n2 == 0:
                Q[i, 0] += p.mu; out += p.mu
            elif n1 >= 1:
                Q[i, idx(n1 - 1, n2)] += p.mu; out += p.mu
            else:
                Q[i, idx(0, n2 - 1)] += p.mu; out += p.mu
            if n1 >= 1 and n2 + 1 < M:
                r = p.gamma1 if p.hol1 else p.gamma1 * n1
                if r > 0.0:
                    Q[i, idx(n1 - 1, n2 + 1)] += r; out += r
            if n2 >= 1 and n1 + 1 < M:
                r = p.gamma2 * n2
                if r > 0.0:
                    Q[i, idx(n1 + 1, n2 - 1)] += r; out += r
            if n1 >= 1:
                r = p.theta1 if p.hol1 else p.theta1 * n1
                if r > 0.0:
                    Q[i, idx(n1 - 1, n2)] += r; out += r
            if n2 >= 1:
                r = p.theta2 * n2
                if r > 0.0:
                    Q[i, idx(n1, n2 - 1)] += r; out += r
            Q[i, i] = -out

    A = (Q.T).tolil()
    A[-1, :] = 1.0                      # normalisation row
    A = A.tocsr()
    b = np.zeros(n); b[-1] = 1.0
    pi = spsolve(A, b)
    pij = np.zeros((M, M))
    for n1 in range(M):
        for n2 in range(M):
            pij[n1, n2] = pi[idx(n1, n2)]
    tail = pij[-1, :].sum() + pij[:, -1].sum()      # mass on the truncation edge
    return dict(pi_idle=float(pi[0]), pi_joint=pij, edge_mass=float(tail))


def Nmax_for(rho, has_aband):
    if has_aband:
        return 90
    return 60 if rho <= 0.7 else 150


def ctmc_metrics(p: Params, rho):
    res = solve_stationary(p, Nmax_for(rho, p.has_abandonments))
    d = diagnostics(p, res["pi_idle"], res["pi_joint"])
    pij = res["pi_joint"]
    P_N1_ge1 = float(pij[1:, :].sum())
    P_N1_ge2 = float(pij[2:, :].sum())
    pi00 = float(pij[0, 0])             # server busy, both queues empty (!= pi_idle)
    E_W1 = d["E_n1"] / p.lam1
    E_W2 = d["E_n2"] / p.lam2
    return dict(E_n1=d["E_n1"], E_n2=d["E_n2"], E_n=d["E_n"],
                E_W1=E_W1, E_W2=E_W2, ratio_W=E_W1 / E_W2,
                pi_idle=res["pi_idle"], pi00=pi00, P_busy=d["P_busy"],
                P_N1_ge1=P_N1_ge1, P_N1_ge2=P_N1_ge2,
                aband_rate=d["abandonment_rate"], throughput=d["throughput"],
                offered=d["offered_load"], carried_plus_lost=d["carried_plus_lost"],
                edge_mass=res["edge_mass"])


# ---------------------------------------------------------------------------
# (2) Per-customer tagged simulation: conditional mean time-to-service of
#     SERVED class-1 customers.  A waiting class-1 customer leaves queue 1 by
#     (a) entering service [SERVED -> record wait], (b) abandoning, or
#     (c) jockeying to class 2.  In-service customers never abandon, so
#     "enters service" == "is served".
# ---------------------------------------------------------------------------
def sim_class1_latency(p: Params, n_events=5_000_000, seed=12345, burn_in_frac=0.1):
    rng = np.random.default_rng(seed)
    busy = False
    t = 0.0
    q1: list[float] = []          # arrival times of WAITING class-1 (FIFO)
    n2 = 0
    burn = int(n_events * burn_in_frac)
    sw_sum = 0.0; n_served = 0; n_aband = 0; n_jock = 0; n_arr1 = 0

    for k in range(n_events):
        rec = k >= burn
        if k == burn:
            sw_sum = 0.0; n_served = n_aband = n_jock = n_arr1 = 0
        if not busy:
            rate = p.lam1 + p.lam2
            t += rng.exponential(1.0 / rate)
            if rng.random() * rate < p.lam1:        # class-1 arrival -> straight to service
                if rec:
                    n_arr1 += 1; n_served += 1      # wait = 0
            busy = True                              # queues remain empty
        else:
            n1 = len(q1)
            r_lam1 = p.lam1; r_lam2 = p.lam2; r_mu = p.mu
            r_g1 = (p.gamma1 if n1 >= 1 else 0.0) if p.hol1 else p.gamma1 * n1
            r_g2 = p.gamma2 * n2
            r_t1 = (p.theta1 if n1 >= 1 else 0.0) if p.hol1 else p.theta1 * n1
            r_t2 = p.theta2 * n2
            rate = r_lam1 + r_lam2 + r_mu + r_g1 + r_g2 + r_t1 + r_t2
            t += rng.exponential(1.0 / rate)
            u = rng.random() * rate
            if u < r_lam1:
                q1.append(t)
                if rec:
                    n_arr1 += 1
            elif u < r_lam1 + r_lam2:
                n2 += 1
            elif u < r_lam1 + r_lam2 + r_mu:
                if q1:
                    at = q1.pop(0)                   # head enters service == served
                    if rec:
                        n_served += 1; sw_sum += (t - at)
                elif n2 >= 1:
                    n2 -= 1
                else:
                    busy = False
            elif u < r_lam1 + r_lam2 + r_mu + r_g1:
                j = 0 if p.hol1 else int(rng.integers(len(q1)))
                q1.pop(j); n2 += 1                   # class-1 jockeys to class 2
                if rec:
                    n_jock += 1
            elif u < r_lam1 + r_lam2 + r_mu + r_g1 + r_g2:
                n2 -= 1; q1.append(t)                # class-2 jockeys to 1 (gamma2; dead for our models)
            elif u < r_lam1 + r_lam2 + r_mu + r_g1 + r_g2 + r_t1:
                j = 0 if p.hol1 else int(rng.integers(len(q1)))
                q1.pop(j)                            # class-1 abandons
                if rec:
                    n_aband += 1
            else:
                n2 -= 1                              # class-2 abandons

    cond = sw_sum / n_served if n_served else float("nan")
    return dict(cond_time_to_service=float(cond),
                frac_served=n_served / n_arr1 if n_arr1 else float("nan"),
                n_served=int(n_served), n_aband=int(n_aband),
                n_jock=int(n_jock), n_arr1=int(n_arr1))


# ---------------------------------------------------------------------------
# Model registry
# ---------------------------------------------------------------------------
def models_at(rho):
    l1, l2 = split_lams(rho)
    return {
        "A":  model_A(l1, l2, MU),
        "B2": model_B2(l1, l2, MU, MECH),
        "C2": model_theta1_only(l1, l2, MU, MECH),
        "BH": model_B21(l1, l2, MU, MECH),
        "CH": model_C21(l1, l2, MU, MECH),
    }


def main():
    out = {"params": {"mu": MU, "mech": MECH, "split": list(SPLIT), "rhos": RHOS},
           "ctmc": {}, "conditional_latency": {}, "alpha_star": {},
           "EN1_gap_B2_vs_BH": {}, "P_N1_ge2": {}, "conservation_C2": {},
           "loss_fraction_system": {}, "loss_theta_sweep": {}}

    # ---- (1,4,5) CTMC metrics across the rho grid ----
    for rho in RHOS:
        out["ctmc"][f"{rho}"] = {}
        out["P_N1_ge2"][f"{rho}"] = {}
        for name, p in models_at(rho).items():
            m = ctmc_metrics(p, rho)
            out["ctmc"][f"{rho}"][name] = m
            out["P_N1_ge2"][f"{rho}"][name] = m["P_N1_ge2"]
        # loss fractions (abandonment flow / lambda1), C2 and CH
        l1, _ = split_lams(rho)
        for nm in ("C2", "CH"):
            mm = out["ctmc"][f"{rho}"][nm]
            mm["loss_fraction_class1"] = mm["aband_rate"] / l1
        # B2 vs head-of-line E[N1] gap
        en1_b2 = out["ctmc"][f"{rho}"]["B2"]["E_n1"]
        en1_bh = out["ctmc"][f"{rho}"]["BH"]["E_n1"]
        out["EN1_gap_B2_vs_BH"][f"{rho}"] = {"B2": en1_b2, "BH": en1_bh,
                                             "gap_BH_minus_B2": en1_bh - en1_b2}
        # conservation for C2
        c2 = out["ctmc"][f"{rho}"]["C2"]
        out["conservation_C2"][f"{rho}"] = {
            "offered": c2["offered"], "carried_plus_lost": c2["carried_plus_lost"],
            "abs_err": abs(c2["offered"] - c2["carried_plus_lost"]),
            "ok": abs(c2["offered"] - c2["carried_plus_lost"]) < 1e-6}
        # system-wide loss fraction L = (pi_idle - (1-rho))/rho = L1 * rho1/rho,
        # cf. eq:comp:lossfrac, for C2 and CH
        out["loss_fraction_system"][f"{rho}"] = {}
        for nm in ("C2", "CH"):
            pi0 = out["ctmc"][f"{rho}"][nm]["pi_idle"]
            out["loss_fraction_system"][f"{rho}"][nm] = (pi0 - (1 - rho)) / rho

    # off-grid theta1 sweep (Figure~\ref{fig:c2:abandonment}) at the canonical
    # rho=0.70 split: class-1 loss fraction L1 for the full-rate C2 model
    l1_canon, l2_canon = split_lams(0.70)
    for theta1, key in ((0.05, "0.05"), (5.0, "5.0")):
        p = model_theta1_only(l1_canon, l2_canon, MU, theta1)
        m = ctmc_metrics(p, 0.70)
        out["loss_theta_sweep"][key] = m["aband_rate"] / l1_canon

    # ---- (2) conditional latency at canonical rho=0.70 ----
    canon = models_at(0.70)
    for nm in ("A", "B2", "C2", "CH"):
        sim = sim_class1_latency(canon[nm], n_events=6_000_000, seed=20240611)
        uncond = out["ctmc"]["0.7"][nm]["E_W1"]
        sim["uncond_E_W1"] = uncond
        out["conditional_latency"][nm] = sim

    # ---- (3) alpha* of E[W1]/E[W2] over the class split at rho=0.70 ----
    rho = 0.70
    alphas = np.round(np.linspace(0.10, 0.90, 17), 4)
    for nm in ("A", "B2", "C2", "BH", "CH"):
        ratios = []
        for a in alphas:
            l1 = a * rho; l2 = (1 - a) * rho
            if nm == "A":      p = model_A(l1, l2, MU)
            elif nm == "B2":   p = model_B2(l1, l2, MU, MECH)
            elif nm == "C2":   p = model_theta1_only(l1, l2, MU, MECH)
            elif nm == "BH":   p = model_B21(l1, l2, MU, MECH)
            else:              p = model_C21(l1, l2, MU, MECH)
            r = solve_stationary(p, 70)
            d = diagnostics(p, r["pi_idle"], r["pi_joint"])
            ratios.append((d["E_n1"] / l1) / (d["E_n2"] / l2))
        ratios = np.array(ratios)
        imax = int(np.argmax(ratios))
        spread = float(ratios.max() - ratios.min())
        out["alpha_star"][nm] = {
            "alpha_star": float(alphas[imax]),
            "ratio_at_star": float(ratios[imax]),
            "ratio_min": float(ratios.min()), "ratio_max": float(ratios.max()),
            "is_interior": bool(0 < imax < len(alphas) - 1),
            "near_invariant": bool(spread < 1e-3),
            "monotone": bool(np.all(np.diff(ratios) <= 1e-9) or np.all(np.diff(ratios) >= -1e-9)),
        }

    os.makedirs(os.path.join(os.path.dirname(__file__), "..", "results"), exist_ok=True)
    rpath = os.path.join(os.path.dirname(__file__), "..", "results", "derived_metrics.json")
    with open(rpath, "w") as f:
        json.dump(out, f, indent=2)
    print("wrote", os.path.abspath(rpath))

    write_macros(out)
    print_sanity(out)
    return out


# ---------------------------------------------------------------------------
# LaTeX macro file
# ---------------------------------------------------------------------------
RHO_WORD = {"0.5": "Fifty", "0.7": "Seventy", "0.9": "Ninety"}


def write_macros(out):
    L = []
    L.append("% Auto-generated by Code/compute_derived_metrics.py -- DO NOT EDIT BY HAND.")
    L.append("% Derived metrics for the Results/Comparison prose. \\input this file.")
    L.append("")

    def cmd(name, val):
        L.append(rf"\newcommand{{\{name}}}{{{val}}}")

    # (1) loss fractions (3 d.p.) for C2 and CH at each load
    for rho in ["0.5", "0.7", "0.9"]:
        w = RHO_WORD[rho]
        cmd(f"lossCtwo{w}", f"{out['ctmc'][rho]['C2']['loss_fraction_class1']:.3f}")
        cmd(f"lossCH{w}",   f"{out['ctmc'][rho]['CH']['loss_fraction_class1']:.3f}")
    # canonical aliases
    cmd("lossCtwoCanon", f"{out['ctmc']['0.7']['C2']['loss_fraction_class1']:.3f}")
    cmd("lossCHCanon",   f"{out['ctmc']['0.7']['CH']['loss_fraction_class1']:.3f}")
    L.append("")

    # (1b) system-wide loss fraction L = (pi0-(1-rho))/rho = L1*rho1/rho (3 d.p.)
    for rho in ["0.5", "0.7", "0.9"]:
        w = RHO_WORD[rho]
        cmd(f"lossSysCtwo{w}", f"{out['loss_fraction_system'][rho]['C2']:.3f}")
        cmd(f"lossSysCH{w}",   f"{out['loss_fraction_system'][rho]['CH']:.3f}")
    cmd("lossSysCtwoCanon", f"{out['loss_fraction_system']['0.7']['C2']:.3f}")
    L.append("")

    # (1c) off-grid theta1 sweep: class-1 loss fraction L1 for full-rate C2 at
    # rho=0.70, theta1 in {0.05, 5.0} (Figure~\ref{fig:c2:abandonment})
    cmd("lossCtwoThetaLow",  f"{out['loss_theta_sweep']['0.05']:.3f}")
    cmd("lossCtwoThetaHigh", f"{out['loss_theta_sweep']['5.0']:.3f}")
    L.append("")

    # (2) conditional vs unconditional class-1 latency at canonical rho=0.70
    for nm, mac in (("A", "A"), ("B2", "Btwo"), ("C2", "Ctwo"), ("CH", "CH")):
        cl = out["conditional_latency"][nm]
        cmd(f"condWone{mac}", f"{cl['cond_time_to_service']:.4f}")
        cmd(f"uncondWone{mac}", f"{cl['uncond_E_W1']:.4f}")
        cmd(f"fracServed{mac}", f"{cl['frac_served']:.3f}")
    L.append("")

    # (3) alpha* of the priority ratio (2 d.p.) per model
    for nm, mac in (("A", "A"), ("B2", "Btwo"), ("C2", "Ctwo"), ("BH", "BH"), ("CH", "CH")):
        a = out["alpha_star"][nm]
        cmd(f"alphaStar{mac}", f"{a['alpha_star']:.2f}")
        cmd(f"ratioPeak{mac}", f"{a['ratio_at_star']:.3f}")
    L.append("")

    # (4) B2 vs head-of-line E[N1] gap (4 d.p.) per load
    for rho in ["0.5", "0.7", "0.9"]:
        w = RHO_WORD[rho]
        g = out["EN1_gap_B2_vs_BH"][rho]
        cmd(f"ENoneBtwo{w}", f"{g['B2']:.4f}")
        cmd(f"ENoneBH{w}",   f"{g['BH']:.4f}")
        cmd(f"gapENone{w}",  f"{g['gap_BH_minus_B2']:.4f}")
    L.append("")

    # (5) P(N1>=2) (4 d.p.) per model per load
    for rho in ["0.5", "0.7", "0.9"]:
        w = RHO_WORD[rho]
        for nm, mac in (("A", "A"), ("B2", "Btwo"), ("C2", "Ctwo"), ("BH", "BH"), ("CH", "CH")):
            cmd(f"PNGetwo{mac}{w}", f"{out['P_N1_ge2'][rho][nm]:.4f}")
    L.append("")

    # (6) priority premium E[W2]/E[W1] (2 d.p.) for A/B2/C2 at rho=0.70 and 0.90
    for rho in ["0.7", "0.9"]:
        w = RHO_WORD[rho]
        for nm, mac in (("A", "A"), ("B2", "Btwo"), ("C2", "Ctwo")):
            c = out["ctmc"][rho][nm]
            cmd(f"premium{mac}{w}", f"{c['E_W2'] / c['E_W1']:.2f}")
    L.append("")

    # (7) throughput (all five models), abandonment flow (C2, CH) and offered load, at the
    #     three loads -- for the loss-accounting companion table (tab:comp:loss_acct) and the
    #     throughput-deficit validation. C2/CH have light tails so these are exact to 4 d.p.;
    #     the conserving models A/B2/BH carry zero abandonment by construction.
    for rho in ["0.5", "0.7", "0.9"]:
        w = RHO_WORD[rho]
        cmd(f"offered{w}", f"{out['ctmc'][rho]['A']['offered']:.2f}")
        for nm, mac in (("A", "A"), ("B2", "Btwo"), ("BH", "BH"), ("C2", "Ctwo"), ("CH", "CH")):
            cmd(f"throughput{mac}{w}", f"{out['ctmc'][rho][nm]['throughput']:.4f}")
        for nm, mac in (("C2", "Ctwo"), ("CH", "CH")):
            cmd(f"lostflow{mac}{w}", f"{out['ctmc'][rho][nm]['aband_rate']:.4f}")
    L.append("")

    # (8) full per-model per-load descriptor grid (macro-ises the inline CTMC readouts
    #     quoted in chapters/12_comparison.tex and chapters/15_appendix_numerics.tex; D7).
    #     pi0 (idle), pi00 (busy-empty, != pi0), E[N], E[N2], E[W1], E[W2] for all five
    #     models at the three reference loads. E[N1] is emitted in block (4) for B2/BH, so
    #     only A/C2/CH are added here to complete that family without redefining a macro.
    MODELMAC = (("A", "A"), ("B2", "Btwo"), ("C2", "Ctwo"), ("BH", "BH"), ("CH", "CH"))
    for rho in ["0.5", "0.7", "0.9"]:
        w = RHO_WORD[rho]
        for nm, mac in MODELMAC:
            c = out["ctmc"][rho][nm]
            cmd(f"piZero{mac}{w}", f"{c['pi_idle']:.4f}")
            cmd(f"piZZ{mac}{w}",   f"{c['pi00']:.4f}")
            cmd(f"EN{mac}{w}",     f"{c['E_n']:.4f}")
            cmd(f"ENtwo{mac}{w}",  f"{c['E_n2']:.4f}")
            cmd(f"EWone{mac}{w}",  f"{c['E_W1']:.4f}")
            cmd(f"EWtwo{mac}{w}",  f"{c['E_W2']:.4f}")
        for nm, mac in (("A", "A"), ("C2", "Ctwo"), ("CH", "CH")):
            cmd(f"ENone{mac}{w}", f"{out['ctmc'][rho][nm]['E_n1']:.4f}")
    L.append("")

    # (9) priority premium E[W2]/E[W1] for the head-of-line models (block 6 covers A/B2/C2)
    for rho in ["0.7", "0.9"]:
        w = RHO_WORD[rho]
        for nm, mac in (("BH", "BH"), ("CH", "CH")):
            c = out["ctmc"][rho][nm]
            cmd(f"premium{mac}{w}", f"{c['E_W2'] / c['E_W1']:.2f}")
    L.append("")

    # (10) derived percentage changes quoted in the comparison/appendix prose (1 d.p.):
    #      class-2 wait inflation under B2, and class-1 queue reduction under B2 / BH, at rho=0.70
    c7 = out["ctmc"]["0.7"]
    cmd("EWtwoBtwoInflationSeventy",
        f"{100.0 * (c7['B2']['E_W2'] - c7['A']['E_W2']) / c7['A']['E_W2']:.1f}")
    cmd("ENoneBtwoReductionSeventy",
        f"{100.0 * (c7['A']['E_n1'] - c7['B2']['E_n1']) / c7['A']['E_n1']:.1f}")
    cmd("ENoneBHReductionSeventy",
        f"{100.0 * (c7['A']['E_n1'] - c7['BH']['E_n1']) / c7['A']['E_n1']:.1f}")

    path = os.path.join(os.path.dirname(__file__), "..", "results", "derived_metrics.tex")
    with open(path, "w") as f:
        f.write("\n".join(L) + "\n")
    print("wrote", os.path.abspath(path), f"({sum(1 for x in L if x.startswith(chr(92)+'newcommand'))} macros)")


def print_sanity(out):
    print("\n=== SANITY CHECKS ===")
    print(f"loss C2 @rho=0.70 : {out['ctmc']['0.7']['C2']['loss_fraction_class1']:.4f}  "
          f"(expected ~0.232)")
    print(f"E[N1] C2 @rho=0.70: {out['ctmc']['0.7']['C2']['E_n1']:.4f}  (expected ~0.1392)")
    print(f"E[W1] C2 @rho=0.70: {out['ctmc']['0.7']['C2']['E_W1']:.4f}  (expected ~0.4639)")
    print("conditional vs unconditional E[W1] @rho=0.70:")
    for nm in ("A", "B2", "C2", "CH"):
        cl = out["conditional_latency"][nm]
        print(f"  {nm:3s}: cond={cl['cond_time_to_service']:.4f}  "
              f"uncond E[W1]={cl['uncond_E_W1']:.4f}  frac_served={cl['frac_served']:.3f}")
    print("alpha* (argmax of E[W1]/E[W2]) per model:")
    for nm in ("A", "B2", "C2", "BH", "CH"):
        a = out["alpha_star"][nm]
        print(f"  {nm:3s}: alpha*={a['alpha_star']:.2f} interior={a['is_interior']} "
              f"monotone={a['monotone']} invariant={a['near_invariant']} "
              f"ratio[min,max]=[{a['ratio_min']:.3f},{a['ratio_max']:.3f}]")
    print("conservation (C2) carried+lost == offered:")
    for rho in ["0.5", "0.7", "0.9"]:
        c = out["conservation_C2"][rho]
        print(f"  rho={rho}: offered={c['offered']:.4f} carried+lost={c['carried_plus_lost']:.4f} "
              f"abs_err={c['abs_err']:.2e} ok={c['ok']}")
    print("edge mass (truncation) max over CTMC solves:")
    em = max(out["ctmc"][r][nm]["edge_mass"] for r in out["ctmc"] for nm in out["ctmc"][r])
    print(f"  max edge_mass = {em:.2e} (small => truncation adequate)")


if __name__ == "__main__":
    main()
