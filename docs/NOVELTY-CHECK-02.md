# NOVELTY-CHECK-02 — ENAQT-regime walks as exact MCMC proposals (status: CLOSED 2026-08-18; refresh at submission)

Claim under test: "dephased (noise-assisted) quantum-walk proposals inside an
exact Metropolis-Hastings sampler, with dephasing rate as a tuned resource on
NISQ hardware, and a γ*/Δ matching-condition study" is novel.

**Sweep outcome in one line: the highest-risk item HIT — fastest mixing at
intermediate dephasing is established walk literature (2003–2009, including
on the hypercube) — so C5 is narrowed; the exactness characterization, the
exact-MH embedding, and the envelope law survive as ours.**

## Nearest neighbors found so far (2026-08-18 quick sweep — NOT sufficient)

| Work | What it is | Why it's not us |
|---|---|---|
| Layden et al. 2203.12497 | Coherent quench proposals, exact MH | γ=0 limit of our kernel; noise treated as nuisance (robustness), not resource |
| Lemieux et al. 1910.01659; 2506.11576 | Szegedy quantum-walk MH circuits | Coherent, fault-tolerant-era; walk is the *whole* chain, not a noisy proposal |
| Orfi & Sels 2403.03087 | Bounds on qe-MCMC speedup | Theory bound on Layden-style kernels; check whether bounds already cover dephased kernels |
| Holbrook multiproposal / nonreversible lines | FT-era walk primitives | Different machine model entirely |
| 2111.02897 | Digital simulation of ENAQT | Transport physics target, not sampling; we reuse their circuit unravellings |
| D-Wave noise/temperature sampling (2109.01690) | Analog device noise sampling | Biased device sampling; no exactness layer |

## Sweep checklist (Phase 0, task R2)

- [x] All papers citing 2203.12497 (re-sweep with walk/noise/dephasing lens, 2026-08-18)
- [x] All papers citing 1111.4982 (Goldilocks) with algorithm/sampling angle — citation tree stays in transport/photosynthesis; nothing sampling-flavored found
- [x] All papers citing 2111.02897 — exciton transport/simulation only (Gallina et al. follow-up 2404.06264 on non-Markovian memory; note their remark that converting intrinsic device noise into a programmable stochastic process "has not yet been achieved")
- [x] Quantum stochastic walk / dephased-walk mixing-time literature — **HIT, see verdict §1** ← highest-risk item, resolved
- [x] "noise-assisted" / "dephasing-assisted" × "Metropolis" / "MCMC" / "Gibbs sampling" full-text searches — no exact-MH embedding with tuned dephasing found; closest are Richter's decoherent-walk uniform sampling (2007) and the engineered-dissipation Gibbs-sampler line (different machine model, see table)
- [ ] Google Scholar alerts set for the above (MANUAL — cannot be done from this session; set alerts for: "quantum-enhanced MCMC" + noise, "dephasing" + "Metropolis", citations of Layden 2023 / Orfi-Sels 2024)

## Verdict (R2 exit, 2026-08-18)

### 1. The mixing-time item HIT — the solvable corner's phenomenon is known

"Fastest mixing at intermediate dephasing" is established quantum-walk
literature, with a direct hypercube antecedent of our α=1 corner:

- **Kendon & Tregenna, PRA 67, 042315 (2003)** — DTQW on line/cycle/
  hypercube (numerics): small decoherence *enhances* algorithmic properties;
  optimal rate p·T ≈ 2.6–5; minimum mixing time on the cycle below the
  classical value.
- **Alagic & Russell, PRA 72, 062304 (2005)** — CTQW on the hypercube:
  decoherence threshold below which linear instantaneous mixing survives;
  beyond it classical Θ(n log n) behavior, with Zeno retardation at large
  rate.
- **Fedichkin, Solenov & Tamon, QIC 6, 263 (2006)** — CTQW on cycles,
  *analytic*: mixing time improves linearly in the decoherence rate at small
  rates, degrades linearly at large rates; unique interior optimum.
- **Richter, PRA 76, 042306 & NJP 9, 072 (2007)** — decoherent walks always
  mix; mixing robust to any smooth decoherence; explicit MCMC/sampling
  framing; threshold mixing proved for the hypercube Z₂ⁿ; conjectured √δ
  quantum speedup of classical mixing. Uniform targets only; no Metropolis
  filter.
