"""build_charts.py: Arista Networks Q3 2026 Earnings update charts. Edit PARAMS for the next quarter."""
import sys
sys.path.insert(0, "/home/claude")
import numpy as np, pandas as pd
import matplotlib.pyplot as plt, matplotlib.dates as mdates, matplotlib.ticker as mticker
import syz_charts as sc

PARAMS = dict(
    xlsx="/home/claude/data/ANET.xlsx",
    out="/home/claude/work",
    ticker="ANET", asof="3 Nov 2026",
    reaction_pct=9.0, reaction_date="4 Nov 2026", reaction_kind="pre-market", premarket_px=185.10,
    window_start="2015-03-20",            # first 200-day MA reading
    # Chart 1: surprise by line (%), from the release and analyst first takes
    c1_labels=["Q3 revenue", "Q3 EPS vs. guide", "2026 revenue guide", "2027 revenue guide"],
    c1_values=[(3657.6 / 3334 - 1) * 100, (1.20 / 1.07 - 1) * 100, (13.3 / 12.68 - 1) * 100, 14.5],
)


def load_daily(path):
    """This export is daily (Bloomberg, newest first, dates partly as Excel serials) with 40- and 200-day MAs."""
    df = pd.read_excel(path)
    conv = lambda v: (pd.Timestamp("1899-12-30") + pd.Timedelta(days=float(v))
                      if isinstance(v, (int, float, np.integer, np.floating)) else pd.Timestamp(v))
    cols = {c: c.lower() for c in df.columns}
    pick = lambda *k: next(c for c, l in cols.items() if all(x in l for x in k))
    out = pd.DataFrame({"date": df[pick("date")].map(conv),
                        "price": pd.to_numeric(df[pick("last price")], errors="coerce"),
                        "ma40d": pd.to_numeric(df[pick("smavg (40)")], errors="coerce"),
                        "ma200d": pd.to_numeric(df[pick("smavg (200)")], errors="coerce")})
    return out.dropna(subset=["price"]).sort_values("date").reset_index(drop=True)


def price_ma_chart(path, df, title, footnote, premarket=None):
    """Chart 2 variant without consensus EPS / P/E: share price (log) vs. 200-day MA, and the premium
    of the price to that MA (orange above, blue-grey below)."""
    x = mdates.date2num(df["date"])
    prem = (df["price"] / df["ma200d"] - 1).to_numpy(float) * 100
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12.5, 8.6), dpi=200, sharex=True,
                                   gridspec_kw={"height_ratios": [2.45, 1], "hspace": 0.16})
    fig.subplots_adjust(top=0.875, bottom=0.085, left=0.07, right=0.96)
    sc.style_ax(ax1); ax1.set_yscale("log")
    ax1.plot(x, df["price"], color=sc.BLUEB, linewidth=1.6, zorder=4, label="Share price, USD")
    ax1.plot(x, df["ma200d"], color=sc.NAVY, linewidth=1.3, linestyle=sc.DASH, zorder=3, label="200-day moving average")
    sc._log_ticks(ax1, float(df["price"].min()), float(df["price"].max()), subs=(1, 2.5, 5))
    ax1.yaxis.set_major_formatter(mticker.FuncFormatter(lambda v, _: f"{v:,.0f}" if v >= 10 else f"{v:g}"))
    ax1.set_ylabel("Share price (USD, log scale)", fontsize=10, color=sc.AXIS_TXT, fontweight="bold")
    ax1.set_title("Share price and 200-day moving average (log scale)", fontsize=12, fontweight="bold", color=sc.NAVY, loc="left", pad=8)
    last = float(df["price"].iloc[-1])
    ax1.plot(x[-1], last, "o", color=sc.BLUEB, ms=5, zorder=5)
    ax1.annotate(f"{last:,.0f}", (x[-1], last), xytext=(10, -16), textcoords="offset points",
                 color=sc.BLUEB, fontsize=10.5, fontweight="bold")
    if premarket:
        ax1.plot(x[-1], premarket, "o", mfc="white", mec=sc.ORANGE, mew=1.6, ms=6, zorder=6,
                 label="4 Nov pre-market, +9%")
        ax1.annotate(f"{premarket:,.0f}", (x[-1], premarket), xytext=(10, 6), textcoords="offset points",
                     color=sc.ORANGE, fontsize=10.5, fontweight="bold")
    sc.legend(ax1, loc="upper left")

    sc.style_ax(ax2)
    ax2.plot(x, prem, color=sc.ORANGE, linewidth=1.3, zorder=3, label="Price vs. 200-day moving average")
    ax2.axhline(0, color=sc.NAVY, linewidth=1.0, zorder=2)
    ax2.fill_between(x, prem, 0, where=prem >= 0, interpolate=True, color=sc.ORANGE, alpha=0.12, zorder=1)
    ax2.fill_between(x, prem, 0, where=prem < 0, interpolate=True, color=sc.BLUEB, alpha=0.14, zorder=1)
    ax2.yaxis.set_major_formatter(mticker.FuncFormatter(lambda v, _: f"{v:+.0f}%"))
    ax2.set_title("Premium of the share price to its 200-day moving average", fontsize=12, fontweight="bold", color=sc.NAVY, loc="left", pad=8)
    ax2.plot(x[-1], prem[-1], "o", color=sc.ORANGE, ms=5, zorder=4)
    ax2.annotate(f"{prem[-1]:+.1f}%", (x[-1], prem[-1]), xytext=(10, -4), textcoords="offset points",
                 color=sc.ORANGE, fontsize=10.5, fontweight="bold")
    ax2.set_ylim(-40, 90)
    sc.legend(ax2, loc="upper left")
    ax2.xaxis.set_major_locator(mdates.YearLocator(1)); ax2.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))
    ax2.set_xlim(x[0] - 30, x[-1] + 330)
    sc.header(fig, title, None, footnote, title_y=0.955, foot_y=0.028, rule=False)
    fig.savefig(path, dpi=200, facecolor="white"); plt.close(fig)
    return {"price": last, "ma200d": float(df["ma200d"].iloc[-1]), "ma40d": float(df["ma40d"].iloc[-1]),
            "prem200": float(prem[-1])}


