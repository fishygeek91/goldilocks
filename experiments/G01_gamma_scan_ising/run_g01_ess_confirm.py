"""G01 ESS confirmation at n=6 — closes the pilot's gap-only caveat (Fig 3 honesty).

Usage: gvenv/bin/python experiments/G01_gamma_scan_ising/run_g01_ess_confirm.py [--quick]

Covers EXACTLY the pilot's cells (G01_PILOT_RESULTS.md): n=6, targets
{e01-chain, SK}, T in {0.1, 0.3, 1.0}, alpha in {0.05, 0.15, 0.3, 0.5},
gamma/Delta_3 in {0, 0.03, 0.1, 0.3, 1, 3, 10}, window t*Delta_3 in [2, 12]
with 6 time points (pilot convention). For every cell it reports the exact
spectral gap (recomputed — pilot regression anchor) PLUS the protocol
metrics the pilot lacked: ESS/step AND ESS/sec over 5 seeds with split-R-hat
<= 1.05 gating (the frozen-chain ESS pathology at large gamma — see
G05_RESULTS.md ESS spot-check — is excluded by exactly this gate).

n=8/10 are NOT attempted: the dense-table kernel is n<=6; the trajectory
kernel is not wired into this runner (TASKS.md Phase 1 leftover).

Verdict question (written to G01_PILOT_RESULTS.md as an addendum): does the
ESS/step ordering over gamma rank-agree with the pilot's gap ordering in
every cell, after R-hat gating?
"""
from __future__ import annotations

import csv
import sys
from pathlib import Path

import numpy as np

from goldilocks.diagnostics import (ess, magnetization, mh_transition_matrix,
                                    spectral_gap, split_rhat)
from goldilocks.engine import run_chain
from goldilocks.hamiltonians import delta_spectral_width, walk_hamiltonian
from goldilocks.kernels import (DephasedWalkKernel, SingleFlipKernel,
                                UniformFlipKernel)
from goldilocks.targets import IsingTarget

QUICK = "--quick" in sys.argv

# ---- pilot grid (G01_PILOT_RESULTS.md), restricted per session brief ------
N = 6
TARGETS = ("chain",) if QUICK else ("chain", "sk")
TEMPS = (0.3,) if QUICK else (0.1, 0.3, 1.0)
ALPHAS = (0.5,) if QUICK else (0.05, 0.15, 0.3, 0.5)
GAMMA_REL = (0.0, 0.1, 10.0) if QUICK else (0.0, 0.03, 0.1, 0.3, 1.0, 3.0, 10.0)
T_WINDOW_REL = (2.0, 12.0)   # t * Delta_3 window (pilot convention)
N_TIME_POINTS = 6            # pilot used 6 window points
N_STEPS = 2_000 if QUICK else 50_000
SEEDS = range(2 if QUICK else 5)
RHAT_GATE = 1.05

out = Path(__file__).parent / ("results_ess_confirm_quick.csv" if QUICK
                               else "results_ess_confirm.csv")


def make_target(kind: str, T: float) -> IsingTarget:
    """Pilot targets: e01 chain (seed 42) and SK (seed 7) at n=6."""
    if kind == "chain":
        return IsingTarget.e01_chain(N, T=T)
    if kind == "sk":
        return IsingTarget.sk(N, T=T)
    raise ValueError(f"unknown target kind: {kind}")


rows = []
for kind in TARGETS:
    for T in TEMPS:
        tgt = make_target(kind, T)
        for alpha in ALPHAS:
            H = walk_hamiltonian(tgt.energies, alpha=alpha)
            D3 = delta_spectral_width(H)
            tw = (T_WINDOW_REL[0] / D3, T_WINDOW_REL[1] / D3)

            kernels: dict[str, object] = {
                "single_flip": SingleFlipKernel(N),
                "uniform": UniformFlipKernel(N),
            }
            for g_rel in GAMMA_REL:
                kernels[f"walk_g{g_rel:.3g}"] = DephasedWalkKernel(
                    H, g_rel * D3, tw, n_time_points=N_TIME_POINTS)

            for name, ker in kernels.items():
                gap = np.nan
                if hasattr(ker, "proposal_matrix"):
                    gap = spectral_gap(mh_transition_matrix(ker.proposal_matrix, tgt))
                ess_steps, ess_secs, acc_rates, mags = [], [], [], []
                for s in SEEDS:
                    r = run_chain(tgt, ker, N_STEPS, x0=s % 2**N, seed=s)
                    m = magnetization(r["states"], N)
                    mags.append(m)
                    e = ess(m)
                    ess_steps.append(e / N_STEPS)
                    ess_secs.append(e / r["wall_seconds"])
                    acc_rates.append(r["accept_rate"])
                rhat = split_rhat(np.array(mags))
                rows.append({
                    "target": kind, "n": N, "T": T, "alpha": alpha,
                    "kernel": name, "gap": gap,
                    "ess_per_step": np.mean(ess_steps),
                    "ess_per_step_se": np.std(ess_steps) / np.sqrt(len(ess_steps)),
                    "ess_per_sec": np.mean(ess_secs),
                    "accept_rate": np.mean(acc_rates),
                    "split_rhat": rhat, "gated_out": rhat > RHAT_GATE,
                    "D3_width": D3,
                })
                print(f"{kind} T={T} a={alpha} {name:<12} gap={gap:.4g} "
                      f"ess/step={np.mean(ess_steps):.4g} "
                      f"ess/sec={np.mean(ess_secs):.4g} "
                      f"acc={np.mean(acc_rates):.3f} Rhat={rhat:.3f}"
                      f"{'  [GATED OUT]' if rhat > RHAT_GATE else ''}",
                      flush=True)

with open(out, "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=rows[0].keys())
    w.writeheader()
    w.writerows(rows)
print(f"\nwrote {out} ({len(rows)} rows) — rank-agreement analysis is next", flush=True)
