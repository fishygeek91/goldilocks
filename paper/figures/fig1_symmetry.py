"""Fig 1 — symmetry defect vs channel class (log scale).

Reads docs/R1_results.txt. Highlights the equal/unequal sigma+/- pair.
Verifies Table 1 numbers from characterization_theorem.md against the file
before writing PDF/PNG. Does not re-run scripts/run_r1.py.

Usage: gvenv/bin/python paper/figures/fig1_symmetry.py
"""
from __future__ import annotations

import sys
from collections import defaultdict
from pathlib import Path

import numpy as np

# Allow running as a script from any cwd.
_HERE = Path(__file__).resolve().parent
if str(_HERE) not in sys.path:
    sys.path.insert(0, str(_HERE))

from _style import (  # noqa: E402
    BREAKING_CHANNELS,
    CHANNEL_LABELS,
    CHANNEL_ORDER,
    HIGHLIGHT_PAIR,
    OKABE_ITO,
    REPO_ROOT,
    SYMMETRIC_CHANNELS,
    apply_style,
    close_enough,
    savefig_pair,
    verify_or_die,
)

R1_PATH = REPO_ROOT / "docs" / "R1_results.txt"
OUT_STEM = _HERE / "fig1_symmetry"

# Characterization table claims (docs/characterization_theorem.md).
CLAIM_WORST_TC = 1.2e-14
CLAIM_MIN_BREAK = 3.5e-2
# Narrative "up to 0.55" is NOT in the current R1 file (amp-damp is run at
# fixed kappa = 0.1 Delta). Printed as a discrepancy, not a save-blocker.
NARRATIVE_MAX_AMP = 0.55


def load_r1(path: Path) -> list[tuple[int, float, float, str, float]]:
    """Parse R1_results.txt rows: n, gamma/Delta, t*Delta, noise, defect."""
    if not path.is_file():
        raise FileNotFoundError(f"missing R1 results file: {path}")
    rows: list[tuple[int, float, float, str, float]] = []
    with path.open() as fh:
        header = fh.readline().strip().split()
        if header != ["n", "gamma/Delta", "t*Delta", "noise", "defect"]:
            raise ValueError(f"unexpected R1 header: {header}")
        for line_no, line in enumerate(fh, start=2):
            parts = line.split()
            if len(parts) != 5:
                raise ValueError(f"{path}:{line_no}: expected 5 fields, got {parts}")
            n_s, g_s, t_s, noise, d_s = parts
            if noise not in CHANNEL_ORDER:
                raise ValueError(f"{path}:{line_no}: unknown channel {noise}")
            rows.append((int(n_s), float(g_s), float(t_s), noise, float(d_s)))
    if len(rows) == 0:
        raise ValueError(f"{path} contains no data rows")
    return rows


