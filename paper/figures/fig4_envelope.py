"""Fig 4 — envelope-law scatter (peak gap vs envelope, 50 G05 cells).

Marks cell 46 (+1.17%) and insets the margin histogram.

Usage: gvenv/bin/python paper/figures/fig4_envelope.py
"""
from __future__ import annotations

import csv
import sys
from pathlib import Path

import numpy as np

_HERE = Path(__file__).resolve().parent
if str(_HERE) not in sys.path:
    sys.path.insert(0, str(_HERE))

from _style import (  # noqa: E402
    OKABE_ITO,
    REPO_ROOT,
    apply_style,
    close_enough,
    savefig_pair,
    verify_or_die,
)

G05_CSV = REPO_ROOT / "experiments" / "G05_monotonicity" / "results.csv"
OUT_STEM = _HERE / "fig4_envelope"

# gamma>0 columns written by run_g05.py (logspace(-2, 2, 9)).
GAP_POS_COLS = (
    "gap_g0.01",
    "gap_g0.0316",
    "gap_g0.1",
    "gap_g0.316",
    "gap_g1",
    "gap_g3.16",
    "gap_g10",
    "gap_g31.6",
    "gap_g100",
)

CELL46_PEAK = 0.09054842658440276
CELL46_ENV = 0.08949953388089038
CELL46_MARGIN = 0.011719532583357228


def _parse_bool(raw: str) -> bool:
    if raw == "True":
        return True
    if raw == "False":
        return False
    raise ValueError(f"expected True/False, got {raw!r}")


def load_g05(path: Path) -> list[dict[str, str]]:
    if not path.is_file():
        raise FileNotFoundError(f"missing G05 results: {path}")
    with path.open(newline="") as fh:
        rows = list(csv.DictReader(fh))
    if len(rows) == 0:
        raise ValueError(f"{path} is empty")
    return rows


def peak_over_gamma_pos(row: dict[str, str]) -> float:
    """max_{gamma>0} gap — the envelope-law left-hand side."""
    vals = [float(row[c]) for c in GAP_POS_COLS]
    return float(max(vals))


