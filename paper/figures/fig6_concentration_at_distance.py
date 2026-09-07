"""Fig 6 — the Sec. 7 test, executed: concentration alone does not predict
advantage; concentration AT DISTANCE does.

Data: tunnelvision/experiments/D01_demon/m01_cfar_full.csv (M01 run,
2026-08-31): 14 exact-tier kernels x 6 spin-glass instances (n=8,10;
seeds 1-3) x T in {1, 0.3, 0.1}. gap = exact MH spectral gap;
C_kT = off-diagonal pi-weighted proposal mass with |dE| <= 2T (the C8
scalar, kappa=2); C_far = mass with |dE| <= 2 (raw coupling units) AND
Hamming distance >= 3.
"""
from __future__ import annotations

from pathlib import Path
import csv

import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import spearmanr

from _style import OKABE_ITO, apply_style, close_enough, savefig_pair, verify_or_die

_HERE = Path(__file__).resolve().parent
DATA = _HERE / "data" / "m01_cfar_full.csv"

FAMILY_STYLE = {
    "local": dict(color=OKABE_ITO["blue"], marker="o", label="local (single-flip, ADS, demon)"),
    "informed": dict(color=OKABE_ITO["vermillion"], marker="^", label="informed local (DLP, soft-spin)"),
    "naive": dict(color=OKABE_ITO["sky"], marker="s", label="uninformed global (uniform, random-mask)"),
    "quench": dict(color=OKABE_ITO["black"], marker="*", label="coherent quench"),
    "oracle": dict(color=OKABE_ITO["green"], marker="D", label="shell oracle (not implementable)"),
}
GAP_FLOOR = 1e-12


def load() -> list[dict]:
    with DATA.open() as fh:
        return [
            {**r, "gap": float(r["gap"]), "C_kT": float(r["C_kT"]), "C_far": float(r["C_far"])}
            for r in csv.DictReader(fh)
        ]


def per_cell_spearman(rows: list[dict], key: str) -> list[float]:
    cells: dict[tuple, list[dict]] = {}
    for r in rows:
        cells.setdefault((r["n"], r["seed"], r["T"]), []).append(r)
    out = []
    for group in cells.values():
        out.append(spearmanr([g["gap"] for g in group], [g[key] for g in group]).statistic)
    return out


def main() -> None:
    apply_style()
    rows = load()
    imp = [r for r in rows if r["family"] != "oracle"]
    rho_near = per_cell_spearman(imp, "C_kT")
    rho_far = per_cell_spearman(imp, "C_far")

    fig, axes = plt.subplots(1, 2, figsize=(7.0, 3.0), sharey=True)
    for ax, key, rhos, xlabel in (
        (axes[0], "C_kT", rho_near, r"$C_{2T}(q)$:  mass on $|\Delta E|\leq 2T$"),
        (axes[1], "C_far", rho_far, r"$C_{\mathrm{far}}(q)$:  mass on $|\Delta E|\leq 2$ and $d_H\geq 3$"),
    ):
        for fam, style in FAMILY_STYLE.items():
            if key == "C_kT" and fam == "oracle":
                continue  # panel (a) is the C8 scalar test on implementable kernels
            pts = [r for r in rows if r["family"] == fam]
            ax.scatter(
                [max(p[key], 1e-4) for p in pts],
                [max(p["gap"], GAP_FLOOR) for p in pts],
                s=42 if fam in ("quench", "oracle") else 16,
                facecolors="none" if fam == "oracle" else style["color"],
                edgecolors=style["color"],
                marker=style["marker"],
                linewidths=0.9,
                alpha=0.85,
                label=style["label"],
                zorder=3 if fam in ("quench", "oracle") else 2,
            )
        ax.set_xscale("log")
        ax.set_yscale("log")
        ax.set_xlabel(xlabel)
        ax.annotate(
            rf"median per-cell $\rho_s = {np.median(rhos):+.2f}$",
            xy=(0.03, 0.94), xycoords="axes fraction", fontsize=8,
        )
    axes[0].set_ylabel(r"exact MH spectral gap $\delta$")
    axes[0].set_title("(a) concentration alone", loc="left")
    axes[1].set_title("(b) concentration at distance", loc="left")
    axes[1].legend(loc="center left", bbox_to_anchor=(0.02, 0.32), frameon=False, fontsize=6.5, handletextpad=0.2)
    axes[1].annotate("disconnected shells\n($\\varepsilon$ too small)", xy=(0.30, GAP_FLOOR*1.5), fontsize=6.5,
                     color=OKABE_ITO["green"], ha="center", va="bottom")

    quench_rank = []
    cells: dict[tuple, list[dict]] = {}
    for r in imp:
        cells.setdefault((r["n"], r["seed"], r["T"]), []).append(r)
    for group in cells.values():
        order = sorted(group, key=lambda g: -g["C_far"])
        quench_rank.append(1 + next(i for i, g in enumerate(order) if g["family"] == "quench"))

    verify_or_die(
        [
            ("rows", len(rows) == 252, f"{len(rows)} rows (expect 252)"),
            ("cells", len(rho_near) == 18, f"{len(rho_near)} cells (expect 18)"),
            (
                "near-median",
                close_enough(float(np.median(rho_near)), -0.07, 0.0, 0.02),
                f"median rho(C_kT) = {np.median(rho_near):+.3f} (lock -0.07 +/- 0.02)",
            ),
            (
                "far-median",
                close_enough(float(np.median(rho_far)), 0.84, 0.0, 0.02),
                f"median rho(C_far) = {np.median(rho_far):+.3f} (lock +0.84 +/- 0.02)",
            ),
            (
                "quench-top",
                float(np.mean(quench_rank)) <= 1.6,
                f"quench mean C_far rank = {np.mean(quench_rank):.2f} (lock <= 1.6)",
            ),
        ]
    )
    savefig_pair(fig, _HERE / "fig6_concentration_at_distance")


if __name__ == "__main__":
    main()
