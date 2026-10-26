"""build_charts.py: Galp Q3 2026 Earnings update charts. Edit PARAMS for the next quarter."""
import sys
sys.path.insert(0, "/home/claude"); sys.path.insert(0, "/home/claude/galp")
import pandas as pd
import syz_charts as sc
from load import load_galp
import contextlib
import numpy as np
import matplotlib.axes
import matplotlib.ticker as mticker


def _dense_log_ticks(ax, lo, hi, subs=None):
    """Galp trades in a narrow range (EUR 8 to 23, EPS 0.8 to 2.5): the kit's 1-2-5 ladder leaves one tick per axis.
    Use a denser ladder (1, 1.5, 2, 2.5, 3, 4, 5, 7.5) with a %g formatter so 1.5 does not print as 2."""
    ladder = (1, 1.5, 2, 2.5, 3, 4, 5, 7.5)
    ticks = [m * 10 ** e for e in range(int(np.floor(np.log10(lo))) - 1, int(np.ceil(np.log10(hi))) + 2) for m in ladder]
    ticks = [t for t in ticks if lo * 0.97 <= t <= hi * 1.05]
    ax.set_yticks(ticks); ax.set_yticks([], minor=True)
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda v, _: f"{v:g}"))


@contextlib.contextmanager
def _swap_end_labels():
    """EPS ends above the price here, so put the EPS label above its dot and the price label below."""
    orig = matplotlib.axes.Axes.annotate
    swap = {(10, 10): (10, -15), (10, -22): (10, 10)}
    def patched(self, text, xy, *a, **k):
        if k.get("xytext") in swap:
            k["xytext"] = swap[k["xytext"]]
        return orig(self, text, xy, *a, **k)
    matplotlib.axes.Axes.annotate = patched
    try:
        yield
    finally:
        matplotlib.axes.Axes.annotate = orig

PARAMS = {
    "xlsx": "/home/claude/galp/GALP.xlsx",
    "ticker": "GALP",
    "asof": "26 Oct 2026",
    "window_from": "2022-01-01",          # 2020 EPS collapse pushed the P/E above 130x: anchor on the post-2022 regime
    # Chart 1: RCA EBITDA, EUR m (company release 26 Oct 2026; consensus as supplied by the user)
    "c1_labels": ["Q3 2025\nreported", "Q2 2026\nreported", "Q3 2026\nconsensus", "Q3 2026\nreported"],
    "c1_values": [911, 1272, 1471, 1522],
    "out": "/home/claude/galp",
}

if __name__ == "__main__":
    P = PARAMS
    sc.setup_fonts()
    daily, w = load_galp(P["xlsx"])
    df = w[w["date"] >= P["window_from"]].reset_index(drop=True)

    sc.bar_chart(f"{P['out']}/GALP_chart1_rca_ebitda.png", P["c1_labels"], P["c1_values"],
                 f"{P['ticker']}: Q3 2026 RCA EBITDA vs. consensus and history",
                 "EUR m · replacement cost adjusted (RCA) EBITDA",
                 sc.source_line("company filings, Bloomberg", P["asof"], "Galp Q3 2026 results release of 26 Oct 2026",
                                "Consensus: pre-results analyst estimates"),
                 colors=[sc.BLUEB, sc.BLUEB, sc.BLUEB, sc.ORANGE], fmt="{:,.0f}", zero_line=False)

    sc._log_ticks = _dense_log_ticks
    with _swap_end_labels():
      stats = sc.price_eps_pe_chart(
        f"{P['out']}/GALP_chart2_price_eps_pe.png", df, "Galp",
        f"{P['ticker']}: share price vs. consensus earnings and valuation",
        sc.source_line("Bloomberg", P["asof"], "GALP PL Equity, weekly", "BEst 12m-forward consensus",
                       "200-day (c. 40-week) simple MA", "Log scale",
                       "P/E shaded above (orange) / below (blue) its 2022-26 average"),
        ccy="EUR")
    sc.crop_for_pdf(f"{P['out']}/GALP_chart1_rca_ebitda.png", f"{P['out']}/c1_crop.png", "bar")
    sc.crop_for_pdf(f"{P['out']}/GALP_chart2_price_eps_pe.png", f"{P['out']}/c2_crop.png", "price_eps_pe")

    # numbers quoted in the text
    last = df.iloc[-1]
    def at(dt): return daily[daily["date"] <= pd.Timestamp(dt)].iloc[-1]
    y_ago, pre = at(last["date"] - pd.Timedelta(days=365)), at("2026-10-23")
    one_y = w[w["date"] >= last["date"] - pd.Timedelta(days=365)]["pe"].mean()
    hi = daily[daily["date"] >= last["date"] - pd.Timedelta(days=365)]
    hi = hi.loc[hi["price"].idxmax()]
    print({k: round(v, 3) if isinstance(v, float) else v for k, v in stats.items()})
    print(f"last {last['date']:%d %b %Y} price {last['price']} eps {last['eps']} pe {last['pe']}")
    print(f"pre-results {pre['date']:%d %b} price {pre['price']} pe {pre['pe']}  results-day move {last['price']/pre['price']-1:+.1%}")
    print(f"12m ago {y_ago['date']:%d %b %Y} price {y_ago['price']} eps {y_ago['eps']} pe {y_ago['pe']}"
          f"  price {last['price']/y_ago['price']-1:+.1%} eps {last['eps']/y_ago['eps']-1:+.1%}")
    print(f"1y avg pe {one_y:.2f}; 52w high {hi['price']} on {hi['date']:%d %b %Y} ({last['price']/hi['price']-1:+.1%})")
    print(f"pe at 10% EPS cut {last['price']/(last['eps']*0.9):.2f}x ({last['price']/(last['eps']*0.9)/stats['pe_avg']-1:+.1%} vs avg)")
