# Claims and number-lock walk (2026-08-19)

Checked against `paper/SKELETON.md` register C1–C8 and the number lock
in `paper/prose/README.md`. Pass means the prose states the claim at the
registered strength — no stronger, no weaker.

| # | Register | Where | Verdict |
|---|---|---|---|
| C1 | Transpose-closed Kraus ⇒ symmetric proposal; defect ≤ 1.2e−14; credit Layden SM for the *condition*, ours is the *classification* | Thm 1 in `03_exactness.md`; SM credit in §3 opening, §1, §8.2 | PASS |
| C2 | Lindblad semigroups, real-symmetric H, transpose-closed jumps | Thm 2 in `03_exactness.md` | PASS |
| C3 | T₁ unique realistic bias; ‖P_M−P_H‖_{TV,∞} ≤ ε(1/π_min−1); ‖π̃−π‖_{TV} ≤ that·π_min^{−1/2}/δ; un-√ empirical only; file max 0.352 not 0.55; TV ~ O(ε); envelope loose 10⁶–10²¹ | Thms 3–4 in `03_exactness.md` | PASS |
| C4 | Gap-monotonicity in γ is FALSE | §4.1–4.2 (fixed-t + telegraph + n=4) | PASS |
| C5 | Noise can improve window-averaged mixing — phenomenon KNOWN (Kendon–Tregenna 2003; Fedichkin 2006; Alagic–Russell 2005; Drezgich 2009); we claim telegraph + odd/even mechanism + MH embedding; δ: 0.5 → 0.97 | §4.2 and §8.1 | PASS |
| C6 | Envelope law; 49/50 + one +1.17% exception; complementary to Orfi–Sels | §4.3; Orfi–Sels also §1 and §8.2 | PASS |
| C7 | Advantage cells erode beyond γ ≈ 0.03Δ; sub-2% micro-bumps below | G05 L2(b) in §4.3; G01 12/12 in §4.4 | PASS |
| C8 | Energy concentration predicts advantage — CONJECTURE only | Flagged in §7; §5 explicitly refuses the claim | PASS |

## Number / caption lock

- Transpose-closed defect ≤ 1.2e−14; break ≥ 3.5e−2 — §1, §3, Table 1
- R1 amp-damp file max **0.352** (older 0.55 named and discarded) — §3
- Solvable-corner 0.5 → 0.97 and the n=2 six-point list — §4.2, Fig 2
- G05 49/50, +1.17% cell 46, 20/50 peaks, 4/50 advantage, γ ≈ 0.03Δ — §4.3
- Fig 3 caption: T=0.1 cells are gap-only (ESS unmeasurable at 50k steps, R̂-gated)
- Fig 4: cell 46 marked; cell 19 named as sub-ε +0.087% geometric crossing
- Fig 5 caption: C8 is a predictor, not a theorem
- Layden page number locked to Nature **619**, 282 (2023)
- Envelope law stated as not a theorem; convex-hull route open
- Polarities not flattened: peaks exist; they never win

## Length (first draft)

Abstract 248 words (PRX Quantum: ~5% and < 500). Body files ~7.5k words
plus displayed math. Comfortable article length; no PRL cut.
