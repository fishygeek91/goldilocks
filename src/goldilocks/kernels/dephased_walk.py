"""The Goldilocks kernel: dephased quantum-walk proposal.

Dense implementation (n <= 6): precomputes the full proposal matrix
P[y, x] = <y| e^{tL}(|x><x|) |y> once at construction, then sampling is a
table lookup.  This is the SIMULATION path for G01/G02; the hardware path
(G03/G04) replaces the table with circuit shots and idle-delay-tuned gamma.

gamma limits (both must hold in tests):
- gamma = 0  -> Layden quench (E01 regression anchor).
- gamma -> infinity -> Zeno pinning: P -> identity (lazy walk that mostly
  stays put).  NOTE: the useful "classical" comparison point is therefore the
  finite-gamma incoherent-hopping regime, NOT gamma = infinity; the explicit
  classical baselines live in classical_walk.py.  (R2 task: write down the
  effective classical kernel of the large-but-finite-gamma regime.)

Time handling: t is averaged over a window (Layden: t ~ U[t_min, t_max])
by mixing proposal matrices — the mixture of symmetric matrices is symmetric,
so R1's certification extends to the averaged kernel.
"""
from __future__ import annotations

import numpy as np

from ..lindblad import proposal_matrix, symmetry_defect
from .base import ProposalKernel

_SYMMETRY_TOL = 1e-9  # certification threshold; revisit in docs/R1_symmetry.md


class DephasedWalkKernel(ProposalKernel):
    def __init__(
        self,
        H: np.ndarray,
        gamma: float,
        t_window: tuple[float, float],
        n_time_points: int = 8,
        kappa: float = 0.0,
        rng=None,
    ):
        self.gamma = float(gamma)
        self.kappa = float(kappa)
        if kappa == 0.0 and H.shape[0] > 4:
            from ..lindblad import averaged_proposal_matrix

            P = averaged_proposal_matrix(H, gamma, t_window, n_time_points)
        else:  # dense reference path (needed for kappa != 0)
            ts = np.linspace(t_window[0], t_window[1], n_time_points)
            P = np.zeros((H.shape[0], H.shape[0]))
            for t in ts:
                P += proposal_matrix(H, gamma, float(t), kappa)
            P /= len(ts)
        self._P = P
        self._logP = np.log(np.clip(P, 1e-300, None))
        self._defect = symmetry_defect(P)
        self._cum = np.cumsum(P, axis=0)  # column-wise CDFs for sampling

    @property
    def symmetry_defect(self) -> float:
        return self._defect

    @property
    def is_symmetric(self) -> bool:
        # Only assert what has been measured. kappa != 0 is expected to fail.
        return self._defect < _SYMMETRY_TOL

    @property
    def proposal_matrix(self) -> np.ndarray:
        return self._P

    def propose(self, x: int, rng) -> tuple[int, float, float]:
        u = rng.random()
        y = int(np.searchsorted(self._cum[:, x], u))
        y = min(y, self._P.shape[0] - 1)
        # Honest interface: report both logs even when symmetric (they cancel
        # in the engine; if asymmetric — kappa > 0 — the engine sees the truth).
        return y, float(self._logP[y, x]), float(self._logP[x, y])


class TrajectoryDephasedWalkKernel(ProposalKernel):
    """Trajectory-backed Goldilocks kernel for n > 8 (no proposal table).

    q(y|x) is not computed — exactness rests ENTIRELY on the R1 symmetry
    theorem (docs/R1_symmetry.md): for pure dephasing with real symmetric H
    and the time-symmetric jump process, q(y|x) = q(x|y), so the MH ratio is
    1 and we may report (0, 0).  Amplitude damping is NOT allowed here — the
    theorem does not cover it (and run_r1.py shows it fails empirically).
    Each propose() draws t ~ U[t_window] fresh (Layden-style averaging).
    """

    def __init__(self, H: np.ndarray, gamma: float, t_window: tuple[float, float]):
        from ..lindblad import TrajectorySampler

        self._sampler = TrajectorySampler(H, gamma)
        self._tw = t_window
        self.gamma = float(gamma)

    @property
    def is_symmetric(self) -> bool:
        return True  # theorem-backed (R1); certified numerically at n <= 6

    def propose(self, x: int, rng) -> tuple[int, float, float]:
        t = rng.uniform(*self._tw)
        return self._sampler.sample(x, t, rng), 0.0, 0.0
