"""Propagation for the dephased hypercube walk: dense, sparse, and trajectories.

Master equation (hbar = 1):

    drho/dt = -i[H, rho] + gamma * sum_i D[Z_i](rho) + kappa * sum_i D[s^-_i](rho)

with D[A](rho) = A rho A^dag - {A^dag A, rho}/2.  For Z_i (Z_i^2 = I) this is
Z_i rho Z_i - rho: pure computational-basis dephasing at rate gamma — the
Goldilocks knob.  kappa adds amplitude damping (R1 break test only; dense path
only).

Three propagation paths, all agreeing where they overlap (tested):
- dense   n <= 5 : full 4^n x 4^n expm.  Reference implementation.
- sparse  n <= 8 : sparse Liouvillian + expm_multiply on the 2^n population
                   columns.  Orders of magnitude faster; exact.
- traj    n <= ~14: exact stochastic unravelling.  Because Z_i^dag Z_i = I,
                   the MCWF jump rate is state-INDEPENDENT: jumps form a
                   Poisson process of rate n*gamma, each jump applies Z_i with
                   i uniform, and between jumps the evolution is the pure
                   unitary e^{-iHt}.  ("Random telegraph phase kicks.")  This
                   is also the R1 proof's structure and the G03 circuit
                   recipe (stochastic-Hamiltonian unravelling): one shot ==
                   one trajectory == one proposal.

Convention: column-major vec (numpy order='F'); vec index of rho_{ij} is
i + j*d.  All operators real, no conjugates appear.
"""
from __future__ import annotations

import numpy as np
from scipy.linalg import expm, eigh
from scipy.sparse import csr_matrix, identity as sp_identity, kron as sp_kron, diags
from scipy.sparse.linalg import expm_multiply

__all__ = [
    "liouvillian",
    "proposal_matrix",
    "symmetry_defect",
    "TrajectorySampler",
    "rotated_dephasing_jumps",
    "pauli_jumps",
    "thermal_jumps",
]

# A "jump" is a (rate, operator) pair; operators may be complex (e.g. Y).
Jump = tuple[float, np.ndarray]

_MAX_DENSE_N = 5
_MAX_SPARSE_N = 8


def _z_diag(i: int, n: int) -> np.ndarray:
    d = 2**n
    idx = np.arange(d)
    bit = (idx >> (n - 1 - i)) & 1
    return np.where(bit == 0, 1.0, -1.0)


def _single_site(op: np.ndarray, i: int, n: int) -> np.ndarray:
    """Dense embedding of a 2x2 operator on qubit i (qubit 0 = MSB)."""
    I2 = np.eye(2, dtype=op.dtype)
    out = np.array([[1.0]], dtype=op.dtype)
    for k in range(n):
        out = np.kron(out, op if k == i else I2)
    return out


def _sigma_minus(i: int, n: int) -> np.ndarray:
    return _single_site(np.array([[0.0, 1.0], [0.0, 0.0]]), i, n)


# ---- Jump-set builders for the characterization theorem (Table 1 rows) ----

def rotated_dephasing_jumps(n: int, gamma: float, seed: int = 0) -> list[Jump]:
    """Dephasing in a random REAL basis: jumps A_i = V Z_i V^T with V a seeded
    random real orthogonal matrix.  A_i is real symmetric => transpose-closed
    (Theorem 2(ii)); the characterization theorem predicts symmetry."""
    rng = np.random.default_rng(seed)
    d = 2**n
    V, _ = np.linalg.qr(rng.standard_normal((d, d)))
    return [(gamma, V @ np.diag(_z_diag(i, n)) @ V.T) for i in range(n)]


def pauli_jumps(n: int, gx: float, gy: float, gz: float) -> list[Jump]:
    """Depolarizing-type noise: X_i, Y_i, Z_i jumps at rates (gx, gy, gz).
    X^T = X, Z^T = Z, Y^T = -Y (phase only) => transpose-closed."""
    X = np.array([[0.0, 1.0], [1.0, 0.0]])
    Y = np.array([[0.0, -1j], [1j, 0.0]])
    Z = np.array([[1.0, 0.0], [0.0, -1.0]])
    jumps: list[Jump] = []
    for i in range(n):
        for g, op in ((gx, X), (gy, Y), (gz, Z)):
            if g != 0.0:
                jumps.append((g, _single_site(op, i, n)))
    return jumps


