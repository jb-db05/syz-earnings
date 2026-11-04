"""build_charts.py: Arista Networks Q3 2026 Earnings update charts. Edit PARAMS for the next quarter."""
import sys
sys.path.insert(0, "/home/claude")
import numpy as np, pandas as pd
import matplotlib.pyplot as plt, matplotlib.dates as mdates, matplotlib.ticker as mticker
import syz_charts as sc

PARAMS = dict(
    xlsx="/home/claude/data2/ANET_US.xlsx",
    out="/home/claude/work",
    ticker="ANET", asof="4 Nov 2026",
    window_start="2015-01-01",
    reaction_pct=9.0, reaction_date="4 Nov 2026", reaction_kind="pre-market", premarket_px=185.10,
    # Chart 1: surprise by line (%), from the release and analyst first takes
    c1_labels=["Q3 revenue", "Q3 EPS vs. guide", "2026 revenue guide", "2027 revenue guide"],
    c1_values=[(3657.6 / 3334 - 1) * 100, (1.20 / 1.07 - 1) * 100, (13.3 / 12.68 - 1) * 100, 14.5],
)


class Labels:
    """Pass per-bar labels through bar_chart's fmt argument."""
    def __init__(self, labels): self.it = iter(labels)
    def format(self, _v): return next(self.it)


if __name__ == "__main__":
    P = PARAMS
    sc.setup_fonts()
    d = sc.load_bloomberg_sheet(P["xlsx"])
    d = d[d["eps"].notna() & (d["date"] >= P["window_start"])].reset_index(drop=True)   # 2015: skips the post-IPO P/E of 55x-63x
    s = d.set_index("date")
    ago = s.loc[:"2025-11-07"].iloc[-1]
    stats = dict(window=f'{d["date"].iloc[0].date()} to {d["date"].iloc[-1].date()}', last=s["price"].iloc[-1],
                 eps=s["eps"].iloc[-1], eps_prev=s["eps"].iloc[-2],
                 eps_rev_pct=(s["eps"].iloc[-1] / s["eps"].iloc[-2] - 1) * 100,
                 price_12m=(s["price"].iloc[-1] / ago["price"] - 1) * 100, eps_12m=(s["eps"].iloc[-1] / ago["eps"] - 1) * 100,
                 pe_12m_ago=ago["pe"], pe_1y_avg=s.loc["2025-11-05":, "pe"].mean(),
                 pe_peak_2020=s.loc["2020":, "pe"].max(), pe_peak_2020_date=str(s.loc["2020":, "pe"].idxmax().date()),
                 pe_after_q2=s.loc[:"2026-08-07", "pe"].iloc[-1], pe_premarket=s["pe"].iloc[-1] * (1 + P["reaction_pct"] / 100))
    c1 = f"{P['out']}/ANET_c1_surprises.png"
    vals = P["c1_values"]
    sc.bar_chart(c1, P["c1_labels"], vals,
                 "ANET: Q3 2026 results and guidance vs. expectations",
                 "Surprise in %, reported or guided vs. consensus (Q3 EPS vs. the midpoint of the company guide)",
                 sc.source_line("Bloomberg, company filings", "4 Nov 2026",
                                "Consensus: pre-results (analyst first takes)", "2026 and 2027 guides at the midpoint"),
                 fmt=Labels([f"+{v:.1f}%" for v in vals]), ylabel="Surprise, %")
    sc.crop_for_pdf(c1, f"{P['out']}/c1_crop.png", "bar")

    c2 = f"{P['out']}/ANET_c2_price_eps_pe.png"
    r = sc.price_eps_pe_chart(c2, d, "ANET", "ANET: share price vs. consensus earnings and valuation",
                              sc.source_line("Bloomberg", P["asof"], "ANET US Equity, weekly", "BEst 12m-forward consensus",
                                             "40-week simple MA", "Log scale",
                                             "P/E shaded above (orange) / below (blue) its 2015-26 average"),
                              ccy="USD", price_lbl=(10, -16), eps_lbl=(10, 10))
    sc.crop_for_pdf(c2, f"{P['out']}/c2_crop.png", "price_eps_pe")
    stats.update(r)
    for k, v in stats.items(): print(f"{k}: {v:.2f}" if isinstance(v, float) else f"{k}: {v}")
    print("c1 values:", [round(v, 1) for v in vals])
