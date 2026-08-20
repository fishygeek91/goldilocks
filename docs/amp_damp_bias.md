# Amplitude-damping sampling-bias bound

Status: **PROVED + CERTIFIED** (2026-08-19). Upgrades the characterization
residue (T₁ breaks proposal symmetry; defect 3.5e−2–0.41 in the current
`docs/R1_results.txt`) to a quantitative statement about the **free-lunch
Metropolis kernel** a hardware run actually uses. This is the paper's
hardware-section number: exactness is free for every transpose-closed
channel, and for T₁ we now have a proved per-step TV bound plus a crude
stationary envelope.

## 1. Setup — which two kernels?

Let q̃ be a **fixed** κ-damped proposal (window-averaged Lindblad, any
γ ≥ 0; certification uses γ = 0 to isolate T₁). Two Metropolis–Hastings
kernels share the same q̃ and the same target π:

- **P_H** (Hastings / exact). Acceptance
  `a_H(y,x) = min(1, π(y) q̃(x|y) / (π(x) q̃(y|x)))`.
  Implemented as `mh_transition_matrix`. Stationary = π exactly, even
  though q̃ is asymmetric.
- **P_M** (naive Metropolis / device free lunch). Acceptance
  `a_M(y,x) = min(1, π(y)/π(x))` — the q-ratio is ignored.
  Implemented as `naive_metropolis_matrix`. Stationary π̃ ≠ π in general.

This is the hardware question. A device that keeps Layden's free lunch
(no q-evaluation) is running P_M. A device that estimates the T₁
q-ratio, or that has only transpose-closed noise, is running P_H and
stays exact.

The theorem is **not** ||P_{κ=0} − P_κ||. That difference is a
proposal-TV statement and is not controlled by the symmetry defect.

Write ε = max_{x,y} |q̃(y|x) − q̃(x|y)| for the R1 defect, and
r = π(y)/π(x), ρ = q̃(x|y)/q̃(y|x) (ρ := 1 if q̃(y|x) = 0; those
pairs do not contribute to off-diagonal mass).

## 2. Theorem (per-step TV)

**Theorem A.** For every state x,

    ||P_M(·|x) − P_H(·|x)||_TV
        ≤ Σ_{y ≠ x} (π(y)/π(x)) |q̃(y|x) − q̃(x|y)|
        ≤ ε (1/π(x) − 1).

Uniformly over x,

    ||P_M − P_H||_{TV,∞}  ≤  ε (1/π_min − 1),

where π_min = min_x π(x) and
||·||_{TV,∞} = max_x ||·(·|x)||_TV.

The first line is the tighter column form (used in the cert table as
`bound_step_col`). Acceptance ratios enter only through r = π(y)/π(x).

**Proof.** For y ≠ x,
|P_M(y|x) − P_H(y|x)| = q̃(y|x) |min(1, r) − min(1, r ρ)|.
The elementary inequality |min(1, a) − min(1, b)| ≤ |a − b| with
a = r, b = r ρ gives
|min(1, r) − min(1, r ρ)| ≤ r |1 − ρ|, hence

    |ΔP(y|x)| ≤ q̃(y|x) · r · |1 − ρ|
              = (π(y)/π(x)) |q̃(y|x) − q̃(x|y)|.

The diagonal difference equals −Σ_{y ≠ x} ΔP(y|x), so
|ΔP(x|x)| ≤ Σ_{y ≠ x} |ΔP(y|x)|. Therefore

    ||ΔP(·|x)||_TV
        = (1/2) Σ_y |ΔP(y|x)|
        ≤ Σ_{y ≠ x} |ΔP(y|x)|
        ≤ Σ_{y ≠ x} (π(y)/π(x)) |q̃(y|x) − q̃(x|y)|
        ≤ ε (1 − π(x))/π(x)
        = ε (1/π(x) − 1).  ∎

**Corollary.** If ε = 0 (every transpose-closed channel in Table 1),
then P_M = P_H and there is no free-lunch bias. T₁ is still the unique
realistic channel that can make ε > 0.

## 3. Theorem (stationary TV, crude)