def main() -> None:
    apply_style()
    rows = load_r1(R1_PATH)
    by_ch: dict[str, list[float]] = defaultdict(list)
    for _n, _g, _t, noise, defect in rows:
        by_ch[noise].append(defect)

    worst_tc = max(max(by_ch[ch]) for ch in SYMMETRIC_CHANNELS if ch in by_ch)
    best_break = min(min(by_ch[ch]) for ch in BREAKING_CHANNELS if ch in by_ch)
    min_amp = min(by_ch["amp-damp"])
    max_amp = max(by_ch["amp-damp"])
    max_uneq = max(by_ch["thermal-unequal"])
    # File-level anchors from the 2026-08-18 run (plan VERIFY list).
    file_worst_tc = 1.224021e-14
    file_best_break = 3.450743e-02
    file_min_amp = 4.857496e-02
    file_max_amp = 3.515876e-01
    file_max_uneq = 4.078569e-01

    print(
        f"NOTE: narrative amp-damp max {NARRATIVE_MAX_AMP} is not in "
        f"{R1_PATH.name} (file max amp-damp = {max_amp:.3e}). "
        "Plotting the file; leaving the docs unedited."
    )

    verify_or_die(
        [
            (
                "worst transpose-closed defect",
                close_enough(worst_tc, file_worst_tc, rtol=0.05, atol=0.0)
                and worst_tc <= CLAIM_WORST_TC * 1.05,
                f"{worst_tc:.6e} (file {file_worst_tc:.6e}; claim <= {CLAIM_WORST_TC:.1e})",
            ),
            (
                "smallest breaker",
                close_enough(best_break, file_best_break, rtol=0.02, atol=0.0)
                and best_break >= CLAIM_MIN_BREAK * 0.98,
                f"{best_break:.6e} (file {file_best_break:.6e}; claim >= {CLAIM_MIN_BREAK})",
            ),
            (
                "min amp-damp",
                close_enough(min_amp, file_min_amp, rtol=0.02, atol=0.0),
                f"{min_amp:.6e} (file {file_min_amp:.6e})",
            ),
            (
                "max amp-damp",
                close_enough(max_amp, file_max_amp, rtol=0.02, atol=0.0),
                f"{max_amp:.6e} (file {file_max_amp:.6e}; narrative {NARRATIVE_MAX_AMP})",
            ),
            (
                "max thermal-unequal",
                close_enough(max_uneq, file_max_uneq, rtol=0.02, atol=0.0),
                f"{max_uneq:.6e} (file {file_max_uneq:.6e})",
            ),
        ]
    )

    import matplotlib.pyplot as plt
    from matplotlib.patches import FancyBboxPatch

    rng = np.random.default_rng(1)
    fig, ax = plt.subplots(figsize=(7.2, 3.6))

    xs = np.arange(len(CHANNEL_ORDER), dtype=float)
    # Highlight band behind the equal/unequal sigma+/- pair.
    pair_idx = [CHANNEL_ORDER.index(ch) for ch in HIGHLIGHT_PAIR]
    x0, x1 = min(pair_idx) - 0.45, max(pair_idx) + 0.45
    ax.add_patch(
        FancyBboxPatch(
            (x0, 1e-18),
            x1 - x0,
            1e0,
            boxstyle="round,pad=0.02,rounding_size=0.15",
            linewidth=0,
            facecolor=OKABE_ITO["yellow"],
            alpha=0.28,
            zorder=0,
            transform=ax.transData,
        )
    )
    ax.text(
        0.5 * (x0 + x1),
        2.5e-17,
        "same jumps; rate match flips symmetry",
        ha="center",
        va="bottom",
        fontsize=7,
        color=OKABE_ITO["black"],
        zorder=3,
    )

    for i, ch in enumerate(CHANNEL_ORDER):
        vals = np.asarray(by_ch[ch], dtype=float)
        # Floor zeros for log scale (none expected; keep the axis honest).
        vals = np.clip(vals, 1e-18, None)
        jitter = rng.uniform(-0.12, 0.12, size=vals.size)
        if ch in SYMMETRIC_CHANNELS:
            color = OKABE_ITO["blue"] if ch != "thermal-equal" else OKABE_ITO["green"]
            marker = "o"
        else:
            color = OKABE_ITO["vermillion"] if ch != "thermal-unequal" else OKABE_ITO["orange"]
            marker = "D"
        if ch in HIGHLIGHT_PAIR:
            edge = OKABE_ITO["black"]
            lw = 0.8
        else:
            edge = color
            lw = 0.3
        ax.scatter(
            np.full(vals.size, xs[i]) + jitter,
            vals,
            s=18,
            c=color,
            marker=marker,
            edgecolors=edge,
            linewidths=lw,
            alpha=0.75,
            zorder=2,
        )
        ax.hlines(
            float(vals.max()),
            xs[i] - 0.28,
            xs[i] + 0.28,
            colors=color,
            linewidths=1.6,
            zorder=3,
        )

    ax.axhline(1e-12, color=OKABE_ITO["black"], ls=":", lw=0.7, alpha=0.6)
    ax.text(
        xs[-1] + 0.35,
        1e-12,
        "machine prec.",
        va="bottom",
        ha="right",
        fontsize=7,
        color=OKABE_ITO["black"],
        alpha=0.7,
    )
    ax.set_yscale("log")
    ax.set_ylim(5e-19, 1.2)
    ax.set_xlim(-0.6, len(CHANNEL_ORDER) - 0.4)
    ax.set_xticks(xs)
    ax.set_xticklabels([CHANNEL_LABELS[ch] for ch in CHANNEL_ORDER], rotation=18, ha="right")
    ax.set_ylabel(r"symmetry defect $\max_{x,y}\,|q(y|x)-q(x|y)|$")
    ax.set_xlabel("noise channel (Table 1)")
    savefig_pair(fig, OUT_STEM)
    plt.close(fig)


if __name__ == "__main__":
    main()
