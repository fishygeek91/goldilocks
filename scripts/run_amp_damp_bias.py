"""Certify the amplitude-damping Metropolis-vs-Hastings bias bound.

Builds the window-averaged kappa-damped proposal (gamma=0, T1 only),
compares the exact Hastings kernel P_H to the free-lunch Metropolis kernel
P_M, and checks the per-step / stationary TV bounds in docs/amp_damp_bias.md.

Usage: gvenv/bin/python scripts/run_amp_damp_bias.py
Writes docs/amp_damp_bias_results.csv.
"""
from __future__ import annotations

import csv
from pathlib import Path

import numpy as np

from goldilocks.diagnostics import (
    max_column_tv,
    mh_transition_matrix,
    naive_metropolis_matrix,
    spectral_gap,
    stationary_distribution,
    step_tv_bound_columns,
    step_tv_bound_from_defect,
    total_variation,
)
from goldilocks.hamiltonians import delta_spectral_width, walk_hamiltonian
from goldilocks.kernels import DephasedWalkKernel
from goldilocks.lindblad import symmetry_defect
from goldilocks.targets import IsingTarget

REPO = Path(__file__).resolve().parents[1]
OUT = REPO / "docs" / "amp_damp_bias_results.csv"

# Plan grid: isolate T1 (gamma=0), G01 window, n <= 5 dense Lindblad.
CELLS: tuple[tuple[int, float, float], ...] = (
    (4, 1.0, 0.5),
    (4, 0.3, 0.5),
    (5, 1.0, 0.5),
)
KAPPA_REL = (0.01, 0.03, 0.1, 0.3, 1.0)
T_WINDOW_REL = (2.0, 12.0)
N_TIME_POINTS = 6
BOUND_ATOL = 1e-10


def main() -> None:
    rows: list[dict[str, float | int | str]] = []
    for n, T, alpha in CELLS:
        tgt = IsingTarget.e01_chain(n, T=T)
        pi = tgt.exact_dist()
        H = walk_hamiltonian(tgt.energies, alpha=alpha)
        D3 = delta_spectral_width(H)
        tw = (T_WINDOW_REL[0] / D3, T_WINDOW_REL[1] / D3)
        pi_min = float(pi.min())
        print(f"\n=== cell n={n} T={T} alpha={alpha}  pi_min={pi_min:.3e} ===")
        for k_rel in KAPPA_REL:
            ker = DephasedWalkKernel(
                H,
                gamma=0.0,
                t_window=tw,
                n_time_points=N_TIME_POINTS,
                kappa=k_rel * D3,
            )
            Q = ker.proposal_matrix
            eps = symmetry_defect(Q)
            P_H = mh_transition_matrix(Q, tgt)
            P_M = naive_metropolis_matrix(Q, tgt)
            tv_step = max_column_tv(P_M, P_H)
            bound_step = step_tv_bound_from_defect(eps, pi)
            bound_step_col = float(step_tv_bound_columns(Q, pi).max())
            resid_H = float(np.abs(P_H @ pi - pi).max())
            if resid_H > 1e-8:
                raise RuntimeError(
                    f"Hastings failed to fix pi (residual {resid_H:.3e}) "
                    f"at n={n} T={T} kappa/Delta={k_rel}"
                )
            gap_H = spectral_gap(P_H)
            if gap_H <= 0.0:
                raise RuntimeError(f"non-positive Hastings gap {gap_H}")
            pi_M = stationary_distribution(P_M)
            tv_stat = total_variation(pi_M, pi)
            # B_naive: gap envelope without the L2->TV factor (empirical).
            bound_stat = bound_step / gap_H
            # Theorem B (proved): extra pi_min^{-1/2} from the L2(pi)->TV pass.
            bound_stat_rig = bound_stat / np.sqrt(pi_min)
            slack_step = tv_step <= bound_step + BOUND_ATOL
            slack_col = tv_step <= bound_step_col + BOUND_ATOL
            slack_stat = tv_stat <= bound_stat + BOUND_ATOL
            slack_stat_rig = tv_stat <= bound_stat_rig + BOUND_ATOL
            if not slack_step:
                raise RuntimeError(
                    f"per-step bound FAILED: TV={tv_step:.4e} > {bound_step:.4e}"
                )
            if not slack_col:
                raise RuntimeError(
                    f"column bound FAILED: TV={tv_step:.4e} > {bound_step_col:.4e}"
                )
            if not slack_stat:
                raise RuntimeError(
                    f"empirical B_naive FAILED: TV={tv_stat:.4e} > {bound_stat:.4e}"
                )
            if not slack_stat_rig:
                raise RuntimeError(
                    f"Theorem B bound FAILED: TV={tv_stat:.4e} > {bound_stat_rig:.4e}"
                )
            row = {
                "n": n,
                "T": T,
                "alpha": alpha,
                "kappa_over_Delta": k_rel,
                "epsilon": eps,
                "pi_min": pi_min,
                "gap_H": gap_H,
                "tv_step": tv_step,
                "bound_step": bound_step,
                "bound_step_col": bound_step_col,
                "tv_stat": tv_stat,
                "bound_stat": bound_stat,
                "bound_stat_rig": bound_stat_rig,
                "ratio_stat_over_tv": (tv_stat / tv_step) if tv_step > 0 else 0.0,
                "ratio_bound_over_meas": (bound_stat / tv_stat) if tv_stat > 0 else float("inf"),
            }
            rows.append(row)
            print(
                f"  k/D={k_rel:<5} eps={eps:.3e}  TVstep={tv_step:.3e} "
                f"<= {bound_step:.3e}  TVstat={tv_stat:.3e} <= {bound_stat:.3e}  "
                f"slack={bound_stat / tv_stat:.1e}x" if tv_stat > 0
                else f"  k/D={k_rel:<5} eps={eps:.3e}  TVstep={tv_step:.3e} TVstat=0"
            )

    fieldnames = list(rows[0].keys())
    with OUT.open("w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=fieldnames)
        w.writeheader()
        w.writerows(rows)
    print(f"\nwrote {OUT} ({len(rows)} rows)")


if __name__ == "__main__":
    main()
