"""Classical baseline kernels (self-contained mirrors of TunnelVision's).

SingleFlipKernel: flip one uniformly chosen spin — symmetric.
UniformFlipKernel: propose a uniform random state — symmetric.
(AddDeleteSwap is spike-and-slab-specific and does not apply to native-Ising
v1; if a target with asymmetric boundary moves returns, port it from
TunnelVision, where its boundary asymmetry is already handled.)
"""
from __future__ import annotations

import math

from .base import ProposalKernel


class SingleFlipKernel(ProposalKernel):
    def __init__(self, n: int):
        self.n = n
        self._logq = -math.log(n)

    @property
    def is_symmetric(self) -> bool:
        return True

    def propose(self, x: int, rng) -> tuple[int, float, float]:
        i = int(rng.integers(self.n))
        return x ^ (1 << i), self._logq, self._logq


class UniformFlipKernel(ProposalKernel):
    def __init__(self, n: int):
        self.n = n
        self._logq = -n * math.log(2)

    @property
    def is_symmetric(self) -> bool:
        return True

    def propose(self, x: int, rng) -> tuple[int, float, float]:
        return int(rng.integers(2**self.n)), self._logq, self._logq
