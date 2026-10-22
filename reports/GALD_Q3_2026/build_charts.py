"""build_charts.py: Galderma (GALD SW) Q3 2026 earnings update charts.
Chart 1: Q3 sales growth by category at constant currency (bar_chart).
Chart 2: share price vs. consensus EPS and P/E (FY1 variant of price_eps_pe_chart, see below).
Run: python3 build_charts.py  (writes standalone PNGs + PDF crops to /home/claude/galderma)"""
import sys
sys.path.insert(0, "/home/claude")
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.ticker as mticker
import syz_charts
from syz_charts import (setup_fonts, style_ax, header, source_line, legend, _log_ticks, bar_chart, crop_for_pdf,
                        ORANGE, BLUEB, NAVY, GREY, AXIS_TXT, SPINE, DASH)

PARAMS = {
    "xlsx": "/home/claude/data/Galderma.xlsx",
    "out": "/home/claude/galderma",
    "ticker": "GALD",
    "bbg": "GALD SW Equity",
    "asof": "22 Oct 2026",
    "price_ccy": "CHF", "eps_ccy": "USD",
    # Chart 1: Q3 2026 net sales growth at constant currency by category (company release, 22 Oct 2026)
    "c1_labels": ["Neuro-\nmodulators", "Fillers and\nbiostimulators", "Dermatological\nskincare",
                  "Therapeutic\ndermatology", "Group"],
    "c1_values": [24.1, 4.8, 15.6, 58.9, 26.0],
    # dates where the Bloomberg consensus rolls to the next fiscal year (EPS steps up, P/E steps down)
    "fy_rolls": [("2025-01-02", "FY25"), ("2026-01-02", "FY26")],
}


def load_daily(path):
    """Bloomberg daily export, newest first: Date | Last Price | BEst EPS | BEst P/E Ratio | SMAVG (40) | SMAVG (200).
    BEst EPS is the current-fiscal-year (FY1) consensus in USD, published irregularly: forward-filled.
    SMAVG (200) is the 200-day simple MA, the daily equivalent of the 40-week MA used in the house chart."""
    df = pd.read_excel(path, sheet_name=0).dropna(how="all")
    cols = {c: c.lower() for c in df.columns}
    pick = lambda *keys: next(c for c, l in cols.items() if all(k in l for k in keys))
    out = pd.DataFrame({
        "date": pd.to_datetime(df[pick("date")]),
        "price": pd.to_numeric(df[pick("last price")], errors="coerce"),
        "eps": pd.to_numeric(df[pick("best eps")], errors="coerce"),
        "ma40": pd.to_numeric(df[pick("smavg", "200")], errors="coerce"),
        "pe": pd.to_numeric(df[pick("best p/e")], errors="coerce"),
    }).dropna(subset=["date"]).sort_values("date").reset_index(drop=True)
    out["eps"] = out["eps"].ffill()
    return out[out["eps"].notna() & out["pe"].notna()].reset_index(drop=True)   # window starts at first consensus


def bar_chart_2line(*args, **kwargs):
    """Kit bar_chart with bottom margin 0.21 (vs. 0.16) so two-line x labels clear the footnote in the PNG."""
    orig = syz_charts.plt.Figure.subplots_adjust
    def adj(self, **kw):
        kw["bottom"] = 0.21
        return orig(self, **kw)
    syz_charts.plt.Figure.subplots_adjust = adj
    try:
        bar_chart(*args, **kwargs)
    finally:
        syz_charts.plt.Figure.subplots_adjust = orig