- **Drezgich et al., QIC 9, 856 (2009)** — *complete characterization* of
  CTQW mixing on the hypercube vs Markovian decoherence rate AND axis:
  finite optimal rate γ/Δ ≈ 1–5 for almost all decoherence axes (none for
  axes in the x–y plane), derived via the same non-interacting-qubit
  factorization our telegraph solution uses. Also Abal et al.
  (arXiv:0712.0625): DTQW hypercube, broken-link decoherence, mixing-time
  minimum at p ≈ 0.1.
- QSW umbrella: Whitfield et al. 0905.2942 (framework); Caruso et al.,
  NJP 16, 055015 (2014): ~90% quantum / 10% classical universally optimal —
  but for *transport* to a sink, not mixing/sampling.

**Consequence for C5:** the *phenomenon* (interior optimum of mixing speed
in dephasing rate, including on the hypercube at γ ~ Δ) is NOT ours and must
be cited as known. What remains ours in the corner: the exactly solvable
**window-averaged** telegraph analysis (odd-moment vs even-moment/parity
decomposition showing precisely which coherences Layden-style time
randomization cannot kill and dephasing can), its Lindblad verification,
and its role inside the exact-MH sampler. Note also: prior hypercube
results concern the walk's own mixing to uniform; none study the MH chain
built from the dephased proposal against a Gibbs target.

**No contradiction with the envelope law:** the walk literature's
noise-beats-classical results (e.g. cycle mixing below classical value)
compare the decohered walk against the *classical walk on the same sparse
graph* toward a *uniform* target with no acceptance filter. Our law
compares the dephased-proposal MH chain against the classical-kernel
envelope for *Gibbs* targets — the Metropolis filter is what flips the
verdict (§5 mechanism), and at the uniform-target corner the law holds
trivially because uniform-flip already has gap ~1.

### 2. qe-MCMC citation sweep (2203.12497, walk/noise lens)

- **Layden et al.'s own SM** already states the convergence condition we
  formalize: errors are harmless "provided such errors do not break the
  Q(s′|s)=Q(s|s′) symmetry on average," with SPAM-twirling mitigation, and
  the observation that depolarizing noise degrades the proposal toward
  uniform. **C1/C2's related-work text must credit this**: they state the
  symmetry-on-average condition; our Theorem 1/2 is the systematic
  channel-level *classification* of which physical noise satisfies it
  (transpose-closed Kraus ⇔-flavored analysis, unitality, T₁ as the unique
  realistic bias channel) — a strictly stronger and new statement, but not
  a bolt from the blue.
- **Orfi & Sels, PRA 110, 052414 (2024)**: no speedup over classical
  sampling on their worst-case (marked-item) problem for **any unital
  quantum proposal** — dephasing is unital, so their bound already covers
  our whole dephased family *in the worst case*. Complementary to, not
  overlapping with, the envelope law: theirs is one adversarial instance
  vs the uniform baseline; ours is a per-cell, pre-registered, quantitative
  law across typical Ising/SK/RFIM instances against the full baseline
  envelope, plus the γ-resolved erosion measurements. Cite prominently.
- CGQeMCMC (PRR 7, 013231): explicitly says the effect of noise "has not
  been investigated" — confirms the gap we fill.
- 2411.17821 (quantum-enhanced → quantum-inspired): classical surrogate
  proposals; repeats the noise-affects-only-efficiency point; no tuned
  noise. 2506.19538 (causal sets): application, no noise angle.
- FT-era Metropolis-walk line updated: Claudon et al. 2506.11576, penalised
  qubitized walks 2604.15179, Incudini & Mazzola 2607.22818 (fully-quantum
  walks, sixth-degree speedup) — different machine model, cite in passing.
- Engineered-dissipation Gibbs samplers (Zhang-Bosse-Cubitt 2304.04526;
  Chen-Kastoryano-Gilyén 2311.09207 line): noise *engineered* so the
  Lindbladian's fixed point IS the Gibbs state — constructive dissipation,
  different machine model from ambient tuned dephasing inside exact MH.
  One table row, one sentence.

