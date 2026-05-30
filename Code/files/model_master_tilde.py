"""
Native solver and utilities on state space

    S_tilde = {(0)} U {(n_2, n) : 0 <= n_2 <= n}.

The master model parameters (lam1, lam2, mu, gamma1, gamma2, theta1, theta2)
are inherited from `model_master`. This module:

    * Provides a CTMC solver `solve_exact_tilde(p, n_max)` that builds the
      rate matrix on S_tilde directly (triangular enumeration), so the size
      is (n_max+1)(n_max+2)/2 + 1 instead of the (N+1)^2 + 1 of the S-native
      solver. The two solvers must give numerically identical answers for the
      same physical parameters; we cross-check.

    * Wraps the S-native simulator into a `simulate_tilde(...)` that returns
      pi_tilde directly.

    * Exposes utilities that are natural on S_tilde:
        - P_tilde(y, n, pi_tilde):  the partial PGF
          tilde{P}(y, n) = sum_{n2=0}^{n} pi_tilde(n2, n) y^{n2}
        - marginals_tilde(pi_tilde): marginals of n_2, n, and n_1 = n - n_2
        - convert_S_to_Stilde / convert_Stilde_to_S

Normalization convention (matches the thesis and model_master):
    pi_idle + sum_{(n_2, n)} pi_tilde(n_2, n) = 1
    sum_{(n_2, n)} pi_tilde(n_2, n) = P(busy)
    For models WITHOUT abandonments: pi_idle = 1 - rho.
    For models WITH abandonments:    pi_idle > 1 - rho (server idles more).
"""

from __future__ import annotations

from typing import Optional

import numpy as np
from scipy.sparse import lil_matrix

from model_master import Params, simulate as _simulate_S


# ---------------------------------------------------------------------------
# State indexing on the triangle
# ---------------------------------------------------------------------------

def _triangular_idx(n2: int, n: int) -> int:
    """
    Map (n2, n) with 0 <= n2 <= n to a flat index. The idle state is reserved
    at index 0. Triangular enumeration:

        idx(n2, n) = 1 + n(n+1)/2 + n2.

    Examples (the column header is n, row index is n2):
        n =  0  1  2  3 ...
        n2=0    1  2  4  7
        n2=1       3  5  8
        n2=2          6  9
        n2=3            10
    """
    return 1 + (n * (n + 1)) // 2 + n2


def _n_states_tilde(n_max: int) -> int:
    return 1 + (n_max + 1) * (n_max + 2) // 2


# ---------------------------------------------------------------------------
# Native S_tilde solver
# ---------------------------------------------------------------------------

