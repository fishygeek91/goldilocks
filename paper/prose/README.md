# Paper prose (markdown draft)

Frozen first draft of the PRX Quantum article. After Phase 6 (2026-08-20),
the submission source of truth is `paper/main.tex` + `paper/refs.bib`.
Do not dual-maintain: edit the tex for submission polish; leave these
markdown files as the locked first draft. `DRAFT.md` remains a stitch.
Do not flatten the polarity while editing: peaks exist; they never win.
Exactness is free; advantage is not.

**Title.** Noise cannot help quantum-enhanced MCMC: exactness is free,
advantage is not.

**Thesis.** For quantum-walk Metropolis proposals, realistic decoherence
splits cleanly in two: every transpose-closed noise channel (dephasing in
any real basis, depolarizing, infinite-T relaxation) preserves the
evaluation-free exactness of the sampler at any strength — but no amount
of tuned dephasing lifts sampling efficiency above the envelope of the
coherent quench and trivial classical kernels. Noise costs nothing and
buys nothing.

## Files

- `00_frontmatter.md` — title, abstract (248 words), popular-summary draft
- `01_introduction.md` … `08_related_work.md` — numbered sections
- `DRAFT.md` — stitched reading copy (regenerate from the section files)
- `CLAIMS_CHECK.md` — C1–C8 and number-lock walk (2026-08-19, PASS)

Math is LaTeX so the REVTeX conversion is mechanical. Theorem numbers
are the journal numbers (the skeleton’s “§4 = Theorem 2” collides with
the Lindblad theorem):

- Theorem 1 — transpose-closed Kraus ⇒ symmetric proposal (C1)
- Theorem 2 — Lindblad semigroups, time-reversed Dyson (C2)
- Theorem 3 — per-step TV, naive Metropolis vs Hastings (C3)
- Theorem 4 — stationary TV envelope (C3). The un-√ form is empirical only
- Envelope law — not a theorem; proof status open (C6)
- C8 — outlook conjecture only

## Number lock

Copy from the source docs; never “fix” a narrative drift.

- Transpose-closed defect ≤ 1.2e−14; break ≥ 3.5e−2
- R1 file amp-damp max is **0.352**, not the older 0.55
- Solvable-corner window-averaged gap 0.5 → 0.97 (n=2 values in
  `docs/monotonicity.md` §5)
- G05: **49/50**, one **+1.17%** instance-specific bump (cell 46);
  interior peaks **20/50**; advantage cells **4/50**, eroding beyond
  γ ≈ 0.03Δ
- Fig 3 caption **must** say T=0.1 cells are gap-only (ESS unmeasurable
  at 50k steps, R̂-gated)
- Fig 4: mark cell 46; cell 19 is a sub-ε geometric crossing, not an
  L1 violation
- Credit Layden SM for the symmetry-on-average *condition*; ours is the
  channel *classification*
- C5 narrowed: interior-optimum mixing is Kendon–Tregenna 2003 /
  Fedichkin 2006 / hypercube Alagic–Russell 2005 + Drezgich 2009; we
  claim the window-averaged telegraph solution, odd/even-moment
  mechanism, and exact-MH embedding
- Orfi–Sels PRA 110, 052414 is complementary (worst-case unital), not
  overlapping

Claims C1–C8 live in `paper/SKELETON.md`. Every claim sentence in the
prose must match that register.
