# Monotonicity of the MH gap in dephasing — conjecture REFUTED, law corrected

Status: **theory pass complete (2026-08-18).** The G01 conjecture (gap
monotone decreasing in γ for all targets) is FALSE: refuted analytically in
an exactly solvable corner and numerically on real targets. The correct,
falsifiable replacement — the **envelope law** — is pre-registered in
experiments/G05_monotonicity/PREREGISTRATION.md.

## 1. Conjecture v1 (from G01_PILOT_RESULTS.md)

For the window-averaged dephased-walk kernel family, the MH spectral gap
δ(γ) is monotone non-increasing in γ for every target. Motivation: 12/12
pilot cells (n = 6, α ≤ 0.5, T ≤ 1) were monotone; sketch was a
"data-processing" argument via the mixture structure.

## 2. Structure lemma (true, and load-bearing for everything below)

**Lemma.** Let q_γ be the (window-averaged) dephased proposal. Then the MH
transition matrix is an exact convex mixture

    T_γ = E_{t,ω}[ T_{t,ω} ],

where ω is the Poisson(nγ) phase-kick record, T_{t,ω} is the MH chain built
from the kicked-unitary proposal q_{t,ω}(y|x) = |⟨y|W_{t,ω}|x⟩|², and every
member is reversible w.r.t. the same target π.

*Proof.* Each q_{t,ω} is symmetric (R1 / characterization theorem applies
realization-wise after symmetrizing over the time-reversal involution), so
the MH acceptance a(y,x) = min(1, π_y/π_x) is q-independent, and off-diagonal
T(y|x) = q(y|x)·a(y,x) is LINEAR in q. Averaging q averages T off-diagonal;
diagonals absorb the rest. ∎

## 3. Why the naive proof fails (two obstructions)

**Obstruction 1 — concavity points the wrong way.** For reversible chains
sharing π, the Dirichlet form E_T(f) is linear in T, and
δ(T) = inf_f E_T(f)/Var_π(f) is an infimum of linear functionals — CONCAVE
in T. Hence for any mixture, δ(E[T]) ≥ E[δ(T_ω)]: a mixture is at least as
good as the average of its members and CAN beat its best member. The
"mixing kernels cannot beat the best member" intuition from G01 is simply
false. Any true monotonicity must use the γ-structure of the mixture
weights, not mixture-ness alone.

**Obstruction 2 — Peskun ordering fails pointwise.** Monotonicity would
follow from Peskun if q_γ(y|x) were pointwise non-increasing in γ for all
y ≠ x. It is not: at destructive-interference zeros of the coherent walk
(q_0(y|x) = 0), dephasing strictly INCREASES the off-diagonal mass. That is
the ENAQT mechanism itself, alive and well inside the proposal.

## 4. Refutation, part I: fixed quench time

Take α = 1 (pure mixer H = Σᵢ Xᵢ), uniform target, FIXED t = π. Each qubit
is an independent rotation with flip probability sin²t = 0: the γ = 0 chain
is the identity, gap 0. Any γ > 0 gives positive flip probability. Measured
(n = 2, exact Lindblad): δ = 0, 0.145, 0.468, 0.807, 0.990, 0.894 at
γ = 0, 0.05, 0.2, 0.5, 1, 3. **Noise helps enormously at fixed t.**
Conclusion: the conjecture cannot even be posed without window averaging —
time randomization is itself a dephasing-like resource, and at fixed t the
walk keeps interference zeros for noise to fill.

## 5. Refutation, part II: the solvable corner (window-averaged!)

α = 1, uniform target, n qubits, per-qubit dephasing rate γ. The trajectory
picture makes each qubit an independent telegraph-reversed rotation:
θᵢ(t) = ∫₀ᵗ σᵢ(s) ds with σᵢ = ±1 flipping at rate γ, and flip probability
p_γ(t) = (1 − f_γ(t))/2 where f_γ(t) = E[cos 2θ(t)] solves

    f'' + 2γ f' + 4 f = 0,   f(0) = 1, f'(0) = 0
    ⇒ f_γ(t) = e^{−γt}[cos ωt + (γ/ω) sin ωt],  ω = √(4−γ²)   (γ < 2).

(Verified against the exact Lindblad propagator to 6 decimals.) Laplace at
s = 0 gives the exact identity  ∫₀^∞ f_γ dt = γ/2.

