"""G01: gamma-scan on the Ising target — the H1 experiment.

Usage: python experiments/G01_gamma_scan_ising/run_g01.py [--quick]

For each (n, T, gamma) cell: build the dephased-walk kernel, compute the
EXACT MH spectral gap (enumerable at these n), and run seeded chains for
ESS/step + ESS/sec with split-R-hat gating. Baselines: single-flip, uniform,
gamma=0 quench (E01 anchor), near-Zeno gamma. Writes results.csv here.

H1 verdict rule (pre-registered, README §2): a peak exists iff some
intermediate gamma beats BOTH gamma=0 and the largest gamma on spectral gap
AND ESS/step, outside +/- 2 SE over seeds.
"""
from __future__ import annotations

import csv
import sys
from pathlib import Path

import numpy as np

from goldilocks.diagnostics import (ess, magnetization, mh_transition_matrix,
                                    spectral_gap, split_rhat)
from goldilocks.engine import run_chain
from goldilocks.hamiltonians import (delta_edge_energy, delta_mixer,
                                     delta_spectral_width, walk_hamiltonian)
from goldilocks.kernels import DephasedWalkKernel, SingleFlipKernel, UniformFlipKernel
from goldilocks.targets import IsingTarget

QUICK = "--quick" in sys.argv
NS = (6,) if QUICK else (6, 8, 10)          # n>6 needs trajectory sampler: will refuse loudly
TEMPS = (0.1,) if QUICK else (0.1, 0.3, 1.0)
GAMMA_REL = np.logspace(-2, 2, 5 if QUICK else 9)  # gamma / Delta_3
ALPHA = 0.5
N_STEPS = 2_000 if QUICK else 50_000
SEEDS = range(2 if QUICK else 5)
T_WINDOW_REL = (2.0, 12.0)  # t*Delta window, Layden-style average; tune in Phase 1

out = Path(__file__).parent / "results.csv"
rows = []
for n in NS:
    for T in TEMPS:
        tgt = IsingTarget.e01_chain(n, T=T)
        H = walk_hamiltonian(tgt.energies, alpha=ALPHA)
        D3 = delta_spectral_width(H)
        deltas = {"D1_mixer": delta_mixer(ALPHA),
                  "D2_edge": delta_edge_energy(tgt.energies, ALPHA), "D3_width": D3}
        tw = (T_WINDOW_REL[0] / D3, T_WINDOW_REL[1] / D3)

        kernels = {"single_flip": SingleFlipKernel(n), "uniform": UniformFlipKernel(n)}
        for g_rel in [0.0, *GAMMA_REL]:
            kernels[f"walk_g{g_rel:.3g}"] = DephasedWalkKernel(H, g_rel * D3, tw)

        for name, ker in kernels.items():
            gap = np.nan
            if hasattr(ker, "proposal_matrix"):
                gap = spectral_gap(mh_transition_matrix(ker.proposal_matrix, tgt))
            ess_steps, ess_secs, mags = [], [], []
            for s in SEEDS:
                r = run_chain(tgt, ker, N_STEPS, x0=s % 2**n, seed=s)
                m = magnetization(r["states"], n)
                mags.append(m)
                e = ess(m)
                ess_steps.append(e / N_STEPS)
                ess_secs.append(e / r["wall_seconds"])
            rhat = split_rhat(np.array(mags))
            rows.append({"n": n, "T": T, "kernel": name, "gap": gap,
                         "ess_per_step": np.mean(ess_steps), "ess_per_sec": np.mean(ess_secs),
                         "ess_per_step_se": np.std(ess_steps) / np.sqrt(len(ess_steps)),
                         "split_rhat": rhat, "gated_out": rhat > 1.05, **deltas})
            print(f"n={n} T={T} {name:<14} gap={gap:.4g} ess/step={np.mean(ess_steps):.4g} "
                  f"ess/sec={np.mean(ess_secs):.4g} Rhat={rhat:.3f}")

with open(out, "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=rows[0].keys())
    w.writeheader()
    w.writerows(rows)
print(f"\nwrote {out} — verdict analysis + G01_RESULTS.md is a Phase 1 task")