def price_eps_pe_chart_fy1(path, df, title, footnote, fy_rolls=(), price_ccy="CHF", eps_ccy="USD"):
    """price_eps_pe_chart adapted to this export: daily data, FY1 (not 12m-forward) consensus EPS in the reporting
    currency (USD) against a CHF share price, 200-day MA, and dotted markers where the consensus rolls year."""
    x = mdates.date2num(df["date"])
    pe_avg = float(df["pe"].mean())

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12.5, 8.6), dpi=200, sharex=True,
                                   gridspec_kw={"height_ratios": [2.45, 1], "hspace": 0.16})
    fig.subplots_adjust(top=0.875, bottom=0.085, left=0.075, right=0.925)

    style_ax(ax1)
    ax1.set_yscale("log")
    ax1.plot(x, df["eps"], color=ORANGE, linewidth=2.1, zorder=3, label=f"Consensus current-year EPS, {eps_ccy} (lhs)")
    ax1.set_ylabel(f"Consensus current-year EPS ({eps_ccy}, log scale)", fontsize=10, color=ORANGE, fontweight="bold")
    ax1.tick_params(axis="y", colors=ORANGE)
    _log_ticks(ax1, float(df["eps"].min()), float(df["eps"].max()), subs=(1, 2, 3, 5))
    ax1.yaxis.set_major_formatter(mticker.FuncFormatter(lambda v, _: f"{v:,.0f}"))
    ax1.set_title("Share price and consensus current-year EPS (log scale)", fontsize=12, fontweight="bold",
                  color=NAVY, loc="left", pad=8)

    axr = ax1.twinx()
    axr.set_yscale("log")
    axr.spines[["top"]].set_visible(False)
    axr.spines[["right", "left", "bottom"]].set_color(SPINE)
    axr.plot(x, df["price"], color=BLUEB, linewidth=1.6, zorder=4, label=f"Share price, {price_ccy} (rhs)")
    axr.plot(x, df["ma40"], color=BLUEB, linewidth=1.3, linestyle=DASH, zorder=3, label="200-day moving average (rhs)")
    axr.set_ylabel(f"Share price ({price_ccy}, log scale)", fontsize=10, color=AXIS_TXT, fontweight="bold")
    axr.tick_params(axis="y", colors=AXIS_TXT, labelsize=9.5, length=3)
    _log_ticks(axr, float(df["price"].min()), float(df["price"].max()), subs=(1, 1.5, 2, 5, 7.5))
    axr.set_ylim(float(df["price"].min()) * 0.9, 205)
    ax1.set_zorder(axr.get_zorder() + 1); ax1.patch.set_visible(False)

    last_p, last_e = float(df["price"].iloc[-1]), float(df["eps"].iloc[-1])
    axr.plot(x[-1], last_p, "o", color=BLUEB, ms=5, zorder=5)
    # price ends just below EPS here, so the house offsets are swapped to keep the labels apart
    axr.annotate(f"{last_p:,.1f}", (x[-1], last_p), xytext=(10, -20), textcoords="offset points",
                 color=BLUEB, fontsize=10.5, fontweight="bold")
    ax1.plot(x[-1], last_e, "o", color=ORANGE, ms=5, zorder=5)
    ax1.annotate(f"{last_e:,.2f}", (x[-1], last_e), xytext=(10, 6), textcoords="offset points",
                 color=ORANGE, fontsize=10.5, fontweight="bold")

    h1, l1 = axr.get_legend_handles_labels(); h2, l2 = ax1.get_legend_handles_labels()
    leg = ax1.legend(h1 + h2, l1 + l2, loc="upper left", frameon=False, fontsize=10.5, handlelength=2.4)
    for t in leg.get_texts():
        t.set_color(NAVY); t.set_fontweight("bold")

    style_ax(ax2)
    pe = df["pe"].to_numpy(float)
    ax2.plot(x, pe, color=ORANGE, linewidth=1.7, zorder=3, label="P/E on consensus current-year EPS")
    ax2.axhline(pe_avg, color=NAVY, linestyle=DASH, linewidth=1.3, zorder=2,
                label=f"Average since {df['date'].iloc[0].year}: {pe_avg:.1f}x")
    ax2.fill_between(x, pe, pe_avg, where=pe >= pe_avg, interpolate=True, color=ORANGE, alpha=0.12, zorder=1)
    ax2.fill_between(x, pe, pe_avg, where=pe < pe_avg, interpolate=True, color=BLUEB, alpha=0.14, zorder=1)
    ax2.yaxis.set_major_formatter(mticker.FuncFormatter(lambda v, _: f"{v:.0f}x"))
    ax2.set_ylim(min(pe.min() - 3, 30), pe.max() + 12)
    ax2.set_title("P/E on consensus current-year EPS", fontsize=12, fontweight="bold", color=NAVY, loc="left", pad=8)
    ax2.plot(x[-1], pe[-1], "o", color=ORANGE, ms=5, zorder=4)
    ax2.annotate(f"{pe[-1]:.1f}x", (x[-1], pe[-1]), xytext=(10, -4), textcoords="offset points",
                 color=ORANGE, fontsize=10.5, fontweight="bold")
    legend(ax2, loc="upper left", ncol=2)

    for d, lab in fy_rolls:
        xd = mdates.date2num(pd.Timestamp(d))
        for ax in (ax1, ax2):
            ax.axvline(xd, color=GREY, linestyle=(0, (1, 3)), linewidth=1.0, zorder=1)
        ax1.annotate(f"Consensus rolls to {lab}", (xd, 0.04), xycoords=("data", "axes fraction"),
                     xytext=(5, 0), textcoords="offset points", color=GREY, fontsize=9, fontweight="bold")

    ax2.xaxis.set_major_locator(mdates.MonthLocator(bymonth=[1, 4, 7, 10]))
    ax2.xaxis.set_major_formatter(mdates.DateFormatter("%b %Y"))
    ax2.set_xlim(x[0] - 10, x[-1] + 75)

    header(fig, title, None, footnote, title_y=0.955, foot_y=0.028, rule=False)
    fig.savefig(path, dpi=200, facecolor="white"); plt.close(fig)
    return {"price": last_p, "eps": last_e, "pe": float(pe[-1]), "pe_avg": pe_avg,
            "pe_premium_pct": (float(pe[-1]) / pe_avg - 1) * 100,
            "above_ma": last_p > float(df["ma40"].iloc[-1]), "ma40": float(df["ma40"].iloc[-1])}


