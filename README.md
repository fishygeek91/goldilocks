# Goldilocks

**Noise-assisted quantum-walk proposals for exact MCMC** — testing whether biology's
ENAQT trick (dephasing as a *delocalizer*) buys sampling efficiency on today's noisy
hardware, using the TunnelVision exactness harness as the instrument.

Status: **scaffold** (2026-08-18). Nothing implemented yet. Start at `TASKS.md`.

---

## 1. The idea in one paragraph

In photosynthetic exciton transport (FMO complex), transport efficiency is
*non-monotone* in noise: pure coherent dynamics self-traps (Anderson-like
localization), pure classical hopping is slow, and efficiency peaks at an
intermediate dephasing rate — environment-assisted quantum transport (ENAQT).
Lloyd & Mohseni call the underlying principle the "quantum Goldilocks effect":
natural selection tunes systems to the degree of coherence that is *just right*,
via a convergence of timescales (hopping rates, energy mismatches, decoherence).
We ask the analogous question for sampling: build an MCMC **proposal** kernel that
is a *dephased quantum walk* over state space, with dephasing rate γ as a tunable
knob, and look for a non-monotone peak in mixing efficiency at intermediate γ.
The Metropolis accept/reject step stays classical and exact, so the sampler is
correct for **any** γ — including the uncontrolled native noise of NISQ devices.
On hardware, noise is free; we would be tuning *into* it, not mitigating it.

## 2. Hypotheses (falsifiable, in priority order)

- **H1 (ENAQT-for-MCMC):** ESS/step of the dephased-walk kernel is non-monotone
  in γ, with a peak at intermediate dephasing that beats both the coherent (γ=0)
  and fully-dephased (γ→∞, ≈ classical walk) limits on at least one target class.
- **H2 (the constant):** the optimal rate γ* tracks the walk's own energy scale Δ
  (hopping strength / energy mismatch): γ*/Δ ≈ const across targets and sizes.
  NOTE (verified 2026-08-18): Lloyd–Mohseni state the timescale-convergence
  principle qualitatively; the quantitative matching condition is OUR hypothesis,
  not a literature result. If γ*/Δ is invariant, that is a new result.
- **H3 (noise-as-resource):** on a real device, the native decoherence sits near
  enough to γ* that a hardware walk (γ tuned upward via idle delays / scheduling)
  beats its own zero-idle configuration.

