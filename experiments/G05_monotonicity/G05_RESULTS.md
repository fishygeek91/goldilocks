# G05 results — the envelope law (2026-08-18)

Run: 50 pre-registered cells (PREREGISTRATION.md; master seed 20260818),
run_g05.py, full log in run_g05.log, per-cell data in results.csv.

## Verdict: **L1 HOLDS WITH ONE NOTED EXCEPTION** (pre-registered rule: 1–2 marginal violations < 5%)

    L1 violations:   1 / 50   (max margin +1.17%, ε = 0.01)
    interior peaks: 20 / 50
    advantage cells: 4 / 50
    median peak-to-envelope margin: −72.5%

No cell came anywhere near the 5% refutation threshold. The dephased-walk
family never rises materially above max(coherent quench, single-flip,
uniform-flip). **"Noise cannot help" stands in its envelope form.**

## The exception, in full (pre-registered disclosure)

Cell 46: SK instance (seed 46), n = 5, T = 0.085, α = 0.63 — an ADVANTAGE
cell (quench gap 0.0895 vs single-flip 1.3e−6). γ/Δ₃-curve:

    γ/Δ₃ : 0       0.01     0.0316   0.1     0.316    1 ... 100
    gap  : 0.0895  0.0906   0.0815   0.0203  0.00138  ... 4e−9

Peak at γ = 0.01Δ₃, margin +1.17% over the γ=0 envelope.

**Non-binding robustness follow-up** (the prereg mandates this only for ≥5%
violations; done anyway): on a finer γ grid the bump maxes at +1.65%
(γ ≈ 0.02Δ₃, 12 time points) and **survives doubling the time-point count**
(+1.2% at 24 points) — it is a real property of this instance, not
discretization noise. A fresh SK instance (seed 146) at the identical
(n, T, α) is purely monotone (no bump anywhere). Conclusion: an
instance-specific micro-peak at very weak dephasing (γ ~ 0.01–0.03Δ₃),
magnitude ~1–2% — three orders below the kind of effect H1 needed, and
requiring γ-control precision that makes it useless as a resource.

## Secondary observables (L2, pre-registered as descriptive)

- **L2(a) interior peaks: 20/50 cells.** Peaks are generic, as the theory
  pass predicted (docs/monotonicity.md) — conjecture v1 ("monotone for all
  targets") is dead on arrival in this sample too.
- **L2(b) advantage cells: 4/50** (all low-T SK/RFIM, α ∈ [0.63, 0.86],
  T ∈ [0.05, 0.1]; quench beats single-flip by up to ELEVEN orders of
  magnitude — cell 28: 0.071 vs 4.9e−13). In these cells the γ-curve is
  monotone-eroding beyond γ ≈ 0.03Δ₃ in 4/4; micro-bumps at γ ≤ 0.02Δ₃ in
  3/4 (margins +0.09%, −0.02%, +1.17% rel. γ=0). Refined statement of C7:
  *in advantage cells, dephasing erodes the advantage beyond γ ≈ 0.03Δ₃;
  sub-2% instance-specific micro-bumps can occur below that.*
- **L2(c) peak locations:** all γ* ∈ [0.01, 0.32]Δ₃ — peaks live at weak
  dephasing; nothing ENAQT-like at γ ~ Δ (contrast the α=1/uniform solvable
  corner where γ* ~ Δ; real targets pin the useful coherence harder).

## ESS spot-check (pre-registered; does not affect L1)

Cells {0, 10, 20, 30, 40} × γ ∈ {0, 0.316Δ, 31.6Δ}: rank agreement between
ESS/step and gap in 3/5 cells. The 2 failures (cells 0, 20) are both the
frozen-chain pathology at γ = 31.6Δ₃: the near-Zeno chain barely moves, the
magnetization series is near-constant, and the initial-sequence ESS
estimator returns garbage-high values on degenerate series. Split-R̂ gating
(applied in any paper-grade run, per protocol) excludes exactly these; at
the two non-frozen γ values rank agreement is 5/5. Reported as required.

## Standing for the paper (claims register update)

- C6 (envelope law): **HOLDS, 49/50 clean + 1 noted +1.17% exception**
  (instance-specific, reproduced, disclosed).
- C7 (advantage cells): holds in eroded form — see refined statement above.
- The 20/50 peak rate is the paper's "noise CAN help mixing" nuance, now
  with field data: peaks are common; useful peaks are nonexistent.
