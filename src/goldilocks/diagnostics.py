"""Diagnostics: exact spectral gap, ESS/step, ESS/sec, split-R-hat.

The referee's toolkit (TunnelVision's contribution). Every experiment reports
ALL of: spectral gap (when enumerable), ESS/step AND ESS/sec, split-R-hat
gating (<= 1.05 or the run does not count), error vs enumerated truth.
"""
from __future__ import annotations

import numpy as np

__all__ = [
    "mh_transition_matrix",
    "naive_metropolis_matrix",
    "spectral_gap",
    "ess",
    "split_rhat",
    "magnetization",
    "total_variation",
    "max_column_tv",
    "stationary_distribution",
    "step_tv_bound_from_defect",
    "step_tv_bound_columns",
]


def mh_transition_matrix(P_prop: np.ndarray, target) -> np.ndarray:
    """Exact MH transition matrix from proposal matrix P_prop[y,x] (n <= ~12).

    A[y,x] = P_prop[y,x] * min(1, pi(y) q(x|y) / (pi(x) q(y|x))), diagonal
    absorbs rejections. Works for asymmetric proposals too.
    """
    pi = target.exact_dist()
    d = len(pi)
    Q = P_prop
    with np.errstate(divide="ignore", invalid="ignore"):
        ratio = (pi[:, None] * Q.T) / np.clip(pi[None, :] * Q, 1e-300, None)
    Aacc = np.minimum(1.0, ratio)
    A = Q * Aacc
    np.fill_diagonal(A, 0.0)
    A[np.diag_indices(d)] = 1.0 - A.sum(axis=0)
    return A


def naive_metropolis_matrix(P_prop: np.ndarray, target) -> np.ndarray:
    """Free-lunch Metropolis kernel: acceptance ignores the q-ratio.

    A[y,x] = P_prop[y,x] * min(1, pi(y)/pi(x)); diagonal absorbs rejections.
    This is what a hardware run does when it treats an asymmetric (T1-damped)
    proposal as if it were symmetric. Stationary is generally not pi.
    """
    pi = np.asarray(target.exact_dist(), dtype=float)
    Q = np.asarray(P_prop, dtype=float)
    if pi.ndim != 1:
        raise ValueError("target.exact_dist() must return a 1-d distribution")
    if Q.ndim != 2 or Q.shape[0] != Q.shape[1] or Q.shape[0] != pi.size:
        raise ValueError("proposal and target dimensions do not match")
    if np.any(pi <= 0.0):
        raise ValueError("target has a non-positive atom; MH ratios undefined")
    ratio = pi[:, None] / pi[None, :]
    Aacc = np.minimum(1.0, ratio)
    A = Q * Aacc
    np.fill_diagonal(A, 0.0)
    d = Q.shape[0]
    A[np.diag_indices(d)] = 1.0 - A.sum(axis=0)
    if np.any(A < -1e-12):
        raise ValueError("naive Metropolis produced a negative transition")
    A = np.clip(A, 0.0, None)
    col = A.sum(axis=0)
    if np.any(np.abs(col - 1.0) > 1e-10):
        raise ValueError("naive Metropolis columns are not stochastic")
    return A


def total_variation(p: np.ndarray, q: np.ndarray) -> float:
    """TV distance (1/2)||p-q||_1 between two arrays of equal shape."""
    p_arr = np.asarray(p, dtype=float)
    q_arr = np.asarray(q, dtype=float)
    if p_arr.shape != q_arr.shape:
        raise ValueError("TV arguments must have the same shape")
    return 0.5 * float(np.abs(p_arr - q_arr).sum())


def max_column_tv(P: np.ndarray, Q: np.ndarray) -> float:
    """max_x TV(P(·|x), Q(·|x)) for column-stochastic kernels."""
    P_arr = np.asarray(P, dtype=float)
    Q_arr = np.asarray(Q, dtype=float)
    if P_arr.shape != Q_arr.shape or P_arr.ndim != 2 or P_arr.shape[0] != P_arr.shape[1]:
        raise ValueError("expected matching square kernels")
    return 0.5 * float(np.abs(P_arr - Q_arr).sum(axis=0).max())


