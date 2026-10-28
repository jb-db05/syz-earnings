"""build_charts.py: PACCAR Q3 2026 earnings update, data -> charts. Run: python3 build_charts.py <bloomberg.xlsx>"""
import sys, json
import pandas as pd
sys.path.insert(0, "/home/claude")
from syz_charts import *

OUT = "/home/user/syz-earnings/reports/PCAR_Q3_2026"
PARAMS = {
    "ticker": "PCAR", "name": "PACCAR", "ccy": "USD", "asof": "27 Oct 2026",
    "window_start": "2011-01-01",          # 2009-10 forward P/E above 100x on collapsed EPS: excluded
    "prev_results": "2026-07-27",          # Q2 2026 release date (pre-results close)
    "reaction_date": "2026-10-27", "reaction_pct": None, "market_pct": None,   # reaction computed from the daily file
    # Chart 1: surprise vs. consensus / estimates / guidance, %
    "c1_labels": ["Sales ex financial\nservices", "Diluted EPS", "Truck pretax\nprofit", "Parts pretax\nprofit", "Deliveries\nvs. guide"],
    "c1_values": [(7.38 / 7.48 - 1) * 100, (1.61 / 1.61 - 1) * 100, (454.5 / 317.37 - 1) * 100,
                  (404.4 / 468.18 - 1) * 100, (40100 / 42000 - 1) * 100],
}


def load_daily(path):
    """Bloomberg daily export (Date | Last Price | BEst EPS | BEst P/E | SMAVG(40) | SMAVG(200)), newest first.
    Resampled to weekly (Friday, last observation; the last week is dated on its last trading day) and the
    40-week simple MA computed from the weekly closes."""
    raw = pd.read_excel(path).dropna(how="all")
    cols = {c: c.lower() for c in raw.columns}
    pick = lambda *keys: next(c for c, l in cols.items() if all(k in l for k in keys))
    d = pd.DataFrame({
        "date": pd.to_datetime(raw[pick("date")]),
        "price": pd.to_numeric(raw[pick("last price")], errors="coerce"),
        "eps": pd.to_numeric(raw[pick("best eps")], errors="coerce"),
        "pe": pd.to_numeric(raw[pick("best p/e")], errors="coerce"),
    }).sort_values("date").set_index("date")
    d["eps"] = d["eps"].ffill()
    d = d[d["price"].notna()]
    wk = d.resample("W-FRI").last()
    wk.index = pd.DatetimeIndex(d["price"].resample("W-FRI").apply(lambda s: s.index.max()).values, name="date")
    wk["ma40"] = wk["price"].rolling(40).mean()
    return d, wk.reset_index()


if __name__ == "__main__":
    setup_fonts()
    daily, wk = load_daily(sys.argv[1])
    df = wk[(wk["date"] >= PARAMS["window_start"]) & wk["eps"].notna()].reset_index(drop=True)

    # ---- numbers quoted in the text
    p = daily["price"]
    rd = pd.Timestamp(PARAMS["reaction_date"])
    prev = p.loc[:rd - pd.Timedelta(days=1)]
    last = daily.iloc[-1]
    yago = daily.loc[:rd - pd.DateOffset(years=1)].iloc[-1]
    q2 = daily.loc[:PARAMS["prev_results"]].iloc[-1]
    peak_dt = p.loc["2025-10-27":].idxmax()
    pe_since = df["pe"].mean()
    pe_1y = daily.loc[rd - pd.DateOffset(years=1):, "pe"].mean()
    lower_pe = daily.loc[daily["pe"] <= last["pe"]].index
    nums = {
        "last_date": str(daily.index[-1].date()), "last_price": last["price"], "eps": last["eps"], "pe": last["pe"],
        "reaction_pct": (p.loc[rd] / prev.iloc[-1] - 1) * 100,
        "pre_slide_pct": (prev.iloc[-1] / p.loc[:"2026-10-22"].iloc[-1] - 1) * 100,
        "pe_avg_since_2011": pe_since, "pe_premium_pct": (last["pe"] / pe_since - 1) * 100, "pe_1y_avg": pe_1y,
        "price_12m_pct": (last["price"] / yago["price"] - 1) * 100, "eps_12m_pct": (last["eps"] / yago["eps"] - 1) * 100,
        "peak_price": p.loc[peak_dt], "peak_date": str(peak_dt.date()), "pe_at_peak": daily.loc[peak_dt, "pe"],
        "eps_at_peak": daily.loc[peak_dt, "eps"], "from_peak_pct": (last["price"] / p.loc[peak_dt] - 1) * 100,
        "price_since_q2_pct": (last["price"] / q2["price"] - 1) * 100, "eps_since_q2_pct": (last["eps"] / q2["eps"] - 1) * 100,
        "pe_q2": q2["pe"], "ma40w": df["ma40"].iloc[-1], "price_vs_ma40_pct": (last["price"] / df["ma40"].iloc[-1] - 1) * 100,
        "pe_low_since": str(lower_pe[lower_pe < daily.index[-1]].max().date()),
        "eps_peak": daily.loc["2011":, "eps"].max(), "eps_peak_date": str(daily.loc["2011":, "eps"].idxmax().date()),
        "pe_after_10pct_upgrade": last["price"] / (last["eps"] * 1.1),
        "c1_values": PARAMS["c1_values"],
    }

    # ---- Chart 1: surprise vs. consensus and guidance
    t = PARAMS["ticker"]
    plt.rcParams["axes.ymargin"] = 0.16          # room for the -13.6% label above the category labels
    bar_chart(f"{OUT}/PCAR_chart1_surprise.png", PARAMS["c1_labels"], PARAMS["c1_values"],
              f"{t}: Q3 2026 results vs. consensus and guidance",
              "Surprise vs. consensus or analyst estimates, %; deliveries vs. the ~42,000 company guide",
              source_line("Bloomberg, company filings", "27 Oct 2026", "Sales of truck, parts and other",
                          "Consensus and estimates pre-results"), ylabel="Surprise, %")
    crop_for_pdf(f"{OUT}/PCAR_chart1_surprise.png", "/home/claude/c1_crop.png", "bar")
    plt.rcParams["axes.ymargin"] = 0.05

    # ---- Chart 2: price vs. consensus EPS and P/E
    r = price_eps_pe_chart(f"{OUT}/PCAR_chart2_price_eps_pe.png", df, PARAMS["name"],
                           f"{t}: share price vs. consensus earnings and valuation",
                           source_line("Bloomberg", PARAMS["asof"], "PCAR US Equity, weekly", "BEst 12m-forward consensus",
                                       "40-week simple MA", "Log scale",
                                       "P/E shaded above (orange) / below (blue) its 2011-26 average"),
                           ccy=PARAMS["ccy"])
    crop_for_pdf(f"{OUT}/PCAR_chart2_price_eps_pe.png", "/home/claude/c2_crop.png", "price_eps_pe")
    nums.update({f"chart_{k}": v for k, v in r.items()})
    json.dump(nums, open(f"{OUT}/numbers.json", "w"), indent=1, default=float)
    for k, v in nums.items():
        print(f"{k:24s} {v:.2f}" if isinstance(v, float) else f"{k:24s} {v}")
