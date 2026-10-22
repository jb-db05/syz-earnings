"""build_charts.py: TXN Q3 2026 charts. Edit PARAMS for the next quarter."""
import sys; sys.path.insert(0, "/home/claude"); sys.path.insert(0, "/home/claude/txn")
import json, os
from syz_charts import *
from load import load_daily_as_weekly

PARAMS = {
    "xlsx": __import__("os").environ.get("TXN_XLSX", "TXN.xlsx"),   # Bloomberg daily export (not committed)
    "ticker": "TXN", "ccy": "USD", "asof": "22 Oct 2026",
    # reported vs. consensus (Bloomberg consensus, pre-results) and Q4 guide midpoints vs. consensus
    "surprise_labels": ["Revenue, %", "EPS, %", "Gross margin, pp", "Op. margin, pp",
                        "Q4 sales guide, %", "Q4 EPS guide, %"],
    "start": "2010-01-01",   # window starts after the 2008-09 EPS trough, which distorts the P/E scale
    "surprise_values": [(6.06 / 5.92 - 1) * 100, (2.62 / 2.41 - 1) * 100, 64.2 - 61.8, 47.5 - 44.6,
                        (6.05 / 5.73 - 1) * 100, (2.62 / 2.29 - 1) * 100],
}

setup_fonts()
w, _ = load_daily_as_weekly(PARAMS["xlsx"])
w = w[w["date"] >= PARAMS["start"]].reset_index(drop=True)
t, ccy = PARAMS["ticker"], PARAMS["ccy"]

bar_chart("c1.png", PARAMS["surprise_labels"], PARAMS["surprise_values"],
          f"{t}: Q3 2026 results and Q4 guidance vs. consensus",
          "Reported Q3 2026 and Q4 2026 guidance midpoints vs. Bloomberg consensus",
          source_line("Bloomberg, company filings", PARAMS["asof"], "Consensus: Bloomberg pre-results",
                      "Q4 guide at the midpoint of USD 5.8 to 6.3bn revenue and USD 2.45 to 2.79 EPS",
                      "Margins in percentage points"),
          fmt="{:+.1f}")
stats = price_eps_pe_chart("c2.png", w, t, f"{t}: share price vs. consensus earnings and valuation",
          source_line("Bloomberg", PARAMS["asof"], "TXN US Equity, weekly", "BEst 12m-forward consensus",
                      "40-week simple MA", "Log scale", "P/E shaded above (orange) / below (blue) its 2010-26 average"),
          ccy=ccy)
crop_for_pdf("c1.png", "c1_crop.png", "bar")
crop_for_pdf("c2.png", "c2_crop.png", "price_eps_pe")
json.dump(stats, open("stats.json", "w"), indent=1, default=float)
print(stats, [round(v, 2) for v in PARAMS["surprise_values"]])
