"""build_charts.py: Sandoz Q3 2026 earnings update, data -> charts. Run: python3 build_charts.py <bloomberg.xlsx>"""
import sys, json
import pandas as pd
sys.path.insert(0, "/home/claude")
import syz_charts
from syz_charts import *

# Short history (Oct 2023 onwards) and a narrow range: denser log ladders and round tick steps, set from here
# so that the shared kit stays unchanged.
_log_ticks0, _legend0, _style0 = syz_charts._log_ticks, syz_charts.legend, syz_charts.style_ax
def _ticks(ax, lo, hi, subs=None):
    if hi < 10:     # EPS in CHF, 2.5 to 3.7: half steps with one decimal
        _log_ticks0(ax, lo, hi, (1, 2.5, 3, 3.5, 4))
        ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda v, _: f"{v:.1f}"))
    else:
        _log_ticks0(ax, lo, hi, (1, 2.5, 5, 7.5))
syz_charts._log_ticks = _ticks
def _legend(ax, *a, **k):
    ax.yaxis.set_major_locator(mticker.MultipleLocator(5)); return _legend0(ax, *a, **k)
def _style(ax, *a, **k):
    _style0(ax, *a, **k); ax.yaxis.set_major_locator(mticker.MultipleLocator(5))
syz_charts.legend = _legend
_header0 = syz_charts.header
def _header_end2026(fig, *a, **k):
    # x axis ends on 31 December 2026 (the kit leaves ~11 months of blank space after the last date)
    for ax in fig.axes:
        if ax.get_xscale() == "linear" and ax.get_xlim()[1] > mdates.date2num(pd.Timestamp("2026-01-01")):
            ax.set_xlim(right=mdates.date2num(pd.Timestamp("2026-12-31")))
    return _header0(fig, *a, **k)

OUT = "/home/user/syz-earnings/reports/SDZ_Q3_2026"
CROP = "/home/claude/sdz"
PARAMS = {
    "ticker": "SDZ", "name": "Sandoz", "ccy": "CHF", "asof": "28 Oct 2026",
    "prev_results": "2026-08-04",          # H1 2026 release on 5 August: pre-results close
    "reaction_date": "2026-10-28", "reaction_pct": None, "market_pct": None,   # computed from the daily file
    # Chart 1: Q3 2026 sales growth at constant currencies, %
    "c1_labels": ["Group", "Group ex\nB2B headwind", "Biosimilars", "Generics", "North\nAmerica", "Europe"],
    "c1_values": [5, 7, 17, 0, 20, 1],
}


def load_daily(path):
    """Bloomberg daily export (Date | Last Price | BEst EPS | BEst P/E | SMAVG(40) | SMAVG(200)), newest first.
    BEst EPS is in USD (reporting currency) and the price in CHF: EPS in CHF is derived as price / BEst P/E.
    Resampled to weekly (Friday, last observation; each week dated on its last trading day); the 40-week simple
    MA is computed from the weekly closes."""
    raw = pd.read_excel(path).dropna(how="all")
    cols = {c: c.lower() for c in raw.columns}
    pick = lambda *keys: next(c for c, l in cols.items() if all(k in l for k in keys))
    d = pd.DataFrame({
        "date": pd.to_datetime(raw[pick("date")]),
        "price": pd.to_numeric(raw[pick("last price")], errors="coerce"),
        "eps_usd": pd.to_numeric(raw[pick("best eps")], errors="coerce"),
        "pe": pd.to_numeric(raw[pick("best p/e")], errors="coerce"),
    }).sort_values("date").set_index("date")
    d = d[d["price"].notna() & d["pe"].notna()]
    d["eps"] = d["price"] / d["pe"]
    wk = d.resample("W-FRI").last()
    wk.index = pd.DatetimeIndex(d["price"].resample("W-FRI").apply(lambda s: s.index.max()).values, name="date")
    wk["ma40"] = wk["price"].rolling(40).mean()
    return d, wk.reset_index()