**Theorem B.** Let δ = δ(P_H) = 1 − |λ₂(P_H)| be the spectral gap of the
exact Hastings kernel (reversible w.r.t. π). Then

    ||π̃ − π||_TV  ≤  (1/δ) · π_min^{−1/2} · ||P_M − P_H||_{TV,∞}
                   ≤  ε (1/π_min − 1) π_min^{−1/2} / δ.

**Proof.** Stationarity gives π̃ P_M = π̃ and π P_H = π, so

    (π̃ − π)(I − P_H)  =  π̃ (P_M − P_H)  =:  ν      (row-vector convention).

Work in L²(π) via densities f = dμ/dπ. P_H is reversible, so the action
of P_H on densities is self-adjoint in L²(π) with spectrum {λᵢ}; on the
mean-zero subspace, (I − P_H) is invertible with
||(I − P_H)^{-1}||_{L²(π)} = 1/min_{i≥2}|1 − λᵢ| ≤ 1/(1 − |λ₂|) = 1/δ
(for λᵢ < 0, |1 − λᵢ| > 1 > δ). Both π̃ − π and ν are mean-zero. Hence
with f = d(π̃−π)/dπ and g = dν/dπ:

    ||π̃ − π||_TV = (1/2)||f||_{L¹(π)} ≤ (1/2)||f||_{L²(π)}
                 ≤ (1/2δ)||g||_{L²(π)},

and ||g||²_{L²(π)} = Σ_y ν(y)²/π(y) ≤ (1/π_min)(Σ_y |ν(y)|)² ,
so ||g||_{L²(π)} ≤ π_min^{−1/2} · 2||ν||_TV. Finally
||ν||_TV = ||π̃(P_M − P_H)||_TV ≤ max_x ||(P_M − P_H)(·|x)||_TV
= ||P_M − P_H||_{TV,∞} (a π̃-average of column TVs). Combining gives the
first line; Theorem A gives the second. ∎

**Remark (the un-√ envelope).** The simpler expression

    B_naive = ε (1/π_min − 1) / δ

(Theorem B without the π_min^{−1/2} factor) is NOT proved here — the
1/δ inverse bound lives in L²(π), and passing to TV costs the
π_min^{−1/2}. B_naive is reported in the certification table because it
is the natural first guess and it *also* held in every measured cell
(with 10⁶–10²¹ slack); treat it as empirical, the theorem is the line
above.

**Looseness, stated once.** The factor π_min^{−3/2}/δ is exponentially
pessimistic at low T: π_min is Gibbs-small and δ is the worst-case
spectral gap. This is a **guaranteed envelope**, not a prediction.
Empirically (table below) the measured stationary TV is O(ε), while
the envelope sits 10⁶–10²¹ above it. The per-step bound is the
hardware-useful statement; the stationary bound exists so the paper
does not claim "we have no control on π̃."

A device budget that needs ||π̃ − π||_TV < η should treat ε ≲ η as
the working requirement (what the numbers do), not ε ≲ η δ π_min
(what the envelope says). If that is too tight for the device's T₁,
estimate the q-ratio and run Hastings.

## 4. Certification

`scripts/run_amp_damp_bias.py` → `docs/amp_damp_bias_results.csv`.
Exact dense Lindblad, γ = 0, window tΔ₃ ∈ [2, 12] with 6 points
(G01 convention). Three e01-chain cells, κ/Δ₃ ∈ {0.01, 0.03, 0.1, 0.3, 1.0}.
Every row satisfies P_H π = π, TV_step ≤ bound_step, TV_step ≤
bound_step_col, TV_stat ≤ bound_stat (the empirical B_naive), and
TV_stat ≤ bound_stat_rig = B_naive · π_min^{−1/2} (Theorem B).
Pinned by test I13.

