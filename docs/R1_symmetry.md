# R1 — Proposal symmetry of the dephased walk (status: **PASS**, 2026-08-18)

**Question.** Is q_γ(y|x) = ⟨y| e^{tL}(|x⟩⟨x|) |y⟩ symmetric in (x, y) for
L(ρ) = −i[H, ρ] + γ Σᵢ D[Zᵢ](ρ), with H real symmetric? Layden's exactness
free lunch (no q-evaluation in MH) requires it.

## Theorem (pure dephasing, real symmetric H)

For H = Hᵀ real and jump operators {√γ Zᵢ} (any diagonal REAL jump operators
with Aᵀ = A and A†A ∝ I work identically): q_γ(y|x) = q_γ(x|y) for all t, γ.

**Proof (jump-unravelling exchangeability).**
Because Zᵢ†Zᵢ = I, the MCWF unravelling has state-independent jump statistics:
jumps form a Poisson process of rate nγ on [0, t], and each jump applies Zᵢ
with i uniform, independent of everything. Condition on a realization
ω = (m; t₁<…<t_m; i₁,…,i_m). The conditional evolution is the unitary

    W(ω) = U(t−t_m) Z_{i_m} ⋯ Z_{i₁} U(t₁),   U(s) = e^{−iHs}.

so q(y|x) = 𝔼_ω |⟨y|W(ω)|x⟩|².

Each factor is symmetric: U(s)ᵀ = U(s) (H real symmetric) and Zᵢᵀ = Zᵢ
(diagonal). Transposing reverses the order:

    W(ω)ᵀ = U(t₁) Z_{i₁} ⋯ Z_{i_m} U(t−t_m) = W(ω̃),

where ω̃ = (m; t−t_m<…<t−t₁; i_m,…,i₁) is the TIME-REVERSED realization.
Hence ⟨y|W(ω)|x⟩ = ⟨x|W(ω)ᵀ|y⟩ = ⟨x|W(ω̃)|y⟩.

The map ω ↦ ω̃ preserves the law of the jump process: a Poisson process on
[0, t] is invariant under s ↦ t−s (given m, the times are the order
statistics of m iid uniforms — reversal-invariant), and the site labels are
iid uniform, exchangeable. Averaging,

    q(y|x) = 𝔼_ω |⟨y|W(ω)|x⟩|² = 𝔼_ω̃ |⟨x|W(ω̃)|y⟩|² = q(x|y).  ∎

**Corollaries.**
- Averaging/randomizing t (Layden window) preserves symmetry: a mixture of
  symmetric kernels is symmetric. Randomizing γ likewise.
- The theorem justifies `TrajectoryDephasedWalkKernel` reporting log_q ratio 0
  without ever computing q — the free lunch survives dephasing at ANY rate,
  including uncontrolled device DEPHASING. This is the paper's exactness pillar.
- What it does NOT cover: amplitude damping (σ⁻ᵀ = σ⁺ ≠ σ⁻, and A†A ≠ I makes
  jumps state-dependent — both steps fail); complex H (Y terms). Real device
  noise = dephasing + amplitude damping, so H3's hardware claim must either
  (a) bound the T₁-induced asymmetry bias, or (b) estimate q-ratios for the
  damping component. Decision deferred to G03, informed by the measured
  defects below.

## Numerical certification (run_r1.py → R1_results.txt)

- Pure dephasing: max defect ≈ 1e-15 (machine precision) over n ∈ {4,5,6},
  γ/Δ ∈ {0, 0.1, 1, 10}, tΔ ∈ {0.5, 2, 8}.  **CERTIFIED.**
- Amplitude damping κ = 0.1Δ: defect up to ~2e-1 — large, as the theorem
  predicts. Hardware implication: T₁ noise is NOT free; quantify per-device
  in G03 (effective κ̂/γ̂ ratio) before any H3 run.
- Cross-path agreement: dense ≡ sparse (1e-8), trajectories ≡ exact
  (TV < 0.05 @ 4k samples) — tests I8, I9.

## Verdict

**PASS.** The exactness boundary holds for the entire controlled-γ program
(G01, G02) and for dephasing-dominated hardware noise. Phase 1 unblocked.
Open residue → G03: amplitude-damping bias treatment (bound vs estimate).
