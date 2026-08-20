# Characterization theorem — which noise channels preserve proposal symmetry

Status: **PROVED + CERTIFIED** (2026-08-18). Generalizes docs/R1_symmetry.md
(R1 = the pure-dephasing special case). This is the paper's Theorem 1:
"exactness is free."

**Question.** The MH free lunch (no q-evaluation) requires the proposal
q(y|x) = ⟨y| E(|x⟩⟨x|) |y⟩ to be symmetric in (x, y). For which channels E
does symmetry hold? The proposal basis {|x⟩} is real (computational basis)
throughout; transposes are taken in this basis.

## Theorem 1 (transpose-closed Kraus sets ⇒ symmetric proposal)

Let E(ρ) = Σₐ Kₐ ρ Kₐ† be a channel admitting a Kraus representation
{Kₐ}ₐ₌₁..ₘ that is **closed under transposition up to unitary remixing**:

    Kₐᵀ = Σ_b u_{ab} K_b   for some unitary u ∈ U(m).            (TC)

Then q(y|x) = q(x|y) for all x, y.

**Proof.** For real basis vectors, ⟨x|Kₐ|y⟩ = ⟨y|Kₐᵀ|x⟩. Hence

    q(x|y) = Σₐ |⟨x|Kₐ|y⟩|² = Σₐ |⟨y|Kₐᵀ|x⟩|²
           = Σₐ |Σ_b u_{ab} ⟨y|K_b|x⟩|² = Σ_b |⟨y|K_b|x⟩|² = q(y|x),

the last-but-one step because the unitary u preserves the ℓ²-norm of the
amplitude vector v_b = ⟨y|K_b|x⟩. ∎

**Channel-level restatement.** (TC) says {Kₐᵀ} is *also* a Kraus
representation of E. Since {Kₐᵀ} always represents the map Θ∘E★∘Θ (Θ =
transposition, E★ = Heisenberg adjoint, Kraus {Kₐ†}), and two Kraus sets
represent the same channel iff they are unitarily related, (TC) is exactly

    E = Θ ∘ E★ ∘ Θ.                                              (TC′)

So the condition is representation-independent: a channel either has a
transpose-closed Kraus set or it does not.

**(TC) implies unitality.** Unitary mixing preserves Σₐ Aₐ†Aₐ, so (TC) gives
Σₐ (Kₐᵀ)†(Kₐᵀ) = Σₐ Kₐ†Kₐ = I, i.e. conj(Σₐ KₐKₐ†) = I, i.e. E(I) = I.
Consistency check: a symmetric proposal is column-stochastic and symmetric,
hence **doubly stochastic** — and Σₓ q(y|x) = ⟨y|E(I)|y⟩, so

    diag(E(I)) = 1  is *necessary* for symmetry.                 (N)

Non-unital noise with a non-flat diagonal of E(I) — any channel that relaxes
toward a preferred state, e.g. finite-temperature amplitude damping — breaks
symmetry *before any interference argument is needed*.

**On necessity of (TC).** (TC) is sufficient, not necessary: symmetry
constrains only the diagonal-to-diagonal block of E (the transition matrix
P = Pᵀ), while (TC′) constrains the whole superoperator. Contrived channels
can be symmetric without (TC). The honest statement, and the one the paper
makes: (TC) is the natural *structural* characterization — every physically
arising symmetric case below satisfies it, and the physically arising
violator (finite-T damping) already fails the weaker necessary condition (N).

## Theorem 2 (Lindblad semigroups)

Let L(ρ) = −i[H, ρ] + Σⱼ γⱼ D[Lⱼ](ρ) with D[A](ρ) = AρA† − ½{A†A, ρ}.
Suppose:

  (i)   H = Hᵀ real symmetric;
  (ii)  the weighted jump set is transpose-closed: there is a permutation
        j ↦ j′ with Lⱼᵀ = e^{iφⱼ} L_{j′} and γⱼ = γ_{j′};
  (iii) Σⱼ γⱼ Lⱼ†Lⱼ is (real) symmetric — equivalently the effective
        non-Hermitian Hamiltonian H_eff = H − (i/2) Σⱼ γⱼ Lⱼ†Lⱼ satisfies
        H_effᵀ = H_eff.

Then E_t = e^{tL} satisfies (TC) for every t ≥ 0, hence q_t(y|x) = q_t(x|y)
for all t.