class Labels:
    """Pass per-bar labels through bar_chart's fmt argument."""
    def __init__(self, labels): self.it = iter(labels)
    def format(self, _v): return next(self.it)


if __name__ == "__main__":
    P = PARAMS
    sc.setup_fonts()
    sc.CROPS["price_ma"] = sc.CROPS["price_eps_pe"]
    d = load_daily(P["xlsx"])
    d = d[d["date"] >= P["window_start"]].reset_index(drop=True)
    s = d.set_index("date")["price"]
    stats = dict(last_date=str(d["date"].iloc[-1].date()), last=s.iloc[-1],
                 chg_12m=(s.iloc[-1] / s.asof(pd.Timestamp("2025-11-03")) - 1) * 100,
                 chg_ytd=(s.iloc[-1] / s.asof(pd.Timestamp("2025-12-31")) - 1) * 100,
                 since_q2=(s.iloc[-1] / s.asof(pd.Timestamp("2026-08-04")) - 1) * 100,
                 peak=s.max(), peak_date=str(s.idxmax().date()), off_peak=(s.iloc[-1] / s.max() - 1) * 100,
                 low_52w=s.loc["2025-11-04":].min(), low_52w_date=str(s.loc["2025-11-04":].idxmin().date()))

    c1 = f"{P['out']}/ANET_c1_surprises.png"
    vals = P["c1_values"]
    sc.bar_chart(c1, P["c1_labels"], vals,
                 "ANET: Q3 2026 results and guidance vs. expectations",
                 "Surprise in %, reported or guided vs. consensus (Q3 EPS vs. the midpoint of the company guide)",
                 sc.source_line("Bloomberg, company filings", "4 Nov 2026",
                                "Consensus: pre-results (analyst first takes)", "2026 and 2027 guides at the midpoint"),
                 fmt=Labels([f"+{v:.1f}%" for v in vals]), ylabel="Surprise, %")
    sc.crop_for_pdf(c1, f"{P['out']}/c1_crop.png", "bar")

    c2 = f"{P['out']}/ANET_c2_price_ma.png"
    r = price_ma_chart(c2, d, "ANET: share price vs. its 200-day moving average",
                       sc.source_line("Bloomberg", P["asof"], "ANET US Equity, daily", "200-day simple MA", "Log scale",
                                      "Premium shaded above (orange) / below (blue) the MA",
                                      "4 Nov pre-market level from after-hours trading, to be confirmed"),
                       premarket=P["premarket_px"])
    sc.crop_for_pdf(c2, f"{P['out']}/c2_crop.png", "price_ma")
    stats.update(r)
    for k, v in stats.items(): print(f"{k}: {v:.2f}" if isinstance(v, float) else f"{k}: {v}")
    print("c1 values:", [round(v, 1) for v in vals])
