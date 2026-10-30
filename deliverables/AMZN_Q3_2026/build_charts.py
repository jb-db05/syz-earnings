"""build_charts.py: Amazon Q3 2026 earnings update charts (Syz chart kit)."""
import sys
sys.path.insert(0, "/home/claude")
import pandas as pd
from syz_charts import (setup_fonts, load_bloomberg_sheet, price_eps_pe_chart, bar_chart, crop_for_pdf,
                        source_line, BLUEB, ORANGE)

PARAMS = {
    "xlsx": "/home/claude/amzn/Amazon_SharePrice.xlsx",
    "ticker": "AMZN",
    "asof": "29 Oct 2026",
    "reaction_pct": -7.0,          # pre-market, 30 Oct 2026 (results after the US close on 29 Oct)
    "reaction_date": "30 October 2026 (pre-market)",
    "market_pct": None,            # not available at the time of writing
    "out": "/home/claude/amzn",
}


def load_daily_to_weekly(path):
    """This export is daily (Date | Last Price | BEst P/E | BEst EPS | SMAVG(40) | SMAVG(200)).
    Resample to Friday weeks and compute the 40-week simple MA from weekly closes, then shape it
    like load_bloomberg_sheet() output."""
    raw = pd.read_excel(path, sheet_name=0).dropna(how="all", axis=1)
    cols = {c: str(c).lower() for c in raw.columns}
    pick = lambda *keys: next(c for c, l in cols.items() if all(k in l for k in keys))
    d = pd.DataFrame({
        "date": pd.to_datetime(raw[pick("date")]),
        "price": pd.to_numeric(raw[pick("last price")], errors="coerce"),
        "eps": pd.to_numeric(raw[pick("best eps")], errors="coerce"),
        "pe": pd.to_numeric(raw[pick("best p/e")], errors="coerce"),
    }).dropna(subset=["date", "price"]).sort_values("date").set_index("date")
    w = d.resample("W-FRI").last().dropna(subset=["price"])
    w["ma40"] = w["price"].rolling(40).mean()
    w = w.reset_index()
    w = w[w["eps"].notna() & w["pe"].notna()].reset_index(drop=True)   # window starts at first consensus EPS
    w.loc[w.index[-1], "date"] = d.index[-1]                            # last week ends on the last close (29 Oct)
    return w[["date", "price", "eps", "ma40", "pe"]]


if __name__ == "__main__":
    setup_fonts()
    out = PARAMS["out"]
    df = load_daily_to_weekly(PARAMS["xlsx"])

    # Chart 1: Q3 operating income in absolute terms vs. the guidance range and the prior year
    bar_chart(f"{out}/c1.png",
              ["Q3 2025\nreported", "Q3 2026\nguide low", "Q3 2026\nguide high", "Q3 2026\nreported"],
              [17.4, 22.5, 26.5, 28.1],
              "AMZN: Q3 2026 operating income vs. guidance and prior year",
              "USD bn",
              source_line("company filings", "29 Oct 2026", "Q3 2026 guidance from the Q2 2026 release"),
              colors=[BLUEB, BLUEB, BLUEB, ORANGE], fmt="{:,.1f}", zero_line=False)
    crop_for_pdf(f"{out}/c1.png", f"{out}/c1_crop.png", "bar")

    # Chart 2: share price vs. consensus EPS and P/E
    stats = price_eps_pe_chart(
        f"{out}/c2.png", df, "Amazon",
        "AMZN: share price vs. consensus earnings and valuation",
        source_line("Bloomberg", PARAMS["asof"], "AMZN US Equity, weekly", "BEst 12m-forward consensus",
                    "40-week simple MA", "Log scale", "P/E shaded above (orange) / below (blue) its 2018-26 average"),
        ccy="USD", price_lbl=(10, -16), eps_lbl=(10, 10))
    crop_for_pdf(f"{out}/c2.png", f"{out}/c2_crop.png", "price_eps_pe")
    print({k: round(v, 2) if isinstance(v, float) else v for k, v in stats.items()})
    print("window", df["date"].iloc[0].date(), "to", df["date"].iloc[-1].date(), len(df), "weeks")
