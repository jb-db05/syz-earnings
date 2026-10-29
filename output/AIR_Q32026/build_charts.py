"""build_charts.py: Airbus 9M 2026 Earnings update charts (Syz chart kit)."""
import sys
sys.path.insert(0, "/home/claude")
import pandas as pd
from syz_charts import setup_fonts, load_bloomberg_sheet, price_eps_pe_chart, bar_chart, crop_for_pdf, source_line

PARAMS = {
    "xlsx": "/root/.claude/uploads/d22a55a6-7c43-5cbc-aecb-63aca74aa440/098a70b9-LLOYS_AIRBUS_STM_1.xlsx",
    "sheet": "AIR FP",
    "out": "/home/claude/air",
    "ticker": "AIR", "ccy": "EUR", "eps_ccy": "EUR", "asof": "29 Oct 2026",
    "window_start": None,                       # first consensus EPS row (2005); EPS never negative
    "prev_results": "2026-07-31",               # week of the H1 2026 results (29 Jul 2026)
    "prev_close": 191.92,                       # 28 Oct 2026 close, before the release (after the close)
    "reaction_pct": 3.3, "reaction_date": "29 Oct 2026 (close)", "market_pct": 0.8,   # Stoxx Europe 600, 29 Oct
    # Chart 1: surprise vs. pre-results consensus, % (reported / consensus - 1)
    # Q3 lines vs. Q3 consensus; FY26 lines = maintained guide vs. FY26 consensus
    "c1_labels": ["Q3 revenue", "Q3 EBIT adj.", "FY deliveries", "FY EBIT adj.", "FY free cash flow"],
    "c1_reported": [17.469, 1768.0, 870, 7.5, 4.5],
    "c1_consensus": [18.38, 1751.0, 866, 7.69, 4.8],
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
        "pe_week_before": df["pe"].iloc[-2], "pe_year_ago": yago["pe"], "pre_results_vs_peak_pct": (P["prev_close"] / df["price"].max() - 1) * 100,
        "price_12m_pct": (last["price"] / yago["price"] - 1) * 100,
        "eps_12m_pct": (last["eps"] / yago["eps"] - 1) * 100,
        "price_since_prev_pct": (last["price"] / prev["price"] - 1) * 100,
        "eps_since_prev_pct": (last["eps"] / prev["eps"] - 1) * 100,
        "price_vs_ma_pct": (last["price"] / last["ma40"] - 1) * 100,
        "record_price": (df["price"].max(), f"{df.loc[df['price'].idxmax(), 'date']:%d %b %Y}"),
        "week_before_vs_peak_pct": (df["price"].iloc[-2] / df["price"].max() - 1) * 100,
        "eps_vs_2019_peak_pct": (last["eps"] / df[df["date"].dt.year == 2019]["eps"].max() - 1) * 100,
        "pe_avg_5y": df[df["date"] > last["date"] - pd.Timedelta(days=5 * 365)]["pe"].mean(),
        "pe_avg_10y": df[df["date"] > last["date"] - pd.Timedelta(days=10 * 365)]["pe"].mean(),
        "pe_after_10pct_upgrade": last["pe"] / 1.10,
        "surprises_pct": [round((r / c - 1) * 100, 1) for r, c in zip(P["c1_reported"], P["c1_consensus"])],
    }
    stats["pe_premium_pct"] = (stats["pe"] / stats["pe_avg_all"] - 1) * 100
    for k, v in stats.items():
        print(f"{k:24s} {v}")

    # ---- Chart 1: surprise vs. consensus by line
    bar_chart(f"{out}/AIR_results_vs_consensus.png", P["c1_labels"], stats["surprises_pct"],
              "AIR: Q3 2026 results and FY26 guide vs. consensus",
              "Q3 reported vs. Q3 consensus · maintained FY26 guide vs. FY26 consensus, %",
              source_line("Bloomberg, company filings", P["asof"],
                          "Consensus: pre-results analyst estimates",
                          "Free cash flow before customer financing"),
              ylabel="Surprise vs. consensus (%)")
    crop_for_pdf(f"{out}/AIR_results_vs_consensus.png", f"{out}/c1_crop.png", "bar")

    # ---- Chart 2: share price vs. consensus EPS and P/E
    res = price_eps_pe_chart(
        f"{out}/AIR_price_eps_pe.png", df, "Airbus",
        "AIR: share price vs. consensus earnings and valuation",
        source_line("Bloomberg", P["asof"], "AIR FP Equity, weekly", "BEst 12m-forward consensus",
                    "40-week simple MA", "Log scale", "P/E shaded above (orange) / below (blue) its 2005-26 average"),
        ccy=P["ccy"], eps_ccy=P["eps_ccy"], price_lbl=(10, -16), eps_lbl=(10, 10))   # EPS line ends above the price line
    crop_for_pdf(f"{out}/AIR_price_eps_pe.png", f"{out}/c2_crop.png", "price_eps_pe")
    print(res)


if __name__ == "__main__":
    main()
