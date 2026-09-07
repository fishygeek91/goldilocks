# PAPER SKELETON — drafted 2026-08-18 (session 4)

**Working title:** Noise cannot help quantum-enhanced MCMC:
exactness is free, advantage is not.

**Thesis in one sentence.** For quantum-walk Metropolis proposals, realistic
decoherence splits cleanly in two: every transpose-closed noise channel
(dephasing in any real basis, depolarizing, infinite-T relaxation) preserves
the evaluation-free exactness of the sampler at ANY strength — but no amount
of tuned dephasing lifts sampling efficiency above the envelope of the
coherent quench and trivial classical kernels. Noise costs nothing and buys
nothing.

**Polarity note.** This is the TASKS.md Phase-5 "either polarity" write-up,
landed as: one positive theorem (exactness), one negative law with a
refuted-conjecture twist (advantage), packaged with the honest-benchmarking
protocol. The twist (noise DOES create Goldilocks peaks — just never above
the classical envelope) is the interesting part; do not flatten it into a
plain negative.

---

## Section outline

### 1. Introduction
- Layden et al. qe-MCMC: coherent quench proposals, empirically
  noise-robust; robustness unexplained, treated as nuisance.
- ENAQT / quantum Goldilocks premise: dephasing as delocalizer; the natural
  conjecture that intermediate noise HELPS sampling on NISQ hardware
  (noise-as-resource: H1–H3 of this project).
- The two-sided answer (thesis sentence above). Contributions list:
  1. Characterization theorem for exactness-preserving noise (Thm 1).
  2. Refutation of gap-monotonicity + the solvable corner showing noise
     genuinely helps mixing — but only sub-classically (Thm 2 + Law).
  3. Pre-registered 50-target envelope-law test (G05).
  4. The benchmarking protocol as a reusable method (TunnelVision).

### 2. Setup
- Target π on {0,1}ⁿ; MH with proposal q; the free lunch: symmetric q needs
  no q-evaluation.
- The dephased-walk family: L = −i[H,·] + γΣᵢD[Zᵢ], H = (1−α)diag(E) + αΣXᵢ
  real symmetric; window-averaged t (Layden). Limits: γ=0 coherent quench,
  γ→∞ Zeno freeze. Exact propagators + trajectory unravelling (one shot =
  one trajectory = one proposal — also the circuit recipe).

### 3. Theorem 1 — exactness is free (docs/characterization_theorem.md)
- Thm 1 (transpose-closed Kraus ⇒ symmetric proposal), 3-line proof.
- Channel-level form E = Θ∘E★∘Θ; representation-independence; (TC) ⇒ unital;
  necessary condition (N): diag E(I) = 1 (symmetric ⇒ doubly stochastic).
- Thm 2 (Lindblad semigroups): time-reversed Dyson unravelling; why naive
  composition fails and time-reversal is load-bearing.
- **Table 1** (channel classes + certified defects; the equal-vs-unequal
  σ± pair as the sharpest illustration).
- Hardware reading: T_φ, depolarizing, coherent miscalibration all free.
  T₁ is the unique realistic bias channel. A device that keeps the
  free-lunch Metropolis ratio (no q-evaluation) on a κ-damped proposal
  q̃ runs the naive kernel P_M rather than Hastings P_H; writing
  ε = max |q̃(y|x)−q̃(x|y)|,
  ||P_M − P_H||_{TV,∞} ≤ ε (1/π_min − 1) and
  ||π̃ − π||_TV ≤ that · π_min^{−1/2} / δ(P_H) (Theorem B,
  docs/amp_damp_bias.md; the un-√ version is empirical only). The gap
  envelope is a guaranteed bound, typically loose by 10⁶–10²¹; measured
  TV is O(ε). Device budget: treat ε ≲ η as the working requirement for
  ||π̃−π||_TV < η, or estimate the T₁ q-ratio and run Hastings.
  Explains Layden's observed robustness as a theorem, now quantitative.

