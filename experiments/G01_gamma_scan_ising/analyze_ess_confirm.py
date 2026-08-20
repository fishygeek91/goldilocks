"""Rank-agreement analysis for the G01 ESS confirmation run.

Usage: gvenv/bin/python experiments/G01_gamma_scan_ising/analyze_ess_confirm.py

Question (G01_PILOT_RESULTS.md addendum): after split-R-hat <= 1.05 gating,
does the ESS/step ordering over gamma agree with the pilot's exact-gap
ordering in every (target, T, alpha) cell?  Metrics per cell:

- Spearman rank correlation between gap and ESS/step over the NON-GATED
  walk-kernel gamma points (the frozen-chain pathology at large gamma is
  excluded by the gate, per G05's ESS spot-check lesson).
- Monotone-in-gamma check on ESS/step over non-gated points (the pilot's
  gap verdict was 12/12 monotone decreasing).
- Envelope check on ESS/step: does any gamma>0 beat BOTH gamma=0 and the
  best classical baseline (only among non-gated rows)?
"""
from __future__ import annotations

import csv
from collections import defaultdict
from pathlib import Path

import numpy as np

SRC = Path(__file__).parent / "results_ess_confirm.csv"


def spearman(a: np.ndarray, b: np.ndarray) -> float:
    """Spearman rank correlation (no scipy dependency)."""
    ra = np.argsort(np.argsort(a)).astype(float)
    rb = np.argsort(np.argsort(b)).astype(float)
    if ra.std() == 0 or rb.std() == 0:
        return float("nan")
    return float(np.corrcoef(ra, rb)[0, 1])


rows = list(csv.DictReader(open(SRC)))
cells: dict[tuple[str, str, str], list[dict]] = defaultdict(list)
for r in rows:
    cells[(r["target"], r["T"], r["alpha"])].append(r)

print(f"{'cell':<24} {'#ok':>3} {'rho(gap,ESS)':>12} {'ESS mono?':>9} "
      f"{'peak>env?':>9}  note")
n_agree = n_cells_scored = n_peaks = 0
for key in sorted(cells):
    rs = cells[key]
    walks = [r for r in rs if r["kernel"].startswith("walk_g")]
    ok = [r for r in walks if r["gated_out"] == "False"]
    label = f"{key[0]} T={key[1]} a={key[2]}"
    if len(ok) < 3:
        print(f"{label:<24} {len(ok):>3} {'—':>12} {'—':>9} {'—':>9}  "
              f"insufficient non-gated points (chains too slow at 50k steps)")
        continue
    g = np.array([float(r["kernel"][6:]) for r in ok])
    order = np.argsort(g)
    gap = np.array([float(r["gap"]) for r in ok])[order]
    ess_s = np.array([float(r["ess_per_step"]) for r in ok])[order]
    rho = spearman(gap, ess_s)
    mono = bool(np.all(np.diff(ess_s) <= 0))
    # envelope on ESS/step: gamma>0 vs max(gamma=0, non-gated classical)
    base = [float(r["ess_per_step"]) for r in rs
            if not r["kernel"].startswith("walk_g") and r["gated_out"] == "False"]
    g0 = [float(r["ess_per_step"]) for r in ok if float(r["kernel"][6:]) == 0.0]
    env = max(base + g0) if (base or g0) else float("nan")
    peak = bool(np.nanmax(ess_s) > env) if np.isfinite(env) else False
    n_cells_scored += 1
    n_agree += int(rho > 0.8 if np.isfinite(rho) else False)
    n_peaks += int(peak)
    print(f"{label:<24} {len(ok):>3} {rho:>12.3f} {str(mono):>9} "
          f"{str(peak):>9}")

print(f"\nscored cells (>=3 non-gated gamma points): {n_cells_scored}")
print(f"rank agreement (Spearman > 0.8): {n_agree}/{n_cells_scored}")
print(f"cells where some gamma>0 beats envelope on ESS/step: {n_peaks}")
