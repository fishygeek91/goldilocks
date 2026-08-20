# Goldilocks — task plan

Single source of truth for status. Update checkboxes + the log at the bottom.
Rules: R1 gates everything in Phase 1+. Kill criteria in README §2 are binding.
Every experiment reports ESS/step AND ESS/sec, split-R̂ ≤ 1.05 gating, and
error vs enumerated truth wherever n permits enumeration.

## Phase 0 — Research gates (no code beyond scratch until both close)

- [ ] **R1: Proposal symmetry** (exactness-critical; docs/R1_symmetry.md)
  - [ ] Analytic attempt: show q_γ(y|x) = q_γ(x|y) for E_γ = exp(t·L),
        L = -i[H,·] + γ Σᵢ D[Zᵢ], H real symmetric. Sketch: L preserves the
        real-symmetric structure ⇒ transition matrix P(y|x) = ⟨y|E(|x⟩⟨x|)|y⟩
        symmetric. Verify the argument carefully (vectorized-L transpose
        symmetry), including the diagonal-energy term in H.
  - [ ] Numerical certification: n=4–6 dense Lindblad, max |q(y|x)−q(x|y)|
        over all pairs, sweep γ ∈ {0, 0.1Δ, Δ, 10Δ}, t ∈ 3 values.
  - [ ] Break it on purpose: add amplitude damping (device-realistic) and
        measure the asymmetry ⇒ quantifies how much of H3 survives real noise;
        decide fallback (symmetric-noise restriction vs bias bound).
  - Exit: verdict written in docs/R1_symmetry.md. If symmetry fails even for
    pure dephasing ⇒ STOP, rethink kernel (e.g. Kraus-symmetric collision walk).
- [ ] **R2: Novelty check** (docs/NOVELTY-CHECK-02.md)
  - [ ] Citation sweep: papers citing 2203.12497 (again, now for walk/noise
        angles), 1111.4982, 2111.02897; QSW mixing-time literature
        (Whitfield/Govia/Schuld-era quantum stochastic walks); "noise-assisted"
        + "sampling/Metropolis/MCMC" crossings.
  - [ ] Verify the two limits are as believed: γ=0 ≡ Layden quench (same H
        family, same measurement); γ→∞ Zeno limit ⇒ which classical kernel
        exactly (lazy single-flip?). Write it down — it defines our baselines.
  - Exit: nearest-neighbor table + explicit claim statement, or pivot note.

## Phase 1 — G01: γ-scan on Ising (the H1 experiment)

- [ ] Lindblad propagator `src/goldilocks/lindblad.py`: dense superoperator for
      n ≤ 8; quantum-trajectory (MCWF) sampler for n ≤ 12. Cross-validate the
      two at n=6 (TV distance of proposal matrices < 1e-6).
- [ ] Kernel `kernels/dephased_walk.py`: params (γ, t, α); returns
      (y, log_q_fwd, log_q_rev); with R1-symmetry ⇒ log-ratio 0, but keep the
      interface honest. Register with TunnelVision engine untouched.
- [ ] Baselines wired: uniform-flip, single-flip, ADS (classical), γ=0 quench
      (must reproduce E01 numbers — regression anchor), explicit γ→∞ kernel.
- [ ] The scan: E01 Ising target, n = 6, 8, 10; T ∈ {0.1, 0.3, 1.0};
      γ/Δ ∈ log-grid 10⁻² … 10², ~9 points; t averaged over Layden's window.
      Metrics: exact spectral gap δ(P) (enumerable at these n), ESS/step,
      ESS/sec, acceptance rate.
- [ ] Verification pass: seeds ×5, gap-vs-ESS consistency, R̂ gating; write
      G01_RESULTS.md with the honest verdict against H1's kill criterion.
  - Exit: H1 verdict on Ising. Peak ⇒ Phase 2. No peak ⇒ one target-class
    retry (frustrated/glassy instance where coherent walk should localize
    hardest — ENAQT logic says noise helps MOST there), then verdict.

