"""Goldilocks: noise-assisted quantum-walk proposals for exact MCMC.

Exactness boundary (inherited from TunnelVision, binding):
- Kernels NEVER see target log-probabilities.
- Nothing quantum is imported on the accept/reject side.
- Kernels return (y, log_q_fwd, log_q_rev).
- The surrogate/walk Hamiltonian may use problem energies (Layden-style),
  but acceptance uses the exact target only.
"""

__version__ = "0.0.1"
