"""Exactness + physics invariants. All runnable now (n small, seconds).

I1  Proposal columns are normalized distributions.
I2  R1 mini-certification: pure-dephasing proposal symmetric (n=4).
I3  Amplitude damping BREAKS symmetry (guards against a vacuous I2).
I4  gamma=0 kernel == pure unitary quench |<y|U|x>|^2 (E01 anchor, matrix level).
I5  Zeno limit: huge gamma -> proposal ~ identity (walk freezes).
I6  End-to-end exactness: MH chain with dephased kernel recovers the exact
    Ising distribution (TV < tol) at ANY gamma — the whole point of the design.
I7  Engine never imports quantum modules (boundary check).
I8  Sparse path == dense path.
I9  Trajectory sampler == exact propagator.
I10 Characterization theorem, positive rows: rotated-real-basis dephasing
    and depolarizing (X/Y/Z jumps, unequal rates) are symmetric.
I11 Characterization theorem, matched-rate row: sigma^+/- relaxation is
    symmetric at EQUAL rates (infinite-T), asymmetric at unequal rates.
I12 Necessary condition (N): symmetric channels give doubly stochastic
    proposals (rows sum to 1), amplitude damping does not.
I13 Amplitude-damping bias bound: Hastings stays exact; naive Metropolis
    is biased; per-step and stationary TV bounds hold (n=4, one kappa).
"""
import numpy as np
import pytest

from goldilocks.diagnostics import (
    max_column_tv,
    mh_transition_matrix,
    naive_metropolis_matrix,
    spectral_gap,
    stationary_distribution,
    step_tv_bound_from_defect,
    total_variation,
)
from goldilocks.hamiltonians import walk_hamiltonian, delta_spectral_width
from goldilocks.kernels import DephasedWalkKernel
from goldilocks.lindblad import (
    pauli_jumps,
    proposal_matrix,
    rotated_dephasing_jumps,
    symmetry_defect,
    thermal_jumps,
)
from goldilocks.targets import IsingTarget
from scipy.linalg import expm


def _setup(n=4, T=0.5, alpha=0.5):
    tgt = IsingTarget.e01_chain(n, T=T)
    H = walk_hamiltonian(tgt.energies, alpha=alpha)
    return tgt, H, delta_spectral_width(H)


def test_i1_columns_normalized():
    _, H, D = _setup()
    P = proposal_matrix(H, gamma=0.7 * D, t=3.0 / D)
    assert np.allclose(P.sum(axis=0), 1.0, atol=1e-8)
    assert (P >= 0).all()


def test_i2_pure_dephasing_symmetric():
    _, H, D = _setup()
    for g in (0.0, 0.1 * D, D, 10 * D):
        assert symmetry_defect(proposal_matrix(H, g, 2.0 / D)) < 1e-9


def test_i3_amp_damping_breaks_symmetry():
    _, H, D = _setup()
    assert symmetry_defect(proposal_matrix(H, D, 2.0 / D, kappa=0.2 * D)) > 1e-4


def test_i4_gamma_zero_is_quench():
    _, H, D = _setup()
    t = 2.0 / D
    P = proposal_matrix(H, 0.0, t)
    U = expm(-1j * t * H)
    assert np.allclose(P, np.abs(U) ** 2, atol=1e-8)


def test_i5_zeno_freeze():
    _, H, D = _setup()
    P = proposal_matrix(H, 1e4 * D, 1.0 / D)
    assert np.diag(P).min() > 0.9


@pytest.mark.parametrize("g_rel", [0.0, 1.0, 30.0])
def test_i6_end_to_end_exact(g_rel):
    tgt, H, D = _setup(n=4, T=1.0)
    ker = DephasedWalkKernel(H, g_rel * D, (2.0 / D, 8.0 / D))
    A = mh_transition_matrix(ker.proposal_matrix, tgt)
    # stationary distribution of exact MH matrix == target (matrix-level check
    # beats a noisy chain-level KS test)
    pi = tgt.exact_dist()
    assert np.abs(A @ pi - pi).max() < 1e-8


