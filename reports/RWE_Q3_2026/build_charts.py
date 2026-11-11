"""RWE Q3 2026 charts. python3 build_charts.py"""
import sys; sys.path.insert(0, "/home/claude/rwe")
from syz_charts import *
PARAMS = dict(
    xlsx="/root/.claude/uploads/d6e40b82-0167-56c5-a6e6-2a07b9bf16f6/c0e5e945-RWE.xlsx",
    ticker="RWE", asof="11 Nov 2026", window_start=None,
    reaction_pct=2.1, reaction_date="11 November 2026", market_pct=1.0,   # last Bloomberg row 59.34 vs 58.14 close on 10 Nov (web); DAX ~+1% (web)
    # Chart 1: adjusted net income, EUR m (9M 2025 derived from the reported +42.8%; consensus = company-collected poll)
    c1_labels=["9M 2025 reported", "9M 2026 consensus", "9M 2026 reported"], c1_values=[1293, 1709, 1846],
)
setup_fonts()
df = load_bloomberg_sheet(PARAMS["xlsx"]); df = df[df["eps"].notna()].reset_index(drop=True)
bar_chart("c1.png", PARAMS["c1_labels"], PARAMS["c1_values"],
          "RWE: 9M 2026 adjusted net income vs. consensus and prior year",
          "Adjusted net income, EUR m",
          source_line("company release and call", PARAMS["asof"], "Consensus: company-collected poll", "9M 2025 derived from the reported +42.8%"),
          colors=[BLUEB, BLUEB, ORANGE], fmt="{:,.0f}", zero_line=False)
st = price_eps_pe_chart("c2.png", df, "RWE", "RWE: share price vs. consensus earnings and valuation",
          source_line("Bloomberg", PARAMS["asof"], "RWE GY Equity, weekly", "BEst 12m-forward consensus", "40-week simple MA",
                      "Log scale", "P/E shaded above (orange) / below (blue) its 2014-26 average"))
print(st)
crop_for_pdf("c1.png", "c1_crop.png", "bar"); crop_for_pdf("c2.png", "c2_crop.png", "price_eps_pe")
from PIL import Image
for f in ["c1_crop.png", "c2_crop.png"]:
    w, h = Image.open(f).size; print(f, h / w)
