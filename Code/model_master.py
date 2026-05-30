"""
Master module for the two-class non-preemptive priority queue with optional
jockeying (gamma_i) and abandonments (theta_i).

State space S = {(0)} U {(n_1, n_2) : n_1, n_2 >= 0}, where n_1, n_2 are queue
counts (the customer in service is implicit when the server is busy).

The interior balance equation reads
    [lam1 + lam2 + mu + (gam1+the1) n1 + (gam2+the2) n2] pi(n1, n2)
        = mu pi(n1+1, n2)
        + lam1 pi(n1-1, n2)
        + lam2 pi(n1, n2-1)
        + gam1 (n1+1) pi(n1+1, n2-1)        # class-1 jockeys to class-2
        + gam2 (n2+1) pi(n1-1, n2+1)        # class-2 jockeys to class-1
        + the1 (n1+1) pi(n1+1, n2)          # class-1 abandons
        + the2 (n2+1) pi(n1, n2+1)          # class-2 abandons

Specific variants:
    Model A      : gam1 = gam2 = the1 = the2 = 0
    Model B      : gam1, gam2 >= 0; the1 = the2 = 0
    Model B1     : gam1 = 0
    Model B2     : gam2 = 0
    Abandonments : any combination
    "theta1-only": the1 > 0; gam1 = gam2 = the2 = 0

Conventions:
    rho_i = lam_i / mu  (load per class)
    rho   = (lam1+lam2)/mu

Stability:
    Without abandonments:    rho < 1.
    With theta_i > 0:        always positive recurrent.
"""

from __future__ import annotations

from dataclasses import dataclass, asdict, replace
from typing import Optional

import numpy as np
from scipy.sparse import lil_matrix


# ---------------------------------------------------------------------------
# Parameter container
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class Params:
    lam1: float
    lam2: float
    mu: float
    gamma1: float = 0.0
    gamma2: float = 0.0
    theta1: float = 0.0
    theta2: float = 0.0

    @property
    def rho1(self) -> float:
        return self.lam1 / self.mu

    @property
    def rho2(self) -> float:
        return self.lam2 / self.mu

    @property
    def rho(self) -> float:
        return (self.lam1 + self.lam2) / self.mu

    @property
    def has_abandonments(self) -> bool:
        return (self.theta1 > 0.0) or (self.theta2 > 0.0)

    @property
    def has_jockeying(self) -> bool:
        return (self.gamma1 > 0.0) or (self.gamma2 > 0.0)

    def is_stable(self) -> bool:
        return self.has_abandonments or (self.rho < 1.0)

    def label(self) -> str:
        bits = [f"$\\lambda_1={self.lam1:g}$",
                f"$\\lambda_2={self.lam2:g}$",
                f"$\\mu={self.mu:g}$"]
        if self.gamma1: bits.append(f"$\\gamma_1={self.gamma1:g}$")
        if self.gamma2: bits.append(f"$\\gamma_2={self.gamma2:g}$")
        if self.theta1: bits.append(f"$\\theta_1={self.theta1:g}$")
        if self.theta2: bits.append(f"$\\theta_2={self.theta2:g}$")
        return ", ".join(bits)


# Convenience constructors
def model_A(lam1, lam2, mu):
    return Params(lam1, lam2, mu)

def model_B(lam1, lam2, mu, gamma1, gamma2):
    return Params(lam1, lam2, mu, gamma1=gamma1, gamma2=gamma2)

def model_B1(lam1, lam2, mu, gamma2):
    return Params(lam1, lam2, mu, gamma1=0.0, gamma2=gamma2)

def model_B2(lam1, lam2, mu, gamma1):
    return Params(lam1, lam2, mu, gamma1=gamma1, gamma2=0.0)

def model_theta1_only(lam1, lam2, mu, theta1):
    return Params(lam1, lam2, mu, theta1=theta1)


# ---------------------------------------------------------------------------
# Master simulator (event-driven)
# ---------------------------------------------------------------------------