def stationary_distribution(A: np.ndarray) -> np.ndarray:
    """Right eigenvector of eigenvalue 1 for a column-stochastic kernel."""
    A_arr = np.asarray(A, dtype=float)
    if A_arr.ndim != 2 or A_arr.shape[0] != A_arr.shape[1]:
        raise ValueError("expected a square kernel")
    ev, evec = np.linalg.eig(A_arr)
    k = int(np.argmin(np.abs(ev - 1.0)))
    if abs(complex(ev[k]) - 1.0) > 1e-8:
        raise ValueError(f"no eigenvalue near 1 (closest {ev[k]})")
    vec = np.real(evec[:, k])
    if float(vec.sum()) < 0.0:
        vec = -vec
    vec = np.clip(vec, 0.0, None)
    total = float(vec.sum())
    if total <= 0.0:
        raise ValueError("failed to extract a non-negative stationary vector")
    return vec / total


def step_tv_bound_from_defect(epsilon: float, pi: np.ndarray) -> float:
    """Uniform per-step bound: epsilon * (1/pi_min - 1)."""
    if epsilon < 0.0 or not np.isfinite(epsilon):
        raise ValueError("symmetry defect must be a finite non-negative number")
    pi_arr = np.asarray(pi, dtype=float)
    if pi_arr.size == 0 or np.any(pi_arr <= 0.0):
        raise ValueError("target must be a positive distribution")
    return float(epsilon) * (1.0 / float(pi_arr.min()) - 1.0)


def step_tv_bound_columns(Q: np.ndarray, pi: np.ndarray) -> np.ndarray:
    """Tighter per-state bound: sum_y (pi(y)/pi(x)) |Q(y|x) - Q(x|y)|."""
    Q_arr = np.asarray(Q, dtype=float)
    pi_arr = np.asarray(pi, dtype=float)
    if Q_arr.ndim != 2 or Q_arr.shape[0] != Q_arr.shape[1] or Q_arr.shape[0] != pi_arr.size:
        raise ValueError("proposal and target dimensions do not match")
    if np.any(pi_arr <= 0.0):
        raise ValueError("target must be a positive distribution")
    defect = np.abs(Q_arr - Q_arr.T)
    weights = pi_arr[:, None] / pi_arr[None, :]
    return (weights * defect).sum(axis=0)


def spectral_gap(A: np.ndarray) -> float:
    """delta = 1 - |lambda_2| of the transition matrix (columns sum to 1)."""
    ev = np.linalg.eigvals(A)
    ev = np.sort(np.abs(ev))[::-1]
    return float(1.0 - ev[1])


def ess(x: np.ndarray, max_lag: int | None = None) -> float:
    """Effective sample size via initial-positive-sequence autocorrelation sum."""
    x = np.asarray(x, dtype=float)
    m = len(x)
    x = x - x.mean()
    var = float(x @ x) / m
    if var == 0:
        return float(m)
    max_lag = max_lag or m // 3
    # FFT autocovariance
    f = np.fft.rfft(x, n=2 * m)
    acov = np.fft.irfft(f * np.conj(f))[:max_lag] / m
    rho = acov / var
    s, k = 0.0, 1
    while k + 1 < max_lag:
        pair = rho[k] + rho[k + 1]
        if pair < 0:
            break
        s += pair
        k += 2
    return float(m / (1.0 + 2.0 * s))


def split_rhat(chains: np.ndarray) -> float:
    """Split-R-hat over chains array (n_chains, n_steps). Gate: <= 1.05."""
    c = np.asarray(chains, dtype=float)
    n_c, n_s = c.shape
    half = n_s // 2
    sp = np.concatenate([c[:, :half], c[:, half : 2 * half]], axis=0)
    m, n = sp.shape
    means = sp.mean(axis=1)
    B = n * means.var(ddof=1)
    W = sp.var(axis=1, ddof=1).mean()
    if W == 0:
        return 1.0
    return float(np.sqrt(((n - 1) / n * W + B / n) / W))


def magnetization(states: np.ndarray, n: int) -> np.ndarray:
    """Scalar chain statistic for ESS/R-hat: total magnetization per state."""
    bits = (states[:, None] >> np.arange(n - 1, -1, -1)[None, :]) & 1
    return (1.0 - 2.0 * bits).sum(axis=1)
