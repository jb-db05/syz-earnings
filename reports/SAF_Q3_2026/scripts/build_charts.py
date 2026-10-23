"""build_charts.py: Safran Q3 2026 charts (Chart 1 surprises vs. consensus, Chart 2 price vs. EPS and P/E)."""
import sys, json
sys.path.insert(0, "/home/claude/saf")
from syz_charts import *
from data import load

PARAMS = {
    "ccy": "EUR", "asof": "23 Oct 2026", "out": "/home/claude/saf",
    # % vs. consensus. Q3 lines: company-compiled consensus; FY26 guide midpoints vs. consensus (analyst first takes)
    "c1_labels": ["Q3 group\nrevenue", "Q3 Equipment\n& Defense", "Q3 Aircraft\nInteriors", "FY26 operating\nincome guide",
                  "FY26 free cash\nflow guide"],
    "c1_values": [9003 / 8990 * 100 - 100, 3620 / 3530 * 100 - 100, 751 / 761 * 100 - 100, -2.1, -1.8],
}

setup_fonts()
P = PARAMS
bar_chart(f"{P['out']}/c1.png", P["c1_labels"], P["c1_values"],
          "SAF: Q3 2026 revenue and 2026 guidance vs. consensus",
          "Reported Q3 revenue and confirmed FY 2026 guidance (midpoint) vs. consensus, %",
          source_line("company, Bloomberg", P["asof"], "Q3: company-compiled consensus",
                      "FY26: guidance midpoints vs. consensus per analyst first takes"),
          fmt="{:+.1f}%")
d, w = load()
stats = price_eps_pe_chart(f"{P['out']}/c2.png", w, "Safran",
          "SAF: share price vs. consensus earnings and valuation",
          source_line("Bloomberg", P["asof"], "SAF FP Equity, weekly", "BEst 12m-forward consensus",
                      "40-week simple MA", "Log scale", "P/E shaded above (orange) / below (blue) its 2005-26 average"),
          ccy=P["ccy"])
crop_for_pdf(f"{P['out']}/c1.png", f"{P['out']}/c1_crop.png", "bar")
crop_for_pdf(f"{P['out']}/c2.png", f"{P['out']}/c2_crop.png", "price_eps_pe")
from PIL import Image
for k in ["c1_crop", "c2_crop"]:
    im = Image.open(f"{P['out']}/{k}.png"); stats[k + "_aspect"] = im.size[1] / im.size[0]
print(json.dumps(stats, indent=1, default=float))
json.dump(stats, open(f"{P['out']}/stats.json", "w"), default=float)
