"""build_charts.py: STMicroelectronics Q3 2026 Earnings update charts (Syz chart kit)."""
import sys
sys.path.insert(0, "/home/claude")
import pandas as pd
from syz_charts import setup_fonts, load_bloomberg_sheet, price_eps_pe_chart, bar_chart, crop_for_pdf, source_line

PARAMS = {
    "xlsx": "/root/.claude/uploads/d22a55a6-7c43-5cbc-aecb-63aca74aa440/098a70b9-LLOYS_AIRBUS_STM_1.xlsx",
    "sheet": "STMMI IM",
    "out": "/home/claude/stm",
    "ticker": "STMMI", "ccy": "EUR", "eps_ccy": "USD", "asof": "29 Oct 2026",
    "window_start": "2014-01-01",               # EPS negative in 2009, P/E above 100x in 2012-13
    "prev_results": "2026-07-24",               # week of the Q2 2026 results (23 Jul 2026)
    "prev_close": 43.37,                        # 28 Oct 2026 close (Paris), before the release
    "reaction_pct": 1.9, "reaction_date": "29 Oct 2026 (close)", "market_pct": 0.8   # Stoxx Europe 600 and Stoxx Europe 600 Technology, 29 Oct,
    # Chart 1: surprise vs. pre-results consensus, % (reported / consensus - 1)
    "c1_labels": ["Revenue", "Op. income (adj.)", "Adj. EPS", "Q4 revenue guide", "2026 revenue"],
    "c1_reported": [3.757, 429.0, 0.37, 4.15, 14.5],
    "c1_consensus": [3.73, 400.5, 0.41, 4.12, 14.41],
}


def main():
    setup_fonts()
    P, out = PARAMS, PARAMS["out"]
    df = load_bloomberg_sheet(P["xlsx"], sheet=P["sheet"])
    df = df[df["eps"].notna()].reset_index(drop=True)
    if P["window_start"]:
        df = df[df["date"] >= P["window_start"]].reset_index(drop=True)

    # ---- numbers quoted in the text
    last = df.iloc[-1]
    yago = df.iloc[(df["date"] - (last["date"] - pd.Timedelta(days=364))).abs().argsort().iloc[0]]
    prev = df[df["date"] <= P["prev_results"]].iloc[-1]
    stats = {
        "window": f"{df['date'].iloc[0]:%d %b %Y} to {last['date']:%d %b %Y}",
        "price": last["price"], "eps": last["eps"], "pe": last["pe"], "ma40": last["ma40"],
        "move_vs_prev_close_pct": (last["price"] / P["prev_close"] - 1) * 100,
        "pe_avg_all": df["pe"].mean(),
        "pe_avg_1y": df[df["date"] > last["date"] - pd.Timedelta(days=365)]["pe"].mean(),
        "pe_peak": (df["pe"].max(), f"{df.loc[df['pe'].idxmax(), 'date']:%b %Y}"),
        "pe_week_before": df["pe"].iloc[-2],
        "price_12m_pct": (last["price"] / yago["price"] - 1) * 100,
        "eps_12m_pct": (last["eps"] / yago["eps"] - 1) * 100,
        "price_since_prev_pct": (last["price"] / prev["price"] - 1) * 100,
        "eps_since_prev_pct": (last["eps"] / prev["eps"] - 1) * 100,
        "price_vs_ma_pct": (last["price"] / last["ma40"] - 1) * 100,
        "record_price": (df["price"].max(), f"{df.loc[df['price'].idxmax(), 'date']:%d %b %Y}"),
        "week_before_vs_peak_pct": (df["price"].iloc[-2] / df["price"].max() - 1) * 100,
        "eps_vs_2023_peak_pct": (last["eps"] / df[df["date"].dt.year == 2023]["eps"].max() - 1) * 100,
        "pe_after_10pct_upgrade": last["pe"] / 1.10,
        "surprises_pct": [round((r / c - 1) * 100, 1) for r, c in zip(P["c1_reported"], P["c1_consensus"])],
    }
    stats["pe_premium_pct"] = (stats["pe"] / stats["pe_avg_all"] - 1) * 100
    for k, v in stats.items():
        print(f"{k:24s} {v}")

    # ---- Chart 1: surprise vs. consensus by line
    bar_chart(f"{out}/STMMI_results_vs_consensus.png", P["c1_labels"], stats["surprises_pct"],
              "STMMI: Q3 2026 results and Q4 guide vs. consensus",
              "Reported vs. pre-results consensus, % · Q4 guide at the midpoint · 2026 revenue implied by the Q4 guide",
              source_line("Bloomberg, company filings", P["asof"],
                          "Consensus: pre-results analyst estimates",
                          "Adj.: non-GAAP, excluding impairment, restructuring and purchase price allocation"),
              ylabel="Surprise vs. consensus (%)")
    crop_for_pdf(f"{out}/STMMI_results_vs_consensus.png", f"{out}/c1_crop.png", "bar")

    # ---- Chart 2: share price vs. consensus EPS and P/E
    res = price_eps_pe_chart(
        f"{out}/STMMI_price_eps_pe.png", df, "STMicroelectronics",
        "STMMI: share price vs. consensus earnings and valuation",
        source_line("Bloomberg", P["asof"], "STMMI IM Equity, weekly", "BEst 12m-forward consensus (USD)",
                    "40-week simple MA", "Log scale", "P/E shaded above (orange) / below (blue) its 2014-26 average"),
        ccy=P["ccy"], eps_ccy=P["eps_ccy"])
    crop_for_pdf(f"{out}/STMMI_price_eps_pe.png", f"{out}/c2_crop.png", "price_eps_pe")
    print(res)


if __name__ == "__main__":
    main()