def solve_exact_tilde(p: Params, n_max: int = 100):
    """
    Build and solve the CTMC on S_tilde with the truncation n <= n_max.
    Transitions out of the box are dropped (the usual lossy truncation).

    Returns
    -------
    dict with
        pi_idle  : float
        pi_tilde : ndarray (n_max+1, n_max+1) where pi_tilde[n2, n] holds
                   probability mass on state (n2, n) when 0 <= n2 <= n,
                   and 0 above the diagonal (n2 > n).
        Q        : sparse rate matrix (debug)
    """
    if not p.is_stable():
        raise ValueError("Configuration is unstable.")

    n_states = _n_states_tilde(n_max)
    Q = lil_matrix((n_states, n_states))

    # Idle -> (0, 0): rate lam1 + lam2
    Q[0, 0] = -(p.lam1 + p.lam2)
    Q[0, _triangular_idx(0, 0)] = p.lam1 + p.lam2

    for n in range(n_max + 1):
        for n2 in range(n + 1):
            i = _triangular_idx(n2, n)
            n1 = n - n2
            out = 0.0

            # class-1 arrival: (n2, n) -> (n2, n+1)
            if n + 1 <= n_max:
                Q[i, _triangular_idx(n2, n + 1)] += p.lam1
                out += p.lam1
            # class-2 arrival: (n2, n) -> (n2+1, n+1)
            if n + 1 <= n_max:
                Q[i, _triangular_idx(n2 + 1, n + 1)] += p.lam2
                out += p.lam2

            # service completion
            if n == 0:
                # queues empty; server goes idle
                Q[i, 0] += p.mu
                out += p.mu
            elif n2 < n:
                # at least one class-1 in queue (n1 >= 1): class-1 enters service
                Q[i, _triangular_idx(n2, n - 1)] += p.mu
                out += p.mu
            else:
                # n2 == n, n1 == 0: only class-2 in queue; class-2 enters service
                Q[i, _triangular_idx(n2 - 1, n - 1)] += p.mu
                out += p.mu

            # class-1 jockeys to class-2: rate gamma1 * n1, n unchanged
            if n1 >= 1 and p.gamma1 > 0.0:
                rate = p.gamma1 * n1
                Q[i, _triangular_idx(n2 + 1, n)] += rate
                out += rate
            # class-2 jockeys to class-1: rate gamma2 * n2, n unchanged
            if n2 >= 1 and p.gamma2 > 0.0:
                rate = p.gamma2 * n2
                Q[i, _triangular_idx(n2 - 1, n)] += rate
                out += rate
            # class-1 abandonment: rate theta1 * n1, n -> n-1, n2 unchanged
            if n1 >= 1 and p.theta1 > 0.0:
                rate = p.theta1 * n1
                Q[i, _triangular_idx(n2, n - 1)] += rate
                out += rate
            # class-2 abandonment: rate theta2 * n2, n -> n-1, n2 -> n2-1
            if n2 >= 1 and p.theta2 > 0.0:
                rate = p.theta2 * n2
                Q[i, _triangular_idx(n2 - 1, n - 1)] += rate
                out += rate

            Q[i, i] = -out

    # Solve pi Q = 0 with sum pi = 1
    A = Q.T.toarray()
    A[-1, :] = 1.0
    b = np.zeros(n_states)
    b[-1] = 1.0
    pi = np.linalg.solve(A, b)

    pi_tilde = np.zeros((n_max + 1, n_max + 1))
    for n in range(n_max + 1):
        for n2 in range(n + 1):
            pi_tilde[n2, n] = pi[_triangular_idx(n2, n)]

    return dict(pi_idle=pi[0], pi_tilde=pi_tilde, Q=Q.tocsr())


# ---------------------------------------------------------------------------
# Simulator wrapper
# ---------------------------------------------------------------------------

def simulate_tilde(p: Params, n_events: int = 10_000_000,
                   burn_in_frac: float = 0.1, max_n: int = 100,
                   seed: Optional[int] = 0):
    """
    Run the S-native simulator and convert the empirical joint to S_tilde
    representation.

    Returns
    -------
    dict with
        pi_idle, pi_tilde (shape (max_n+1, 2*max_n+1)),
        plus the raw counters from `model_master.simulate`.
    """
    out_S = _simulate_S(p, n_events=n_events, burn_in_frac=burn_in_frac,
                       max_n=max_n, seed=seed)
    pi_tilde = convert_S_to_Stilde(out_S["pi_joint"])
    out = dict(out_S)
    out["pi_tilde"] = pi_tilde
    del out["pi_joint"]
    return out


# ---------------------------------------------------------------------------
# Conversion between joint representations
# ---------------------------------------------------------------------------

def convert_S_to_Stilde(pi_joint: np.ndarray) -> np.ndarray:
    """
    pi_joint indexed by [n1, n2] (square, both in [0, M-1]) is repacked into
    pi_tilde indexed by [n2, n] with n = n1 + n2 in [0, 2*(M-1)].
    The output shape is (M, 2*M - 1).
    """
    M = pi_joint.shape[0]
    pi_tilde = np.zeros((M, 2 * M - 1))
    for n1 in range(M):
        for n2 in range(M):
            pi_tilde[n2, n1 + n2] = pi_joint[n1, n2]
    return pi_tilde


def convert_Stilde_to_S(pi_tilde: np.ndarray) -> np.ndarray:
    """
    Inverse: from pi_tilde[n2, n] reconstruct pi_joint[n1, n2] = pi_tilde[n2, n1+n2].
    The output is shape (M_out, M_out) where M_out = min(n_max+1, n2_max+1).
    """
    n2_dim, n_dim = pi_tilde.shape
    M = min(n2_dim, n_dim)
    pi_joint = np.zeros((M, M))
    for n1 in range(M):
        for n2 in range(M):
            n = n1 + n2
            if n < n_dim and n2 < n2_dim:
                pi_joint[n1, n2] = pi_tilde[n2, n]
    return pi_joint


