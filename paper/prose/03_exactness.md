# 3. Exactness is free

The free lunch requires $q(y|x) = \langle y|\, \mathcal{E}(|x\rangle\langle x|) \,|y\rangle$ to be symmetric in $(x,y)$. Layden *et al.* already state the operational condition in their Supplemental Material: errors are harmless “provided such errors do not break the $Q(s'|s)=Q(s|s')$ symmetry on average.” Our contribution is the channel-level *classification* of which physical noise satisfies that condition, at any strength, together with a quantitative bound for the one realistic violator.

The proposal basis $\{|x\rangle\}$ is the computational basis throughout; transposes are taken in this basis.

## 3.1 Transpose-closed channels

**Theorem 1 (transpose-closed Kraus sets).** Let $\mathcal{E}(\rho) = \sum_a K_a \rho K_a^\dagger$ admit a Kraus representation $\{K_a\}_{a=1}^{m}$ that is closed under transposition up to unitary remixing,
\begin{equation}
  K_a^{\mathsf T}
  =
  \sum_b u_{ab}\, K_b
  \qquad
  \text{for some unitary } u \in \mathrm{U}(m).
  \tag{TC}
\end{equation}
Then $q(y|x) = q(x|y)$ for all $x,y$.

*Proof.* For real basis vectors, $\langle x|K_a|y\rangle = \langle y|K_a^{\mathsf T}|x\rangle$. Hence
\begin{equation}
  q(x|y)
  =
  \sum_a \bigl|\langle x|K_a|y\rangle\bigr|^2
  =
  \sum_a \bigl|\langle y|K_a^{\mathsf T}|x\rangle\bigr|^2
  =
  \sum_a \Bigl|\sum_b u_{ab}\, \langle y|K_b|x\rangle\Bigr|^2
  =
  \sum_b \bigl|\langle y|K_b|x\rangle\bigr|^2
  =
  q(y|x),
\end{equation}
the last-but-one step because $u$ preserves the $\ell^2$-norm of the amplitude vector $v_b = \langle y|K_b|x\rangle$. ∎

