"""build_charts.py: NVIDIA Q3 FY2027 charts (Chart 1 surprises vs. consensus, Chart 2 price vs. EPS and P/E)."""
import sys
sys.path.insert(0, "/home/claude")
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from syz_charts import (style_ax, header, NAVY, AXIS_TXT, setup_fonts, load_bloomberg_sheet, price_eps_pe_chart, crop_for_pdf,
                        source_line, BLUEB, ORANGE)

PARAMS = {
    "xlsx": "/root/.claude/uploads/015ea66a-f78f-5253-91c0-18552fcdb878/7fc18873-NVDA.xlsx",
    "ticker": "NVDA", "ccy": "USD", "asof": "18 Nov 2026",
    # publication-day reaction: results after the 17 Nov close, document written before the 18 Nov session
    "reaction_pct": 4.0, "reaction_date": "17 November 2026 (after hours)", "market_pct": None,
    # Chart 1: surprise vs. consensus (gross margin in percentage points, labelled in bp)
    # surprises as published by Bloomberg (consensus figures in the brief are rounded)
    "c1": [("Revenue", 0.061), ("Data centre", 0.055), ("Gross margin", None),
           ("EPS", 0.085), ("Q4 guide", 0.040), ("Free cash flow", 43.8 / 57.0 - 1)],
    "gm_pts": 74.9 - 74.1,
}


def bar_chart_padded(path, labels, values, lbls, title, subtitle, footnote, ylabel=""):
    """Kit bar_chart with custom value labels and extra room under the lowest bar, so a large negative
    value label does not collide with its category label."""
    vals = np.asarray(values, float)
    colors = [ORANGE if v < 0 else BLUEB for v in vals]
    fig, ax = plt.subplots(figsize=(12.5, 5.0), dpi=200)
    fig.subplots_adjust(top=0.80, bottom=0.16, left=0.07, right=0.96)
    style_ax(ax)
    ax.tick_params(labelsize=12)
    bars = ax.bar(range(len(vals)), vals, color=colors, width=0.62, linewidth=0, zorder=3)
    ax.axhline(0, color=NAVY, linewidth=1.0, zorder=2)
    for b, v, t in zip(bars, vals, lbls):
        ax.annotate(t, (b.get_x() + b.get_width() / 2, v), xytext=(0, 5 if v >= 0 else -17),
                    textcoords="offset points", ha="center", fontsize=12, fontweight="bold", color=NAVY)
    lo, hi = vals.min(), vals.max()
    ax.set_ylim(lo - 0.16 * (hi - lo), hi + 0.14 * (hi - lo))
    ax.set_xticks(range(len(vals))); ax.set_xticklabels(labels, fontsize=12, color=NAVY, fontweight="bold")
    ax.set_ylabel(ylabel, fontsize=10.5, color=AXIS_TXT, fontweight="bold")
    header(fig, title, subtitle, footnote)
    fig.savefig(path, dpi=200, facecolor="white"); plt.close(fig)


def main():
    setup_fonts()
    P = PARAMS
    # ---- Chart 1
    labels = [l for l, _ in P["c1"]]
    vals = [P["gm_pts"] if v is None else v * 100 for l, v in P["c1"]]
    lbls = [f"+{P['gm_pts']*100:.0f}bp" if v is None else f"{v*100:+.1f}%" for l, v in P["c1"]]
    lbls = [s.replace("-", "−") for s in lbls]
    bar_chart_padded("/home/claude/nvda/c1.png", labels, vals, lbls,
              "NVDA: Q3 FY2027 results and Q4 guide vs. consensus",
              "Surprise vs. consensus, % · gross margin in points, labelled in bp",
              source_line("Bloomberg", P["asof"], "Company filings", "Consensus: Bloomberg pre-results",
                          "Free cash flow vs. about USD 57bn expected (FT)"),
              ylabel="Surprise vs. consensus (%)")
    crop_for_pdf("/home/claude/nvda/c1.png", "/home/claude/nvda/c1_crop.png", "bar")

    # ---- Chart 2
    df = load_bloomberg_sheet(P["xlsx"])
    df = df[df["eps"].notna()].reset_index(drop=True)
    stats = price_eps_pe_chart(
        "/home/claude/nvda/c2.png", df, "NVIDIA", "NVDA: share price vs. consensus earnings and valuation",
        source_line("Bloomberg", P["asof"], "NVDA US Equity, weekly", "BEst 12m-forward consensus",
                    "40-week simple MA", "Log scale", "P/E shaded above (orange) / below (blue) its 2014-26 average"),
        ccy="USD", price_lbl=(10, -22), eps_lbl=(10, 10))
    crop_for_pdf("/home/claude/nvda/c2.png", "/home/claude/nvda/c2_crop.png", "price_eps_pe")

    last = df.iloc[-1]
    yr = df[df["date"] >= last["date"] - pd.Timedelta(days=365)]
    ago = df[df["date"] <= last["date"] - pd.Timedelta(days=364)].iloc[-1]
    stats.update({
        "window": (str(df["date"].iloc[0].date()), str(last["date"].date())),
        "pe_1y_avg": float(yr["pe"].mean()), "pe_min": float(df["pe"].min()),
        "pe_peak": float(df["pe"].max()), "pe_peak_date": str(df.loc[df["pe"].idxmax(), "date"].date()),
        "price_12m": float(last["price"] / ago["price"] - 1) * 100, "eps_12m": float(last["eps"] / ago["eps"] - 1) * 100,
        "price_peak": float(df["price"].max()), "price_peak_date": str(df.loc[df["price"].idxmax(), "date"].date()),
        "ma_gap": float(last["price"] / last["ma40"] - 1) * 100,
    })
    for k, v in stats.items():
        print(f"{k}: {v}")
    return stats


if __name__ == "__main__":
    main()
