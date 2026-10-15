"""TSMC Q3 2026 Earnings update: charts. Run: python3 build_charts.py <bloomberg.xlsx>"""
import sys
sys.path.insert(0, "/home/claude")
import pandas as pd
import syz_charts as sc
from syz_charts import (load_bloomberg_sheet, price_eps_pe_chart, bar_chart, crop_for_pdf, source_line,
                        setup_fonts, BLUEB, ORANGE)

PARAMS = {
    "xlsx": sys.argv[1] if len(sys.argv) > 1 else "TSM.xlsx",
    "ticker": "TSM",
    "asof": "15 Oct 2026",
    "window_from": "2010-01-01",       # 2008-09 EPS trough (P/E 66x) would flatten the P/E panel
    "out": "/home/claude",
    # Chart 1: quarterly revenue, TWD bn (Q3 2026 consensus = pre-results estimate)
    "c1_labels": ["Q3 2025\nreported", "Q2 2026\nreported", "Q3 2026\nconsensus", "Q3 2026\nreported"],
    "c1_values": [989.918, 1270.380, 1461.784, 1494.0],
}

setup_fonts()
df = load_bloomberg_sheet(PARAMS["xlsx"])
df = df[df["eps"].notna() & (df["date"] >= PARAMS["window_from"])].reset_index(drop=True)

# Chart 2: the ADR trades in USD, Bloomberg carries the EPS in TWD per ADR. The kit labels both axes
# with one currency, so the EPS label, legend entry and end-label offsets are set through a thin subplots wrapper
c2 = f"{PARAMS['out']}/c2_full.png"
import matplotlib.pyplot as plt
_orig_subplots = plt.subplots
def _subplots(*a, **k):
    fig, axes = _orig_subplots(*a, **k)
    ax1 = axes[0]
    _orig_ylabel, _orig_plotf = ax1.set_ylabel, ax1.plot
    ax1.set_ylabel = lambda s, **kw: _orig_ylabel("12m-forward EPS (TWD per ADR, log scale)", **kw)
    def _plot(*pa, **pk):
        if pk.get("label", "").startswith("12m-forward EPS"):
            pk["label"] = "12m-forward EPS, TWD per ADR (lhs)"
        return _orig_plotf(*pa, **pk)
    ax1.plot = _plot
    # here the EPS line ends above the price: swap the kit's end-label offsets so each sits by its own dot
    _orig_ann1, _orig_twinx = ax1.annotate, ax1.twinx
    ax1.annotate = lambda t, xy, **kw: _orig_ann1(t, xy, **{**kw, "xytext": (10, 8)})
    def _twinx():
        axr = _orig_twinx()
        _orig_annr = axr.annotate
        axr.annotate = lambda t, xy, **kw: _orig_annr(t, xy, **{**kw, "xytext": (10, -20)})
        return axr
    ax1.twinx = _twinx
    return fig, axes
sc.plt.subplots = _subplots
res = price_eps_pe_chart(
    c2, df, "TSMC", f"{PARAMS['ticker']}: share price vs. consensus earnings and valuation",
    source_line("Bloomberg", PARAMS["asof"], "TSM US Equity, weekly", "BEst 12m-forward EPS, TWD per ADR",
                "40-week simple MA", "Log scale",
                "P/E shaded above (orange) / below (blue) its 2010-26 average"),
    ccy="USD")
sc.plt.subplots = _orig_subplots
print(res)
crop_for_pdf(c2, f"{PARAMS['out']}/c2_crop.png", "price_eps_pe")

c1 = f"{PARAMS['out']}/c1_full.png"
bar_chart(c1, PARAMS["c1_labels"], PARAMS["c1_values"],
          f"{PARAMS['ticker']}: Q3 2026 revenue vs. consensus and history",
          "Quarterly revenue, TWD bn",
          source_line("Bloomberg, company filings", PARAMS["asof"], "Q3 2026 consensus: pre-results estimate"),
          colors=[BLUEB, BLUEB, BLUEB, ORANGE], fmt="{:,.0f}", zero_line=False)
crop_for_pdf(c1, f"{PARAMS['out']}/c1_crop.png", "bar")
