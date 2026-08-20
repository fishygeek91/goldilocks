"""Walk Hamiltonians on the n-qubit hypercube, and energy-scale (Delta) definitions.

Layden-family walk Hamiltonian (arXiv:2203.12497 convention, simplified):

    H(alpha) = (1 - alpha) * H_prob + alpha * H_mix

where H_prob = diag(problem energies) in the computational basis and
H_mix = sum_i X_i.  alpha=1 is a pure transverse-field mixer.  gamma=0
evolution under H(alpha) with Layden's time window IS the E01 quench —
that limit is our regression anchor.

All Hamiltonians here are REAL SYMMETRIC matrices (numpy float64). That
reality is what the R1 symmetry argument leans on — do not add complex
terms (e.g. Y couplings) without revisiting docs/R1_symmetry.md.
"""
from __future__ import annotations

import numpy as np

__all__ = [
    "mixer",
    "walk_hamiltonian",
    "delta_mixer",
    "delta_edge_energy",
    "delta_spectral_width",
]


def _pauli_x_on(i: int, n: int) -> np.ndarray:
    """Dense X_i on n qubits (real). Qubit 0 = most significant bit."""
    X = np.array([[0.0, 1.0], [1.0, 0.0]])
    I2 = np.eye(2)
    out = np.array([[1.0]])
    for k in range(n):
        out = np.kron(out, X if k == i else I2)
    return out


def mixer(n: int) -> np.ndarray:
    """H_mix = sum_i X_i (adjacency matrix of the n-hypercube)."""
    H = np.zeros((2**n, 2**n))
    for i in range(n):
        H += _pauli_x_on(i, n)
    return H


def walk_hamiltonian(problem_energies: np.ndarray, alpha: float) -> np.ndarray:
    """H(alpha) = (1-alpha) diag(E) + alpha * mixer. Real symmetric.

    problem_energies: shape (2**n,) — energies of the SURROGATE/walk problem.
    Exactness note: these may equal the target's energies (native-Ising, v1)
    but the accept/reject step must never read them from here.
    """
    E = np.asarray(problem_energies, dtype=float)
    n = int(np.log2(E.size))
    assert 2**n == E.size, "problem_energies length must be a power of 2"
    return (1.0 - alpha) * np.diag(E) + alpha * mixer(n)


# ---- Candidate Delta definitions for H2 (gamma*/Delta constant hunt) ----
# The definition that makes gamma*/Delta invariant across targets IS the
# result (TASKS.md Phase 2). Compute all three for every scan.

def delta_mixer(alpha: float) -> float:
    """Delta_1: bare hopping strength = alpha (mixer coefficient)."""
    return float(alpha)


def delta_edge_energy(problem_energies: np.ndarray, alpha: float) -> float:
    """Delta_2: (1-alpha) * median |E(y)-E(x)| over hypercube edges x~y."""
    E = np.asarray(problem_energies, dtype=float)
    n = int(np.log2(E.size))
    diffs = []
    for x in range(E.size):
        for i in range(n):
            y = x ^ (1 << i)
            if y > x:
                diffs.append(abs(E[y] - E[x]))
    return float((1.0 - alpha) * np.median(diffs))


def delta_spectral_width(H: np.ndarray) -> float:
    """Delta_3: full spectral width of the walk Hamiltonian, max(w)-min(w)."""
    w = np.linalg.eigvalsh(H)
    return float(w[-1] - w[0])