### 4. Theorem 2 + Law — advantage is not (docs/monotonicity.md)
- Conjecture v1 (monotone gap) and its refutation:
  - Structure lemma: T_γ = convex mixture of phase-kicked MH chains.
  - Obstruction: gap is concave over mixtures (Dirichlet form linear) —
    mixtures CAN beat members; "data processing" intuition false.
  - Solvable corner (α=1, uniform π): telegraph f''+2γf'+4f=0,
    ∫₀^∞f = γ/2; parity modes λ_S = E_t[f^|S|]; time-averaging kills odd
    moments only; δ(0) = 1/2 beaten at intermediate γ. Fixed-t version:
    interference zeros make noise arbitrarily helpful at t = π.
    (R2 note: interior-optimum mixing under decoherence is KNOWN —
    Kendon-Tregenna 2003; hypercube: Alagic-Russell 2005, Drezgich et al.
    2009 — cite here; what is new is the window-averaged telegraph
    solution and the odd/even-moment mechanism, per C5 as narrowed.)
  - Mechanism: time randomization and dephasing are both phase
    randomizers; dephasing reaches the even-moment (parity) coherences
    that the time window cannot.
- The envelope law (pre-registered): max_{γ>0} δ(γ) ≤ max(δ(0), δ_SF, δ_UF).
  Noise helps only where the walk was already sub-classical.
- G05 results (experiments/G05_monotonicity/G05_RESULTS.md): 50
  pre-registered random cells; **law holds 49/50** with one disclosed
  +1.17% instance-specific micro-bump (reproduced under doubled time
  points, absent in a fresh instance at the same parameters); interior
  peaks in 20/50 cells (the nuance is generic); 4 advantage cells, all
  monotone-eroding beyond γ ≈ 0.03Δ. G01 pilot data as the
  advantage-regime evidence (n=6, low T: monotone erosion of the quench
  advantage; dephased walk falls below classical by γ ≈ 0.1Δ at T=1).
- Proof status of the law: open; convex-hull boundary conjecture stated.

### 5. Mechanism — why ENAQT does not transfer to sampling
- ENAQT objective: transport to a sink, no filter; everything that arrives
  counts. MH objective: the Metropolis filter prices proposals by energy.
- The coherent quench's value is energy-CONSERVING interference
  (near-degenerate proposals → acceptance at low T); dephasing broadens the
  proposal energy distribution → the filter rejects the spread.
- Quantitative handle (G01 data + solvable corner): delocalization gain
  never outruns acceptance cost in advantage cells.

### 6. Benchmarking protocol (TunnelVision, as method)
- Rules: exactness boundary (kernels never see target log-probs; report
  (y, log_q_fwd, log_q_rev)); ESS/step AND ESS/sec both reported; split-R̂
  ≤ 1.05 gating; error vs enumerated truth at small n; pre-registered kill
  criteria BEFORE data; negative results reported at full strength.
- Case study: how the protocol killed H1 fast (G01), then caught the
  conjecture-v1 overreach (G05 prereg written only after the theory pass).

### 7. Outlook — the energy-concentration advantage predictor
- Forward-looking claim (NOT proven here): the quench's advantage is
  predicted by the proposal mass on near-degenerate pairs,
  C(q) = Σ_{x,y} π(x) q(y|x) · 1[|E(y)−E(x)| ≤ κT] — "energy concentration."
- Everything observed fits it: dephasing lowers C (broadened proposal
  energy) and erodes advantage; time-averaging preserves C (energy
  conservation is per-realization); the α=1 corner has flat E so C is
  trivial and noise can only help sub-classically.
- Proposed test (next project): C(q) vs measured ESS advantage across
  kernels/targets; if predictive, C becomes a design objective — engineer
  kernels for energy concentration, not delocalization.
- Honest escapes from G01 not pursued: site-dependent γᵢ shaping,
  frustrated-basis noise, hitting-time objectives (optimization, not
  sampling).