### 3. Finalized nearest-neighbor table

| Work | What it is | Why it's not us |
|---|---|---|
| Kendon & Tregenna PRA 67, 042315 (2003); Fedichkin-Solenov-Tamon QIC 6 (2006); Abal et al. 0712.0625 | Optimal intermediate decoherence for walk mixing (numerics + cycle analytics) | Walk mixes to uniform, no MH filter, no Gibbs target; **cite as the known phenomenon behind our solvable corner** |
| Alagic & Russell PRA 72, 062304 (2005); Drezgich et al. QIC 9 (2009) | Hypercube CTQW mixing vs decoherence, complete characterization, optimal γ/Δ ≈ 1–5 | Same graph and factorization trick as our α=1 corner, but fixed-t instantaneous mixing to uniform; no window averaging, no MH, no classical-envelope comparison |
| Richter PRA 76, 042306 + NJP 9, 072 (2007) | Decoherent walks always mix; MCMC-motivated uniform sampling; hypercube threshold mixing | Uniform π only; decoherence = repeated measurement; no Metropolis filter, no Gibbs targets, no noise-rate optimization against classical kernels |
| Layden et al. Nature 619 (2023) [2203.12497] | Coherent quench proposals, exact MH; SM has symmetry-on-average robustness | γ=0 limit; noise as nuisance; condition stated but channels not classified — our Thm 1/2 is the classification |
| Orfi & Sels PRA 110, 052414 (2024) [2403.03087] | Worst-case no-speedup bound for ANY unital proposal | Covers dephased kernels in the worst case; single adversarial instance vs uniform baseline — complementary to the per-instance envelope law |
| CGQeMCMC PRR 7, 013231; 2411.17821; 2506.19538 | qe-MCMC scaling/surrogate/application follow-ups | No tuned-noise study (CGQeMCMC says so explicitly) |
| Lemieux 1910.01659; Claudon 2506.11576; 2604.15179; Incudini-Mazzola 2607.22818 | FT-era (fully-)quantum Metropolis walks | Different machine model; walk is the chain, not a noisy proposal |
| Zhang-Bosse-Cubitt 2304.04526; Chen-Kastoryano-Gilyén 2311.09207 | Dissipative/Lindbladian Gibbs samplers | Dissipation engineered to target the Gibbs state; not ambient dephasing in an exact-MH proposal |
| Lloyd et al. 1111.4982; Rebentrost NJP 11; Caruso NJP 16, 055015 | ENAQT / quantum Goldilocks, transport | Transport-to-sink objective; citation trees contain no sampling-algorithm angle |
| 2111.02897 (+2404.06264) | Digital ENAQT circuit unravellings | Transport simulation; we reuse their unravellings; they note programmable device-noise conversion is unachieved |
| D-Wave 2109.01690 | Analog device-noise sampling | Biased sampling, no exactness layer |

### 4. Claim statement for the paper (the R2 exit sentence)

> **For quantum-walk Metropolis proposals we (i) characterize exactly which
> noise channels preserve evaluation-free exactness (transpose-closed Kraus
> sets — dephasing in any real basis, depolarizing, equal-rate σ± — at any
> strength, with T₁ the unique realistic bias channel), and (ii) establish
> the envelope law: tuned dephasing, although it genuinely accelerates the
> walk's own mixing as known since Kendon-Tregenna (2003), never lifts the
> sampler's efficiency above the envelope of the coherent quench and
> trivial classical kernels on Gibbs targets — exactness is free, advantage
> is not.**

Narrowed C5 (solvable corner), stated honestly: our contribution there is
the exact window-averaged telegraph solution and the odd-/even-moment
mechanism separating time-window randomization from genuine dephasing,
embedded in the exact-MH setting — the interior-optimum phenomenon itself
is due to Kendon-Tregenna (2003), Fedichkin-Solenov-Tamon (2006), and, on
the hypercube, Alagic-Russell (2005) / Drezgich et al. (2009).

The γ*/Δ "matching-condition study" (H2) framing from the original claim is
dead regardless — no useful γ* exists (G01/G05) — and the walk literature's
γ*/Δ ≈ 1 optima make clear it would not have been novel either.

_Refresh this sweep at submission time (alerts item above still open)._
