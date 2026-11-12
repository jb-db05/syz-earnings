"""build_charts.py: Siemens Q4 FY2026 Earnings update charts (Chart 1 surprises, Chart 2 price/EPS/P/E)."""
import sys, json
import numpy as np
import pandas as pd
sys.path.insert(0, "/home/claude")
import syz_charts as sc

PARAMS = {
    "xlsx": "SIE.xlsx",
    "ticker": "SIE",
    "bbg": "SIE GY Equity",
    "ccy": "EUR",
    # Rows before Oct 2014 in this export carry another series (price ~15, EPS ~12, no P/E): the window
    # starts at the first week with price, EPS, 40-week MA and P/E all present after that break.
    "window_start": "2014-10-01",
    "asof": "12 Nov 2026",
    "reaction_pct": 3.0,          # intraday, 12 Nov 2026, Xetra (user material, press reports); replace with the close
    "reaction_date": "12 November 2026",
    "market_pct": None,           # DAX move not available at writing
    "c1": {
        "labels": ["Q4 orders", "Q4 revenue", "Q4 industrial profit", "FY free cash flow"],
        "values": [29.0, 1.0, 5.0, (12.1 / 10.3 - 1) * 100],
    },
}


def load(path):
    """Bloomberg export whose newest rows carry Excel serial dates instead of datetimes."""
    df = pd.read_excel(path).dropna(how="all")
    cols = {c: c.lower() for c in df.columns}
    pick = lambda *k: next(c for c, l in cols.items() if all(x in l for x in k))
    conv = lambda d: (pd.Timestamp("1899-12-30") + pd.Timedelta(days=float(d))) if isinstance(d, (int, float, np.integer, np.floating)) else pd.Timestamp(d)
    out = pd.DataFrame({
        "date": df[pick("date")].map(conv),
        "price": pd.to_numeric(df[pick("last price")], errors="coerce"),
        "eps": pd.to_numeric(df[pick("best eps")], errors="coerce"),
        "ma40": pd.to_numeric(df[pick("moving average")], errors="coerce"),
        "pe": pd.to_numeric(df[pick("best p/e")], errors="coerce"),
    }).dropna(subset=["date"]).sort_values("date").reset_index(drop=True)
    out = out[out["date"] >= PARAMS["window_start"]]
    first = out.dropna().index[0]
    return out.loc[first:].reset_index(drop=True)


if __name__ == "__main__":
    sc.setup_fonts()
    df = load(PARAMS["xlsx"])
    start = df["date"].iloc[0]
    t = PARAMS["ticker"]

    # ---- Chart 2
    foot2 = sc.source_line("Bloomberg", PARAMS["asof"], f"{PARAMS['bbg']}, weekly", "BEst 12m-forward consensus",
                           "40-week simple MA", "Log scale",
                           f"P/E shaded above (orange) / below (blue) its {start.year}-26 average")
    st = sc.price_eps_pe_chart("SIE_price_eps_pe.png", df, "Siemens", f"{t}: share price vs. consensus earnings and valuation", foot2,
                               ccy="EUR", price_lbl=(10, -16), eps_lbl=(10, 10))
    sc.crop_for_pdf("SIE_price_eps_pe.png", "c2_crop.png", "price_eps_pe")

    # ---- Chart 1
    c1 = PARAMS["c1"]
    foot1 = sc.source_line("company filings, Bloomberg", PARAMS["asof"],
                           "Consensus: analyst estimates before the release (analyst first takes)",
                           "Free cash flow: fiscal year, all other lines: fiscal Q4")
    sc.bar_chart("SIE_results_vs_consensus.png", c1["labels"], c1["values"], f"{t}: Q4 FY2026 results vs. consensus",
                 "Reported vs. consensus, %", foot1, ylabel="vs. consensus, %")
    sc.crop_for_pdf("SIE_results_vs_consensus.png", "c1_crop.png", "bar")

    # ---- statistics quoted in the text
    last = df.iloc[-1]
    def ago(days):
        return df[df["date"] <= last["date"] - pd.Timedelta(days=days)].iloc[-1]
    y1 = ago(365)
    one_y = df[df["date"] > last["date"] - pd.Timedelta(days=365)]
    peak = df.loc[df["pe"].idxmax()]
    prev = df[df["date"] <= "2026-08-07"].iloc[-1]   # week of the Q3 print (6 Aug 2026)
    stats = dict(st, start=str(start.date()), last_date=str(last["date"].date()), prev_close_week=str(df.iloc[-2]["date"].date()),
                 prev_close_price=float(df.iloc[-2]["price"]),
                 price_12m_pct=(last["price"] / y1["price"] - 1) * 100, eps_12m_pct=(last["eps"] / y1["eps"] - 1) * 100,
                 pe_1y_avg=float(one_y["pe"].mean()), pe_peak=float(peak["pe"]), pe_peak_date=str(peak["date"].date()),
                 pe_min=float(df["pe"].min()), pe_min_date=str(df.loc[df["pe"].idxmin(), "date"].date()),
                 q3_week=str(prev["date"].date()), q3_price=float(prev["price"]), q3_eps=float(prev["eps"]), q3_pe=float(prev["pe"]),
                 price_since_q3_pct=(last["price"] / prev["price"] - 1) * 100, eps_since_q3_pct=(last["eps"] / prev["eps"] - 1) * 100,
                 pe_at_avg_price=float(st["pe_avg"] * last["eps"]),
                 c1_values=c1["values"], rows=len(df))
    json.dump(stats, open("stats.json", "w"), indent=1)
    print(json.dumps(stats, indent=1))