if __name__ == "__main__":
    P = PARAMS; out = P["out"]; tk = P["ticker"]
    setup_fonts()

    bar_chart_2line(f"{out}/{tk}_chart1_growth_by_category.png", P["c1_labels"], P["c1_values"],
              f"{tk}: Q3 2026 sales growth by category at constant currency",
              "Year-on-year growth at constant currency, % · group sales USD 1,632m vs. consensus USD 1,552m (+5.1%)",
              source_line("Galderma Q3 2026 release", P["asof"], "Categories are operating KPIs, not reported segments",
                          "Consensus: company-compiled, pre-results"),
              colors=[BLUEB, BLUEB, BLUEB, BLUEB, ORANGE], fmt="{:+.1f}%", zero_line=True)

    df = load_daily(P["xlsx"])
    r = price_eps_pe_chart_fy1(
        f"{out}/{tk}_chart2_price_eps_pe.png", df,
        f"{tk}: share price vs. consensus earnings and valuation",
        source_line("Bloomberg", P["asof"], f"{P['bbg']}, daily", "BEst consensus current-year EPS (USD)",
                    "200-day simple MA", "Log scale",
                    f"P/E shaded above (orange) / below (blue) its {df['date'].iloc[0].year}-26 average"),
        fy_rolls=P["fy_rolls"], price_ccy=P["price_ccy"], eps_ccy=P["eps_ccy"])
    print({k: round(v, 2) if isinstance(v, float) else v for k, v in r.items()})

    crop_for_pdf(f"{out}/{tk}_chart1_growth_by_category.png", f"{out}/c1_crop.png", "bar")
    crop_for_pdf(f"{out}/{tk}_chart2_price_eps_pe.png", f"{out}/c2_crop.png", "price_eps_pe")