### 8. Related work
- Lift the FINALIZED table from docs/NOVELTY-CHECK-02.md §3 (R2 verdict,
  2026-08-18). Three groups:
  1. **Decohered-walk mixing (the known phenomenon behind our solvable
     corner — cite prominently, first):** Kendon & Tregenna PRA 67, 042315
     (2003; optimal decoherence p·T ≈ 2.6–5, line/cycle/hypercube);
     Alagic & Russell PRA 72, 062304 (2005; hypercube threshold);
     Fedichkin-Solenov-Tamon QIC 6 (2006; analytic interior optimum,
     cycles); Richter PRA 76, 042306 + NJP 9, 072 (2007; decoherent walks
     always mix, MCMC framing, hypercube threshold mixing); Drezgich et al.
     QIC 9 (2009; complete hypercube characterization, optimal γ/Δ ≈ 1–5,
     same qubit factorization as our telegraph corner); Abal et al.
     0712.0625. QSW umbrella: Whitfield 0905.2942; Caruso NJP 16, 055015.
  2. **qe-MCMC line:** Layden 2203.12497 (γ=0 limit; their SM already
     states the symmetry-on-average robustness condition — credit it; our
     Thm 1/2 is the channel classification); Orfi & Sels PRA 110, 052414
     (worst-case no-speedup for ANY unital proposal — covers our dephased
     family in the worst case; complementary to the per-instance envelope
     law); CGQeMCMC PRR 7, 013231 (noise effect "not investigated");
     2411.17821; 2506.19538; FT-era walks (Lemieux 1910.01659, Claudon
     2506.11576, 2604.15179, Incudini-Mazzola 2607.22818); dissipative
     Gibbs samplers (2304.04526, 2311.09207 — engineered dissipation,
     different machine model).
  3. **ENAQT:** Rebentrost NJP 11; Lloyd-Mohseni 1111.4982 (citation tree
     transport-only); digital ENAQT 2111.02897 (+2404.06264); D-Wave
     2109.01690.
- Positioning (post-R2, honest): first channel-level exactness
  characterization for noisy walk proposals (upgrading Layden's SM
  condition to a classification); first study of decohered-walk MIXING
  results embedded in an exact-MH sampler with Gibbs targets; the envelope
  law as the negative answer to noise-as-resource for SAMPLING — the
  interior-optimum mixing phenomenon itself is 2003–2009 walk literature
  and is cited as such, and the Metropolis filter is precisely what
  separates our verdict from theirs (walk-vs-walk, uniform target, no
  filter ⇒ noise wins; kernel-vs-envelope, Gibbs target, MH filter ⇒
  noise never wins).
