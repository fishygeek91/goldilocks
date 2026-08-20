"""G05: the envelope law across ~50 random targets (pre-registered).

Usage: python experiments/G05_monotonicity/run_g05.py [--quick]

Everything below implements PREREGISTRATION.md verbatim: 50 random cells
(class x n x T x alpha), gamma/Delta_3 grid {0} + logspace(-2,2,9),
window-averaged dephased-walk proposal (t*Delta_3 in [2,12], 12 points),
exact MH spectral gaps vs enumerated targets, single-flip and uniform-flip
baselines, ESS spot-check on cells {0,10,20,30,40}. Writes results.csv;
the verdict analysis lives in G05_RESULTS.md.
"""
from __future__ import annotations

import csv
import sys
from pathlib import Path

import numpy as np

from goldilocks.diagnostics import ess, magnetization, mh_transition_matrix, spectral_gap
from goldilocks.engine import run_chain
from goldilocks.hamiltonians import delta_spectral_width, walk_hamiltonian
from goldilocks.kernels import DephasedWalkKernel
from goldilocks.lindblad import averaged_proposal_matrix
from goldilocks.targets import IsingTarget

QUICK = "--quick" in sys.argv
N_CELLS = 6 if QUICK else 50
GAMMA_REL = np.concatenate([[0.0], np.logspace(-2, 2, 9)])  # gamma / Delta_3
T_WINDOW_REL = (2.0, 12.0)
N_TIME_POINTS = 12
EPS = 0.01                     # pre-registered L1 slack
ESS_CELLS = {0, 10, 20, 30, 40}
ESS_STEPS, ESS_SEEDS = 50_000, 3

CLASSES = ("e01", "sk", "rfim")


def make_target(cls_name: str, n: int, T: float, instance_seed: int) -> IsingTarget:
    if cls_name == "e01":
        return IsingTarget.e01_chain(n, T=T, seed=instance_seed)
    if cls_name == "sk":
        return IsingTarget.sk(n, T=T, seed=instance_seed)
    return IsingTarget.rfim_chain(n, T=T, seed=instance_seed)


def single_flip_P(n: int) -> np.ndarray:
    d = 2**n
    P = np.zeros((d, d))
    for x in range(d):
        for i in range(n):
            P[x ^ (1 << i), x] = 1.0 / n
    return P


def uniform_P(n: int) -> np.ndarray:
    d = 2**n
    return np.full((d, d), 1.0 / d)


def main() -> None:
    rng = np.random.default_rng(20260818)  # pre-registered master seed
    out = Path(__file__).parent / "results.csv"
    rows: list[dict] = []
    n_l1_violations = 0

    for cell in range(N_CELLS):
        # Draw the cell exactly as pre-registered (one draw order, fixed).
        cls_name = CLASSES[rng.integers(len(CLASSES))]
        n = int(rng.integers(4, 7))                       # {4, 5, 6}
        T = float(np.exp(rng.uniform(np.log(0.05), np.log(10.0))))
        alpha = float(rng.uniform(0.05, 1.0))
        tgt = make_target(cls_name, n, T, instance_seed=cell)
        H = walk_hamiltonian(tgt.energies, alpha=alpha)
        D3 = delta_spectral_width(H)
        tw = (T_WINDOW_REL[0] / D3, T_WINDOW_REL[1] / D3)

        gaps = np.array([
            spectral_gap(mh_transition_matrix(
                averaged_proposal_matrix(H, g_rel * D3, tw, N_TIME_POINTS), tgt))
            for g_rel in GAMMA_REL
        ])
        gap_sf = spectral_gap(mh_transition_matrix(single_flip_P(n), tgt))
        gap_uf = spectral_gap(mh_transition_matrix(uniform_P(n), tgt))

        envelope = max(gaps[0], gap_sf, gap_uf)
        peak_val = float(gaps[1:].max())                  # over gamma > 0
        margin = float(peak_val / envelope - 1.0)         # >0 means above envelope
        l1_violated = peak_val > (1.0 + EPS) * envelope
        n_l1_violations += int(l1_violated)
        interior_peak = bool(gaps[1:-1].max() > max(gaps[0], gaps[-1]) + 1e-9)
        advantage = bool(gaps[0] > max(gap_sf, gap_uf))
        adv_violation = float((gaps[1:].max() - gaps[0]) / gaps[0]) if advantage else np.nan
        gamma_star = float(GAMMA_REL[int(np.argmax(gaps))])

        row = {
            "cell": cell, "class": cls_name, "n": n, "T": T, "alpha": alpha,
            "gap_sf": gap_sf, "gap_uf": gap_uf,
            **{f"gap_g{g:.3g}": gp for g, gp in zip(GAMMA_REL, gaps)},
            "envelope": envelope, "peak_over_envelope": margin,
            "l1_violated": l1_violated, "interior_peak": interior_peak,
            "advantage_cell": advantage, "adv_violation_rel": adv_violation,
            "gamma_star_rel": gamma_star,
        }

        if cell in ESS_CELLS and not QUICK:               # pre-registered spot-check
            for g_rel in (GAMMA_REL[0], GAMMA_REL[4], GAMMA_REL[8]):
                ker = DephasedWalkKernel(H, g_rel * D3, tw, n_time_points=N_TIME_POINTS)
                es = []
                for s in range(ESS_SEEDS):
                    r = run_chain(tgt, ker, ESS_STEPS, x0=s % 2**n, seed=s)
                    es.append(ess(magnetization(r["states"], n)) / ESS_STEPS)
                row[f"ess_per_step_g{g_rel:.3g}"] = float(np.mean(es))

        rows.append(row)
        print(f"cell={cell:02d} {cls_name:<4} n={n} T={T:7.3f} a={alpha:.2f} "
              f"gap0={gaps[0]:.3g} peak={peak_val:.3g} env={envelope:.3g} "
              f"margin={margin:+.2%} viol={l1_violated} peakflag={interior_peak} "
              f"adv={advantage}", flush=True)

    fieldnames: list[str] = sorted({k for r in rows for k in r}, key=str)
    with open(out, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        w.writerows(rows)

    n_peaks = sum(r["interior_peak"] for r in rows)
    n_adv = sum(r["advantage_cell"] for r in rows)
    print(f"\nL1 violations: {n_l1_violations}/{len(rows)}   "
          f"interior peaks: {n_peaks}/{len(rows)}   advantage cells: {n_adv}/{len(rows)}")
    print(f"wrote {out} — verdict goes to G05_RESULTS.md")


if __name__ == "__main__":
    main()
