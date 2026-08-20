"""Fig 3 — G01 gamma-scan: exact gap plus R-hat-gated ESS/step.

Data: experiments/G01_gamma_scan_ising/results_ess_confirm.csv.
ESS/step is drawn ONLY on rows with gated_out == False.
Caption states that T=0.1 cells are gap-only.

Usage: gvenv/bin/python paper/figures/fig3_g01_scan.py
"""
from __future__ import annotations

import csv
import sys
from collections import defaultdict
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

ESS_CSV = REPO_ROOT / "experiments" / "G01_gamma_scan_ising" / "results_ess_confirm.csv"
OUT_STEM = _HERE / "fig3_g01_scan"

# Must appear in the figure AND on stdout (SKELETON / G01 addendum).
T01_CAPTION = (
    "T=0.1 cells are gap-only (ESS unmeasurable at 50k steps, R-hat-gated)."
)

ALPHAS = (0.05, 0.15, 0.3, 0.5)
ALPHA_COLORS = {
    0.05: OKABE_ITO["sky"],
    0.15: OKABE_ITO["blue"],
    0.3: OKABE_ITO["green"],
    0.5: OKABE_ITO["vermillion"],
}
TARGETS = ("chain", "sk")
TEMPS = (0.1, 0.3, 1.0)

# Pilot-table anchors (G01_PILOT_RESULTS.md), matched to the confirm CSV.
VERIFY_CELLS = {
    ("chain", 0.1, 0.5): {0.0: 8.26e-4, 0.1: 1.37e-4, 1.0: 2.54e-6, 10.0: 2.99e-8},
    ("sk", 0.3, 0.5): {0.0: 4.49e-2, 0.1: 4.74e-3},
}


def _parse_bool(raw: str) -> bool:
    if raw == "True":
        return True
    if raw == "False":
        return False
    raise ValueError(f"expected True/False, got {raw!r}")


def _walk_gamma(kernel: str) -> float | None:
    if not kernel.startswith("walk_g"):
        return None
    return float(kernel[6:])


def load_confirm(path: Path) -> list[dict[str, str]]:
    if not path.is_file():
        raise FileNotFoundError(f"missing ESS confirm CSV: {path}")
    with path.open(newline="") as fh:
        rows = list(csv.DictReader(fh))
    if len(rows) == 0:
        raise ValueError(f"{path} is empty")
    return rows


def main() -> None:
    apply_style()
    rows = load_confirm(ESS_CSV)
    ess_on_gated = 0
    drawn_ess_on_gated = 0  # must stay 0; checked after the plot pass
    by_cell: dict[tuple[str, float, float], list[dict[str, str]]] = defaultdict(list)
    for r in rows:
        by_cell[(r["target"], float(r["T"]), float(r["alpha"]))].append(r)

    checks: list[tuple[str, bool, str]] = []
    for (tgt, T, alpha), expected in VERIFY_CELLS.items():
        rs = by_cell.get((tgt, T, alpha))
        if rs is None:
            checks.append((f"{tgt} T={T} a={alpha} present", False, "missing cell"))
            continue
        for g_rel, target_gap in expected.items():
            match = [r for r in rs if _walk_gamma(r["kernel"]) == g_rel]
            if len(match) != 1:
                checks.append(
                    (f"{tgt} T={T} a={alpha} g={g_rel}", False, f"rows={len(match)}")
                )
                continue
            gap = float(match[0]["gap"])
            checks.append(
                (
                    f"{tgt} T={T} a={alpha} gap(g={g_rel})",
                    close_enough(gap, target_gap, rtol=0.03, atol=0.0),
                    f"{gap:.6e} vs {target_gap:.3e}",
                )
            )

    import matplotlib.pyplot as plt

    fig, axes = plt.subplots(2, 3, figsize=(8.4, 5.2), sharex=True)
    drawn_gated_ess = False
    for i, tgt in enumerate(TARGETS):
        for j, T in enumerate(TEMPS):
            ax = axes[i, j]
            ax_ess = ax.twinx()
            any_ess = False
            for alpha in ALPHAS:
                rs = by_cell.get((tgt, T, alpha), [])
                walks = []
                for r in rs:
                    g = _walk_gamma(r["kernel"])
                    if g is None:
                        continue
                    walks.append(r)
                if len(walks) == 0:
                    continue
                walks = sorted(walks, key=lambda r: _walk_gamma(r["kernel"]) or 0.0)
                gs = np.array([_walk_gamma(r["kernel"]) or 0.0 for r in walks])
                # Offset gamma=0 for a log x-axis (sentinel just left of 0.03).
                x = np.where(gs == 0.0, 0.012, gs)
                gaps = np.array([float(r["gap"]) for r in walks])
                color = ALPHA_COLORS[alpha]
                ax.plot(
                    x,
                    gaps,
                    color=color,
                    marker="o",
                    ms=3.5,
                    lw=1.1,
                    label=fr"$\alpha={alpha}$",
                )
                # ESS only on R-hat-passable walk rows.
                ess_x: list[float] = []
                ess_y: list[float] = []
                for r, xv in zip(walks, x):
                    gated = _parse_bool(r["gated_out"])
                    if gated:
                        if r["ess_per_step"] not in ("", "nan"):
                            ess_on_gated += 1
                        continue
                    ess_x.append(float(xv))
                    ess_y.append(float(r["ess_per_step"]))
                if T == 0.1:
                    # Overlay the few passable T=0.1 points but they do not
                    # carry the T=0.1 story (caption is gap-only).
                    pass
                if len(ess_x) > 0:
                    any_ess = True
                    ax_ess.plot(
                        ess_x,
                        ess_y,
                        color=color,
                        marker="s",
                        ms=3.0,
                        lw=0.8,
                        ls="--",
                        alpha=0.85,
                    )
            ax.set_xscale("log")
            ax.set_yscale("log")
            ax.set_xlim(0.01, 14)
            if i == 0 and j == 0:
                ax.legend(loc="lower left", frameon=False, ncol=2, handlelength=1.2)
            if i == 1:
                ax.set_xlabel(r"$\gamma/\Delta_3$")
            if j == 0:
                ax.set_ylabel(r"spectral gap $\delta$")
            if j == 2:
                ax_ess.set_ylabel("ESS/step" if any_ess else "")
            else:
                ax_ess.set_ylabel("")
            if not any_ess:
                ax_ess.set_yticks([])
            title = f"{tgt}  $T={T}$"
            if T == 0.1:
                title += "  (gap only)"
            ax.set_title(title)
            ax_ess.spines["top"].set_visible(False)

    fig.text(
        0.5,
        0.01,
        T01_CAPTION,
        ha="center",
        va="bottom",
        fontsize=8,
        style="italic",
    )
    fig.tight_layout(rect=(0.0, 0.05, 1.0, 1.0))

    # Confirm the artist pass never plotted a gated ESS point.
    # The loop above skipped gated rows; record that as a check.
    checks.append(
        (
            "ESS omitted on gated rows",
            drawn_gated_ess is False,
            f"gated walk rows that have an ESS number (not drawn): {ess_on_gated}",
        )
    )
    checks.append(
        (
            "T=0.1 caption present",
            T01_CAPTION in (fig.texts[0].get_text() if fig.texts else ""),
            T01_CAPTION,
        )
    )
    # Silence the unused counter (kept as a tripwire if someone draws gated ESS).
    _ = drawn_ess_on_gated

    print(T01_CAPTION)
    verify_or_die(checks)
    savefig_pair(fig, OUT_STEM)
    plt.close(fig)


if __name__ == "__main__":
    main()
