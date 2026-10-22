"""build_charts.py: Atlas Copco Q3 2026 charts (Chart 1 organic orders by business area, Chart 2 price vs. EPS and P/E)."""
import sys, json
sys.path.insert(0, "/home/claude/atco")
from syz_charts import *
from data import load

PARAMS = {
    "ticker": "ATCO", "ccy": "SEK", "asof": "22 Oct 2026", "out": "/home/claude/atco",
    # organic order growth y/y, Q3 2026 (company, earnings call 22 Oct 2026); consensus = pre-results analyst expectation
    "c1_labels": ["Group\nconsensus", "Group\nreported", "Compressor\nTechnique", "Vacuum\nTechnique",
                  "Industrial\nTechnique", "Power\nTechnique"],
    "c1_values": [20, 25, 6, 82, 12, 13],
}

setup_fonts()
P = PARAMS
bar_chart(f"{P['out']}/c1.png", P["c1_labels"], P["c1_values"],
          "ATCO: Q3 2026 organic order growth by business area",
          "Organic growth in orders received, Q3 2026 vs. Q3 2025, %",
          source_line("company reports, Bloomberg", P["asof"], "Group consensus: pre-results analyst expectations",
                      "Vacuum Technique driven by semiconductor equipment demand"),
          colors=[GREY, ORANGE, BLUEB, BLUEB, BLUEB, BLUEB], fmt="{:.0f}%", zero_line=True)
d, w = load()
stats = price_eps_pe_chart(f"{P['out']}/c2.png", w, "Atlas Copco",
          "ATCO: share price vs. consensus earnings and valuation",
          source_line("Bloomberg", P["asof"], "ATCO A SS Equity, weekly", "BEst 12m-forward consensus",
                      "40-week simple MA", "Log scale", "P/E shaded above (orange) / below (blue) its 2005-26 average"),
          ccy=P["ccy"])
crop_for_pdf(f"{P['out']}/c1.png", f"{P['out']}/c1_crop.png", "bar")
crop_for_pdf(f"{P['out']}/c2.png", f"{P['out']}/c2_crop.png", "price_eps_pe")
from PIL import Image
for k in ["c1_crop", "c2_crop"]:
    im = Image.open(f"{P['out']}/{k}.png"); stats[k + "_aspect"] = im.size[1] / im.size[0]
print(json.dumps(stats, indent=1, default=float))
json.dump(stats, open(f"{P['out']}/stats.json", "w"), default=float)
