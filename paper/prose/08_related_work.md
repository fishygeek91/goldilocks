# 8. Related work

We group neighbors in the order a reader should meet them: the decohered-walk mixing literature that already owns the interior-optimum phenomenon; the quantum-enhanced MCMC line we sit on; and ENAQT, whose objective we do not share. A novelty sweep closed on 2026-08-18 [docs/NOVELTY-CHECK-02.md] should be refreshed at submission; Scholar alerts for the citation trees below are still to be set manually.

## 8.1 Decohered-walk mixing — the known phenomenon

Fastest mixing at intermediate decoherence is established walk literature, including on the hypercube that is our $\alpha=1$ graph.

Kendon and Tregenna [PRA **67**, 042315 (2003)] showed numerically that small decoherence enhances discrete-time walks on the line, cycle, and hypercube, with an optimal rate $p\cdot T \approx 2.6$–$5$ and a mixing time on the cycle below the classical value. Fedichkin, Solenov, and Tamon [QIC **6**, 263 (2006)] gave the analytic counterpart on cycles: mixing time improves linearly in the decoherence rate at small rates, degrades linearly at large rates, and has a unique interior optimum. Abal *et al.* [arXiv:0712.0625] found a mixing-time minimum at broken-link probability $p\approx 0.1$ for a discrete-time hypercube walk.

On the continuous-time hypercube, Alagic and Russell [PRA **72**, 062304 (2005)] identified a decoherence threshold below which linear instantaneous mixing survives, with classical $\Theta(n\log n)$ behavior and Zeno retardation beyond it. Drezgich *et al.* [QIC **9**, 856 (2009)] gave a complete characterization versus Markovian decoherence rate *and* axis: a finite optimal rate $\gamma/\Delta \approx 1$–$5$ for almost all decoherence axes (none for axes in the $x$–$y$ plane), derived from the same non-interacting-qubit factorization our telegraph solution uses. Those results are fixed-$t$ instantaneous mixing to uniform; they have no window average, no Metropolis filter, and no classical-envelope comparison.

Richter [PRA **76**, 042306 (2007); NJP **9**, 072 (2007)] is the closest in spirit: decoherent walks always mix; mixing is robust to any smooth decoherence; the framing is already MCMC/sampling; threshold mixing is proved for the hypercube $\mathbb{Z}_2^n$; a $\sqrt{\delta}$ quantum speedup of classical mixing is conjectured. The target is uniform; decoherence is repeated measurement; there is no Metropolis filter, no Gibbs target, and no noise-rate optimization against a classical-kernel envelope.

The quantum-stochastic-walk umbrella [Whitfield *et al.*, arXiv:0905.2942] and the transport-optimal $90\%$/$10\%$ quantum/classical mixture of Caruso *et al.* [NJP **16**, 055015 (2014)] belong here as framework, but the latter optimizes transport to a sink, not mixing.

We cite this group first and prominently because it is the phenomenon behind our solvable corner. Our claim in that corner is the window-averaged telegraph solution, the odd/even-moment mechanism, and the exact-MH embedding — not the existence of an interior mixing optimum.

## 8.2 Quantum-enhanced MCMC

Layden *et al.* [Nature **619**, 282 (2023); arXiv:2203.12497] is the $\gamma=0$ limit of our kernel: coherent quench proposals, exact MH, noise treated as a nuisance. Their Supplemental Material already states the convergence condition we formalize — errors are harmless provided they do not break $Q(s'|s)=Q(s|s')$ symmetry on average — with SPAM-twirling mitigation, and notes that depolarizing noise degrades the proposal toward uniform. Theorems 1 and 2 are the systematic channel-level classification of which physical noise satisfies that condition (transpose-closed Kraus, unitality, $T_1$ as the unique realistic bias channel). That is a strictly stronger statement, and not a bolt from the blue.

Orfi and Sels [PRA **110**, 052414 (2024); arXiv:2403.03087] prove that *any* unital quantum proposal has no speedup over classical sampling on their marked-item worst case. Dephasing is unital, so their bound covers our whole dephased family on that adversarial instance, against the uniform baseline. The envelope law is complementary: per-cell, pre-registered, quantitative, on typical Ising/SK/RFIM instances, against the full baseline envelope, with $\gamma$-resolved erosion. We cite them as a sibling, not as a special case of us or the reverse.

Follow-ups in the qe-MCMC line have not studied tuned noise. Coarse-grained qe-MCMC [PRR **7**, 013231] says explicitly that the effect of noise “has not been investigated.” The quantum-inspired surrogate of arXiv:2411.17821 repeats the noise-affects-only-efficiency point without a $\gamma$ scan. The causal-set application [arXiv:2506.19538] has no noise angle.

Fault-tolerant Metropolis walks are a different machine model: the walk *is* the chain, not a noisy proposal inside classical MH. We cite Lemieux *et al.* [arXiv:1910.01659], Claudon *et al.* [arXiv:2506.11576], penalised qubitized walks [arXiv:2604.15179], and Incudini and Mazzola [arXiv:2607.22818] in passing.

Dissipative Gibbs samplers [Zhang, Bosse, and Cubitt, arXiv:2304.04526; Chen, Kastoryano, and Gilyén, arXiv:2311.09207] engineer a Lindbladian whose fixed point *is* the Gibbs state. That is constructive dissipation, not ambient tuned dephasing inside an exact MH proposal.

## 8.3 ENAQT and device-noise sampling

Rebentrost *et al.* [NJP **11**, 033003 (2009)] and Lloyd and Mohseni [arXiv:1111.4982] are the transport Goldilocks; their citation trees stay in photosynthesis and exciton transport. Digital ENAQT [arXiv:2111.02897, with the non-Markovian follow-up arXiv:2404.06264] supplies the circuit unravellings we reuse (stochastic-Hamiltonian phase kicks; collision scheme). Those works target transport simulation; they note that converting intrinsic device noise into a programmable stochastic process has not been achieved. D-Wave device-noise sampling [arXiv:2109.01690] is analog and biased, with no exactness layer.

## 8.4 Positioning

What is ours, stated after the 2026-08-18 sweep: the first channel-level exactness characterization for noisy walk proposals, upgrading Layden’s SM condition to a classification; the first study of decohered-walk *mixing* results embedded in an exact MH sampler with Gibbs targets; and the envelope law as the negative answer to noise-as-resource for *sampling*. The interior-optimum mixing phenomenon itself is 2003–2009 walk literature and is cited as such. The Metropolis filter is what separates the verdicts. Walk-versus-walk, uniform target, no filter: noise can win. Kernel-versus-envelope, Gibbs target, MH filter: noise never wins.