if __name__ == "__main__":
    import os; os.makedirs(CROP, exist_ok=True)
    setup_fonts()
    daily, wk = load_daily(sys.argv[1])
    df = wk[wk["eps"].notna()].reset_index(drop=True)

    p = daily["price"]
    rd = pd.Timestamp(PARAMS["reaction_date"])
    prev = p.loc[:rd - pd.Timedelta(days=1)]
    last = daily.iloc[-1]
    yago = daily.loc[:rd - pd.DateOffset(years=1)].iloc[-1]
    ytd0 = daily.loc[:"2025-12-31"].iloc[-1]
    q2 = daily.loc[:PARAMS["prev_results"]].iloc[-1]
    peak_dt = p.idxmax()
    pe_peak_dt = daily["pe"].idxmax()
    nums = {
        "last_date": str(daily.index[-1].date()), "last_price": last["price"], "eps_chf": last["eps"],
        "eps_usd": daily["eps_usd"].ffill().iloc[-1], "pe": last["pe"], "prev_close": prev.iloc[-1],
        "reaction_pct": (p.loc[rd] / prev.iloc[-1] - 1) * 100,
        "ytd_pct_pre": (prev.iloc[-1] / ytd0["price"] - 1) * 100, "ytd_pct": (last["price"] / ytd0["price"] - 1) * 100,
        "pe_pre": daily["pe"].loc[:rd - pd.Timedelta(days=1)].iloc[-1],
        "pe_avg_since_start": df["pe"].mean(), "pe_premium_pct": (last["pe"] / df["pe"].mean() - 1) * 100,
        "pe_1y_avg": daily.loc[rd - pd.DateOffset(years=1):, "pe"].mean(),
        "pe_peak": daily["pe"].max(), "pe_peak_date": str(pe_peak_dt.date()),
        "price_12m_pct": (last["price"] / yago["price"] - 1) * 100, "eps_chf_12m_pct": (last["eps"] / yago["eps"] - 1) * 100,
        "eps_usd_12m_pct": (daily["eps_usd"].ffill().iloc[-1] / daily["eps_usd"].ffill().loc[:yago.name].iloc[-1] - 1) * 100,
        "peak_price": p.loc[peak_dt], "peak_date": str(peak_dt.date()),
        "price_since_h1_pct": (last["price"] / q2["price"] - 1) * 100, "eps_chf_since_h1_pct": (last["eps"] / q2["eps"] - 1) * 100,
        "pe_h1": q2["pe"], "ma40w": df["ma40"].iloc[-1], "price_vs_ma40_pct": (last["price"] / df["ma40"].iloc[-1] - 1) * 100,
        "price_since_spinoff_pct": (last["price"] / p.iloc[0] - 1) * 100, "first_date": str(p.index[0].date()),
        "pe_after_10pct_upgrade": last["price"] / (last["eps"] * 1.1),
        "eps_chf_first": df["eps"].iloc[0], "pe_first": df["pe"].iloc[0],
    }

    t = PARAMS["ticker"]
    syz_charts.style_ax = _style
    plt.rcParams["axes.ymargin"] = 0.1           # headroom for the +20% label
    bar_chart(f"{OUT}/SDZ_chart1_growth.png", PARAMS["c1_labels"], PARAMS["c1_values"],
              f"{t}: Q3 2026 sales growth by business and region",
              "Net sales growth at constant currencies, %",
              source_line("company filings", "28 Oct 2026", "B2B headwind: anti-infective active ingredients"),
              colors=[NAVY, NAVY, BLUEB, BLUEB, BLUEB, BLUEB], fmt="{:+.0f}%", ylabel="Growth, % at CC")
    crop_for_pdf(f"{OUT}/SDZ_chart1_growth.png", f"{CROP}/c1_crop.png", "bar")
    syz_charts.style_ax = _style0
    plt.rcParams["axes.ymargin"] = 0.05

    syz_charts.header = _header_end2026
    r = price_eps_pe_chart(f"{OUT}/SDZ_chart2_price_eps_pe.png", df, PARAMS["name"],
                           f"{t}: share price vs. consensus earnings and valuation",
                           source_line("Bloomberg", PARAMS["asof"], "SDZ SW Equity, weekly", "BEst 12m-forward consensus",
                                       "EPS in CHF = price / P/E", "40-week simple MA", "Log scale",
                                       "P/E shaded vs. its average since Oct 2023"),
                           ccy=PARAMS["ccy"])
    crop_for_pdf(f"{OUT}/SDZ_chart2_price_eps_pe.png", f"{CROP}/c2_crop.png", "price_eps_pe")
    syz_charts.header = _header0
    nums.update({f"chart_{k}": v for k, v in r.items()})
    json.dump(nums, open(f"{OUT}/numbers.json", "w"), indent=1, default=float)
    for k, v in nums.items():
        print(f"{k:24s} {v:.2f}" if isinstance(v, float) else f"{k:24s} {v}")
