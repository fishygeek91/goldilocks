# G05 pre-registration — the envelope law (WRITTEN BEFORE ANY RUNS)

Registered: 2026-08-18, before executing run_g05.py. Nothing below may be
changed after results exist; deviations must be reported as deviations.

## History note (why this is not the G01 conjecture)

The originally planned law — "gap monotone non-increasing in γ for all
targets" — was REFUTED during the theory pass of this same session
(docs/monotonicity.md: analytic counterexample at α = 1 / uniform target;
numerical peaks in all n = 4 cells at finer resolution). Pre-registering a
law already known false would be theater. What is registered instead is the
corrected claim that survived every check performed so far, tested on fresh
random instances it has never seen.

## The law under test

**L1 (envelope law).** For every cell (target instance, T, α), with
δ(γ) the exact spectral gap of the MH chain built from the window-averaged
dephased-walk proposal:

    max_{γ > 0} δ(γ)  ≤  (1 + ε) · max( δ(γ=0), δ_SF, δ_UF )

where δ_SF, δ_UF are the exact gaps of Metropolized single-flip and
uniform-flip kernels, and ε = 0.01 (slack for propagator discretization;
all margins reported regardless of sign or size).

**L2 (secondary, descriptive — reported, not thresholded).**
(a) Fraction of cells with an interior peak: some grid γ with
    δ(γ) > max(δ(first), δ(last)) + 1e-9.
(b) "Advantage cells": δ(γ=0) > max(δ_SF, δ_UF). In these cells, report
    whether δ(γ) ≤ δ(γ=0) for all γ (the G01-regime claim), and the worst
    violation margin if any.
(c) Peak location γ*/Δ₃ distribution over cells with a peak (feeds the
    forward-looking γ*-scaling question).

## Verdict rule (binding)

- L1 HOLDS if 0 of ~50 cells violate at ε = 0.01. Any violating cell is
  reported with its full γ-curve regardless of magnitude; 1–2 marginal
  violations (< 5% relative) ⇒ "holds with noted exceptions"; any violation
  ≥ 5% ⇒ **L1 REFUTED** — and that cell is a live Goldilocks-advantage
  candidate, to be re-examined at larger n before any paper claim either way.
- The paper reports the outcome whichever way it lands.

## Design (fixed before running)

- **Cells:** 50, seeded rng(20260818); per cell draw independently:
  - target class ~ uniform{e01-chain, SK, RFIM} with fresh instance seed
    (0..49; instance couplings drawn per class constructors in
    src/goldilocks/targets/ising.py),
  - n ~ uniform{4, 5, 6},
  - T ~ log-uniform [0.05, 10]   (widened: peaks live at high T too),
  - α ~ uniform [0.05, 1.0]      (widened: peaks are largest at α = 1).
- **γ grid:** {0} ∪ logspace(−2, 2, 9) in units of Δ₃ = spectral width of H.
- **Kernel:** window-averaged dephased walk, tΔ₃ ∈ [2, 12], 12 time points
  (same family as G01; sparse expm_multiply path).
- **Metric:** exact spectral gap δ = 1 − |λ₂| of the MH transition matrix
  vs the enumerated target (diagnostics.mh_transition_matrix/spectral_gap).
- **Baselines per cell:** Metropolized single-flip (P[y,x] = 1/n on
  Hamming-1 pairs) and uniform-flip (P = 1/2ⁿ), exact gaps.
- **ESS spot-check:** 5 pre-chosen cells (indices 0, 10, 20, 30, 40):
  50k-step chains × 3 seeds at γ ∈ {0, γ_grid[4], γ_grid[8]}, confirm
  ESS/step rank-agrees with the gap (Spearman > 0 across the 3 points).
  Failure ⇒ reported, does not modify L1's verdict rule.
- **Output:** results.csv (every cell × γ, gaps + baselines + flags) and
  G05_RESULTS.md with the verdict against the rules above.

## What would make us abandon the law honestly

A ≥ 5% violation of L1, reproduced at a second seed of the same instance
class and stable under doubling the time-point count, is a positive
noise-assisted-advantage result — the OPPOSITE headline to the paper title.
It would be written up as such, not buried. (E02/E03 discipline.)