def thermal_jumps(n: int, k_down: float, k_up: float) -> list[Jump]:
    """Relaxation sigma^- at rate k_down and excitation sigma^+ at rate k_up.
    (sigma^-)^T = sigma^+, so the set is transpose-closed IFF k_down == k_up
    (infinite-temperature limit).  k_up != k_down is the symmetry breaker."""
    jumps: list[Jump] = []
    for i in range(n):
        sm = _sigma_minus(i, n)
        if k_down != 0.0:
            jumps.append((k_down, sm))
        if k_up != 0.0:
            jumps.append((k_up, sm.T))
    return jumps


def _check_H(H: np.ndarray) -> tuple[int, int]:
    H = np.asarray(H, dtype=float)
    d = H.shape[0]
    n = int(np.log2(d))
    assert 2**n == d and H.shape == (d, d)
    assert np.allclose(H, H.T, atol=1e-12), "H must be real symmetric (see docs/R1_symmetry.md)"
    return d, n


def _hamming_matrix(n: int) -> np.ndarray:
    d = 2**n
    idx = np.arange(d)
    x = idx[:, None] ^ idx[None, :]
    # popcount via bit tricks (n <= 24)
    h = np.zeros((d, d), dtype=float)
    for b in range(n):
        h += (x >> b) & 1
    return h


def liouvillian(
    H: np.ndarray, gamma: float, kappa: float = 0.0, jumps: list[Jump] | None = None
) -> np.ndarray:
    """Dense Liouvillian (reference; n <= _MAX_DENSE_N).

    gamma: computational-basis dephasing rate (Z_i jumps).
    kappa: amplitude-damping rate (sigma^-_i jumps) — R1's break test.
    jumps: additional generic (rate, operator) Lindblad terms, possibly
           complex — used for the characterization-theorem certification
           (rotated-basis dephasing, depolarizing, thermal sigma^+/-).
    Convention (column-major vec): vec(A rho B) = kron(B^T, A) vec(rho).
    """
    d, n = _check_H(H)
    if n > _MAX_DENSE_N:
        raise ValueError(f"dense Liouvillian refused for n={n} > {_MAX_DENSE_N}; use sparse/trajectories")
    H = np.asarray(H, dtype=float)
    I = np.eye(d)
    L = -1j * (np.kron(I, H) - np.kron(H.T, I))
    if gamma != 0.0:
        for i in range(n):
            z = _z_diag(i, n)
            L += gamma * (np.kron(np.diag(z), np.diag(z)) - np.eye(d * d))
    all_jumps: list[Jump] = list(jumps) if jumps else []
    if kappa != 0.0:
        all_jumps += [(kappa, _sigma_minus(i, n)) for i in range(n)]
    for rate, A in all_jumps:
        A = np.asarray(A, dtype=complex)
        AtA = A.conj().T @ A
        L = L + rate * (
            np.kron(A.conj(), A)
            - 0.5 * (np.kron(np.eye(d), AtA) + np.kron(AtA.T, np.eye(d)))
        )
    return L


def _sparse_liouvillian(H: np.ndarray, gamma: float):
    """Sparse L for pure dephasing.  Dephasing is DIAGONAL in the vec basis:
    coherence rho_{ij} decays at 2*gamma*hamming(i, j)."""
    d, n = _check_H(H)
    Hs = csr_matrix(np.asarray(H, dtype=complex))
    I = sp_identity(d, format="csr", dtype=complex)
    L = -1j * (sp_kron(I, Hs, format="csr") - sp_kron(Hs.T, I, format="csr"))
    if gamma != 0.0:
        ham = _hamming_matrix(n)                      # ham[i, j]
        decay = (-2.0 * gamma * ham).reshape(-1, order="F")  # vec index i + j*d
        L = L + diags(decay.astype(complex), format="csr")
    return L


