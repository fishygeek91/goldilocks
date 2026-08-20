"""Exact Metropolis-Hastings engine — the exactness boundary.

Minimal self-contained engine mirroring TunnelVision's contract so goldilocks
runs standalone; swap in tunnelvision.engine for the paper runs (it carries
the battle-tested diagnostics wiring).  Nothing quantum is imported here.

Acceptance: log a = [log pi(y) - log pi(x)] + [log_q_rev - log_q_fwd],
accept if log u < min(0, log a).  Kernels report both q logs; symmetric
kernels report equal values and the correction cancels — the engine does NOT
special-case symmetry (honesty over micro-optimization; R1 asymmetry, if any,
flows through automatically).
"""
from __future__ import annotations

import math
import time

import numpy as np


def run_chain(target, kernel, n_steps: int, x0: int, seed: int = 0):
    """Returns dict with states (int array), acceptance rate, wall seconds.

    ESS/sec accounting (TunnelVision lesson #2): wall time covers the WHOLE
    loop including proposal generation. For hardware kernels, propose() must
    block on the device so this number stays honest.
    """
    rng = np.random.default_rng(seed)
    x = int(x0)
    lp_x = target.log_prob(x)
    states = np.empty(n_steps, dtype=np.int64)
    accepts = 0
    t0 = time.perf_counter()
    for k in range(n_steps):
        y, lq_f, lq_r = kernel.propose(x, rng)
        lp_y = target.log_prob(y)
        log_a = (lp_y - lp_x) + (lq_r - lq_f)
        if math.log(rng.random()) < min(0.0, log_a):
            x, lp_x = y, lp_y
            accepts += 1
        states[k] = x
    wall = time.perf_counter() - t0
    return {"states": states, "accept_rate": accepts / n_steps, "wall_seconds": wall}
