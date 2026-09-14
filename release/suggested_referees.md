# Suggested referees — PRX Quantum

Guidance used: pick reviewers who know quantum-enhanced sampling, decohered quantum
walks, or MCMC benchmarking well enough to judge the theorems and the pre-registration,
while avoiding direct competitors whose own advantage claims this paper tensions against
(they can referee, but flag the potential bias). Contact details are on the authors'
institutional pages; verify current affiliations at submission.

## Strong fits (theory + benchmarking)

1. **Matthias Troyer** (Microsoft) — co-author of the wall-clock/I-O critique of quantum
   advantage the paper builds its extraction-pricing rule on; ideal judge of the
   honest-benchmarking framing and the "advantage is not free" claim. Not a qe-MCMC
   competitor.

2. **Daniel Lidar** (USC) — decoherence-free subspaces and open-system quantum dynamics;
   the natural referee for the transpose-closed / conserved-charge exactness theorems and
   the free-certificate result.

3. **Juan Carrasquilla** (ETH Zürich) — classical and quantum sampling, spin glasses,
   and ML for many-body systems; well placed to assess the fourteen-kernel zoo, the
   shell-oracle mechanism, and the spin-glass instance design.

## Good fits (sampling / walks / statistics)

4. **Christian P. Robert** (Université Paris-Dauphine) — a leading MCMC methodologist;
   can referee the Metropolis–Hastings exactness boundary, ESS/split-R̂ methodology, and
   the pre-registration discipline from the statistics side.

5. **Viv Kendon** (University of Strathclyde) — foundational work on decohered quantum
   walks and the interior-optimum mixing phenomenon the paper cites and then bounds; can
   check that the ENAQT-does-not-transfer argument is fair to that literature.

6. **Leo Zhou** (UCLA / Caltech) — QAOA, quantum optimization, and constrained/mixer
   Hamiltonians; suited to the NOETHER/sector material and the conserved-charge framing.

## Potentially biased (competent, but flag)

- **David Layden** (IBM) — original quench-proposal author; deeply expert, but the paper
  reproduces and then bounds his construction. Excellent for a fairness check; disclose
  the tension.
- **Tameem Albash / Itay Hen** (USC/ISI) — constrained quantum annealing drivers cited in
  the sector discussion; competent but adjacent to the claims.

## Suggested to exclude

- Authors of recent per-step quantum-annealing-MCMC advantage papers that the manuscript
  explicitly critiques for lacking wall-clock metrics (e.g. the QAEMCMC line): a direct
  conflict on the central claim.
