# 6. Benchmarking protocol

Quantum-algorithm benchmarks are easy to fool. The rules below are the instrument, not the appendix. They are the TunnelVision exactness harness, applied here to a noise-as-resource hypothesis and offered as a reusable method.

*Exactness boundary.* Proposal kernels never see target log-probabilities. Nothing quantum sits on the accept side of MH. A kernel returns a triple $(y,\, \log q_{\mathrm{fwd}},\, \log q_{\mathrm{rev}})$; for every transpose-closed channel the two logs are identically zero by Theorems 1 and 2, but the interface does not get to assume that. The G01/G05 runners consume the triple and never a $\pi$-lookup from the kernel.

*Two clocks.* Every experiment reports ESS per step *and* ESS per second. A kernel that wins per step and loses wall-clock by orders of magnitude is a negative result at the system level. Spectral gap, where the $2^n\times 2^n$ kernel can be built, is a third number, not a substitute.

*Mixing gate.* Split-$\hat R\le 1.05$ gates a chain before its ESS is believed. The gate exists because frozen chains produce garbage-high ESS on a near-constant series — the pathology that appeared in G05 at $\gamma=31.6\Delta$ and in $92$ of $216$ G01 kernel-cells. Those cells are excluded, not averaged away.

*Enumerated truth.* At $n$ small enough to enumerate, we report error against the exact $\pi$ (and the exact gap) rather than against a surrogate. No translation layer: the walk graph *is* the spin system.

*Pre-registration.* Kill criteria are written before data. G01’s H1 rule — an interior $\gamma$ must beat both $\gamma=0$ and the largest $\gamma$ outside $\pm 2$ SE — was fixed in the runner. G05’s envelope law, the $1\%$ slack, the $5\%$ refutation threshold, and the “holds with noted exceptions” band for one or two sub-$5\%$ violations were fixed in PREREGISTRATION.md before `run_g05.py` existed. The originally tempting law (monotone gap for all targets) was *not* registered: the theory pass had already refuted it, and pre-registering a known-false claim would have been theater.

*Negatives at full strength.* A failed hypothesis is a result. H1 is reported as killed, not as “more work needed.” Cell 46 is reported in full, not absorbed into a mean. The un-$\sqrt{\phantom{x}}$ stationary bound is flagged as empirical. C5 is narrowed in public to the analysis we actually own.

The protocol earned its keep twice. It killed H1 on the G01 pilot: twelve of twelve cells monotone in the gap, zero ESS peaks under $\hat R$ gating, envelope intact on both clocks. It then caught the overreach of conjecture v1. The theory pass produced interior peaks at $\alpha=1$ and on a fine $n=4$ grid; registering monotonicity at that point would have been a pre-registered falsehood. The corrected, pre-registered claim is the envelope law, tested on fifty cells the theory pass had never seen. That sequence — kill fast, then refuse to promote a refuted conjecture — is the method contribution. H2 and H3 are moot as stated: no useful $\gamma^\ast$ exists, so a matching-condition study and a hardware-idle test do not proceed.
