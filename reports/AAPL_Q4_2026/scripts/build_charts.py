"""build_charts.py: Apple (AAPL) fiscal Q4 2026 Earnings update charts. Edit PARAMS for the next quarter."""
import sys
sys.path.insert(0, "/home/claude")
import pandas as pd
import syz_charts as sc

PARAMS = {
    "xlsx": "/home/claude/aapl/AAPL.xlsx",
    "ticker": "AAPL",
    "ccy": "USD",
    "window_start": "2010-01-01",      # 2005-07 multiples (up to 56x on tiny EPS) distort the long-run average
    "last_date": "2026-11-02",         # 2 Nov close, before the after-close release; 3 Nov row has EPS only
    "asof": "2 Nov 2026",
    "reaction_pct": -3.47,             # after hours, 2 Nov 2026 (user material); replace with 3 Nov close-to-close
    "reaction_date": "2 November 2026 (after hours)",
    "market_pct": None,                # not available at the time of writing
    # Chart 1: surprise vs. LSEG consensus (press reports of 2 Nov 2026); % for sales/EPS, points for margins/growth guide
    "c1": [
        ("Revenue",    114.477 / 113.39 - 1, "pct"),
        ("iPhone",     57.583 / 56.54 - 1,   "pct"),
        ("Mac",        10.792 / 9.61 - 1,    "pct"),
        ("iPad",       6.229 / 6.70 - 1,     "pct"),
        ("Wearables",  8.300 / 9.06 - 1,     "pct"),
        ("Services",   31.573 / 31.58 - 1,   "pct"),
        ("EPS*",       2.05 / 1.99 - 1,      "pct"),   # ex USD 0.05 tariff refund
        ("GM*",        (46.9 - 47.5) / 100,  "bp"),    # 47.9% less ~1pt tariff refund vs. 47.5%
        ("Sales guide", (8.5 - 6.1) / 100,   "pt"),    # Dec-q growth midpoint 8.5% vs. 6.1%
        ("GM guide",   (45.5 - 46.3) / 100,  "bp"),    # Dec-q 45.5% midpoint vs. 46.3%
    ],
}


def load_daily_to_weekly(path, last_date, start):
    raw = pd.read_excel(path)
    cols = {c: c.lower() for c in raw.columns}
    pick = lambda *k: next(c for c, l in cols.items() if all(x in l for x in k))
    d = pd.DataFrame({
        "date": pd.to_datetime(raw[pick("date")]),
        "price": pd.to_numeric(raw[pick("last price")], errors="coerce"),
        "eps": pd.to_numeric(raw[pick("best eps")], errors="coerce"),
        "pe": pd.to_numeric(raw[pick("best p/e")], errors="coerce"),
    }).dropna(subset=["date"]).sort_values("date")
    d = d[d["date"] <= last_date].dropna(subset=["price"])
    w = d.set_index("date").resample("W-FRI").last().dropna(subset=["price"])
    w["ma40"] = w["price"].rolling(40).mean()          # true 40-week simple MA on weekly closes
    w = w.reset_index()
    w.loc[w.index[-1], "date"] = pd.Timestamp(last_date)  # last point dated at the actual close
    w = w[(w["date"] >= start) & w["eps"].notna()].reset_index(drop=True)
    return w


def main():
    sc.setup_fonts()
    sc.plt.rcParams["axes.ymargin"] = 0.12   # room for the value labels of the deepest bars
    P = PARAMS
    df = load_daily_to_weekly(P["xlsx"], P["last_date"], P["window_start"])

    labels = [l for l, _, _ in P["c1"]]
    vals = []
    fmts = []
    for _, v, kind in P["c1"]:
        if kind == "pct":
            vals.append(v * 100); fmts.append(f"{v*100:+.1f}%")
        elif kind == "bp":
            vals.append(v * 100); fmts.append(f"{v*1e4:+.0f}bp")
        else:
            vals.append(v * 100); fmts.append(f"{v*100:+.1f}pt")
    fmts = ["0.0%" if f in ("-0.0%", "+0.0%") else f for f in fmts]
    fmts = [f.replace("-", "\u2212") for f in fmts]
    colors = [sc.BLUEB if round(v, 1) >= 0 else sc.ORANGE for v in vals]
    it = iter(fmts)

    class _Fmt:                      # bar_chart calls fmt.format(v): hand back the prepared labels in order
        def format(self, _v):
            return next(it)

    sc.bar_chart("/home/claude/aapl/c1_aapl_surprise.png", labels, vals,
                 "AAPL: Q4 2026 results and December-quarter guide vs. consensus",
                 "Surprise vs. LSEG consensus: % for sales and EPS, points for margins and the growth guide",
                 sc.source_line("LSEG consensus as reported 2 Nov 2026, company filings", P["asof"],
                                "*EPS and gross margin (GM) ex tariff refunds", "Guides at midpoint, December quarter"),
                 fmt=_Fmt(), ylabel="Surprise (% or points)", colors=colors)

    stats = sc.price_eps_pe_chart(
        "/home/claude/aapl/c2_aapl_price_eps_pe.png", df, "Apple",
        "AAPL: share price vs. consensus earnings and valuation",
        sc.source_line("Bloomberg", P["asof"], "AAPL US Equity, weekly", "BEst 12m-forward consensus",
                       "40-week simple MA", "Log scale", "P/E shaded above (orange) / below (blue) its 2010-26 average"),
        ccy=P["ccy"])
    sc.crop_for_pdf("/home/claude/aapl/c1_aapl_surprise.png", "/home/claude/aapl/c1_crop.png", "bar")
    sc.crop_for_pdf("/home/claude/aapl/c2_aapl_price_eps_pe.png", "/home/claude/aapl/c2_crop.png", "price_eps_pe")
    print({k: (round(v, 2) if isinstance(v, float) else v) for k, v in stats.items()})
    print("window", df["date"].iloc[0].date(), "to", df["date"].iloc[-1].date(), len(df), "weeks")


if __name__ == "__main__":
    main()