**Proof (time-reversed Dyson unravelling — generalizes R1).** The standard
time-ordered decomposition of e^{tL} is the continuous Kraus family indexed
by jump records ω = (m; t₁ < … < t_m; j₁, …, j_m):

    K_ω = G(t−t_m) √γ_{j_m} L_{j_m} ⋯ √γ_{j₁} L_{j₁} G(t₁),
    G(s) = e^{−iH_eff s},

with e^{tL}(ρ) = Σ_m ∫ dt₁…dt_m Σ_{j₁..j_m} K_ω ρ K_ω†. Transposition
reverses the operator order; by (iii) G(s)ᵀ = G(s), and by (ii) each Lⱼᵀ is
a phase times L_{j′} with the *same rate*. Hence

    K_ωᵀ = e^{iΦ(ω)} K_ω̃,   ω̃ = (m; t−t_m < … < t−t₁; j_m′, …, j₁′),

the time-reversed, transpose-relabelled record. The map ω ↦ ω̃ is a
measure-preserving involution of the index set (Lebesgue measure on the
time-simplex is invariant under s ↦ t−s; the rate weights match by (ii)),
and phases are killed by |·|². So the Kraus family is transpose-closed and
Theorem 1 applies. ∎

**Remarks.**
- Condition (iii) is implied by (i)+(ii) when the Lⱼ are real (up to phase)
  and **normal** (LᵀL = LLᵀ): then (Lⱼ†Lⱼ)ᵀ = LⱼᵀL̄ⱼ = Lⱼ†Lⱼ up to the
  matched relabelling. All examples below have normal jumps.
- The time-reversal step is *load-bearing*: naive composition fails, because
  a product of symmetric operators is not symmetric ((AB)ᵀ = BA). This is
  why "each instant is symmetric" does not trivially give "the semigroup is
  symmetric" — R1's exchangeability trick is the general mechanism.
- **Closure properties.** Symmetry survives convex mixtures (Layden's random
  t-window, random γ) and time-reversal-symmetric compositions, but NOT
  arbitrary composition of two different symmetric channels.

## The characterization table (paper Table 1)

| Noise channel | Transpose closure | Symmetric? | Certified defect |
|---|---|---|---|
| Computational-basis dephasing, jumps Zᵢ, any rate | Zᵢᵀ = Zᵢ | YES | ≤ 3.3e−16 (R1) |
| Dephasing in ANY real basis: jump A = V D Vᵀ, V real orthogonal, D real diagonal | Aᵀ = A (real symmetric) | YES | ≤ 1.3e−14 |
| Depolarizing / any Pauli-jump noise (X, Y, Z rates arbitrary) | Xᵀ=X, Zᵀ=Z, Yᵀ=−Y (phase) | YES | ≤ 1e−15 |
| Infinite-temperature relaxation (σ⁻ and σ⁺ at EQUAL rates) | (σ⁻)ᵀ = σ⁺, rates matched | YES | ≤ 1e−15 |
| Amplitude damping (σ⁻ only; finite-T relaxation, unequal rates) | (σ⁻)ᵀ = σ⁺ ∉ set; fails (N): non-unital | NO | ≥ 3.5e−2, up to 5.5e−1 |

The last two rows are the sharpest pair: the *same* jump operators, and the
matching condition γ₊ = γ₋ is exactly what flips symmetry on. Noise that
drives toward the maximally mixed state preserves the free lunch; noise that
knows a preferred state (T₁ relaxation toward |0⟩) breaks it.

## Hardware translation

Device noise ≈ dephasing (T_φ) + amplitude damping (T₁) + gate depolarizing
+ coherent overrotation (real H errors). By the table: T_φ at any rate,
depolarizing gate noise, and real-Hamiltonian miscalibration are ALL exactness-
free. **T₁ relaxation is the unique realistic bias channel.** Any hardware
claim must bound or estimate only the damping component (G03's task as
scoped in R1's corollary) — everything else rides free.

## Numerical certification

`scripts/run_r1.py` (extended 2026-08-18) certifies every row of the table:
worst defect over ALL transpose-closed channels is **1.2e−14** across
n ∈ {4, 5} (n = 6 for computational dephasing), γ/Δ ∈ {0.1, 1, 10},
tΔ ∈ {0.5, 2, 8} (rotated-basis dephasing with a seeded random orthogonal V;
depolarizing with per-site X, Y, Z jumps at rates 0.5γ/0.3γ/γ; equal-rate σ±
relaxation). Both negative controls (amplitude damping; unequal-rate σ± with
γ₊ = γ₋/4) break at defect ≥ 3.5e−2. Full grid in docs/R1_results.txt.
Tests I10–I12 in tests/test_exactness.py pin each class permanently.
