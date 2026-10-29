"""build_charts.py: Microsoft Q1 FY2027 Earnings update charts (Syz chart kit)."""
import sys
sys.path.insert(0, "/home/claude")
import pandas as pd
from syz_charts import (setup_fonts, load_bloomberg_sheet, price_eps_pe_chart, bar_chart, crop_for_pdf,
                        source_line, BLUEB, ORANGE)

PARAMS = {
    "xlsx": "/root/.claude/uploads/d22a55a6-7c43-5cbc-aecb-63aca74aa440/182c0245-MSFT_1.xlsx",
    "out": "/home/claude/msft",
    "ticker": "MSFT", "ccy": "USD", "asof": "29 Oct 2026",
    "window_start": None,                       # first consensus EPS row (April 2005); EPS never negative
    "prev_results": "2026-07-31",               # week of the Q4 FY2026 results (29 Jul 2026)
    "reaction_pct": 1.0, "reaction_date": "29 Oct 2026 (pre-market)", "market_pct": None,
    # Chart 1: surprise vs. pre-results consensus, % (reported / consensus - 1)
    "c1_labels": ["Revenue", "Operating income", "Adj. EPS", "Commercial RPO", "Q2 revenue guide"],
    "c1_reported": [92.28, 45.92, 4.89, 677.0, 96.55],
    "c1_consensus": [90.69, 44.06, 4.73, 705.6, 95.60],
}


def main():
    setup_fonts()
    P, out = PARAMS, PARAMS["out"]
    df = load_bloomberg_sheet(P["xlsx"])
    df = df[df["eps"].notna()].reset_index(drop=True)
    if P["window_start"]:
        df = df[df["date"] >= P["window_start"]].reset_index(drop=True)

    # ---- numbers quoted in the text
    last = df.iloc[-1]
    yago = df.iloc[(df["date"] - (last["date"] - pd.Timedelta(days=364))).abs().argsort().iloc[0]]
    prev = df[df["date"] <= P["prev_results"]].iloc[-1]
    since23 = df[df["date"] >= "2023-01-01"]
    stats = {
        "window": f"{df['date'].iloc[0]:%d %b %Y} to {last['date']:%d %b %Y}",
        "price": last["price"], "eps": last["eps"], "pe": last["pe"], "ma40": last["ma40"],
        "pe_avg_all": df["pe"].mean(),
        "pe_avg_1y": df[df["date"] > last["date"] - pd.Timedelta(days=365)]["pe"].mean(),
        "pe_avg_5y": df[df["date"] > last["date"] - pd.Timedelta(days=5 * 365)]["pe"].mean(),
        "pe_peak": (df["pe"].max(), f"{df.loc[df['pe'].idxmax(), 'date']:%b %Y}"),
        "pe_trough_since_2023": (since23["pe"].min(), f"{since23.loc[since23['pe'].idxmin(), 'date']:%b %Y}"),
        "pe_year_ago": yago["pe"],
        "price_12m_pct": (last["price"] / yago["price"] - 1) * 100,
        "eps_12m_pct": (last["eps"] / yago["eps"] - 1) * 100,
        "price_since_prev_pct": (last["price"] / prev["price"] - 1) * 100,
        "eps_since_prev_pct": (last["eps"] / prev["eps"] - 1) * 100,
        "price_vs_ma_pct": (last["price"] / last["ma40"] - 1) * 100,
        "record_price": (df["price"].max(), f"{df.loc[df['price'].idxmax(), 'date']:%d %b %Y}"),
        "pe_after_10pct_upgrade": last["pe"] / 1.10,
        "surprises_pct": [round((r / c - 1) * 100, 1) for r, c in zip(P["c1_reported"], P["c1_consensus"])],
    }
    stats["pe_premium_pct"] = (stats["pe"] / stats["pe_avg_all"] - 1) * 100
    for k, v in stats.items():
        print(f"{k:24s} {v}")

    # ---- Chart 1: surprise vs. consensus by line
    bar_chart(f"{out}/MSFT_results_vs_consensus.png", P["c1_labels"], stats["surprises_pct"],
              "MSFT: Q1 FY2027 results and Q2 guide vs. consensus",
              "Reported vs. pre-results consensus, % · Q2 revenue guide at the midpoint",
              source_line("Bloomberg, company filings", P["asof"],
                          "Consensus: pre-results analyst estimates",
                          "Adj. EPS excludes the OpenAI investment impact",
                          "RPO: remaining performance obligation"),
              ylabel="Surprise vs. consensus (%)")
    crop_for_pdf(f"{out}/MSFT_results_vs_consensus.png", f"{out}/c1_crop.png", "bar")

    # ---- Chart 2: share price vs. consensus EPS and P/E
    res = price_eps_pe_chart(
        f"{out}/MSFT_price_eps_pe.png", df, "Microsoft",
        "MSFT: share price vs. consensus earnings and valuation",
        source_line("Bloomberg", P["asof"], "MSFT US Equity, weekly", "BEst 12m-forward consensus",
                    "40-week simple MA", "Log scale",
                    "P/E shaded above (orange) / below (blue) its 2005-26 average"),
        ccy=P["ccy"], price_lbl=(10, -16), eps_lbl=(10, 10))   # EPS line ends above the price line
    crop_for_pdf(f"{out}/MSFT_price_eps_pe.png", f"{out}/c2_crop.png", "price_eps_pe")
    print(res)


if __name__ == "__main__":
    main()
