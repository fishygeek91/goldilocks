# 2. Setup

We sample a target $\pi$ on the hypercube $\{0,1\}^n$. The Metropolis–Hastings (MH) kernel built from a proposal $q(\cdot|x)$ is
\begin{equation}
  P(y|x)
  =
  q(y|x)\, a(y,x)
  \qquad (y \neq x),
\end{equation}
with $P(x|x) = 1 - \sum_{y \neq x} P(y|x)$ and acceptance
\begin{equation}
  a(y,x)
  =
  \min\Bigl(1,\;
  \frac{\pi(y)\, q(x|y)}{\pi(x)\, q(y|x)}\Bigr).
\end{equation}
If $q$ is symmetric, $q(y|x) = q(x|y)$, the proposal ratio cancels and the acceptance collapses to the evaluation-free Metropolis ratio $\min(1,\pi(y)/\pi(x))$. That is the free lunch of Layden *et al.* [Nature **619**, 282 (2023)]: a quantum proposal that never has to be evaluated still yields an exactly correct sampler, provided symmetry holds.

The family we study is a *dephased quantum walk* used only as a proposal. The walk Hamiltonian is real symmetric,
\begin{equation}
  H
  =
  (1-\alpha)\, \mathrm{diag}(E)
  +
  \alpha \sum_{i=1}^{n} X_i,
\end{equation}
with mixer weight $\alpha \in (0,1]$ and $E$ the classical energy whose Gibbs distribution is $\pi$. The generator is the Lindbladian
\begin{equation}
  \mathcal{L}(\rho)
  =
  -i[H,\rho]
  +
  \gamma \sum_{i=1}^{n} \mathcal{D}[Z_i](\rho),
  \qquad
  \mathcal{D}[A](\rho)
  =
  A\rho A^\dagger - \tfrac12 \{A^\dagger A,\rho\}.
\end{equation}
A single proposal from $x$ is a computational-basis measurement of $\mathcal{E}_t(|x\rangle\langle x|)$,
\begin{equation}
  q_t(y|x)
  =
  \langle y|\, \mathcal{E}_t(|x\rangle\langle x|) \,|y\rangle,
  \qquad
  \mathcal{E}_t = e^{t\mathcal{L}}.
\end{equation}
Following Layden, we average $t$ uniformly over a fixed window (in units of the spectral width $\Delta$ of $H$; the G01/G05 window is $t\Delta \in [2,12]$). The window-averaged proposal is written $q_\gamma$. Two limits are named: $\gamma = 0$ is the coherent quench of Layden *et al.*; $\gamma \to \infty$ is a Zeno freeze in the computational basis, recovered in practice as a lazy classical kernel.

Two equivalent realizations of $\mathcal{E}_t$ are used throughout. At $n \le 6$ we exponentiate the dense superoperator (or apply it sparsely on a time grid) and read the proposal matrix exactly. At larger $n$ the same channel is sampled by a quantum-trajectory unravelling: one shot is one Poisson record of phase kicks, one trajectory, and one proposal. That unravelling is also the circuit recipe (stochastic Hamiltonian phase kicks, or a collision scheme with ancilla resets). Because the jump statistics of computational-basis dephasing are state-independent, the trajectory sampler never consults $\pi$.

Classical baselines, used only as competitors and never as ingredients of the walk, are Metropolized single-flip (Hamming-1) and uniform-flip (the complete graph). Efficiency is reported as the MH spectral gap $\delta(P) = 1-|\lambda_2(P)|$ wherever the $2^n \times 2^n$ kernel can be built, and as effective sample size per step and per second on gated MCMC runs (Sec.~6). Nothing in this section is a claim about noise; the claims begin when $\gamma > 0$ or when the channel is replaced by a different physical noise model.
