# G01 pilot — exact-gap γ-scan (2026-08-18)  **H1: preliminary NEGATIVE**

Setup: n=6, window-averaged dephased-walk kernel (tΔ ∈ [2,12], 6 points),
exact MH spectral gap vs enumerated target. Grid: γ/Δ₃ ∈
{0, .03, .1, .3, 1, 3, 10}; targets e01-chain and SK; T ∈ {0.1, 0.3, 1.0};
mixer weight α ∈ {0.05, 0.15, 0.3, 0.5} (small α = Anderson-localized
coherent walk — the regime where ENAQT logic most predicts a noise peak).

## Result: 12/12 cells MONOTONE DECREASING in γ. No interior peak anywhere.

Representative (gap):

| cell | γ=0 | γ=0.1Δ | γ=Δ | γ=10Δ | single-flip |
|---|---|---|---|---|---|
| chain T=0.1 α=.5 | 8.3e-4 | 1.4e-4 | 2.5e-6 | 3.0e-8 | 3.9e-9 |
| sk T=0.3 α=.5 | 4.5e-2 | 4.7e-3 | 1.4e-4 | 1.3e-5 | 4.9e-4 |
| sk T=0.3 α=.05 (localized) | 1.2e-5 | 1.0e-5 | 2.6e-6 | 2.8e-7 | — |
| chain T=1.0 α=.5 | 2.1e-2 | 1.1e-2 | 1.8e-3 | 1.8e-4 | 1.8e-2 |

γ=0 (pure quench) is optimal in every cell; the E01-type quantum advantage
over single-flip persists at low T but is strictly ERODED by dephasing, and
at T=1 the dephased walk falls below the classical baseline by γ≈0.1Δ.

## Why ENAQT does not transfer (working explanation)

ENAQT's objective is transport to a sink with NO acceptance filter: noise
breaks destructive-interference traps and everything that arrives counts.
The MH objective interposes the Metropolis filter: the coherent quench's
value is precisely its energy-CONSERVING interference (proposals concentrate
on near-degenerate states → high acceptance at low T). Dephasing broadens
the proposal's energy distribution; the filter then rejects the spread. The
delocalization benefit never outruns the acceptance cost — even when the
γ=0 walk is strongly localized (α=0.05), where delocalization gain should
be maximal. Conjecture worth one theory pass: for kernels of this family,
gap(γ) is monotone decreasing ∀ targets (a data-processing-style argument —
dephasing = convex mixture of phase-kicked unitaries, and mixing kernels
cannot beat the best member on gap?  NB the best member at every kick
realization has the same |⟨y|W|x⟩|² structure... make precise or refute).

> **ADDENDUM (2026-08-18, session 4): conjecture REFUTED — see
> docs/monotonicity.md.** Mixtures CAN beat their best member (gap is
> concave over mixtures), and interior peaks exist in every n=4 cell on a
> finer scan (large at α=1, invisible at α≤0.5 on this pilot's grid). The
> pilot's 12 cells stand; the "no peak anywhere" extrapolation does not.
> The corrected, pre-registered claim is the ENVELOPE LAW
> (experiments/G05_monotonicity/): noise never lifts the family above
> max(γ=0 quench, classical baselines).

## ADDENDUM (2026-08-18, session 5): ESS CONFIRMATION at n=6 — pilot CONFIRMED

Run: run_g01_ess_confirm.py (full protocol: ESS/step AND ESS/sec, 50k steps
× 5 seeds, split-R̂ ≤ 1.05 gating) over exactly this pilot's 24 (target, T,
α) cells × {γ grid + single-flip + uniform} = 216 kernel-cells. Data:
results_ess_confirm.csv, log run_g01_ess_confirm.log; analysis:
analyze_ess_confirm.py. n=8/10 not attempted (trajectory kernel not wired
into the runner — dense table is n≤6).

**Verdict: ESS rank-agrees with the pilot's gap ordering; no ESS peak
anywhere; the pilot's H1-negative stands on the full protocol.**

- Gating: 92/216 kernel-cells R̂-gated (frozen/near-frozen chains at large
  γ and the slow chains at T=0.1 — the G05 ESS pathology, excluded exactly
  as the protocol intends; e.g. single-flip at T=0.1 reports a garbage
  ESS/step of 0.41 at acceptance 4e-5 with R̂ = 70).
- Rank agreement: of the 14/24 cells with ≥3 non-gated γ points,
  Spearman ρ(gap, ESS/step) > 0.8 in 12/14, exactly 1.0 in 9.
- H1 kill criterion on ESS (pre-registered rule in run_g01.py): 0/24 cells
  show an interior γ beating both γ=0 and the largest γ outside ±2 SE.
- Envelope on ESS: no γ>0 beats max(γ=0, classical baselines) on ESS/step
  OR ESS/sec in any cell. The one automated flag (chain T=0.1 α=0.5) is
  the pilot's known ADVANTAGE cell: the walk family beats uniform-flip
  there (the quantum advantage itself, as it should); within the family,
  ESS differences across γ ∈ {0, 0.03, 0.1} are within 1 SE
  (0.021±0.011 / 0.023±0.010 / 0.028±0.010) — no significant reversal of
  the gap's monotone erosion, and γ ≥ 0.3 is R̂-gated.
- The two imperfect-rank cells (sk T=0.1 α=0.3, ρ=0.71; sk T=0.3 α=0.15,
  ρ=0.40): ESS(magnetization) bumps at γ ∈ [0.3, 1] where gaps are
  1e-5–1e-7 — observable-specific decorrelation (higher acceptance ⇒ fast
  in-basin motion) vs the worst-case spectral gap; irrelevant to the
  verdict since uniform-flip dominates both cells by 5–25× on ESS.
- Honest limitation for Fig 3: at T=0.1 (chain) and other tiny-gap cells,
  50k-step chains cannot mix (gap ≤ 1e-6 ⇒ relaxation ≫ chain length), so
  ESS is unmeasurable and the R̂ gate excludes them; the exact gap remains
  the evidence in those cells and the figure caption must say so.

## Status / what would change the verdict

- ~~Pilot is gap-only, n=6, one t-window family. ESS confirmation is cheap
  and expected to agree (gap and ESS tracked in TunnelVision throughout).~~
  DONE — see addendum above; agreement confirmed under R̂ gating.
- Untested escapes: (a) engineered non-uniform dephasing (site-dependent γᵢ
  shaping WHERE proposals land, not just how coherent they are); (b) noise in
  the BASIS of the problem's frustrated subspace rather than computational;
  (c) transport-style objectives (hitting time to a target set, e.g. ground-
  state search) where the sink analogy is literal — closer to optimization
  than sampling. These are new hypotheses, not rescues of H1.
- H2/H3 are moot as stated (no γ* exists). G02/G03/G04 do not proceed in
  their current form.

## The live positive result from Phase 0

R1 THEOREM (docs/R1_symmetry.md): proposal symmetry — hence MH exactness
with zero q-evaluation — survives computational-basis dephasing at ANY rate
(certified to 3e-16). This is a formal proof of the noise-robustness Layden
et al. observed empirically, plus a proof that amplitude damping (defect up
to 0.55) is the ONLY bias channel to worry about on hardware. Candidate
headline for the honest-benchmarking paper: "dephasing-invariant exactness,
dephasing-eroded advantage" — both halves now proven/measured.