def main() -> None:
    apply_style()
    rows = load_g05(G05_CSV)
    envelopes = np.array([float(r["envelope"]) for r in rows])
    peaks = np.array([peak_over_gamma_pos(r) for r in rows])
    margins = np.array([float(r["peak_over_envelope"]) for r in rows])
    cells = np.array([int(r["cell"]) for r in rows])
    interior = np.array([_parse_bool(r["interior_peak"]) for r in rows])
    advantage = np.array([_parse_bool(r["advantage_cell"]) for r in rows])
    n_above = int(np.sum(margins > 0.0))
    above_cells = cells[margins > 0.0]
    l1_flags = np.array([_parse_bool(r["l1_violated"]) for r in rows])
    l1_cells = cells[l1_flags]
    cell46 = rows[int(np.where(cells == 46)[0][0])] if 46 in cells else None
    median_margin = float(np.median(margins))
    # Cell 19 is a sub-epsilon (+0.087%) bump: above y=x but not an L1 violation
    # (prereg ε=0.01). G05_RESULTS.md counts L1 violations, not geometric crossings.
    cell19_margin = float(margins[cells == 19][0]) if 19 in cells else float("nan")

    checks = [
        ("n cells", len(rows) == 50, f"{len(rows)}"),
        (
            "L1 violations = {46} only",
            int(l1_flags.sum()) == 1 and list(l1_cells) == [46],
            f"l1_cells={list(l1_cells)}",
        ),
        (
            "positive margins are cells 19 (+0.087%) and 46 (+1.17%)",
            n_above == 2 and set(int(c) for c in above_cells) == {19, 46}
            and close_enough(cell19_margin, 0.0008675, 0.02, 0.0),
            f"n_above={n_above} cells={list(above_cells)} m19={cell19_margin:.6f}",
        ),
        (
            "cell 46 envelope",
            cell46 is not None
            and close_enough(float(cell46["envelope"]), CELL46_ENV, 1e-8, 0.0),
            f"{None if cell46 is None else cell46['envelope']} vs {CELL46_ENV}",
        ),
        (
            "cell 46 peak",
            cell46 is not None
            and close_enough(peak_over_gamma_pos(cell46), CELL46_PEAK, 1e-8, 0.0),
            f"{None if cell46 is None else peak_over_gamma_pos(cell46)} vs {CELL46_PEAK}",
        ),
        (
            "cell 46 margin +1.17%",
            cell46 is not None
            and close_enough(float(cell46["peak_over_envelope"]), CELL46_MARGIN, 1e-6, 0.0),
            f"{None if cell46 is None else cell46['peak_over_envelope']}",
        ),
        ("interior peaks 20/50", int(interior.sum()) == 20, f"{int(interior.sum())}"),
        ("advantage cells 4/50", int(advantage.sum()) == 4, f"{int(advantage.sum())}"),
        (
            "median margin ~ -72.5%",
            close_enough(median_margin, -0.725, rtol=0.03, atol=0.01),
            f"{median_margin:.4f}",
        ),
    ]

    import matplotlib.pyplot as plt
    from mpl_toolkits.axes_grid1.inset_locator import inset_axes

    fig, ax = plt.subplots(figsize=(5.2, 5.0))
    lo = min(float(envelopes.min()), float(peaks.min())) * 0.5
    hi = max(float(envelopes.max()), float(peaks.max())) * 1.8
    grid = np.array([lo, hi])
    ax.plot(grid, grid, color=OKABE_ITO["black"], lw=1.0, zorder=1)
    ax.fill_between(grid, grid, hi, color=OKABE_ITO["vermillion"], alpha=0.07, zorder=0)
    ax.fill_between(grid, lo, grid, color=OKABE_ITO["green"], alpha=0.07, zorder=0)

    mask46 = cells == 46
    ax.scatter(
        envelopes[~mask46],
        peaks[~mask46],
        s=28,
        c=OKABE_ITO["blue"],
        edgecolors=OKABE_ITO["black"],
        linewidths=0.3,
        zorder=2,
        label="G05 cells",
    )
    ax.scatter(
        envelopes[mask46],
        peaks[mask46],
        s=70,
        c=OKABE_ITO["vermillion"],
        marker="*",
        edgecolors=OKABE_ITO["black"],
        linewidths=0.4,
        zorder=3,
        label="cell 46 (+1.17%)",
    )
    ax.annotate(
        "cell 46\n+1.17%",
        xy=(float(envelopes[mask46][0]), float(peaks[mask46][0])),
        xytext=(0.25, 0.35),
        textcoords="data",
        fontsize=8,
        color=OKABE_ITO["vermillion"],
        arrowprops={
            "arrowstyle": "->",
            "color": OKABE_ITO["vermillion"],
            "lw": 0.8,
        },
    )
    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xlim(lo, hi)
    ax.set_ylim(lo, hi)
    ax.set_xlabel(r"envelope $\max(\delta(0),\delta_{\mathrm{SF}},\delta_{\mathrm{UF}})$")
    ax.set_ylabel(r"peak$_{\gamma>0}\,\delta(\gamma)$")
    ax.legend(loc="lower right", frameon=False)

    inset = inset_axes(ax, width="38%", height="32%", loc="upper left", borderpad=0.8)
    inset.hist(
        100.0 * margins,
        bins=16,
        color=OKABE_ITO["sky"],
        edgecolor=OKABE_ITO["black"],
        linewidth=0.4,
    )
    inset.axvline(0.0, color=OKABE_ITO["black"], lw=0.8)
    inset.axvline(1.17, color=OKABE_ITO["vermillion"], lw=0.8, ls="--")
    inset.set_xlabel("margin (%)", fontsize=7)
    inset.set_ylabel("cells", fontsize=7)
    inset.tick_params(labelsize=6)
    inset.spines["top"].set_visible(False)
    inset.spines["right"].set_visible(False)

    verify_or_die(checks)
    savefig_pair(fig, OUT_STEM)
    plt.close(fig)


if __name__ == "__main__":
    main()
