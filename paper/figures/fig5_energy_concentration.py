"""Fig 5 — energy-concentration cartoon (outlook schematic).

Not data. Two schematic proposal-dE densities (narrow coherent quench
versus broadened dephasing) against the Metropolis acceptance window.
Verification is structural only: two curves, window present, labels.

Usage: gvenv/bin/python paper/figures/fig5_energy_concentration.py
"""
from __future__ import annotations

import sys
from pathlib import Path

import numpy as np
from numpy.typing import NDArray

_HERE = Path(__file__).resolve().parent
if str(_HERE) not in sys.path:
    sys.path.insert(0, str(_HERE))

from _style import (  # noqa: E402
    OKABE_ITO,
    apply_style,
    savefig_pair,
    verify_or_die,
)

OUT_STEM = _HERE / "fig5_energy_concentration"

# Schematic scales (mixer-energy units). Not fitted to any experiment.
TEMPERATURE = 1.0
WINDOW_KAPPA = 1.0
SIGMA_COHERENT = 0.25
SIGMA_DEPHASED = 1.20
X_MIN = -4.0
X_MAX = 4.0
N_GRID = 801


def gaussian_density(x: NDArray[np.float64], sigma: float) -> NDArray[np.float64]:
    """Return a normalized Gaussian density on ``x`` with mean 0.

    Parameters
    ----------
    x
        Abscissa grid.
    sigma
        Standard deviation. Must be positive and finite.
    """
    if not np.isfinite(sigma) or sigma <= 0.0:
        raise ValueError("sigma must be a positive finite float, got " + repr(sigma))
    if x.size == 0:
        raise ValueError("x must be a non-empty grid")
    norm = 1.0 / (sigma * np.sqrt(2.0 * np.pi))
    return np.asarray(norm * np.exp(-0.5 * (x / sigma) ** 2), dtype=np.float64)


def metropolis_acceptance(delta_e: NDArray[np.float64], temperature: float) -> NDArray[np.float64]:
    """Return ``min(1, exp(-dE / T))`` on the energy-change grid.

    Parameters
    ----------
    delta_e
        Proposal energy change E(y) - E(x).
    temperature
        Target temperature. Must be positive and finite.
    """
    if not np.isfinite(temperature) or temperature <= 0.0:
        raise ValueError(
            "temperature must be a positive finite float, got " + repr(temperature)
        )
    raw = np.exp(-delta_e / temperature)
    return np.asarray(np.minimum(1.0, raw), dtype=np.float64)


def structural_checks(
    x: NDArray[np.float64],
    rho_coherent: NDArray[np.float64],
    rho_dephased: NDArray[np.float64],
    acceptance: NDArray[np.float64],
    window_half: float,
    xlabel: str,
    ylabel: str,
    legend_labels: tuple[str, str, str],
) -> list[tuple[str, bool, str]]:
    """Build the verify-then-save checklist for this cartoon.

    Parameters
    ----------
    x, rho_coherent, rho_dephased, acceptance
        Plotted arrays.
    window_half
        Half-width of the shaded Metropolis window, ``kappa * T``.
    xlabel, ylabel
        Axis labels that will be written on the figure.
    legend_labels
        The three legend strings (coherent, dephased, acceptance).
    """
    two_curves = (
        rho_coherent.shape == x.shape
        and rho_dephased.shape == x.shape
        and np.all(np.isfinite(rho_coherent))
        and np.all(np.isfinite(rho_dephased))
    )
    acc_ok = (
        acceptance.shape == x.shape
        and np.all(np.isfinite(acceptance))
        and float(np.min(acceptance)) >= 0.0
        and float(np.max(acceptance)) <= 1.0 + 1e-12
    )
    # Coherent proposal must be the narrower of the two Gaussians.
    narrower = SIGMA_COHERENT < SIGMA_DEPHASED
    window_ok = np.isfinite(window_half) and window_half > 0.0
    labels_ok = (
        "Delta" in xlabel or r"\Delta" in xlabel
    ) and len(ylabel) > 0
    legend_ok = (
        "0" in legend_labels[0]
        and (">" in legend_labels[1] or "gamma" in legend_labels[1])
        and "accept" in legend_labels[2].lower()
    )
    return [
        ("two density curves", two_curves, "coherent and dephased densities on shared grid"),
        (
            "coherent is narrower",
            narrower,
            "sigma0=" + str(SIGMA_COHERENT) + " < sigma_g=" + str(SIGMA_DEPHASED),
        ),
        ("acceptance in [0, 1]", acc_ok, "Metropolis min(1, exp(-dE/T)) present"),
        ("window present", window_ok, "half-width kappa T = " + str(window_half)),
        ("axis labels", labels_ok, "xlabel=" + xlabel + "; ylabel=" + ylabel),
        ("legend names gamma and accept", legend_ok, " / ".join(legend_labels)),
    ]


def main() -> None:
    """Draw the outlook cartoon and refuse to save if structure is missing."""
    apply_style()

    x = np.linspace(X_MIN, X_MAX, N_GRID, dtype=np.float64)
    rho0 = gaussian_density(x, SIGMA_COHERENT)
    rhog = gaussian_density(x, SIGMA_DEPHASED)
    acc = metropolis_acceptance(x, TEMPERATURE)
    window_half = WINDOW_KAPPA * TEMPERATURE

    xlabel = r"proposal energy change $\Delta E = E(y)-E(x)$"
    ylabel = r"proposal density $q(\Delta E)$"
    legend = (
        r"$\gamma=0$ (quench)",
        r"$\gamma>0$ (dephased)",
        "Metropolis acceptance",
    )
    verify_or_die(
        structural_checks(x, rho0, rhog, acc, window_half, xlabel, ylabel, legend)
    )

    import matplotlib.pyplot as plt

    fig, ax = plt.subplots(figsize=(5.6, 3.4))
    ax.axvspan(
        -window_half,
        window_half,
        color=OKABE_ITO["yellow"],
        alpha=0.35,
        zorder=0,
        label=r"acceptance window $|\Delta E|\leq \kappa T$",
    )
    ax.plot(x, rho0, color=OKABE_ITO["blue"], lw=1.8, label=legend[0], zorder=2)
    ax.plot(x, rhog, color=OKABE_ITO["vermillion"], lw=1.8, label=legend[1], zorder=2)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_xlim(X_MIN, X_MAX)
    ax.set_ylim(0.0, float(np.max(rho0)) * 1.15)

    ax_acc = ax.twinx()
    ax_acc.plot(
        x,
        acc,
        color=OKABE_ITO["black"],
        lw=1.2,
        ls="--",
        label=legend[2],
        zorder=1,
    )
    ax_acc.set_ylabel(r"Metropolis acceptance $\min(1,e^{-\Delta E/T})$")
    ax_acc.set_ylim(-0.02, 1.05)
    ax_acc.spines["top"].set_visible(False)

    # Combine legends from both axes so the caption's three objects appear.
    handles, labels = ax.get_legend_handles_labels()
    handles_acc, labels_acc = ax_acc.get_legend_handles_labels()
    ax.legend(
        handles + handles_acc,
        labels + labels_acc,
        frameon=False,
        loc="upper right",
        fontsize=7,
    )

    savefig_pair(fig, OUT_STEM)
    plt.close(fig)


if __name__ == "__main__":
    main()
