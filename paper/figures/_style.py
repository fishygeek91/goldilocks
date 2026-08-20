"""Shared matplotlib style and verify-then-save helpers for paper figures.

Every figure script must call ``verify_or_die`` *before* ``savefig_pair``.
A failed check prints the VERIFY block and refuses to write PDF/PNG.
"""
from __future__ import annotations

from pathlib import Path
from typing import Sequence

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np

# Okabe-Ito colorblind palette (Wong, Nat. Methods 2011).
OKABE_ITO: dict[str, str] = {
    "black": "#000000",
    "orange": "#E69F00",
    "sky": "#56B4E9",
    "green": "#009E73",
    "yellow": "#F0E442",
    "blue": "#0072B2",
    "vermillion": "#D55E00",
    "purple": "#CC79A7",
}

# Table 1 channel order and display names (characterization_theorem.md).
# Table 1 classes, with the equal/unequal sigma+/- pair adjacent so the
# highlight band does not swallow amplitude damping.
CHANNEL_ORDER: tuple[str, ...] = (
    "dephasing",
    "rot-dephasing",
    "depolarizing",
    "thermal-equal",
    "thermal-unequal",
    "amp-damp",
)
CHANNEL_LABELS: dict[str, str] = {
    "dephasing": "comp. dephasing",
    "rot-dephasing": "rot. dephasing",
    "depolarizing": "depolarizing",
    "thermal-equal": r"equal $\sigma^\pm$",
    "amp-damp": "amp. damping",
    "thermal-unequal": r"unequal $\sigma^\pm$",
}
SYMMETRIC_CHANNELS: frozenset[str] = frozenset(
    {"dephasing", "rot-dephasing", "depolarizing", "thermal-equal"}
)
BREAKING_CHANNELS: frozenset[str] = frozenset({"amp-damp", "thermal-unequal"})
HIGHLIGHT_PAIR: tuple[str, str] = ("thermal-equal", "thermal-unequal")

REPO_ROOT = Path(__file__).resolve().parents[2]


def apply_style() -> None:
    """Apply a compact, paper-like rcParams block."""
    mpl.rcParams.update(
        {
            "figure.dpi": 120,
            "savefig.dpi": 300,
            "savefig.bbox": "tight",
            "savefig.pad_inches": 0.04,
            "font.size": 9,
            "axes.labelsize": 10,
            "axes.titlesize": 10,
            "legend.fontsize": 8,
            "xtick.labelsize": 8,
            "ytick.labelsize": 8,
            "axes.spines.top": False,
            "axes.spines.right": False,
            "pdf.fonttype": 42,
            "ps.fonttype": 42,
        }
    )


def verify_or_die(checks: Sequence[tuple[str, bool, str]]) -> None:
    """Print a VERIFY block; raise SystemExit if any check failed.

    Parameters
    ----------
    checks
        Sequence of (name, passed, detail) triples.
    """
    if len(checks) == 0:
        raise ValueError("verify_or_die requires at least one check")
    print("===== VERIFY =====")
    failed: list[str] = []
    for name, passed, detail in checks:
        mark = "PASS" if passed else "FAIL"
        print(f"  [{mark}] {name}: {detail}")
        if not passed:
            failed.append(name)
    print("==================")
    if failed:
        raise SystemExit(
            "verification failed (" + ", ".join(failed) + "); refusing to save figure"
        )


def close_enough(value: float, target: float, rtol: float, atol: float) -> bool:
    """Absolute-or-relative closeness used by figure verification."""
    if not np.isfinite(value) or not np.isfinite(target):
        return False
    return bool(abs(value - target) <= atol + rtol * abs(target))


def savefig_pair(fig: plt.Figure, stem: Path) -> None:
    """Write ``stem.pdf`` and ``stem.png``; ``stem`` has no suffix."""
    pdf_path = stem.with_suffix(".pdf")
    png_path = stem.with_suffix(".png")
    fig.savefig(pdf_path)
    fig.savefig(png_path)
    print(f"wrote {pdf_path}")
    print(f"wrote {png_path}")
