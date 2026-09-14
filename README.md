# Goldilocks

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.22758619.svg)](https://doi.org/10.5281/zenodo.22758619)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

**Noise cannot help quantum-enhanced MCMC: exactness is free, advantage is not.**

The tempting conjecture for today's noisy quantum devices is that a tuned dephasing
rate should help a quantum-walk Metropolis proposal the way environment-assisted
transport (ENAQT) helps an exciton: noise would cost nothing (exactness already
survives it) and might buy mixing. We tested that conjecture and it fails, cleanly and
in two provable halves.

**Exactness is free.** Every transpose-closed noise channel — dephasing in any real
basis, depolarizing noise, infinite-temperature relaxation — preserves the
evaluation-free exactness of the sampler at *any* strength (Theorems 1–2). Amplitude
damping (T₁) is the unique realistic channel that does not, and the bias it induces is
bounded. So the noise that dominates today's devices is exactly the free kind.

**Advantage is not.** Intermediate dephasing genuinely creates "Goldilocks" peaks in
the walk's own mixing — but a pre-registered test on fifty random Ising,
Sherrington–Kirkpatrick, and random-field instances finds that those peaks never lift
the sampler above the envelope of the coherent quench and the trivial classical kernels
(49/50 cells, one disclosed +1.17% exception). Wherever the quantum proposal already
wins, dephasing erodes it; wherever dephasing helps the walk, a classical kernel was
already better. **Noise costs nothing and buys nothing.**

A **free-certificate theorem** (added in v1.0.0) generalizes the exactness result: a
conserved diagonal charge confines every measured outcome to its symmetry sector at zero
cost while preserving evaluation-free exactness within it — the classical side of that
guarantee is a completeness certificate that scales badly, censored beyond n = 24. And a
pre-registered **PORTAL race** kills the amortized device-mined-library architecture on
classical grounds, reported at full strength as a registered negative.

## Paper and archive

- Manuscript: [`paper/main.pdf`](paper/main.pdf) (REVTeX / PRX Quantum format)
- Archived release (this repo + [tunnelvision](https://github.com/fishygeek91/tunnelvision)):
  **[10.5281/zenodo.22758619](https://doi.org/10.5281/zenodo.22758619)**
- Companion experiment code and data: [tunnelvision](https://github.com/fishygeek91/tunnelvision)

## What's here

```
paper/            the manuscript (main.tex), figures, bibliography, popular summary
  main.tex        REVTeX source; data availability points at the Zenodo DOI
  figures/        figure generators + data (fig6 = concentration-at-distance)
  SKELETON.md     claim register (C1–C16), each claim traced to a run
docs/             R1 symmetry proof, characterization + monotonicity notes
release/          this release's checklist and provenance
```

The theory certification scripts, the G05 pre-registration and verdict, and the
amplitude-damping bias measurements all live with the manuscript source; every claim in
the paper is registered in `paper/SKELETON.md` and traced to a reproducible run.

## Citing

```bibtex
@misc{Kovac2026Goldilocks,
  author       = {Kovac, Dustin},
  title        = {Noise cannot help quantum-enhanced {MCMC}:
                  exactness is free, advantage is not},
  year         = {2026},
  doi          = {10.5281/zenodo.22758619},
  note         = {Zenodo archival deposit}
}
```

## License

MIT — see [LICENSE](LICENSE).