- **R2 status: CLOSED 2026-08-18** (docs/NOVELTY-CHECK-02.md verdict;
  claim sentence there is the paper's claim). Refresh sweep at submission;
  Scholar alerts still to be set manually.

---

## Claims register (claim → evidence → status)

| # | Claim | Evidence | Status |
|---|---|---|---|
| C1 | Transpose-closed Kraus ⇒ symmetric proposal (exactness free) | Thm 1 proof; certification defect ≤ 1.2e−14 (4 channel classes, run_r1.py); credit Layden SM for stating the symmetry-on-average condition — ours is the channel classification | PROVED + CERTIFIED |
| C2 | Extends to Lindblad semigroups w/ real-symmetric H, transpose-closed jumps | Thm 2 (Dyson time-reversal); same certification | PROVED + CERTIFIED |
| C3 | T₁ (finite-T damping) is the unique realistic bias channel; naive-Metropolis vs Hastings obeys ||P_M−P_H||_{TV,∞} ≤ ε(1/π_min−1) and ||π̃−π||_TV ≤ that·π_min^{−1/2}/δ (Thm B; un-√ version empirical only) | Thm A/B in docs/amp_damp_bias.md; R1 defect 3.5e−2–0.41 in current file (narrative 0.55 is an older grid); certified n≤5, 3 cells × 5 κ/Δ (measured TV ~ O(ε); gap envelope loose by 10⁶–10²¹) | PROVED + BOUNDED + CERTIFIED |
| C4 | Gap-monotonicity in γ is FALSE in general | solvable-corner analytics + fixed-t counterexample + n=4 peaks | PROVED (refutation) |
| C5 | Noise can strictly improve window-averaged mixing (parity modes) — **NARROWED per R2**: the interior-optimum phenomenon is known (Kendon-Tregenna 2003; Fedichkin et al. 2006; hypercube: Alagic-Russell 2005, Drezgich et al. 2009); ours is the exact window-averaged telegraph solution + odd/even-moment mechanism + MH embedding | telegraph solution, δ: 0.5 → 0.97; Lindblad-verified | PROVED (solvable corner); phenomenon KNOWN — claim only the analysis + embedding |
| C6 | Envelope law: noise never beats max(coherent, classical) | pre-registered G05, 50 random targets; complementary to Orfi-Sels PRA 110, 052414 (worst-case unital bound — covers dephased proposals on their adversarial instance; ours is per-instance, family-wide, quantitative) | HOLDS 49/50 + one +1.17% noted exception |
| C7 | In advantage cells, dephasing erodes beyond γ≈0.03Δ (sub-2% micro-bumps below) | G01 pilot (12/12), G05 L2(b) 4/4 | MEASURED (pilot + G05) |
| C8 | Energy concentration predicts advantage | M01 zoo test (2026-08-31): 14 kernels × 18 cells, exact gaps; scalar C(κT): per-cell median ρ_s = −0.07 with systematic informed-local counterexamples | REFUTED as scalar (test in §7.1) |
| C9 | Concentration AT DISTANCE predicts advantage: C_far (|ΔE|≤2 raw AND d_H≥3) — window set by coupling scale, not T | M01: per-cell median ρ_s = +0.84 (min +0.26); quench top-ranked by C_far 16/18 cells (mean rank 1.17), top by gap 18/18 | MEASURED (n≤10 exact tier); refined conjecture beyond |
| C10 | Shell sufficiency + classical gap: uniform-on-shell oracle (ε≈2–4) matches/beats quench gap on every instance (ε≲1 can disconnect); no implementable classical kernel in the zoo (local, demon, DLP, soft-spin, MTM) reaches the quench — 1.8–26× gap deficit (median 11×); more local information hurts monotonically | D01/D02/M01 (tunnelvision experiments/D01_demon) | MEASURED (n≤10 exact tier) |
| C11 | ICM (Houdayer two-replica cluster moves) is not the cheap shell kernel: faithful move = exact replica swap on all-to-all (no-op); restricted clusters lose pair-energy conservation (acceptance 0.000 at T=0.1); disagreement set empty in 52–100% of stationary draws at T=0.1; mixed into single-flip, pair gap never above the dilution floor 0.50–0.51× | M02 (tunnelvision experiments/D01_demon/M02_ICM_RESULTS.md, m02a/m02b CSVs) | MEASURED (n=8 exact pair tier; n=10 proposal stats) |
| C12 | De-novo classical shell sampling via CNF (SAT+XOR hashing): exact vs enumeration (sym-diff 0, 12/12), TV ≤ 0.03 from uniform (M03a, VALID). Timing rows of M03b/M04 labelled "cold" were generated by a chain with a uint8 wraparound bug (2*x−1 → 255): those states were NOT low-energy; their timings are real measurements of arbitrary states but the depth attribution is WITHDRAWN and superseded by C13 | M03/M04 CSVs stand as data; depth claims superseded by M05 | PARTIALLY WITHDRAWN 2026-09-07 |
| C13 | Depth law + PB-native flank (temperature ladder, n=20, correct states): CNF sampler cost rises 0.15 s (T=30, ~2^17 members) → 4 s (T≈T_c, ~10^3) → 10^2–10^3 s censored (T<T_c, 10^2–10^0 members, shells shrink and empty); Exact (PB-native) enumerates the same deep shells in 0.1–36 s, 10–3,500× faster; certified CNF tools (UniGen/ApproxMC) time out. Residual PB-native gap to quench (1e-2 s) is 1–3 orders at n=20; n-scaling with PB-native solver NOT measured | M05 (tunnelvision experiments/M05_depth/) | MEASURED (seeds 1–2 complete, seed 3 in progress at writing) |

## Figures list

0. **Fig 6 — concentration at distance (§7.1):** (a) gap vs C8 scalar (fails); (b) gap vs C_far with quench + shell oracle (holds). [data: paper/figures/data/m01_cfar_full.csv; script: paper/figures/fig6_concentration_at_distance.py; verify-locked: ρ medians −0.07/+0.84, quench rank ≤1.6]

1. **Fig 1 — Table 1 as a figure:** symmetry defect vs channel class
   (log scale, machine precision to 0.5); the equal/unequal σ± pair
   highlighted. [data: docs/R1_results.txt; script: paper/figures/fig1_symmetry.py]
2. **Fig 2 — the solvable corner:** (a) f_γ(t) curves; (b) window-averaged
   gap vs γ showing the peak, with parity-mode explanation inset (λ_{|S|=1}
   vs λ_{|S|=2}). [data: docs/monotonicity.md §5 formula; script: paper/figures/fig2_solvable_corner.py]
3. **Fig 3 — G01 γ-scan:** gap vs γ at n=6 across (T, α) cells; the
   monotone erosion in advantage cells; ESS/step overlay where R̂-passable.
   Caption: T=0.1 cells gap-only (ESS unmeasurable at 50k steps, R̂-gated).
   [data: results_ess_confirm.csv; script: paper/figures/fig3_g01_scan.py]
4. **Fig 4 — the envelope law:** per-cell peak gap vs envelope (scatter,
   50 cells, diagonal = law boundary); margins histogram inset.
   [data: experiments/G05_monotonicity/results.csv; script: paper/figures/fig4_envelope.py]
5. **Fig 5 (outlook) — energy-concentration cartoon:** proposal energy
   distribution at γ=0 vs γ>0 against the Metropolis acceptance window.

## Open items before first full draft

- [x] G05 verdict lands in §4 and C6/C7 — done (49/50 + noted exception).
- [x] ESS confirmation of G01 pilot at n=6 — DONE 2026-08-18
      (run_g01_ess_confirm.py; addendum in G01_PILOT_RESULTS.md): rank
      agreement 12/14 scored cells, zero ESS peaks, envelope holds on
      ESS/step and ESS/sec. Fig 3 caption must note T=0.1 cells are
      gap-only (ESS unmeasurable at 50k steps; R̂-gated).
- [x] R2 novelty sweep (§8 TODO) — CLOSED 2026-08-18; mixing-time item hit,
      C5 narrowed, claim sentence finalized in docs/NOVELTY-CHECK-02.md §4.
- [x] Amplitude-damping bias BOUND — DONE 2026-08-19
      (docs/amp_damp_bias.md; scripts/run_amp_damp_bias.py; test I13).
      Per-step ||P_M−P_H||_{TV,∞} ≤ ε(1/π_min−1); stationary ≤ that/δ.
      Certified n≤5. C3 upgraded. Hardware section is now quantitative.
- [x] Venue/format — **recommend PRX Quantum article**, not PRL+supplement.
      Two theorems, a refuted-conjecture twist, a 50-cell prereg, a
      reusable protocol, a T₁ bias bound, and four data figures is a
      methods/results paper. PRL's 3750 words would force the envelope-law
      nuance (peaks exist; they never win) and the T₁ bound into a
      supplement that reviewers of a "noise cannot help" claim will
      actually need. Stay at PRX Quantum length; do not draft a PRL cut.
