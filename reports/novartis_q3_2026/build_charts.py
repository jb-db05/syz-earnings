"""build_charts.py: Novartis Q3 2026 earnings update, data -> charts (standalone PNGs + PDF crops).
Usage: python3 build_charts.py   (edit PARAMS for the next quarter)"""
import json
import os
import sys

sys.path.insert(0, "/home/claude")
import pandas as pd
from syz_charts import (setup_fonts, load_bloomberg_sheet, price_eps_pe_chart, bar_chart, crop_for_pdf,
                        source_line)

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "out")

PARAMS = {
    "xlsx": "/root/.claude/uploads/a7719d31-c90a-5c22-a8c3-689842f9e47d/548dad9a-Novartis_shareprice.xlsx",
    "ticker": "NOVN",
    "bbg": "NOVN SW Equity",
    "ccy": "CHF",            # listing currency (price, P/E)
    "eps_ccy": "USD",        # reporting currency of the consensus EPS
    "asof": "26 Oct 2026",   # last close in the export (pre-results; the 27 Oct row has no price yet)
    "quarter": "Q3 2026",
    # publication-day reaction: results released before the open on 27 Oct 2026; close not yet available,
    # pre-market indication (Julius Baer, 08:39 CET, finanzen.net) used and flagged for a Bloomberg check
    "reaction_pct": 1.2,
    "reaction_price": 129.05,
    "reaction_date": "27 October 2026",
    "market_pct": None,
    # Chart 1: reported vs. pre-results consensus, % (analyst first takes and press of 27 Oct 2026)
    "c1_labels": ["Net sales", "Core operating\nincome", "Core net\nincome", "Core EPS", "Rhapsido", "Scemblix",
                  "Pluvicto"],
    "c1_values": [0.6, 7.6, 7.4, 7.0, 16.0, -2.1, -7.7],
}


def main():
    os.makedirs(OUT, exist_ok=True)
    setup_fonts()
    p = PARAMS

    # ---------------- data
    df = load_bloomberg_sheet(p["xlsx"], weekly=True)
    df = df[df["eps"].notna() & df["pe"].notna()].reset_index(drop=True)
    last = df.iloc[-1]
    yr_ago = df[df["date"] <= last["date"] - pd.DateOffset(years=1)].iloc[-1]
    one_y = df[df["date"] > last["date"] - pd.DateOffset(years=1)]
    stats = {
        "window": f"{df['date'].iloc[0]:%d %b %Y} to {last['date']:%d %b %Y}",
        "price": float(last["price"]), "eps": float(last["eps"]), "pe": float(last["pe"]),
        "ma200": float(last["ma40"]),
        "pe_avg": float(df["pe"].mean()),
        "pe_avg_1y": float(one_y["pe"].mean()),
        "pe_peak": float(df["pe"].max()), "pe_peak_date": f"{df.loc[df['pe'].idxmax(), 'date']:%d %b %Y}",
        "price_12m_pct": float(last["price"] / yr_ago["price"] - 1) * 100,
        "eps_12m_pct": float(last["eps"] / yr_ago["eps"] - 1) * 100,
    }
    stats["pe_premium_pct"] = (stats["pe"] / stats["pe_avg"] - 1) * 100
    stats["pe_after_3pct_upgrade"] = stats["pe"] / 1.03

    # ---------------- Chart 2: price vs. consensus EPS and P/E (fixed)
    c2 = os.path.join(OUT, f"{p['ticker']}_price_eps_pe.png")
    foot2 = source_line("Bloomberg", p["asof"], f"{p['bbg']}, weekly", "BEst 12m-forward EPS (USD), price (CHF)",
                        "200-day simple MA", "Log scale", "P/E shaded vs. its 2005-26 average")
    res = price_eps_pe_chart(c2, df, "Novartis", f"{p['ticker']}: share price vs. consensus earnings and valuation",
                             foot2, ccy=p["ccy"], eps_ccy=p["eps_ccy"], ma_label="200-day moving average",
                             p1_title="Share price (CHF) and consensus 12m-forward EPS (USD), log scale",
                             eps_subs=(1, 2, 3, 5, 7))
    stats.update({k: res[k] for k in ("pe_premium_pct", "above_ma")})
    crop_for_pdf(c2, os.path.join(OUT, "c2_crop.png"), "price_eps_pe")

    # ---------------- Chart 1: surprise vs. consensus
    c1 = os.path.join(OUT, f"{p['ticker']}_q3_2026_vs_consensus.png")
    foot1 = source_line("company filings, analyst first takes", "27 Oct 2026",
                        "Reported vs. pre-results consensus", "Rhapsido, Scemblix and Pluvicto: brand-level estimates")
    bar_chart(c1, p["c1_labels"], p["c1_values"], f"{p['ticker']}: {p['quarter']} results vs. consensus",
              "Reported vs. pre-results consensus, %", foot1, ylabel="Surprise vs. consensus (%)")
    crop_for_pdf(c1, os.path.join(OUT, "c1_crop.png"), "bar")

    json.dump(stats, open(os.path.join(OUT, "stats.json"), "w"), indent=1, default=str)
    for k, v in stats.items():
        print(f"{k:24s} {v:.2f}" if isinstance(v, float) else f"{k:24s} {v}")


if __name__ == "__main__":
    main()