def simulate(p: Params,
             n_events: int = 10_000_000,
             burn_in_frac: float = 0.1,
             max_n: int = 1000,
             seed: Optional[int] = 0,
             track_abandonments: bool = True):
    """
    Discrete-event simulation of the master model. Returns the empirical
    stationary distribution and a few useful counters.

    Returns
    -------
    out : dict with keys
        pi_idle     : float
        pi_joint    : ndarray (max_n+1, max_n+1), pi(n1, n2) for n1, n2 in [0, max_n]
        T_record    : float, total simulated time spent in the recording phase
        n_arrivals  : (a1, a2) class-1 and class-2 admissions
        n_completed : number of customers fully served
        n_abandoned : (b1, b2) class-1 and class-2 abandonments

    Notes
    -----
    p.is_stable() must be True. When p.rho >= 1 with no abandonments, the queue
    grows without bound and the truncation `max_n` will be hit; in that case
    the routine raises ValueError.
    """
    if not p.is_stable():
        raise ValueError(
            f"Configuration is unstable: rho={p.rho:.3f} >= 1 and "
            "no abandonments are present.")

    rng = np.random.default_rng(seed)

    n1 = n2 = 0
    busy = False
    t = 0.0
    t_record_start: Optional[float] = None
    burn_in_events = int(n_events * burn_in_frac)

    time_idle = 0.0
    time_in_state = np.zeros((max_n + 1, max_n + 1))
    a1 = a2 = b1 = b2 = c = 0  # arrivals (entered queue or service), aban., completed

    for k in range(n_events):
        recording = k >= burn_in_events
        if k == burn_in_events:
            t_record_start = t
            time_idle = 0.0
            time_in_state[:] = 0.0
            a1 = a2 = b1 = b2 = c = 0

        if not busy:
            rate = p.lam1 + p.lam2
            tau = rng.exponential(1.0 / rate)
            if recording:
                time_idle += tau
            t += tau
            # arrival -> goes directly into service
            busy = True
            n1 = n2 = 0
            # class doesn't matter for state dynamics, but count it
            if rng.random() * rate < p.lam1:
                if recording: a1 += 1
            else:
                if recording: a2 += 1
        else:
            # rates at busy non-empty state (or busy empty queue)
            r_lam1 = p.lam1
            r_lam2 = p.lam2
            r_mu   = p.mu
            r_g1   = p.gamma1 * n1
            r_g2   = p.gamma2 * n2
            r_t1   = p.theta1 * n1
            r_t2   = p.theta2 * n2
            rate = r_lam1 + r_lam2 + r_mu + r_g1 + r_g2 + r_t1 + r_t2

            tau = rng.exponential(1.0 / rate)
            if recording and n1 <= max_n and n2 <= max_n:
                time_in_state[n1, n2] += tau
            elif recording:
                # truncation hit; signal an error
                raise RuntimeError(
                    f"Simulation reached n1={n1}, n2={n2} which exceeds "
                    f"max_n={max_n}. Increase max_n or check stability.")
            t += tau

            u = rng.random() * rate
            if u < r_lam1:
                n1 += 1
                if recording: a1 += 1
            elif u < r_lam1 + r_lam2:
                n2 += 1
                if recording: a2 += 1
            elif u < r_lam1 + r_lam2 + r_mu:
                # service completion: next class-1 if any, else class-2, else idle
                if recording: c += 1
                if n1 >= 1:
                    n1 -= 1
                elif n2 >= 1:
                    n2 -= 1
                else:
                    busy = False
            elif u < r_lam1 + r_lam2 + r_mu + r_g1:
                # class-1 jockeys to class-2
                n1 -= 1; n2 += 1
            elif u < r_lam1 + r_lam2 + r_mu + r_g1 + r_g2:
                # class-2 jockeys to class-1
                n2 -= 1; n1 += 1
            elif u < r_lam1 + r_lam2 + r_mu + r_g1 + r_g2 + r_t1:
                # class-1 abandonment
                n1 -= 1
                if recording: b1 += 1
            else:
                # class-2 abandonment
                n2 -= 1
                if recording: b2 += 1

    total = time_idle + time_in_state.sum()
    return dict(
        pi_idle=time_idle / total,
        pi_joint=time_in_state / total,
        T_record=total,
        n_arrivals=(a1, a2),
        n_completed=c,
        n_abandoned=(b1, b2),
    )


# ---------------------------------------------------------------------------
# Exact stationary distribution via truncated CTMC
# ---------------------------------------------------------------------------

