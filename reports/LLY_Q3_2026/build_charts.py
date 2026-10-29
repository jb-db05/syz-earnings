"""build_charts.py: Eli Lilly Q3 2026 charts (Syz Earnings update). Run: python3 build_charts.py"""
import sys
import pandas as pd
sys.path.insert(0, "/home/claude")
import syz_charts as sc

PARAMS = {
    "xlsx": "/home/claude/LLY.xlsx",          # Bloomberg daily export: Date, BEst P/E, BEst EPS, Last Price, SMAVG(40), SMAVG(200)
    "ticker": "LLY", "name": "Eli Lilly", "ccy": "USD",
    "asof": "29 Oct 2026",
    "reaction_pct": 1393.37 / 1288.30 * 100 - 100,   # 29 Oct (intraday at export) vs. 28 Oct close
    "reaction_date": "29 October 2026", "market_pct": None,
    "out": "/home/claude",
}


def load_daily_as_weekly(path):
    """The LLY export is daily: resample to weekly (last trading day of each week) and compute the
    40-week simple MA from weekly closes so the chart matches the kit's 40-week convention."""
    d = pd.read_excel(path)
    pick = lambda *k: next(c for c in d.columns if all(x in c.lower() for x in k))
    d = pd.DataFrame({"date": pd.to_datetime(d[pick("date")]),
                      "price": pd.to_numeric(d[pick("last price")], errors="coerce"),
                      "eps": pd.to_numeric(d[pick("best eps")], errors="coerce"),
                      "pe": pd.to_numeric(d[pick("best p/e")], errors="coerce")})
    d = d.dropna(subset=["price"]).sort_values("date")
    d["wk"] = d["date"].dt.to_period("W-FRI")
    w = d.groupby("wk").last().reset_index(drop=True)          # keeps the actual last date of each week
    w["ma40"] = w["price"].rolling(40).mean()
    w = w[w["eps"].notna() & w["pe"].notna()].reset_index(drop=True)   # window starts at first consensus EPS
    return w[["date", "price", "eps", "ma40", "pe"]]


def main():
    sc.setup_fonts()
    out = PARAMS["out"]

    # Chart 1: Q3 2026 surprise by line (consensus from analyst first takes; guide vs. prior guide)
    labels = ["Revenue", "Ex one-offs", "EPS", "Mounjaro ex-US", "Foundayo", "FY26 guide"]
    values = [(24.397 / 22.6 - 1) * 100,           # reported revenue vs. ~USD 22.6bn consensus (USD 1.8bn beat)
              ((24.397 - 0.9) / 22.6 - 1) * 100,   # less ~USD 0.9bn Jardiance milestones and rebate adjustments
              (7.48 / 5.68 - 1) * 100,             # non-GAAP EPS vs. 5.68 consensus
              (5.7 / (5.7 - 0.415) - 1) * 100,     # Mounjaro outside US, USD 415m above consensus
              (184 / (184 + 45) - 1) * 100,        # Foundayo, USD 45m below consensus
              (91.5 / 86.0 - 1) * 100]             # FY26 revenue guide midpoint vs. prior guide
    sc.bar_chart(f"{out}/c1.png", labels, values,
                 "LLY: Q3 2026 results vs. consensus",
                 "Surprise vs. consensus, % · FY26 guide: revenue midpoint vs. prior guide",
                 sc.source_line("Bloomberg, company release of 29 Oct 2026, analyst research notes", PARAMS["asof"],
                                "Ex one-offs strips about USD 0.9bn of Jardiance milestones and rebate adjustments"))
    sc.crop_for_pdf(f"{out}/c1.png", f"{out}/c1_crop.png", "bar")

    # Chart 2: price vs. consensus 12m-forward EPS and P/E
    df = load_daily_as_weekly(PARAMS["xlsx"])
    stats = sc.price_eps_pe_chart(
        f"{out}/c2.png", df, PARAMS["name"],
        "LLY: share price vs. consensus earnings and valuation",
        sc.source_line("Bloomberg", PARAMS["asof"], "LLY US Equity, weekly", "BEst 12m-forward consensus",
                       "40-week MA", "Log scale", "P/E shaded vs. its 2018-26 average", "Last point intraday"),
        ccy="USD", price_lbl=(10, -20), eps_lbl=(10, 8))
    sc.crop_for_pdf(f"{out}/c2.png", f"{out}/c2_crop.png", "price_eps_pe")

    last = df.iloc[-1]
    yr = df[df["date"] > last["date"] - pd.Timedelta(days=365)]
    a12 = df[df["date"] <= last["date"] - pd.Timedelta(days=365)].iloc[-1]
    print("window", df["date"].iloc[0].date(), "to", last["date"].date(), len(df), "weeks")
    print({k: round(v, 2) if isinstance(v, float) else v for k, v in stats.items()})
    print("1y avg P/E", round(yr["pe"].mean(), 1), "| peak", df["pe"].max(), df.loc[df["pe"].idxmax(), "date"].date())
    print("12m price", round((last["price"] / a12["price"] - 1) * 100, 1), "% | P/E a year ago", a12["pe"])
    print("reaction", round(PARAMS["reaction_pct"], 1), "%")
    print("chart 1", [round(v, 1) for v in values])


if __name__ == "__main__":
    main()