Condition (TC) says that $\{K_a^{\mathsf T}\}$ is *also* a Kraus representation of $\mathcal{E}$. The set $\{K_a^{\mathsf T}\}$ always represents the map $\Theta \circ \mathcal{E}^\star \circ \Theta$, where $\Theta$ is transposition and $\mathcal{E}^\star$ is the Heisenberg adjoint (Kraus $\{K_a^\dagger\}$). Two Kraus sets represent the same channel if and only if they are unitarily related, so (TC) is exactly the representation-independent identity
\begin{equation}
  \mathcal{E}
  =
  \Theta \circ \mathcal{E}^\star \circ \Theta.
  \tag{TC$'$}
\end{equation}
A channel either has a transpose-closed Kraus set or it does not.

Unitary remixing preserves $\sum_a A_a^\dagger A_a$, so (TC) implies $\sum_a (K_a^{\mathsf T})^\dagger (K_a^{\mathsf T}) = \sum_a K_a^\dagger K_a = I$, hence $\mathcal{E}(I) = I$: every transpose-closed channel is unital. A symmetric proposal is column-stochastic and symmetric, hence doubly stochastic, and $\sum_x q(y|x) = \langle y|\mathcal{E}(I)|y\rangle$, so
\begin{equation}
  \mathrm{diag}\bigl(\mathcal{E}(I)\bigr) = 1
  \quad
  \text{is necessary for symmetry.}
  \tag{N}
\end{equation}
Non-unital noise with a non-flat diagonal of $\mathcal{E}(I)$ — any channel that relaxes toward a preferred state, including finite-temperature amplitude damping — breaks symmetry before any interference argument is needed.

Condition (TC) is sufficient, not necessary. Symmetry constrains only the diagonal-to-diagonal block of $\mathcal{E}$ (the transition matrix $P = P^{\mathsf T}$), while (TC$'$) constrains the whole superoperator. Contrived channels can be symmetric without (TC). The honest statement, and the one we make, is structural: every physically arising symmetric case below satisfies (TC), and the physically arising violator (finite-$T$ damping) already fails the weaker necessary condition (N).

## 3.2 Lindblad semigroups

**Theorem 2 (Lindblad semigroups).** Let $\mathcal{L}(\rho) = -i[H,\rho] + \sum_j \gamma_j \mathcal{D}[L_j](\rho)$. Suppose
(i) $H = H^{\mathsf T}$ is real symmetric;
(ii) the weighted jump set is transpose-closed: there is a permutation $j \mapsto j'$ with $L_j^{\mathsf T} = e^{i\phi_j} L_{j'}$ and $\gamma_j = \gamma_{j'}$;
(iii) $\sum_j \gamma_j L_j^\dagger L_j$ is real symmetric, or equivalently the effective non-Hermitian Hamiltonian $H_{\mathrm{eff}} = H - (i/2)\sum_j \gamma_j L_j^\dagger L_j$ satisfies $H_{\mathrm{eff}}^{\mathsf T} = H_{\mathrm{eff}}$.
Then $\mathcal{E}_t = e^{t\mathcal{L}}$ satisfies (TC) for every $t \ge 0$, hence $q_t(y|x) = q_t(x|y)$ for all $t$.

*Proof (time-reversed Dyson unravelling).* The time-ordered decomposition of $e^{t\mathcal{L}}$ is the continuous Kraus family indexed by jump records $\omega = (m;\, t_1 < \cdots < t_m;\, j_1,\ldots,j_m)$,
\begin{equation}
  K_\omega
  =
  G(t-t_m)\, \sqrt{\gamma_{j_m}} L_{j_m} \cdots \sqrt{\gamma_{j_1}} L_{j_1}\, G(t_1),
  \qquad
  G(s) = e^{-i H_{\mathrm{eff}} s},
\end{equation}
with $e^{t\mathcal{L}}(\rho) = \sum_m \int dt_1\cdots dt_m \sum_{j_1\ldots j_m} K_\omega \rho K_\omega^\dagger$. Transposition reverses operator order. By (iii), $G(s)^{\mathsf T} = G(s)$; by (ii), each $L_j^{\mathsf T}$ is a phase times $L_{j'}$ at the same rate. Hence
\begin{equation}
  K_\omega^{\mathsf T}
  =
  e^{i\Phi(\omega)}\, K_{\tilde\omega},
  \qquad
  \tilde\omega
  =
  (m;\, t-t_m < \cdots < t-t_1;\, j_m',\ldots,j_1'),
\end{equation}
the time-reversed, transpose-relabelled record. The map $\omega \mapsto \tilde\omega$ is a measure-preserving involution of the index set (Lebesgue measure on the time-simplex is invariant under $s \mapsto t-s$; the rate weights match by (ii)), and phases are killed by $|\cdot|^2$. The Kraus family is therefore transpose-closed and Theorem 1 applies. ∎

Condition (iii) is implied by (i)+(ii) when the jumps are real (up to phase) and normal ($L^{\mathsf T}L = LL^{\mathsf T}$); every row of Table 1 has normal jumps. Time-reversal is load-bearing: a product of symmetric operators is not symmetric, $(AB)^{\mathsf T} = BA$, so “each instant is symmetric” does not give “the semigroup is symmetric.” Naive composition fails; the Dyson involution is the mechanism. Symmetry survives convex mixtures — including Layden’s random $t$-window and a random $\gamma$ — and time-reversal-symmetric compositions, but not arbitrary composition of two different symmetric channels.

## 3.3 Which physical noise is free

Table 1 and Fig.~1 collect the classification. Computational-basis dephasing ($Z_i$ jumps, any rate), dephasing in *any* real basis (jumps $A = VDV^{\mathsf T}$ with $V$ real orthogonal), depolarizing and arbitrary Pauli-jump noise, and infinite-temperature relaxation ($\sigma^-$ and $\sigma^+$ at equal rates) all satisfy (TC). Amplitude damping ($\sigma^-$ only) and finite-$T$ relaxation at unequal rates fail (N) and break symmetry.

The last two rows are the sharp pair: the same jump operators, and the matching condition $\gamma_+ = \gamma_-$ is exactly what flips symmetry on. Noise that drives toward the maximally mixed state preserves the free lunch; noise that knows a preferred state ($T_1$ relaxation toward $|0\rangle$) breaks it.

Certification (`scripts/run_r1.py`; tests I10–I12) pins every row. The worst defect over all transpose-closed channels is $1.2\times 10^{-14}$ across $n\in\{4,5\}$ ($n=6$ for computational dephasing), $\gamma/\Delta \in \{0.1,1,10\}$, and $t\Delta \in \{0.5,2,8\}$. Both negative controls — amplitude damping, and unequal-rate $\sigma^\pm$ with $\gamma_+ = \gamma_-/4$ — break at defect $\ge 3.5\times 10^{-2}$. The R1-file maximum for amplitude damping is $0.352$ (at $\kappa = 0.1\Delta$, $t\Delta \le 8$); an older grid’s $0.55$ is not in the current file and is not used here.

**Table 1.** Channel classes, transpose closure, and certified symmetry defect $\max_{x,y}|q(y|x)-q(x|y)|$.

| Noise channel | Transpose closure | Symmetric? | Certified defect |
|---|---|---|---|
| Computational-basis dephasing, jumps $Z_i$, any rate | $Z_i^{\mathsf T} = Z_i$ | yes | $\le 3.3\times 10^{-16}$ |
| Dephasing in any real basis, $A = VDV^{\mathsf T}$ | $A^{\mathsf T} = A$ | yes | $\le 1.3\times 10^{-14}$ |
| Depolarizing / Pauli-jump noise (rates arbitrary) | $X^{\mathsf T}=X$, $Z^{\mathsf T}=Z$, $Y^{\mathsf T}=-Y$ | yes | $\le 10^{-15}$ |
| Infinite-$T$ relaxation (equal-rate $\sigma^\pm$) | $(\sigma^-)^{\mathsf T}=\sigma^+$, rates matched | yes | $\le 10^{-15}$ |
| Amplitude damping / unequal-rate $\sigma^\pm$ | $(\sigma^-)^{\mathsf T}=\sigma^+\notin$ set; fails (N) | no | $\ge 3.5\times 10^{-2}$ (file max $0.352$) |

**Figure 1.** Symmetry defect versus channel class on a log scale, from `docs/R1_results.txt`. Transpose-closed classes sit at machine precision; amplitude damping and unequal-rate $\sigma^\pm$ sit between $3.5\times 10^{-2}$ and $0.352$. The equal/unequal $\sigma^\pm$ pair is highlighted: the same jumps, and only the rate-matching condition, decide exactness.

Device noise is, to a first accounting, dephasing ($T_\varphi$) plus amplitude damping ($T_1$) plus gate depolarizing plus coherent overrotation (real $H$ errors). By Table 1, $T_\varphi$ at any rate, depolarizing gate noise, and real-Hamiltonian miscalibration are all exactness-free. *$T_1$ relaxation is the unique realistic bias channel.* A hardware claim has to bound or estimate only the damping component; everything else rides free. That is the formal content of the robustness Layden *et al.* observed empirically.

## 3.4 $T_1$ bias: naive Metropolis versus Hastings

A device that keeps the free-lunch Metropolis ratio on a $\kappa$-damped proposal $\tilde q$ is *not* running the exact Hastings kernel. Write $P_H$ for Hastings on $\tilde q$ (acceptance includes the $q$-ratio; stationary distribution exactly $\pi$) and $P_M$ for naive Metropolis (acceptance $\min(1,\pi(y)/\pi(x))$; stationary $\tilde\pi \neq \pi$ in general). The theorem is not $\|\tilde q_{\kappa=0} - \tilde q_\kappa\|$; that is a proposal-TV statement and is not controlled by the symmetry defect. Write $\varepsilon = \max_{x,y} |\tilde q(y|x) - \tilde q(x|y)|$ for the R1 defect.

**Theorem 3 (per-step TV).** For every state $x$,
\begin{equation}
  \bigl\| P_M(\cdot|x) - P_H(\cdot|x) \bigr\|_{\mathrm{TV}}
  \le
  \sum_{y\neq x} \frac{\pi(y)}{\pi(x)}\, \bigl|\tilde q(y|x) - \tilde q(x|y)\bigr|
  \le
  \varepsilon \bigl(1/\pi(x) - 1\bigr).
\end{equation}
Uniformly over $x$,
\begin{equation}
  \|P_M - P_H\|_{\mathrm{TV},\infty}
  \le
  \varepsilon \bigl(1/\pi_{\min} - 1\bigr),
\end{equation}
where $\pi_{\min} = \min_x \pi(x)$ and $\|\cdot\|_{\mathrm{TV},\infty} = \max_x \|\cdot(\cdot|x)\|_{\mathrm{TV}}$.

*Proof.* For $y\neq x$, $|P_M(y|x)-P_H(y|x)| = \tilde q(y|x)\, |\min(1,r)-\min(1,r\rho)|$ with $r=\pi(y)/\pi(x)$ and $\rho = \tilde q(x|y)/\tilde q(y|x)$ ($\rho:=1$ if $\tilde q(y|x)=0$). The elementary inequality $|\min(1,a)-\min(1,b)|\le |a-b|$ gives $|\min(1,r)-\min(1,r\rho)| \le r|1-\rho|$, hence
\begin{equation}
  |\Delta P(y|x)|
  \le
  \tilde q(y|x)\, r\, |1-\rho|
  =
  \frac{\pi(y)}{\pi(x)}\, \bigl|\tilde q(y|x)-\tilde q(x|y)\bigr|.
\end{equation}
The diagonal difference equals $-\sum_{y\neq x}\Delta P(y|x)$, so $|\Delta P(x|x)| \le \sum_{y\neq x}|\Delta P(y|x)|$. Therefore
\begin{equation}
  \|\Delta P(\cdot|x)\|_{\mathrm{TV}}
  =
  \tfrac12 \sum_y |\Delta P(y|x)|
  \le
  \sum_{y\neq x} |\Delta P(y|x)|
  \le
  \varepsilon\bigl(1/\pi(x)-1\bigr).
\end{equation}
∎

If $\varepsilon=0$ — every transpose-closed channel in Table 1 — then $P_M=P_H$ and there is no free-lunch bias. $T_1$ remains the unique realistic channel that can make $\varepsilon>0$. Hastings on a $T_1$-damped proposal is still exact; the cost is evaluating the $q$-ratio.

**Theorem 4 (stationary TV).** Let $\delta = \delta(P_H) = 1-|\lambda_2(P_H)|$ be the spectral gap of the exact Hastings kernel. Then
\begin{equation}
  \|\tilde\pi - \pi\|_{\mathrm{TV}}
  \le
  \frac{1}{\delta}\, \pi_{\min}^{-1/2}\, \|P_M-P_H\|_{\mathrm{TV},\infty}
  \le
  \varepsilon \bigl(1/\pi_{\min}-1\bigr)\, \pi_{\min}^{-1/2}/\delta.
\end{equation}

*Proof.* Stationarity gives $\tilde\pi P_M = \tilde\pi$ and $\pi P_H = \pi$, so $(\tilde\pi-\pi)(I-P_H) = \tilde\pi(P_M-P_H) =: \nu$. Work in $L^2(\pi)$ via densities $f = d\mu/d\pi$. $P_H$ is reversible, hence self-adjoint on densities in $L^2(\pi)$; on the mean-zero subspace, $\|(I-P_H)^{-1}\|_{L^2(\pi)} \le 1/\delta$. Both $\tilde\pi-\pi$ and $\nu$ are mean-zero. With $f = d(\tilde\pi-\pi)/d\pi$ and $g = d\nu/d\pi$,
\begin{equation}
  \|\tilde\pi-\pi\|_{\mathrm{TV}}
  =
  \tfrac12 \|f\|_{L^1(\pi)}
  \le
  \tfrac12 \|f\|_{L^2(\pi)}
  \le
  \tfrac{1}{2\delta}\|g\|_{L^2(\pi)}.
\end{equation}
Then $\|g\|_{L^2(\pi)}^2 = \sum_y \nu(y)^2/\pi(y) \le \pi_{\min}^{-1}(\sum_y|\nu(y)|)^2$, so $\|g\|_{L^2(\pi)} \le \pi_{\min}^{-1/2}\cdot 2\|\nu\|_{\mathrm{TV}}$. Finally $\|\nu\|_{\mathrm{TV}} = \|\tilde\pi(P_M-P_H)\|_{\mathrm{TV}} \le \|P_M-P_H\|_{\mathrm{TV},\infty}$. Combining and applying Theorem 3 gives the claim. ∎

The simpler expression $B_{\mathrm{naive}} = \varepsilon(1/\pi_{\min}-1)/\delta$ — Theorem 4 without the $\pi_{\min}^{-1/2}$ factor — is *not* proved. The $1/\delta$ inverse lives in $L^2(\pi)$, and the passage to TV costs $\pi_{\min}^{-1/2}$. $B_{\mathrm{naive}}$ held in every certified cell (with $10^6$–$10^{21}$ slack); we treat it as empirical. The theorem is the displayed line.

The factor $\pi_{\min}^{-3/2}/\delta$ is exponentially pessimistic at low $T$: $\pi_{\min}$ is Gibbs-small and $\delta$ is the worst-case gap. This is a guaranteed envelope, not a prediction. Certification (`scripts/run_amp_damp_bias.py`; test I13; $n\le 5$, three e01-chain cells, five $\kappa/\Delta$ values) finds measured stationary TV of order $\varepsilon$, typically $0.7$–$3\times$ the per-step TV, while the envelope sits $10^6$–$10^{21}$ above it. At $T=0.3$ the uniform bound is vacuous ($\pi_{\min}\sim 10^{-18}$) while the measured bias at device-relevant $\kappa/\Delta = 0.01$ is $2.5\%$. No claim is made at hardware $n$; no claim is made that $T_1$ is negligible on devices. The claim is: $T_1$ is the only realistic term to budget, the per-step TV error is $O(\varepsilon)$, and $\varepsilon$ is a few percent at $\kappa \sim 0.01\Delta$ on the G01 window (tens of percent at $\kappa \sim 0.1\Delta$).

A device that needs $\|\tilde\pi-\pi\|_{\mathrm{TV}} < \eta$ should treat $\varepsilon \lesssim \eta$ as the working requirement — what the numbers do — not $\varepsilon \lesssim \eta\,\delta\,\pi_{\min}$, what the envelope says. If that is too tight for the device’s $T_1$, estimate the $q$-ratio and run Hastings.