**Kill criteria** (in the spirit of E02/E03 — decide fast, decide honestly):
H1 dead if no γ-scan on any target shows a peak exceeding both limits by more
than error bars. H2 dead if γ*/Δ drifts by more than ~an order of magnitude
across targets where H1 holds. ESS/sec is reported alongside ESS/step from day
one; a kernel that wins per-step and loses wall-clock by orders of magnitude is
a *negative* result at the system level (TunnelVision lesson #2).

## 3. Lessons carried from TunnelVision (binding, not advisory)

1. **No translation layer.** The quench won only when the target WAS the machine
   (E01 Ising, 26× gap); it died behind a surrogate even at 0.998 Spearman.
   Goldilocks walks operate on targets native to the walk graph — spin systems
   on the hypercube first. No surrogates in v1.
2. **ESS/sec is the referee.** The 4-orders-of-magnitude wall-clock loss killed
   E02c, not ESS/step. Every experiment reports both, plus split-R̂ gating and
   error-vs-enumerated-truth where enumerable.
3. **Noise-as-temperature failed (E03); noise-as-delocalizer is a different
   mechanism.** The daemon heated the proposal; ENAQT breaks localization. Do
   not conflate them in analysis or writing.
4. **Exactness boundary is sacred.** Kernels never see target log-probs; nothing
   quantum on the accept side; kernels return `(y, log_q_fwd, log_q_rev)`.

## 4. The exactness-critical design question (resolve FIRST — task R1)

Layden's quench proposal is exact-without-evaluating-q because it is
**symmetric**: q(y|x) = |⟨y|U|x⟩|² with real H and time-reversal symmetry gives
q(y|x) = q(x|y), so the proposal ratio cancels in the MH acceptance. Our kernel
is a *channel*, not a unitary: q_γ(y|x) = ⟨y| E_γ(|x⟩⟨x|) |y⟩. **We must prove
(or numerically certify, or engineer) q_γ(y|x) = q_γ(x|y)** for the
computational-basis-dephasing Lindbladian with a real, symmetric walk
Hamiltonian — for controlled γ AND for realistic device noise (amplitude
damping is the likely symmetry breaker). If symmetry fails, fallback options:
(a) restrict to symmetric noise models, (b) estimate q ratios (costly, breaks
the free-lunch), (c) treat the asymmetry as a bias and bound it — but then we
are outside the exactness story and must say so. Nothing gets built on top of
an unresolved R1.

## 5. Architecture

Reuse, don't rebuild. TunnelVision (../tunnelvision) provides the MH engine
(exactness boundary), diagnostics (ESS/step, ESS/sec, split-R̂, PIP/error vs
enumerated truth), classical baseline kernels, and the Ising target with exact
spectral-gap enumeration at small n. Goldilocks adds:

    goldilocks/
      README.md                  ← this file
      TASKS.md                   ← the plan; single source of truth for status
      docs/
        R1_symmetry.md           ← proof/certification of proposal symmetry
        NOVELTY-CHECK-02.md      ← citation sweep (owed before any paper claim)
      src/goldilocks/
        lindblad.py              ← dense Lindblad / quantum-trajectory propagator (small n)
        kernels/
          dephased_walk.py       ← the Goldilocks kernel: (y, log_q_fwd, log_q_rev)
          classical_walk.py      ← γ→∞ limit as its own explicit baseline
      experiments/
        G01_gamma_scan_ising/    ← γ-scan on the E01 Ising target (n ≤ 10, exact gaps)
        G02_constant_hunt/       ← γ*/Δ across targets (frustrated Ising, RFIM, low-T)
        G03_circuits/            ← digital unravellings (stochastic-H + collision), Aer noise
        G04_hardware/            ← IBM device, γ via idle-delay scheduling (only if G01–G03 pass)
      tests/
        test_exactness.py        ← TunnelVision invariants + symmetry certification test

Kernel physics, v1: walk graph = n-dim hypercube (single spin flips); walk
Hamiltonian H = transverse-field mixer (α·Σᵢ Xᵢ, optionally + problem-energy
diagonal, exactly Layden's family so E01 is the γ=0 anchor point); dephasing =
computational-basis Lindblad jump operators Zᵢ at rate γ; evolve time t, measure
→ proposal y. Two limits are known: γ=0 reproduces the E01 quench; γ→∞ Zeno-pins
the walk toward (lazy) classical single-site dynamics. The experiment is the
middle.

## 6. Novelty position (as of 2026-08-18 — full sweep owed, task R2)

Nearest neighbors found: Szegedy-style quantum-walk Metropolis circuits
(Lemieux et al. 1910.01659; 2506.11576 follow-up) — coherent, fault-tolerant-era
constructions, no noise-assistance; qe-MCMC speedup bounds (2403.03087);
multiproposal / nonreversible-chain quantum walks (Holbrook line) —
fault-tolerant primitives. Digital simulation of dephasing-assisted transport
exists (2111.02897: stochastic-Hamiltonian and collision-scheme unravellings,
log-qubit encoding, quadratic gates) but targets transport physics, not
sampling. **No work found marrying ENAQT-regime dephased walks to exact
Metropolis proposals.** That is the gap we claim — pending R2's citation sweep
of everything citing 2203.12497, 1111.4982-descendants, and QSW mixing papers.

## 7. Key references

- Layden et al., qe-MCMC — arXiv:2203.12497 (Nature 619, 282 (2023))
- Lloyd & Mohseni, quantum Goldilocks — arXiv:1111.4982
- Rebentrost et al., ENAQT — New J. Phys. 11, 033003; ordered-systems NJP 14, 053041
- Digital dephasing-assisted transport — arXiv:2111.02897
- Quantum-walk MH circuits — arXiv:1910.01659; arXiv:2506.11576
- qe-MCMC speedup bounds — arXiv:2403.03087
- Coarse-grained qe-MCMC (scale-up route) — Phys. Rev. Research 7, 013231
- TunnelVision final verdict — ../tunnelvision, status memory 2026-08-14

## 8. Decision log

- 2026-08-18: Direction chosen (Path B over native-Ising A, advantage-constant C,
  radical-pair D). Morph TunnelVision, don't restart. Scaffold created; README +
  TASKS first, implementation next session. R1 (symmetry) identified as the
  gating design question during scaffold review.