def test_i7_engine_boundary():
    import goldilocks.engine as eng
    src = open(eng.__file__).read()
    for banned in ("lindblad", "qiskit", "dephased_walk"):
        assert banned not in src, f"engine imports quantum-side module: {banned}"


def test_i8_sparse_matches_dense():
    _, H, D = _setup(n=4)
    for g in (0.0, 0.7 * D, 5 * D):
        Pd = proposal_matrix(H, g, 2.0 / D, method="dense")
        Ps = proposal_matrix(H, g, 2.0 / D, method="sparse")
        assert np.abs(Pd - Ps).max() < 1e-8


def test_i9_trajectories_match_exact():
    from goldilocks.lindblad import TrajectorySampler
    _, H, D = _setup(n=4)
    g, t = 1.0 * D, 2.0 / D
    P = proposal_matrix(H, g, t)
    rng = np.random.default_rng(0)
    ts = TrajectorySampler(H, g)
    col = ts.estimate_proposal_column(3, t, 4000, rng)
    tv = 0.5 * np.abs(col - P[:, 3]).sum()
    assert tv < 0.05, f"trajectory/exact TV distance {tv}"


def test_i10_transpose_closed_channels_symmetric():
    _, H, D = _setup()
    t = 2.0 / D
    for jumps in (
        rotated_dephasing_jumps(4, 0.5 * D, seed=1),
        pauli_jumps(4, gx=0.4 * D, gy=0.25 * D, gz=0.7 * D),
    ):
        assert symmetry_defect(proposal_matrix(H, 0.0, t, jumps=jumps)) < 1e-9


def test_i11_thermal_rates_matched_vs_unmatched():
    _, H, D = _setup()
    t, k = 2.0 / D, 0.3 * D
    equal = proposal_matrix(H, 0.0, t, jumps=thermal_jumps(4, k_down=k, k_up=k))
    assert symmetry_defect(equal) < 1e-9
    unequal = proposal_matrix(H, 0.0, t, jumps=thermal_jumps(4, k_down=k, k_up=0.25 * k))
    assert symmetry_defect(unequal) > 1e-4


def test_i12_necessary_condition_doubly_stochastic():
    _, H, D = _setup()
    t = 2.0 / D
    P_sym = proposal_matrix(H, 0.7 * D, t)
    assert np.allclose(P_sym.sum(axis=1), 1.0, atol=1e-9)  # rows too: (N) holds
    P_ad = proposal_matrix(H, 0.0, t, kappa=0.3 * D)
    assert np.abs(P_ad.sum(axis=1) - 1.0).max() > 1e-3  # non-unital: (N) fails


def test_i13_amp_damp_bias_bound():
    """Hastings stays exact; naive Metropolis is biased and respects the TV bound."""
    tgt, H, D = _setup(n=4, T=1.0, alpha=0.5)
    tw = (2.0 / D, 12.0 / D)
    ker = DephasedWalkKernel(H, 0.0, tw, n_time_points=6, kappa=0.1 * D)
    Q = ker.proposal_matrix
    eps = symmetry_defect(Q)
    assert eps > 1e-4
    pi = tgt.exact_dist()
    P_H = mh_transition_matrix(Q, tgt)
    P_M = naive_metropolis_matrix(Q, tgt)
    assert np.abs(P_H @ pi - pi).max() < 1e-8
    tv_stat = total_variation(stationary_distribution(P_M), pi)
    tv_step = max_column_tv(P_M, P_H)
    bound_step = step_tv_bound_from_defect(eps, pi)
    gap = spectral_gap(P_H)
    assert tv_stat > 0.0
    assert tv_step <= bound_step + 1e-12
    # Theorem B (proved): gap envelope with the L2(pi)->TV factor.
    assert tv_stat <= (bound_step / gap) / np.sqrt(pi.min()) + 1e-12
    # Empirical B_naive (unproved, documented as such) also holds here.
    assert tv_stat <= (bound_step / gap) + 1e-12
