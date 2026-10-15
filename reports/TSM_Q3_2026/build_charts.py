"""build_charts.py: TSMC (TSM US) Q3 2026 earnings update charts. Parameterised for the next quarter via PARAMS."""
import os
import sys
sys.path.insert(0, "/home/claude")
import numpy as np
import matplotlib.pyplot as plt
import syz_charts as sc

PARAMS = {
    "xlsx": "/home/claude/data/TSM.xlsx",
    "ticker": "TSM",
    "asof": "15 Oct 2026",
    "c2_start": "2010-01-01",
    "out": "/home/claude/out",
    # Chart 1 rows: (label, surprise, value label, reported vs. consensus), biggest surprise first.
    # Consensus levels are implied by the reported surprise (revenue and gross-margin consensus approximate).
    "c1_rows": [
        ("Q4 revenue guide", 6.5, "+6.5%", "USD 53.3bn vs. ~50.0bn"),
        ("Q3 revenue", 3.0, "+3.0%", "USD 46.7bn vs. ~45.3bn"),
        ("Q3 EPS per ADR", (29.43 / 28.67 - 1) * 100, "+2.7%", "USD 4.54 vs. 4.43"),
        ("Q3 gross margin", 66.4 - 67.0, "−0.6pp", "66.4% vs. ~67.0%"),
    ],
}


def surprise_chart(path, rows, title, subtitle, footnote):
    """bar_chart geometry (same crop preset), no y axis: each bar carries its surprise in large type and the
    reported vs. consensus figures next to it. Lead bar Space Blue, other beats Blueberry, misses Tiger Orange."""
    vals = np.array([r[1] for r in rows], float)
    colors = [sc.ORANGE if v < 0 else (sc.NAVY if i == 0 else sc.BLUEB) for i, v in enumerate(vals)]
    fig, ax = plt.subplots(figsize=(12.5, 5.0), dpi=200)
    fig.subplots_adjust(top=0.80, bottom=0.16, left=0.07, right=0.96)
    sc.style_ax(ax)
    ax.grid(False)
    ax.spines[["left", "bottom"]].set_visible(False)
    ax.set_yticks([])
    bars = ax.bar(range(len(vals)), vals, color=colors, width=0.6, linewidth=0, zorder=3)
    ax.axhline(0, color=sc.NAVY, linewidth=1.2, zorder=4)
    for b, v, (_, _, big, small) in zip(bars, vals, rows):
        x = b.get_x() + b.get_width() / 2
        col = sc.ORANGE if v < 0 else sc.NAVY
        if v >= 0:
            ax.annotate(big, (x, v), xytext=(0, 27), textcoords="offset points", ha="center", va="bottom",
                        fontsize=22, fontweight="extra bold", color=col)
            ax.annotate(small, (x, v), xytext=(0, 6), textcoords="offset points", ha="center", va="bottom",
                        fontsize=13.5, color=sc.AXIS_TXT)
        else:
            ax.annotate(big, (x, v), xytext=(0, -6), textcoords="offset points", ha="center", va="top",
                        fontsize=22, fontweight="extra bold", color=col)
            ax.annotate(small, (x, v), xytext=(0, -38), textcoords="offset points", ha="center", va="top",
                        fontsize=13.5, color=sc.AXIS_TXT)
    ax.set_ylim(vals.min() - 3.4, vals.max() + 2.6)
    ax.set_xticks(range(len(vals)))
    ax.set_xticklabels([r[0] for r in rows], fontsize=13, color=sc.NAVY, fontweight="bold")
    ax.tick_params(axis="x", length=0, pad=8)
    sc.header(fig, title, subtitle, footnote)
    fig.savefig(path, dpi=200, facecolor="white"); plt.close(fig)


def main(p=PARAMS):
    os.makedirs(p["out"], exist_ok=True)
    sc.setup_fonts()
    df = sc.load_bloomberg_sheet(p["xlsx"])
    df = df[df["eps"].notna()].reset_index(drop=True)

    # Chart 1
    c1 = f"{p['out']}/TSM_chart1_surprises.png"
    surprise_chart(c1, p["c1_rows"], "TSM: everything beat except the margin",
                   "Q3 2026 results and Q4 guide, surprise vs. pre-results consensus (gross margin in percentage points)",
                   sc.source_line("Bloomberg, company filings, analyst research notes", p["asof"],
                                  "Revenue and gross-margin consensus approximate",
                                  "Q4 guide at midpoint",
                                  "EPS per ADR in USD at the 15 Oct exchange rate"))
    sc.crop_for_pdf(c1, f"{p['out']}/c1_crop.png", "bar")

    # Chart 2: USD only. Bloomberg's BEst EPS for TSM US is in TWD per ADR; restate it in USD per ADR with the
    # exchange rate Bloomberg itself uses in the P/E (EPS_USD = price / P/E), so price, EPS and P/E stay consistent
    c2 = f"{p['out']}/TSM_chart2_price_eps_pe.png"
    d2 = df[df["date"] >= p["c2_start"]].dropna(subset=["pe"]).copy()
    d2["eps"] = d2["price"] / d2["pe"]
    d2 = d2.reset_index(drop=True)
    stats = sc.price_eps_pe_chart(
        c2, d2, "TSM", "TSM: share price vs. consensus earnings and valuation",
        sc.source_line("Bloomberg", p["asof"], "TSM US Equity (ADR), weekly", "BEst 12m-forward consensus EPS per ADR in USD",
                       "40-week simple MA", "Log scale",
                       "P/E shaded above (orange) / below (blue) its 2010-26 average"),
        ccy="USD")
    sc.crop_for_pdf(c2, f"{p['out']}/c2_crop.png", "price_eps_pe")
    print(stats)
    return stats


if __name__ == "__main__":
    main()