def proposal_matrix(
    H: np.ndarray,
    gamma: float,
    t: float,
    kappa: float = 0.0,
    method: str = "auto",
    jumps: list[Jump] | None = None,
) -> np.ndarray:
    """P[y, x] = <y| exp(tL)(|x><x|) |y> — the kernel's proposal distribution.

    method: 'auto' (dense for n <= 5 or kappa != 0 or generic jumps, else
    sparse), 'dense', 'sparse'.  kappa != 0 or jumps require the dense path.
    """
    d, n = _check_H(H)
    has_generic = kappa != 0.0 or bool(jumps)
    if method == "auto":
        method = "dense" if (n <= _MAX_DENSE_N or has_generic) else "sparse"
    if has_generic and method != "dense":
        raise ValueError("amplitude damping / generic jumps implemented on the dense path only")

    if method == "dense":
        E = expm(t * liouvillian(H, gamma, kappa, jumps))
        diag_idx = np.arange(d) * (d + 1)
        P = np.real(E[np.ix_(diag_idx, diag_idx)])
    elif method == "sparse":
        if n > _MAX_SPARSE_N:
            raise ValueError(f"sparse path refused for n={n} > {_MAX_SPARSE_N}; use TrajectorySampler")
        L = _sparse_liouvillian(H, gamma)
        diag_idx = np.arange(d) * (d + 1)
        B = np.zeros((d * d, d), dtype=complex)
        B[diag_idx, np.arange(d)] = 1.0          # columns = vec(|x><x|)
        out = expm_multiply(L * t, B)
        P = np.real(out[diag_idx, :])
    else:
        raise ValueError(method)

    P = np.clip(P, 0.0, None)
    P /= P.sum(axis=0, keepdims=True)
    return P


def averaged_proposal_matrix(
    H: np.ndarray, gamma: float, t_window: tuple[float, float], n_time_points: int = 6
) -> np.ndarray:
    """Window-averaged P via ONE sparse expm_multiply time-grid sweep.

    ~10x faster than averaging separate proposal_matrix calls (measured 3.5s
    vs ~40s at n=6). Pure dephasing only; n <= _MAX_SPARSE_N.
    """
    d, n = _check_H(H)
    if n > _MAX_SPARSE_N:
        raise ValueError(f"refused for n={n} > {_MAX_SPARSE_N}; use TrajectorySampler")
    L = _sparse_liouvillian(H, gamma).tocsc()
    diag_idx = np.arange(d) * (d + 1)
    B = np.zeros((d * d, d), dtype=complex)
    B[diag_idx, np.arange(d)] = 1.0
    out = expm_multiply(L, B, start=t_window[0], stop=t_window[1], num=n_time_points, endpoint=True)
    P = np.clip(np.real(out[:, diag_idx, :]).mean(axis=0), 0.0, None)
    P /= P.sum(axis=0, keepdims=True)
    return P


def symmetry_defect(P: np.ndarray) -> float:
    """max_{x,y} |P[y,x] - P[x,y]| — R1's certification quantity."""
    return float(np.max(np.abs(P - P.T)))


class TrajectorySampler:
    """Exact trajectory unravelling of the pure-dephasing walk (n <= ~14).

    Precomputes eigh(H) once (dense 2^n x 2^n — the practical ceiling).
    sample(x, t, rng): Poisson(n*gamma*t) phase-kick jumps at uniform times,
    unitary evolution between kicks, computational-basis measurement at t.
    Returns the proposed state y.  One call == one hardware shot (G03).
    """

    def __init__(self, H: np.ndarray, gamma: float):
        d, n = _check_H(H)
        self.d, self.n, self.gamma = d, n, float(gamma)
        w, V = eigh(np.asarray(H, dtype=float))
        self._w, self._V = w, V
        # Z_i sign tables for phase kicks
        self._signs = np.stack([_z_diag(i, n) for i in range(n)])

    def _evolve(self, psi: np.ndarray, dt: float) -> np.ndarray:
        c = self._V.T @ psi
        c *= np.exp(-1j * self._w * dt)
        return self._V @ c

    def sample(self, x: int, t: float, rng) -> int:
        psi = np.zeros(self.d, dtype=complex)
        psi[x] = 1.0
        n_jumps = rng.poisson(self.n * self.gamma * t) if self.gamma > 0 else 0
        times = np.sort(rng.random(n_jumps)) * t
        prev = 0.0
        for tk in times:
            psi = self._evolve(psi, tk - prev)
            psi = self._signs[rng.integers(self.n)] * psi
            prev = tk
        psi = self._evolve(psi, t - prev)
        p = np.abs(psi) ** 2
        p /= p.sum()
        return int(rng.choice(self.d, p=p))

    def estimate_proposal_column(self, x: int, t: float, n_samples: int, rng) -> np.ndarray:
        col = np.zeros(self.d)
        for _ in range(n_samples):
            col[self.sample(x, t, rng)] += 1
        return col / n_samples