## Phase 2 — G02: the constant hunt (H2)

- [ ] Targets: ferromagnetic Ising (G01), frustrated/spin-glass instances
      (SK-like at small n), random-field Ising; low-T regime prioritized
      (TunnelVision lesson #2: go where classical kernels are exponentially bad).
- [ ] For each target where H1 holds: locate γ* (refined scan around the peak),
      compute candidate Δ definitions (mixer strength α; median |ΔE| over walk
      edges; spectral width of H). Test γ*/Δ invariance across targets, sizes,
      temperatures for each Δ definition — the definition that makes it
      constant IS the result.
- [ ] Falsification honesty: pre-register the invariance tolerance (≤ 10×
      drift) before looking. Write G02_RESULTS.md either way.

## Phase 3 — G03: circuits (only if H1 survives)

- [ ] Implement the two unravellings from 2111.02897 (stochastic-Hamiltonian
      phase kicks; collision scheme with ancilla resets) as Qiskit circuits;
      validate against Lindblad at n=6.
- [ ] Aer realistic-noise runs: does the device's native noise land the
      effective γ̂ near γ*? (Recall E03: Aer λ̂≈0.65 — measure, don't assume.)
- [ ] ESS/sec at circuit level with honest shot/latency accounting — the E02c
      kill-shot test, applied to ourselves before anyone else does.

## Phase 4 — G04: hardware (only if G03 ESS/sec is not hopeless)

- [ ] γ-tuning via idle-delay insertion / dynamical-decoupling *removal*;
      calibrate effective γ̂ per device.
- [ ] H3 test: hardware walk at tuned idle vs zero-idle, small frustrated
      instance. Pre-register metrics.

## Phase 5 — Write-up (either polarity)

- [ ] Positive: "Noise-assisted quantum-walk proposals for exact MCMC" —
      H1 peak + γ*/Δ + exactness-under-any-noise as the pillars.
- [ ] Negative: fold into the TunnelVision honest-benchmarking paper as a
      second, mechanistically distinct noise hypothesis killed by the same
      protocol (tempering AND delocalization) — arguably strengthens that paper.
- [ ] Either way: R2's novelty table refreshed at submission time.

## Phase 5′ — the theorems paper (ACTIVE; supersedes Phase 5's two polarities)

Landed polarity: "Noise cannot help quantum-enhanced MCMC: exactness is
free, advantage is not" — one positive theorem, one corrected negative law,
plus the protocol. Skeleton: paper/SKELETON.md.

- [x] **Characterization theorem** (docs/characterization_theorem.md):
      transpose-closed Kraus sets ⇒ symmetric proposal; Lindblad corollary
      via time-reversed Dyson; Table 1 (real-basis dephasing / depolarizing /
      equal-rate σ± YES; amp damping / unequal σ± NO); certified 1.2e−14 /
      ≥3.5e−2 (run_r1.py extended; tests I10–I12).
- [x] **Monotonicity theory pass** (docs/monotonicity.md): conjecture v1
      REFUTED (gap concave over mixtures; solvable α=1 corner via telegraph
      ODE — noise beats γ=0 on parity modes; fixed-t interference-zero
      counterexample). Corrected claim = ENVELOPE LAW.
- [x] **G05 pre-registration** (experiments/G05_monotonicity/
      PREREGISTRATION.md) — written before runs; envelope law, 50 random
      cells, ε=0.01, binding verdict rules.
- [x] **G05 run + verdict** (run_g05.py → results.csv → G05_RESULTS.md):
      envelope law HOLDS 49/50 (one +1.17% instance-specific micro-bump,
      reproduced + disclosed); interior peaks 20/50; advantage cells 4/50,
      all eroding beyond γ ≈ 0.03Δ.
- [x] ESS confirmation of G01 pilot at n=6 (paper Fig 3 honesty):
      run_g01_ess_confirm.py, 216 kernel-cells, R̂-gated; rank agreement
      12/14 scored cells, 0 ESS peaks, pilot verdict CONFIRMED (addendum in
      G01_PILOT_RESULTS.md). n=8/10 skipped (trajectory kernel not wired).
- [x] R2 novelty sweep — CLOSED (docs/NOVELTY-CHECK-02.md verdict).
      Mixing-time item HIT: interior-optimum mixing under dephasing known
      2003–2009 incl. hypercube (Kendon-Tregenna; Fedichkin et al.;
      Alagic-Russell; Drezgich et al.) ⇒ C5 narrowed to the window-averaged
      telegraph analysis + exact-MH embedding. Also: Layden SM already
      states symmetry-on-average (credit in C1); Orfi-Sels PRA 110, 052414
      covers unital (⊇ dephased) proposals worst-case (complementary to
      envelope law). Claim sentence finalized. Scholar alerts still manual.
- [x] Amplitude-damping bias bound (upgrade hardware section)
      (docs/amp_damp_bias.md; naive Metropolis vs Hastings; per-step
      TV ≤ ε(1/π_min−1), stationary ≤ that·π_min^{−1/2}/δ (Thm B; un-√
      form empirical only); certified n≤5, 3×5 grid; test I13).
      C3 now PROVED + BOUNDED + CERTIFIED.
- [x] Paper prose markdown draft (paper/prose/; Fig 5 built during §7).
      Theorems 1–4 + envelope law; claims walk in
      paper/prose/CLAIMS_CHECK.md; reading copy paper/prose/DRAFT.md.
      Markdown is the frozen first draft after Phase 6.

## Phase 6 — REVTeX conversion (2026-08-20)

- [x] Figs 1–5 regenerated (verify-then-save; all PASS).
- [x] `paper/refs.bib` from the NOVELTY-CHECK-02 nearest-neighbor table
      (published records preferred; arXiv-only entries tagged journal=arXiv).
- [x] `paper/main.tex` — REVTeX 4.2, `aps,prx,reprint,floatfix`;
      Theorems 1–4; Table I; Figs 1–5; journal-voice related work;
      Darth Kuvius stub; DAS + `TODO: ZENODO-DOI`. Compiles with Tectonic
      to `paper/main.pdf` (12 pages).
- [x] `paper/popular_summary.txt` extracted from frontmatter (not in body).
- [ ] Scholar alerts (MANUAL).
- [ ] Novelty-sweep refresh at submission.
- [ ] Zenodo DOI / public archival deposit at submission.

## Estimated session budget

Phase 0 ≈ 1 session (R1 numerics are cheap; R2 is reading). Phase 1 ≈ 1–2
sessions (propagator + scan). Phase 2 ≈ 1 session. Phases 3–4 only on a live H1.

## Log

- 2026-08-18: Scaffold created (README + TASKS). R1 identified as gating
  question. No code yet. Next session: Phase 0.
- 2026-08-18 (later): Full code scaffold: lindblad dense propagator, dephased
  walk + classical kernels, Ising targets (e01/sk/rfim), minimal exact engine,
  diagnostics (gap/ESS/R-hat), G01 runner, R1 script, docs, 9 tests ALL PASSING
  (incl. matrix-level end-to-end exactness at any gamma, gamma=0 == quench,
  Zeno freeze). PRELIMINARY R1 NUMERICS: pure dephasing symmetric to machine
  precision (defect 1.7e-17 at n=5, 1e-12-ish at n=4 across gamma); amplitude
  damping breaks it hard (defect 0.178 at kappa=0.1*Delta) — as predicted.
  Remaining for R1 exit: the ANALYTIC argument (docs/R1_symmetry.md step 2)
  + n=6 certification (dense expm at n=6 is slow, ~1 min/call — batch it or
  accept n<=5 + the proof). MCWF trajectory sampler (n 7-12) still Phase 1.
- 2026-08-18 (session 3): **R1 CLOSED — PASS.** Analytic proof found
  (jump-unravelling exchangeability: Poisson phase kicks are time-reversal
  invariant; symmetric factors transpose to the reversed realization) +
  full certification, worst pure-dephasing defect 3.3e-16; amp-damp 0.55.
  Sparse expm_multiply time-grid path (10x faster) + TrajectorySampler
  (state-independent Poisson kicks, n<=~14) + TrajectoryDephasedWalkKernel
  implemented; 11/11 tests pass. **G01 PILOT RUN — H1 preliminary NEGATIVE:
  12/12 cells (chain+SK, T in {.1,.3,1}, alpha in {.05,.15,.3,.5}) monotone
  decreasing gap in gamma; no Goldilocks peak even in the localized regime.**
  Mechanism: Metropolis filter rewards energy-conserving coherence; dephasing
  broadens proposal energy -> rejected. See G01_PILOT_RESULTS.md (incl. the
  monotonicity conjecture and 3 untested escapes). G02-G04 do not proceed as
  written. LIVE POSITIVE: R1 theorem = formal proof of Layden noise
  robustness; candidate paper pillar. Next: (i)   ESS confirmation of pilot,
  (ii) decide among escapes (site-dependent gamma_i shaping / hitting-time
  objective) vs (iii) pivot to writing the theorem + honest-benchmark paper.
- 2026-08-18 (session 4): **Theorems-paper session (Phase 5′).**
  (1) CHARACTERIZATION THEOREM proved + certified: transpose-closed Kraus
  sets preserve proposal symmetry (channel-level E = Θ∘E★∘Θ; implies
  unitality; necessary condition diag E(I)=1). Lindblad corollary via
  time-reversed Dyson unravelling. Certified: real-basis dephasing,
  depolarizing, equal-rate sigma± all ≤ 1.2e−14; amp-damp and UNequal-rate
  sigma± break at ≥ 3.5e−2 (the equal/unequal pair is the sharpest
  illustration). 14/14 tests pass (new I10–I12).
  (2) MONOTONICITY CONJECTURE **REFUTED**, not proven: gap is CONCAVE over
  convex mixtures of reversible chains (G01's data-processing sketch had the
  inequality backwards); exactly solvable corner (alpha=1, uniform target,
  telegraph ODE f''+2γf'+4f=0, ∫f=γ/2) shows window-averaged gap PEAKS at
  intermediate γ (0.5→0.97, Lindblad-verified to 6 decimals) because
  dephasing kills even-moment parity coherences that time-averaging cannot.
  n=4 real targets: peaks in EVERY cell (large at alpha=1, invisible at
  alpha≤0.5 — reconciles G01's 12/12). BUT peak never beats classical
  baselines → corrected, PRE-REGISTERED **ENVELOPE LAW** (G05, 50 random
  cells, written before running). Quick-mode 6/6 cells consistent.
  (3) Paper skeleton drafted (paper/SKELETON.md) with claims register
  C1–C8 and figures list. Local venv at gvenv/ (pip install -e . + pytest).
  (4) **G05 VERDICT: envelope law HOLDS, 49/50 clean.** One +1.17%
  micro-bump (SK n=5 T=0.085 α=0.63, γ*≈0.02Δ) — real (survives 2x time
  points), instance-specific (fresh instance monotone), disclosed per
  prereg. Peaks generic (20/50) but never useful; 4 advantage cells all
  erode beyond γ≈0.03Δ. ESS spot-check 3/5 rank-agree (2 failures = frozen-
  chain ESS pathology at γ=31.6Δ, R̂-gateable). Remaining for the paper:
  G01 ESS confirmation, R2 sweep, amp-damp bias bound.
- 2026-08-18 (session 5): **G01 ESS CONFIRMATION + R2 SWEEP, both closed.**
  (1) ESS confirmation at n=6 over the pilot's 24 cells (full protocol,
  50k×5 seeds, R̂ gating): 92/216 kernel-cells gated (frozen chains,
  exactly the G05 pathology); Spearman(gap, ESS/step) > 0.8 in 12/14
  scorable cells; ZERO ESS peaks; no γ>0 beats the envelope on ESS/step or
  ESS/sec; the only flag is the known advantage cell (walk > uniform-flip,
  as it should be; γ-differences within 1 SE). Pilot verdict stands on the
  full protocol. Fig 3 caption must note T=0.1 cells are gap-only (ESS
  unmeasurable at 50k steps, R̂-gated).
  (2) R2 CLOSED — the highest-risk item HIT: fastest mixing at
  intermediate dephasing is known walk literature (Kendon-Tregenna 2003;
  Fedichkin-Solenov-Tamon 2006; hypercube: Alagic-Russell 2005 + Drezgich
  et al. 2009 with optimal γ/Δ ≈ 1–5 via the same qubit factorization as
  our telegraph corner). C5 narrowed accordingly (SKELETON claims register
  updated); C1 credits Layden SM's symmetry-on-average condition; C6
  positioned as complementary to Orfi-Sels' worst-case unital bound.
  Exact-MH embedding + envelope law + channel classification remain ours.
  Nearest-neighbor table finalized + claim sentence written
  (docs/NOVELTY-CHECK-02.md §3–4). Remaining for paper: amp-damp bias
  bound, prose. Manual: set Scholar alerts.
- 2026-08-19 (session 6): **Phase 5′ figures + T₁ bias bound.**
  (1) Figs 1–4 built under paper/figures/ (PDF+PNG), each script
  verify-then-save against source docs. Fig 1 from R1_results.txt
  (file max amp-damp 0.352; narrative 0.55 is an older grid, not
  silently "fixed"). Fig 2 telegraph formula + n=2 Lindblad match
  at 8e−16. Fig 3 from results_ess_confirm.csv, ESS only on
  R̂-passable rows, T=0.1 caption present. Fig 4 G05 scatter, cell 46
  marked; cell 19 is a sub-ε +0.087% geometric crossing, not an L1
  violation. (2) Amplitude-damping bias bound CLOSED:
  docs/amp_damp_bias.md Theorems A/B (P_M vs P_H); certified 15/15
  cells (n≤5, 3 (T,α) × 5 κ/Δ); test I13. Measured TV ~ O(ε);
  1/δ envelope holds and is loose by 10⁶–10²¹. SKELETON C3 →
  PROVED + BOUNDED + CERTIFIED; venue decision: PRX Quantum article
  (not PRL+supplement). Remaining for paper: prose. Manual: Scholar alerts.
- 2026-08-19 (session 7): **Paper prose, first full draft.** Markdown
  under paper/prose/ (00 frontmatter through 08 related work + stitched
  DRAFT.md). Wave 1 §2–§4 from the theorem docs (Theorems 1–4, envelope
  law not a theorem); wave 2 §1/§5; wave 3 §6–§8 + abstract (248 words)
  + Fig 5 cartoon (fig5_energy_concentration.py, verify-then-save).
  Claims walk C1–C8 and number lock PASS (CLAIMS_CHECK.md). Remaining:
  REVTeX conversion, popular-summary polish, author block, submission
  refresh of the novelty sweep. Manual: Scholar alerts.
- 2026-08-20 (session 8): **Phase 6 — REVTeX conversion.** Regenerated
  Figs 1–5 (verify-then-save, all PASS). Wrote `paper/main.tex` +
  `paper/refs.bib` + `paper/popular_summary.txt`. Author stub Darth
  Kuvius; empty affiliation/email; DAS with Zenodo TODO. Number lock
  walked in the tex (TC 1.2e−14 / break 3.5e−2; amp-damp file max 0.352;
  corner 0.5→0.97; G05 49/50 +1.17% cell 46; peaks 20/50; four advantage
  cells; Fig 3 T=0.1 gap-only; Fig 4 cell 19 sub-ε +0.087%). Compiles
  with Tectonic (`aps,prx,reprint,floatfix`) to a 12-page PDF. Markdown
  under paper/prose/ is now the frozen first draft; tex is the submission
  source. Remaining: Scholar alerts (manual), novelty refresh at
  submission, Zenodo DOI, real editorial-system identity.