All the kernels P_t (and their t-average) are diagonal in the parity basis
χ_S, with eigenvalues λ_S = E_t[f_γ(t)^{|S|}]. Window-average over t ∈ [0,T]:

- |S| = 1 (magnetization modes): E_t[f_0] → 0 — time-averaging kills the
  odd moments; and E_t[f_γ] ≈ γ/2T. Small either way.
- |S| = 2 (parity/correlation modes): E_t[f_0²] = E_t[cos² 2t] → **1/2** —
  time-averaging does NOT kill even moments of the coherent oscillation.
  With γ > 0, f_γ² decays and E_t[f_γ²] = O(1/T) → 0.

So δ(γ=0) = 1/2 while intermediate γ reaches δ ≈ 1 − max(γ/2T, O(1/T)):
**the window-averaged gap has an interior maximum.** Measured (n = 2,
window tΔ ∈ [0,20]): δ = 0.505, 0.874, 0.952, 0.973, 0.923, 0.753 at
γ = 0, 0.1, 0.3, 1, 3, 10 — matching the formula (0.505 ↔ 1/2;
0.753 ↔ 1 − 10/40). Conjecture v1 is **refuted**.

**Mechanism, stated once:** time randomization and dephasing are both phase
randomizers, but time-averaging only kills phases linearly (odd moments);
coherent correlations surviving in even moments (parity observables) are
killed only by genuine decoherence. Noise CAN help mixing — by destroying
coherent structure that the time window cannot reach.

## 6. Reconciling G01: real targets, and where the peak lives

Finer scan on the e01 chain at n = 4 (γ/Δ ∈ {0, .03, .1, .3, 1, 3, 10},
window tΔ ∈ [2,12]): interior peaks exist in EVERY cell, but their size is
controlled by α:

- α = 0.3, 0.5: bumps of ~0–8% over γ = 0 (invisible on G01's coarse grid
  at n = 6 — the pilot's "12/12 monotone" is correct for its cells but not
  a law).
- α = 1.0 (pure mixer, the solvable corner's neighborhood): peaks up to
  2× over γ = 0, e.g. T = 0.3: δ(0) = 0.049 → δ(0.3Δ) = 0.100; T = 1.0:
  0.065 → 0.109.

BUT in all 15 cells the peak stayed BELOW the best classical baseline
(single-flip gap 0.17–0.25, uniform-flip up to 0.55 at high T). Noise
helped the walk only where the walk was not worth using.

## 7. The corrected law (pre-registered → G05)

**Envelope law.** For every target/temperature cell,

    max_{γ>0} δ(γ)  ≤  max( δ(γ=0), δ_single-flip, δ_uniform-flip ).

Noise can create a Goldilocks peak, but never lifts the dephased family
above the envelope of the coherent quench and trivial classical kernels.
Equivalently: **wherever the quantum kernel has an advantage, dephasing only
erodes it; wherever dephasing helps, a classical kernel was already
better.** This is the paper's second pillar in falsifiable form — "exactness
is free, advantage is not."

Consistency checks already in hand: the solvable-corner peak (0.99) sits
below uniform-flip at the uniform target (δ = 1); all 15 n = 4 cells above
satisfy it; all 12 G01 cells satisfy it trivially (monotone, and γ=0 is the
envelope in the advantage cells).

Proof status: OPEN. Plausible route — the dephased kernel lies in the convex
hull of phase-kicked quench kernels; conjecture that this hull's gap
envelope is attained on the boundary {coherent quenches} ∪ {Zeno/classical
limit}. Not attempted further this session; the pre-registered 50-target
test (experiments/G05_monotonicity/) is the paper's evidence either way.

**G05 outcome (same day):** law HOLDS 49/50 with one disclosed +1.17%
instance-specific micro-bump (SK, n=5, T=0.085, α=0.63, γ*≈0.02Δ;
reproduced under doubled time resolution, absent in a fresh instance);
interior peaks in 20/50 cells confirm the refutation of conjecture v1 in
the wild. See experiments/G05_monotonicity/G05_RESULTS.md.

## 8. Status of conjecture v1 artifacts

G01_PILOT_RESULTS.md's conjecture paragraph is superseded by this document.
Its data stand; its extrapolation ("no peak anywhere") does not — the peak
was hiding at α = 1 and in the parity sector.