| n | T | κ/Δ | ε | TV_step | bound_step | TV_stat | bound_stat | slack |
|---|---|---|---|---|---|---|---|---|
| 4 | 1.0 | 0.01 | 3.93e−2 | 3.97e−2 | 1.20e+4 | 6.99e−2 | 1.25e+5 | 1.8e6× |
| 4 | 1.0 | 0.03 | 1.12e−1 | 1.04e−1 | 3.42e+4 | 1.85e−1 | 2.73e+5 | 1.5e6× |
| 4 | 1.0 | 0.10 | 3.17e−1 | 3.27e−1 | 9.66e+4 | 4.16e−1 | 1.41e+6 | 3.4e6× |
| 4 | 1.0 | 0.30 | 6.38e−1 | 7.32e−1 | 1.95e+5 | 6.20e−1 | 1.47e+7 | 2.4e7× |
| 4 | 1.0 | 1.00 | 9.19e−1 | 9.70e−1 | 2.80e+5 | 8.65e−1 | 1.92e+9 | 2.2e9× |
| 4 | 0.3 | 0.01 | 3.93e−2 | 1.53e−2 | 1.52e+16 | 2.54e−2 | 1.31e+17 | 5.2e18× |
| 4 | 0.3 | 0.03 | 1.12e−1 | 4.00e−2 | 4.33e+16 | 7.54e−2 | 3.61e+17 | 4.8e18× |
| 4 | 0.3 | 0.10 | 3.17e−1 | 8.19e−2 | 1.22e+17 | 2.40e−1 | 2.22e+18 | 9.2e18× |
| 4 | 0.3 | 0.30 | 6.38e−1 | 1.23e−1 | 2.46e+17 | 5.69e−1 | 2.53e+19 | 4.4e19× |
| 4 | 0.3 | 1.00 | 9.19e−1 | 8.67e−1 | 3.55e+17 | 8.26e−1 | 8.70e+20 | 1.1e21× |
| 5 | 1.0 | 0.01 | 3.67e−2 | 3.77e−2 | 2.04e+5 | 1.20e−1 | 3.19e+6 | 2.6e7× |
| 5 | 1.0 | 0.03 | 1.05e−1 | 1.15e−1 | 5.85e+5 | 2.91e−1 | 7.78e+6 | 2.7e7× |
| 5 | 1.0 | 0.10 | 3.10e−1 | 3.78e−1 | 1.72e+6 | 5.44e−1 | 6.92e+7 | 1.3e8× |
| 5 | 1.0 | 0.30 | 6.47e−1 | 8.46e−1 | 3.59e+6 | 6.75e−1 | 4.50e+9 | 6.7e9× |
| 5 | 1.0 | 1.00 | 9.27e−1 | 9.94e−1 | 5.15e+6 | 8.98e−1 | 2.38e+12 | 2.6e12× |

(bound_stat here is B_naive; the proved bound_stat_rig is larger by
π_min^{−1/2} and holds a fortiori — full columns in the CSV.)

Read-off: TV_step tracks ε (sometimes a few tens of percent above it);
TV_stat is the same order, typically 0.7–3× TV_step. The gap envelope
is finite and holds, and is useless as a numerical prediction. At T = 0.3
the uniform bound is vacuous (π_min ~ 10⁻¹⁸) while the *measured* bias
at device-relevant κ/Δ = 0.01 is still only 2.5%.

## 5. Scope notes

- The bound is for **naive Metropolis vs Hastings on the same q̃**, not
  for "damping changes the walk." Hastings on a T₁-damped proposal is
  still exact; the cost is evaluating the q-ratio.
- Transpose-closed channels have ε = 0, so the free lunch stays exact
  at any strength (Theorems 1–2 of `docs/characterization_theorem.md`).
- R1 file max amp-damp defect is **0.352** (κ = 0.1 Δ, tΔ ≤ 8). The
  narrative "up to 0.55" is from an earlier/different grid and is **not**
  in the current `docs/R1_results.txt`. This document uses the file.
  Window-averaged κ-scans here reach ε ≈ 0.93 at κ = Δ, as expected:
  long-time T₁ relaxation is almost maximally asymmetric.
- n ≤ 5 is the dense-Lindblad ceiling. No claim is made at hardware n.
- No claim that T₁ is negligible on devices. The claim is: T₁ is the
  *only* realistic term to budget, the per-step TV error is O(ε), and
  ε is the R1 defect (a few percent at κ ~ 0.01 Δ on the G01 window;
  tens of percent at κ ~ 0.1 Δ).
- Low-T: the proved envelope cannot certify a small stationary bias.
  Either keep κt ≪ 1 (so ε itself is small — the T = 0.3, κ/Δ = 0.01
  row) or estimate the q-ratio.
