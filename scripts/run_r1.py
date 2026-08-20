"""R1 + characterization-theorem numerical certification (proposal symmetry).

Usage: python scripts/run_r1.py  (from repo root; pip install -e . first)
Certifies every row of docs/characterization_theorem.md Table 1:
- pure computational-basis dephasing (sparse path, n up to 6)   -> symmetric
- dephasing in a random REAL basis (dense, n <= 5)              -> symmetric
- depolarizing / Pauli-jump noise, unequal X/Y/Z rates (dense)  -> symmetric
- infinite-T relaxation, sigma^+/- at EQUAL rates (dense)       -> symmetric
- amplitude damping (dense)                                     -> BREAKS
- finite-T relaxation, sigma^+/- at UNEQUAL rates (dense)       -> BREAKS
Writes docs/R1_results.txt.
Result 2026-08-18: pure dephasing defect <= 3.3e-16 (CERTIFIED); amp-damp
defect up to 5.5e-1 (breaks, as the theorem predicts).
"""
from __future__ import annotations

import numpy as np

from goldilocks.hamiltonians import walk_hamiltonian, delta_spectral_width
from goldilocks.lindblad import (
    pauli_jumps,
    proposal_matrix,
    rotated_dephasing_jumps,
    symmetry_defect,
    thermal_jumps,
)
from goldilocks.targets import IsingTarget

rows = []
for n in (4, 5, 6):
    tgt = IsingTarget.e01_chain(n, T=0.1)
    H = walk_hamiltonian(tgt.energies, alpha=0.5)
    D = delta_spectral_width(H)
    for g_rel in (0.0, 0.1, 1.0, 10.0):
        for tD in (0.5, 2.0, 8.0):
            g, t = g_rel * D, tD / D
            d = symmetry_defect(proposal_matrix(H, g, t))
            rows.append((n, g_rel, tD, "dephasing", d))
            print(f"n={n} g/D={g_rel:<4} tD={tD:<4} dephasing defect={d:.3e}")
            if n <= 5 and g_rel > 0.0:  # dense-path channel classes (Table 1)
                cases = {
                    "rot-dephasing": {"jumps": rotated_dephasing_jumps(n, g, seed=n)},
                    "depolarizing": {"jumps": pauli_jumps(n, gx=0.5 * g, gy=0.3 * g, gz=g)},
                    "thermal-equal": {"jumps": thermal_jumps(n, k_down=g, k_up=g)},
                    "amp-damp": {"kappa": 0.1 * D},
                    "thermal-unequal": {"jumps": thermal_jumps(n, k_down=g, k_up=0.25 * g)},
                }
                for name, kw in cases.items():
                    dc = symmetry_defect(proposal_matrix(H, 0.0, t, **kw))
                    rows.append((n, g_rel, tD, name, dc))
                    print(f"n={n} g/D={g_rel:<4} tD={tD:<4} {name} defect={dc:.3e}")

with open("docs/R1_results.txt", "w") as f:
    f.write("n gamma/Delta t*Delta noise defect\n")
    for r in rows:
        f.write(f"{r[0]} {r[1]} {r[2]} {r[3]} {r[4]:.6e}\n")

SYMMETRIC = ("dephasing", "rot-dephasing", "depolarizing", "thermal-equal")
BREAKING = ("amp-damp", "thermal-unequal")
worst_sym = max(r[4] for r in rows if r[3] in SYMMETRIC)
best_break = min(r[4] for r in rows if r[3] in BREAKING)
print(f"\nWorst transpose-closed defect:  {worst_sym:.3e}  "
      f"({'CERTIFIED symmetric' if worst_sym < 1e-9 else 'SYMMETRY FAILS — STOP (see TASKS.md R1 exit)'})")
print(f"Smallest symmetry-breaking defect: {best_break:.3e}  "
      f"({'breaks as predicted' if best_break > 1e-4 else 'UNEXPECTEDLY SYMMETRIC — theorem table wrong?'})")