# ---------------------------------------------------------------------------
# Quantities natural on S_tilde
# ---------------------------------------------------------------------------

def P_tilde(y, n: int, pi_tilde: np.ndarray):
    """
    Partial PGF in the class-2 variable, conditioned on total queue length n
    and on the server being busy:

        tilde{P}(y, n) = sum_{n2=0}^{n} pi_tilde(n2, n) * y^{n2}.

    Accepts y as scalar or array; returns matching shape (scalar in -> scalar out).
    """
    y_arr = np.asarray(y, dtype=float)
    out = np.zeros_like(y_arr, dtype=float)
    n2_max = min(n, pi_tilde.shape[0] - 1)
    for n2 in range(n2_max + 1):
        out = out + pi_tilde[n2, n] * y_arr ** n2
    return out.item() if out.ndim == 0 else out


def marginals_tilde(pi_tilde: np.ndarray):
    """
    Marginals on S_tilde:
        pi_n  : ndarray (n_max+1,)        — total queue distribution
        pi_n2 : ndarray (n_max+1,)        — class-2 queue distribution
        pi_n1 : ndarray (n_max+1,)        — class-1 queue distribution = n - n_2

    All three sum to P(busy) = sum(pi_tilde), not to 1.
    """
    n2_dim, n_dim = pi_tilde.shape
    pi_n  = pi_tilde.sum(axis=0)
    pi_n2 = pi_tilde.sum(axis=1)
    pi_n1 = np.zeros(n_dim)  # n1 = n - n2 ranges in [0, n_dim - 1]
    for n in range(n_dim):
        for n2 in range(min(n + 1, n2_dim)):
            pi_n1[n - n2] += pi_tilde[n2, n]
    return dict(pi_n=pi_n, pi_n2=pi_n2, pi_n1=pi_n1)


def diagnostics_tilde(p: Params, pi_idle: float, pi_tilde: np.ndarray):
    """Same bundle as model_master.diagnostics, computed from pi_tilde."""
    m = marginals_tilde(pi_tilde)
    n_dim = pi_tilde.shape[1]
    ns = np.arange(n_dim)
    E_n  = float(np.dot(ns, m["pi_n"]))
    n2_dim = pi_tilde.shape[0]
    E_n2 = float(np.dot(np.arange(n2_dim), m["pi_n2"]))
    E_n1 = E_n - E_n2
    P_busy = 1.0 - pi_idle
    throughput = p.mu * P_busy
    aban = p.theta1 * E_n1 + p.theta2 * E_n2
    return dict(
        E_n1=E_n1, E_n2=E_n2, E_n=E_n,
        P_busy=P_busy, throughput=throughput,
        abandonment_rate=aban,
        offered_load=p.lam1 + p.lam2,
        carried_plus_lost=throughput + aban,
        normalization_check=pi_idle + pi_tilde.sum(),  # must be 1.0
    )


# ---------------------------------------------------------------------------
# Cohen-trick approximation (Model A only) for cross-reference
# ---------------------------------------------------------------------------

def y_star(y, p: Params) -> np.ndarray:
    """The negative-sign root used in the Model A approximation."""
    a = p.lam1 + p.lam2 + p.mu
    disc = a * a - 4.0 * p.mu * (p.lam1 + p.lam2 * np.asarray(y, dtype=float))
    return (a - np.sqrt(disc)) / (2.0 * p.mu)


def P_tilde_approx_modelA(y, n: int, p: Params) -> np.ndarray:
    """
    Approximation from neglecting the non-homogeneous term and applying
    Cohen's trick (Model A only; gamma = theta = 0):

        tilde{P}_approx(y, n) = (1-rho) rho [y_star(y)]^n.

    Note: only valid when p.gamma1 = p.gamma2 = p.theta1 = p.theta2 = 0.
    """
    if (p.gamma1 or p.gamma2 or p.theta1 or p.theta2):
        raise ValueError("The Cohen-trick approximation is for Model A only "
                         "(no jockeying, no abandonments).")
    return (1.0 - p.rho) * p.rho * y_star(y, p) ** n