def solve_exact(p: Params, N_max: int = 100):
    """
    Build and solve the truncated CTMC on {idle} U {(n1, n2) : 0 <= n1, n2 <= N_max}.

    At the truncation boundary, transitions leading outside the box are simply
    deleted (so probability mass is conserved). This is a "lossy" truncation
    that becomes exact in the limit N_max -> infinity, but for parameter regimes
    where the joint distribution has light tails (e.g. abandonments or low load),
    a modest N_max suffices.

    Returns
    -------
    out : dict
        pi_idle  : float
        pi_joint : ndarray (M, M), pi(n1, n2)
        Q        : sparse matrix (debug)
    """
    if not p.is_stable():
        raise ValueError("Configuration is unstable.")

    M = N_max + 1
    n_states = 1 + M * M

    def idx(n1, n2):
        return 1 + n1 * M + n2

    Q = lil_matrix((n_states, n_states))

    # Idle state: only arrival, lambda_1 + lambda_2 -> state (0, 0)
    Q[0, 0] = -(p.lam1 + p.lam2)
    Q[0, idx(0, 0)] = p.lam1 + p.lam2

    for n1 in range(M):
        for n2 in range(M):
            i = idx(n1, n2)
            out = 0.0

            # class-1 arrival
            if n1 + 1 < M:
                Q[i, idx(n1 + 1, n2)] += p.lam1
                out += p.lam1
            # class-2 arrival
            if n2 + 1 < M:
                Q[i, idx(n1, n2 + 1)] += p.lam2
                out += p.lam2
            # service completion
            if n1 == 0 and n2 == 0:
                Q[i, 0] += p.mu
                out += p.mu
            elif n1 >= 1:
                Q[i, idx(n1 - 1, n2)] += p.mu
                out += p.mu
            else:  # n1 == 0, n2 >= 1
                Q[i, idx(0, n2 - 1)] += p.mu
                out += p.mu
            # class-1 jockeying (n1 -> n1-1, n2 -> n2+1)
            if n1 >= 1 and n2 + 1 < M:
                rate = p.gamma1 * n1
                if rate > 0.0:
                    Q[i, idx(n1 - 1, n2 + 1)] += rate
                    out += rate
            # class-2 jockeying (n2 -> n2-1, n1 -> n1+1)
            if n2 >= 1 and n1 + 1 < M:
                rate = p.gamma2 * n2
                if rate > 0.0:
                    Q[i, idx(n1 + 1, n2 - 1)] += rate
                    out += rate
            # class-1 abandonment (n1 -> n1-1)
            if n1 >= 1:
                rate = p.theta1 * n1
                if rate > 0.0:
                    Q[i, idx(n1 - 1, n2)] += rate
                    out += rate
            # class-2 abandonment (n2 -> n2-1)
            if n2 >= 1:
                rate = p.theta2 * n2
                if rate > 0.0:
                    Q[i, idx(n1, n2 - 1)] += rate
                    out += rate

            Q[i, i] = -out

    # Solve pi Q = 0, sum pi = 1
    A = Q.T.toarray()
    A[-1, :] = 1.0
    b = np.zeros(n_states)
    b[-1] = 1.0
    pi = np.linalg.solve(A, b)

    pi_joint = np.zeros((M, M))
    for n1 in range(M):
        for n2 in range(M):
            pi_joint[n1, n2] = pi[idx(n1, n2)]

    return dict(pi_idle=pi[0], pi_joint=pi_joint, Q=Q.tocsr())


# ---------------------------------------------------------------------------
# Diagnostics from the joint distribution
# ---------------------------------------------------------------------------

def marginals(pi_joint: np.ndarray):
    """Marginals of n1, n2, and n = n1+n2 (queue counts only)."""
    M = pi_joint.shape[0]
    pi_n1 = pi_joint.sum(axis=1)
    pi_n2 = pi_joint.sum(axis=0)
    pi_n = np.zeros(2 * M - 1)
    for n1 in range(M):
        for n2 in range(M):
            pi_n[n1 + n2] += pi_joint[n1, n2]
    return dict(pi_n1=pi_n1, pi_n2=pi_n2, pi_n=pi_n)


def mean_queue_lengths(pi_joint: np.ndarray):
    M = pi_joint.shape[0]
    idx = np.arange(M)
    E_n1 = float(np.sum(pi_joint * idx[:, None]))
    E_n2 = float(np.sum(pi_joint * idx[None, :]))
    return E_n1, E_n2


def diagnostics(p: Params, pi_idle: float, pi_joint: np.ndarray):
    """
    Bundle of summary statistics:
        E[N1], E[N2], E[N]            mean queue lengths (queue, not system)
        P(busy)                        = sum(pi_joint) = 1 - pi_idle
        throughput                     = mu * P(busy)
        abandonment_rate               = theta1 E[N1] + theta2 E[N2]
        offered_load                   = lam1 + lam2
        carried_plus_lost              = throughput + abandonment_rate
                                          (= offered_load in steady state)
        normalization_check            = pi_idle + sum(pi_joint) (must be 1)

    Convention reminder (thesis): pi(n1, n2) is the JOINT probability that
    the server is busy AND the queue lengths are (n1, n2). Therefore
    sum(pi_joint) = P(busy), NOT 1. The full distribution is pi_idle + sum.

    For models WITHOUT abandonments, pi_idle = 1 - rho and sum(pi_joint) = rho.
    For models WITH abandonments, pi_idle > 1 - rho (the server idles more)
    and sum(pi_joint) = throughput / mu < rho.
    """
    E_n1, E_n2 = mean_queue_lengths(pi_joint)
    E_n = E_n1 + E_n2
    P_busy = 1.0 - pi_idle
    throughput = p.mu * P_busy
    aban = p.theta1 * E_n1 + p.theta2 * E_n2
    return dict(
        E_n1=E_n1, E_n2=E_n2, E_n=E_n,
        P_busy=P_busy, throughput=throughput,
        abandonment_rate=aban,
        offered_load=p.lam1 + p.lam2,
        carried_plus_lost=throughput + aban,
        normalization_check=pi_idle + pi_joint.sum(),
    )
