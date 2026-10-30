"""AstraZeneca Q3 2026: Chart 1 (surprise vs. consensus by line) and Chart 2 (price vs. EPS and P/E)."""
import sys
sys.path.insert(0, "/home/claude")
import numpy as np
import matplotlib.ticker as mticker
import syz_charts as sc
from load import load_weekly

PARAMS = {
    "xlsx": "/home/claude/data/AZN.xlsx",
    "ticker": "AZN",
    "asof": "29 Oct 2026",                 # last close in the export, before the 30 October release
    "window_start": None,                  # first consensus EPS: 2 Nov 2018
    "reaction_pct": 3.14, "reaction_date": "30 Oct 2026 (morning trading)", "market_pct": None,
    # Q3 2026 reported vs. consensus (USD m, USD), user material of 30 Oct 2026
    "lines": [("Revenue", 16209, 15942), ("Oncology", None, 1.0), ("Rare disease", None, 2.0),
              ("CVRM", None, -1.0), ("Core op. profit", 5855, 5362), ("Core EPS", 2.79, 2.59)],
}


def _log_ticks(ax, lo, hi, subs=(1, 2, 5)):
    """Narrow log range (price x2.7, EPS x3.3 over the window): a 1-1.5-2-3-5-7 ladder keeps three ticks or more."""
    subs = (1, 1.5, 2, 3, 5, 7)
    ticks = [m * 10 ** e for e in range(int(np.floor(np.log10(lo))) - 1, int(np.ceil(np.log10(hi))) + 2) for m in subs]
    ticks = [t for t in ticks if lo * 0.9 <= t <= hi * 1.35]
    ax.set_yticks(ticks); ax.set_yticks([], minor=True)
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda v, _: f"{v:,.0f}" if v >= 1 else f"{v:g}"))


sc._log_ticks = _log_ticks
_legend = sc.legend
# P/E panel: the series sits near 30x at the start of the window, so the legend goes to the empty band below 21x
sc.legend = lambda ax, loc="upper left", ncol=1: _legend(ax, "lower center" if ncol == 2 else loc, ncol)

if __name__ == "__main__":
    sc.setup_fonts()
    P = PARAMS
    labels, vals = [], []
    for name, rep, cons in P["lines"]:
        labels.append(name)
        vals.append(cons if rep is None else (rep / cons - 1) * 100)
    print("surprises:", dict(zip(labels, np.round(vals, 2))))
    sc.bar_chart("/home/claude/azn/c1.png", labels, vals,
                 f"{P['ticker']}: Q3 2026 surprise vs. consensus by line",
                 "Reported vs. consensus, %",
                 sc.source_line("company filings, consensus", "30 Oct 2026",
                                "Consensus: pre-results analyst estimates", "Segments rounded to the nearest percent",
                                "CVRM: cardiovascular, renal and metabolism"),
                 fmt="{:+.0f}%", ylabel="vs. consensus (%)")
    sc.crop_for_pdf("/home/claude/azn/c1.png", "/home/claude/azn/c1_crop.png", "bar")

    df = load_weekly(P["xlsx"], P["window_start"])
    out = sc.price_eps_pe_chart(
        "/home/claude/azn/c2.png", df, "AstraZeneca",
        f"{P['ticker']}: share price vs. consensus earnings and valuation",
        sc.source_line("Bloomberg", P["asof"], "AZN LN Equity, weekly", "BEst 12m-forward consensus",
                       "40-week simple MA", "Log scale",
                       "P/E shaded above (orange) / below (blue) its 2018 to 2026 average"),
        ccy="GBp", eps_ccy="BEst", price_lbl=(10, 8), eps_lbl=(10, -20))
    sc.crop_for_pdf("/home/claude/azn/c2.png", "/home/claude/azn/c2_crop.png", "price_eps_pe")
    print(out)
