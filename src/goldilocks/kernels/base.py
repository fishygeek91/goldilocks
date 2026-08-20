"""Kernel interface — identical contract to TunnelVision's kernels/base.py.

Invariants (enforced by tests/test_exactness.py):
- propose(x, rng) returns (y, log_q_fwd, log_q_rev); log values are LOGS of
  q(y|x) and q(x|y) up to a common additive constant (only the difference
  enters MH acceptance).
- Kernels never see target log-probabilities. Construction-time access to
  SURROGATE/walk energies is allowed (Layden-style); runtime access to the
  target is not.
"""
from __future__ import annotations

from abc import ABC, abstractmethod


class ProposalKernel(ABC):
    @abstractmethod
    def propose(self, x: int, rng) -> tuple[int, float, float]:
        """Return (y, log_q_fwd, log_q_rev) for current state x (int bitstring)."""

    @property
    def is_symmetric(self) -> bool:
        """True if q(y|x) == q(x|y) exactly, letting the engine skip the ratio.

        For DephasedWalkKernel this is a CLAIM certified by R1 — the kernel
        refuses to assert it until the defect has been measured (see there).
        """
        return False
