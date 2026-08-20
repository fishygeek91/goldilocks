"""Ising targets: pi(s) ~ exp(-E(s)/T), states as ints, spins s_i in {+1,-1}.

Native-Ising v1 (TunnelVision lesson #1): the walk Hamiltonian's diagonal IS
the target energy — no surrogate, no translation layer.  Instances:
- e01: the E01 ferromagnetic/random instance family (1D chain + fields) used
  as regression anchor; couplings drawn with a fixed seed for reproducibility.
- sk: Sherrington-Kirkpatrick (all-to-all Gaussian J) — the frustrated/glassy
  class where ENAQT logic predicts noise helps MOST (G01 retry / G02).
- rfim: random-field Ising chain.
"""
from __future__ import annotations

import numpy as np


class IsingTarget:
    def __init__(self, J: np.ndarray, h: np.ndarray, T: float):
        self.n = len(h)
        self.J, self.h, self.T = J, h, float(T)
        self._E = self._enumerate() if self.n <= 24 else None

    # -- construction helpers -------------------------------------------------
    @classmethod
    def e01_chain(cls, n: int, T: float, seed: int = 42) -> "IsingTarget":
        """1D chain, J ~ U[-2,2] on edges, h ~ U[-2,2] (Layden-style random)."""
        rng = np.random.default_rng(seed)
        J = np.zeros((n, n))
        for i in range(n - 1):
            J[i, i + 1] = rng.uniform(-2, 2)
        return cls(J, rng.uniform(-2, 2, n), T)

    @classmethod
    def sk(cls, n: int, T: float, seed: int = 7) -> "IsingTarget":
        rng = np.random.default_rng(seed)
        J = rng.normal(0.0, 1.0 / np.sqrt(n), (n, n))
        J = np.triu(J, 1)
        return cls(J, np.zeros(n), T)

    @classmethod
    def rfim_chain(cls, n: int, T: float, h_scale: float = 1.0, seed: int = 11) -> "IsingTarget":
        rng = np.random.default_rng(seed)
        J = np.zeros((n, n))
        for i in range(n - 1):
            J[i, i + 1] = 1.0
        return cls(J, rng.normal(0, h_scale, n), T)

    # -- energies / probabilities --------------------------------------------
    def spins(self, x: int) -> np.ndarray:
        bits = (x >> np.arange(self.n - 1, -1, -1)) & 1
        return 1.0 - 2.0 * bits  # bit 0 -> +1, bit 1 -> -1

    def energy(self, x: int) -> float:
        s = self.spins(x)
        return float(-s @ self.J @ s - self.h @ s)

    def _enumerate(self) -> np.ndarray:
        idx = np.arange(2**self.n)
        bits = (idx[:, None] >> np.arange(self.n - 1, -1, -1)[None, :]) & 1
        S = 1.0 - 2.0 * bits
        return -np.einsum("xi,ij,xj->x", S, self.J, S) - S @ self.h

    @property
    def energies(self) -> np.ndarray:
        """All 2^n energies (n <= 24 only) — feeds the walk Hamiltonian AND
        exact diagnostics. The MH engine reads log_prob(), never this array."""
        if self._E is None:
            raise ValueError("enumeration refused for n > 24 (E02c lesson: refuse loudly)")
        return self._E

    def log_prob(self, x: int) -> float:
        return -self.energy(x) / self.T

    def exact_dist(self) -> np.ndarray:
        w = np.exp(-(self.energies - self.energies.min()) / self.T)
        return w / w.sum()
