"""PANW fiscal Q1 2027 charts. python3 build_charts.py"""
import sys; sys.path.insert(0, "/home/claude"); sys.path.insert(0, "/home/claude/panw")
from syz_charts import *
from load import load   # mixed Excel-serial / datetime dates in this export

PARAMS = dict(
    ticker="PANW", name="Palo Alto Networks", ccy="USD", asof="19 Nov 2026",
    reaction_pct=5.4, reaction_date="19 Nov 2026 (intraday)", market_pct=None,
    # surprises, % : Q1 vs consensus (rev 3.44 vs 3.31, EPS 1.05 vs 0.97), NGS ARR vs top of guide (9.73 vs 9.56),
    # FY27 guide midpoints vs prior guide midpoints (rev 14.545 vs 14.15, NGS ARR 11.5 vs 11.125, EPS 4.28 vs 4.175)
    window_start="2016-01-01",
    c1_labels=["Q1 revenue", "Q1 EPS", "Q1 NGS ARR", "FY27 revenue", "FY27 NGS ARR", "FY27 EPS"],
    c1_values=[(3.44/3.31-1)*100, (1.05/0.97-1)*100, (9.73/9.56-1)*100,
               (14.545/14.15-1)*100, (11.50/11.125-1)*100, (4.28/4.175-1)*100],
)
setup_fonts()
P = PARAMS
bar_chart("/home/claude/c1.png", P["c1_labels"], P["c1_values"],
          "PANW: fiscal Q1 2027 beat and FY27 guidance raise",
          "Q1 vs consensus (revenue, EPS) and vs top of guide (NGS ARR); FY27 guide midpoints vs prior guide, %",
          source_line("company filings, Bloomberg consensus", P["asof"], "EPS and operating figures non-GAAP",
                      "NGS ARR: next-generation security annualised recurring revenue"),
          ylabel="Surprise, %")
crop_for_pdf("/home/claude/c1.png", "/home/claude/c1_crop.png", "bar")

df = load(); df = df[df["eps"].notna()]
# window from 2016: the post-IPO years at 100-130x forward earnings distort the long-run average and collide with the legend
df = df[df["date"] >= P["window_start"]].reset_index(drop=True)
out = price_eps_pe_chart("/home/claude/c2.png", df, P["name"],
    "PANW: share price vs. consensus earnings and valuation",
    source_line("Bloomberg", P["asof"], "PANW US Equity, weekly, split-adjusted", "BEst 12m-forward consensus",
                "40-week simple MA", "Log scale", "P/E shaded vs. its 2016-26 average", "Last point intraday"),
    ccy="USD", price_lbl=(10, -16), eps_lbl=(10, 10))
crop_for_pdf("/home/claude/c2.png", "/home/claude/c2_crop.png", "price_eps_pe")
print({k: round(v, 2) if isinstance(v, float) else v for k, v in out.items()})
print([round(v, 1) for v in P["c1_values"]])
