# 7. Outlook: energy concentration as a predictor

The observations of Secs.~4 and 5 fit a single accounting: the quench is valuable when its proposals sit on near-degenerate pairs, and dephasing spends that value by broadening proposal energy. We record that accounting as a conjecture, not as a theorem of this paper.

**Conjecture (energy concentration; C8).** The advantage of a proposal $q$ over trivial classical kernels is predicted by the proposal mass on near-degenerate pairs,
\begin{equation}
  C(q)
  =
  \sum_{x,y} \pi(x)\, q(y|x)\, \mathbf{1}\bigl[\,|E(y)-E(x)| \le \kappa T\,\bigr],
\end{equation}
for an $O(1)$ window $\kappa$. Kernels should be engineered for energy concentration, not for delocalization.

Everything already measured is consistent with $C(q)$ and does not prove it. Dephasing lowers $C$ (broadened proposal energy) and erodes advantage (G01, G05 L2(b)). Time-averaging preserves $C$, because energy conservation is per-realization of a real Hamiltonian, and does not erode advantage the way dephasing does. The $\alpha=1$ corner has flat $E$, so $C$ is identically $1$ and noise can only help sub-classically — which is what the telegraph solution shows. Figure 5 is the cartoon of that split, not a fit to data.

**Figure 5 (schematic).** Proposal energy change $\Delta E = E(y)-E(x)$ at $\gamma=0$ (narrow, sitting inside the Metropolis window) versus $\gamma>0$ (broadened, spilling out of the window). The overlaid curve is the Metropolis acceptance $\min(1,e^{-\Delta E/T})$. Energy concentration $C(q)$ is a proposed predictor of advantage, not a theorem of this paper.

A next-project test is direct: compute $C(q)$ for the quench, the dephased family, single-flip, and uniform-flip across a draw of targets, and regress measured ESS (or gap) advantage on $C$. If the regression is tight, $C$ becomes a design objective. If it is not, the mechanism of Sec.~5 is still the right qualitative story and the scalar is the wrong summary.

Three escapes from G01 were not pursued, and we do not want them read as hidden rescues of H1. Site-dependent rates $\gamma_i$ could *shape* where proposals land rather than how coherent they are. Noise in the basis of a frustrated subspace, rather than the computational basis, is a different channel, still transpose-closed if the jumps are real-symmetric (Theorem 1) but not the family G01/G05 scanned. Hitting-time objectives — first arrival at a ground-state set — restore a sink, and are optimization, not sampling. Each is a new hypothesis. None of them, if true, would change Theorems 1–4 or the envelope law as stated for uniform computational-basis dephasing inside exact MH.
