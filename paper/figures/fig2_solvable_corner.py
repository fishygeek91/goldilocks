"""Fig 2 — solvable corner: telegraph f_gamma(t) and window-averaged gap.

Regenerates data from the formula in docs/monotonicity.md §5 (mixer units,
window t in [0, 20]). Lindblad-verifies the gap at n=2 before saving.

Usage: gvenv/bin/python paper/figures/fig2_solvable_corner.py
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
from numpy.typing import NDArray

_HERE = Path(__file__).resolve().parent
if str(_HERE) not in sys.path:
    sys.path.insert(0, str(_HERE))

from _style import (  # noqa: E402
    OKABE_ITO,
    apply_style,
    close_enough,
    savefig_pair,
    verify_or_die,
)

OUT_STEM = _HERE / "fig2_solvable_corner"
T_MAX = 20.0
# Dense quadrature for formula-side averages (ODE time, mixer units).
N_QUAD = 4001
# Lindblad window average at n=2 (16 x 16 Liouvillian; cheap).
N_LINDBLAD_T = 401

# docs/monotonicity.md §5 measured values (n=2, window [0, 20]).
DOC_GAMMAS = (0.0, 0.1, 0.3, 1.0, 3.0, 10.0)
DOC_GAPS = (0.505, 0.874, 0.952, 0.973, 0.923, 0.753)


class UniformTarget:
    """Enumerated uniform target on {0,1}^n (solvable-corner setting)."""

    def __init__(self, n: int) -> None:
        if n < 1:
            raise ValueError(f"n must be a positive integer, got {n}")
        self.n = n
        d = 2**n
        self._pi = np.full(d, 1.0 / d, dtype=float)

    def exact_dist(self) -> NDArray[np.float64]:
        return self._pi.copy()


def telegraph_f(gamma: float, t: NDArray[np.float64]) -> NDArray[np.float64]:
    """Closed form of f'' + 2 gamma f' + 4 f = 0, f(0)=1, f'(0)=0.

    Underdamped (gamma < 2): exp(-gamma t) [cos ωt + (gamma/ω) sin ωt],
    ω = sqrt(4 - gamma^2). Overdamped / critical as in monotonicity.md §5.
    """
    if gamma < 0.0:
        raise ValueError(f"gamma must be >= 0, got {gamma}")
    tt = np.asarray(t, dtype=float)
    if gamma == 0.0:
        return np.cos(2.0 * tt)
    if abs(gamma - 2.0) < 1e-12:
        return np.exp(-2.0 * tt) * (1.0 + 2.0 * tt)
    if gamma < 2.0:
        omega = float(np.sqrt(4.0 - gamma * gamma))
        return np.exp(-gamma * tt) * (
            np.cos(omega * tt) + (gamma / omega) * np.sin(omega * tt)
        )
    omega_h = float(np.sqrt(gamma * gamma - 4.0))
    return np.exp(-gamma * tt) * (
        np.cosh(omega_h * tt) + (gamma / omega_h) * np.sinh(omega_h * tt)
    )


def window_mode_means(
    gamma: float, t_max: float = T_MAX, n_quad: int = N_QUAD, n_qubits: int = 2
) -> tuple[float, NDArray[np.float64]]:
    """Return (gap, lambda_{|S|=k} for k=1..n) via trapezoid time-average."""
    if t_max <= 0.0 or n_quad < 8:
        raise ValueError("need a positive window and a dense quadrature")
    t = np.linspace(0.0, t_max, n_quad)
    f = telegraph_f(gamma, t)
    lams = np.empty(n_qubits, dtype=float)
    for k in range(1, n_qubits + 1):
        lams[k - 1] = float(np.trapezoid(f**k, t) / t_max)
    gap = 1.0 - float(np.max(np.abs(lams)))
    return gap, lams


def integrate_f_to_inf(gamma: float, t_cut: float = 80.0) -> float:
    """Numerical check of the Laplace identity ∫_0^∞ f = gamma/2 (gamma>0)."""
    if gamma <= 0.0:
        raise ValueError("Laplace identity is for gamma > 0")
    t = np.linspace(0.0, t_cut, 8001)
    return float(np.trapezoid(telegraph_f(gamma, t), t))


def lindblad_window_gap(
    gamma: float, n_t: int = N_LINDBLAD_T
) -> tuple[float, NDArray[np.float64]]:
    """Exact n=2 Lindblad window-averaged MH gap (uniform target, H = mixer)."""
    from goldilocks.diagnostics import mh_transition_matrix, spectral_gap
    from goldilocks.hamiltonians import mixer
    from goldilocks.lindblad import proposal_matrix

    H = mixer(2)
    tgt = UniformTarget(2)
    ts = np.linspace(0.0, T_MAX, n_t)
    P = np.zeros((4, 4), dtype=float)
    for t in ts:
        P = P + proposal_matrix(H, gamma, float(t))
    P = P / float(n_t)
    return spectral_gap(mh_transition_matrix(P, tgt)), ts


def discrete_formula_gap(gamma: float, ts: NDArray[np.float64], n_qubits: int = 2) -> float:
    """Formula gap on the same discrete t-grid as the Lindblad average."""
    f = telegraph_f(gamma, ts)
    lams = [float(np.mean(f**k)) for k in range(1, n_qubits + 1)]
    return 1.0 - max(abs(lam) for lam in lams)


def main() -> None:
    apply_style()
    formula_gaps: list[float] = []
    formula_l1: list[float] = []
    formula_l2: list[float] = []
    for g in DOC_GAMMAS:
        gap, lams = window_mode_means(g)
        formula_gaps.append(gap)
        formula_l1.append(float(lams[0]))
        formula_l2.append(float(lams[1]))

    # Lindblad check at the documented gamma grid (n=2), same t-grid as formula.
    lb_errs: list[float] = []
    for g in DOC_GAMMAS:
        lb_gap, ts = lindblad_window_gap(g)
        disc = discrete_formula_gap(g, ts)
        lb_errs.append(abs(lb_gap - disc))
    max_lb_err = max(lb_errs)

    int_03 = integrate_f_to_inf(0.3)
    int_1 = integrate_f_to_inf(1.0)

    checks: list[tuple[str, bool, str]] = []
    for g, doc, got in zip(DOC_GAMMAS, DOC_GAPS, formula_gaps):
        checks.append(
            (
                f"formula gap(gamma={g})",
                close_enough(got, doc, rtol=0.02, atol=0.008),
                f"{got:.4f} vs doc {doc}",
            )
        )
    checks.append(
        (
            "Lindblad vs formula (n=2)",
            max_lb_err < 1e-5,
            f"max |delta_LB - delta_f| = {max_lb_err:.3e} (claim ~1e-6)",
        )
    )
    checks.append(
        (
            "Laplace identity gamma=0.3",
            close_enough(int_03, 0.3 / 2.0, rtol=1e-3, atol=1e-3),
            f"int f = {int_03:.5f} vs gamma/2 = {0.15:.5f}",
        )
    )
    checks.append(
        (
            "Laplace identity gamma=1",
            close_enough(int_1, 0.5, rtol=1e-3, atol=1e-3),
            f"int f = {int_1:.5f} vs 0.5",
        )
    )

    verify_or_die(checks)

    import matplotlib.pyplot as plt
    from mpl_toolkits.axes_grid1.inset_locator import inset_axes

    fig, (ax_f, ax_gap) = plt.subplots(1, 2, figsize=(8.4, 3.6))

    t_plot = np.linspace(0.0, 12.0, 800)
    f_gammas = (0.0, 0.3, 1.0, 3.0)
    f_colors = {
        0.0: OKABE_ITO["black"],
        0.3: OKABE_ITO["blue"],
        1.0: OKABE_ITO["green"],
        3.0: OKABE_ITO["vermillion"],
    }
    for g in f_gammas:
        ax_f.plot(
            t_plot,
            telegraph_f(g, t_plot),
            color=f_colors[g],
            lw=1.3,
            label=fr"$\gamma={g}$",
        )
    ax_f.axhline(0.0, color=OKABE_ITO["black"], lw=0.5, alpha=0.4)
    ax_f.set_xlabel(r"$t$ (mixer units)")
    ax_f.set_ylabel(r"$f_\gamma(t)$")
    ax_f.set_title(r"(a) telegraph $f_\gamma(t)$")
    ax_f.legend(frameon=False, loc="upper right")

    g_grid = np.concatenate(
        [np.linspace(0.0, 1.8, 37), np.linspace(2.05, 12.0, 40)]
    )
    gaps_grid = []
    l1_grid = []
    l2_grid = []
    for g in g_grid:
        gap, lams = window_mode_means(g)
        gaps_grid.append(gap)
        l1_grid.append(abs(float(lams[0])))
        l2_grid.append(abs(float(lams[1])))

    ax_gap.plot(g_grid, gaps_grid, color=OKABE_ITO["blue"], lw=1.5)
    ax_gap.scatter(
        list(DOC_GAMMAS),
        formula_gaps,
        s=28,
        c=OKABE_ITO["vermillion"],
        zorder=3,
        label="§5 check points",
    )
    ax_gap.set_xlabel(r"$\gamma$ (mixer units)")
    ax_gap.set_ylabel(r"window-averaged gap $\delta(\gamma)$")
    ax_gap.set_title(r"(b) $\delta(\gamma)$ on $t\in[0,20]$")
    ax_gap.set_xlim(0.0, 12.0)
    ax_gap.set_ylim(0.35, 1.02)
    ax_gap.legend(frameon=False, loc="lower right")

    inset = inset_axes(ax_gap, width="48%", height="38%", loc="upper right", borderpad=0.7)
    inset.plot(g_grid, l1_grid, color=OKABE_ITO["orange"], lw=1.2, label=r"$|\lambda_{|S|=1}|$")
    inset.plot(g_grid, l2_grid, color=OKABE_ITO["purple"], lw=1.2, label=r"$|\lambda_{|S|=2}|$")
    inset.set_xlim(0.0, 12.0)
    inset.set_ylim(0.0, 0.55)
    inset.set_xlabel(r"$\gamma$", fontsize=7)
    inset.tick_params(labelsize=6)
    inset.legend(frameon=False, fontsize=6, loc="upper right")
    inset.spines["top"].set_visible(False)
    inset.spines["right"].set_visible(False)

    savefig_pair(fig, OUT_STEM)
    plt.close(fig)


if __name__ == "__main__":
    main()
