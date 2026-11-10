"""build_charts.py: Embraer Q3 2026 charts. Run: python3 build_charts.py"""
import pandas as pd, numpy as np
from syz_charts import (setup_fonts, load_bloomberg_sheet, price_eps_pe_chart, bar_chart, crop_for_pdf,
                        source_line, BLUEB, ORANGE)

PARAMS = {
    "xlsx": "/home/claude/Embraer.xlsx", "ticker": "EMBJ3", "ccy": "BRL", "asof": "10 Nov 2026",
    "window_start": None,          # full window (Sep 2014): loss weeks masked instead
    "PE_CLIP": 40, "TROUGH": ("2019-01-01", "2022-06-30"),   # Boeing JV unwind, Covid losses and recovery: blanked;                 # P/E readings above 40x blanked and excluded from the average (2019 to 2021 trough)
    "reaction_pct": 5.86, "reaction_date": "10 Nov 2026, 10:24 Brasilia (intraday, press-reported)", "market_pct": None,
    # Chart 1: Q3 surprises vs. consensus (press-reported) and FY26 guide revisions vs. previous guide
    "c1_labels": ["Revenue", "Adj. EBIT", "Adj. net income", "FY26 revenue guide", "FY26 FCF guide"],
    "c1_values": [11.0, 22.0, (379.8 / 764 - 1) * 100, (8.5 / 8.35 - 1) * 100, (700 / 400 - 1) * 100],
}

def main():
    setup_fonts()
    P = PARAMS
    df = load_bloomberg_sheet(P["xlsx"])
    df = df[df["eps"].notna()].reset_index(drop=True)
    if P["window_start"]:
        df = df[df["date"] >= P["window_start"]].reset_index(drop=True)
    trough = df["date"].between(*P["TROUGH"]) | (df["eps"] <= 0)                # loss and near-zero EPS (2019 to mid-2022)
    df.loc[trough, "eps"] = np.nan                                              # off the log axis
    df.loc[trough | (df["pe"] <= 0) | (df["pe"] > P["PE_CLIP"]), "pe"] = np.nan  # off the panel and the average
    t = P["ticker"]
    foot2 = source_line("Bloomberg", P["asof"], f"{t} BZ Equity, weekly", "BEst 12m-forward consensus",
                        "40-week MA", "Log scale", "Jan 2019 to Jun 2022 earnings trough blanked",
                        "P/E shaded vs. its 2014-26 average")
    r = price_eps_pe_chart("/home/claude/c2.png", df, t, f"{t}: share price vs. consensus earnings and valuation",
                           foot2, ccy=P["ccy"])
    print("chart 2:", {k: round(v, 2) if isinstance(v, float) else v for k, v in r.items()})

    vals = P["c1_values"]
    foot1 = source_line("company filings, Bloomberg", P["asof"], "Consensus: press-reported pre-results estimates",
                        "Net income compared in BRL", "Guides vs. previous guide (revenue midpoint, FCF floor)")
    bar_chart("/home/claude/c1.png", P["c1_labels"], vals,
              f"{t}: Q3 2026 surprises vs. consensus and guide revisions", "% vs. consensus (Q3) and vs. previous guide (FY26)",
              foot1, fmt="{:+.0f}%")
    crop_for_pdf("/home/claude/c1.png", "/home/claude/c1_crop.png", "bar")
    crop_for_pdf("/home/claude/c2.png", "/home/claude/c2_crop.png", "price_eps_pe")
    print("chart 1:", [round(v, 1) for v in vals])

if __name__ == "__main__":
    main()
