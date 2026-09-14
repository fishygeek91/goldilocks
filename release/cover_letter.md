# Cover letter — PRX Quantum submission

Dustin Kovac
Independent researcher, Pinedale, Wyoming, USA
fishygeek91@gmail.com

Date: 14 September 2026

To the Editors, PRX Quantum

Dear Editors,

I am submitting for your consideration the manuscript **"Noise cannot help
quantum-enhanced MCMC: exactness is free, advantage is not"** for publication in PRX
Quantum.

Quantum-enhanced Markov-chain Monte Carlo — using a short coherent quench as the
proposal inside an otherwise classical Metropolis–Hastings sampler (Layden et al.,
*Nature* **619**, 282 (2023)) — has become an active line of work on near-term
hardware. A recurring hope is that device noise, rather than being a liability, might
help: the sampler's exactness survives noise, and environment-assisted transport
(ENAQT) shows that intermediate dephasing can accelerate a quantum walk. This manuscript
settles that hope, and does so on both the theory and benchmarking sides in a way I
believe is of broad interest to the PRX Quantum readership.

The central results are two-sided and, I think, unusually clean:

- **Exactness is free.** We give a channel-level characterization of which noise
  preserves the evaluation-free exactness of the sampler: every transpose-closed Kraus
  set (dephasing in any real basis, depolarizing, infinite-temperature relaxation) does
  so at any strength, and amplitude damping (T₁) is the unique realistic exception, with
  a bounded bias. This classifies a condition that Layden et al. stated only as a
  symmetry-on-average property.

- **Advantage is not.** Intermediate dephasing does create Goldilocks peaks in the
  walk's own mixing — we give an exact window-averaged telegraph solution explaining
  the mechanism — but a pre-registered test on fifty random instances shows those peaks
  never lift the sampler above the envelope of the coherent quench and trivial classical
  kernels (49/50 cells, one disclosed +1.17% exception). This is the per-instance,
  family-wide complement to the worst-case unital bound of Orfi and Sels.

The revised manuscript adds a **free-certificate theorem** — a conserved diagonal charge
confines every measured outcome to its symmetry sector at zero cost while preserving
evaluation-free exactness within it, where the corresponding classical certificate scales
badly — and an **extraction-pricing design rule** with a **pre-registered negative
result** (the "PORTAL" race) that kills the natural amortized architecture on classical
grounds. Throughout, the work models a benchmarking discipline I hope the community will
adopt: kernels never see target log-probabilities, wall-clock and per-step efficiency are
both reported, split-R̂ gates every convergence claim, and kill criteria are fixed before
data are taken.

I believe this fits PRX Quantum's mandate for rigorous, broadly significant results on
quantum information science, and specifically its willingness to publish decisive
negative results and methodological contributions that shape a fast-moving field. A
credible, pre-registered "noise does not help" result — with the exactness theory that
explains *why* — is, I think, exactly the kind of course-correction the quantum-enhanced
sampling literature currently needs.

This work is entirely my own, was conducted without institutional affiliation or
external funding, and is not under consideration elsewhere. All manuscript source,
certification scripts, pre-registrations, and numerical results are archived at Zenodo
(DOI 10.5281/zenodo.22758619) and available in the accompanying public repositories. I
used an AI assistant (Claude) under my direction for literature search, derivation
checking, and code implementation, as disclosed in the acknowledgments; the scientific
claims, experimental design, and conclusions are my responsibility.

Thank you for considering the manuscript.

Sincerely,
Dustin Kovac
