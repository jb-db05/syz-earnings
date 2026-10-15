"""build_charts.py: TSMC (TSM US) Q3 2026 earnings update charts. Parameterised for the next quarter via PARAMS."""
import sys
sys.path.insert(0, "/home/claude")
import matplotlib.pyplot as plt
import syz_charts as sc

PARAMS = {
    "xlsx": "/home/claude/data/TSM.xlsx",
    "ticker": "TSM",
    "asof": "15 Oct 2026",
    "c2_start": "2010-01-01",
    "out": "/home/claude/out",
    # Chart 1: surprise vs. consensus (revenue and gross-margin consensus approximate, per analyst first takes)
    "c1_labels": ["Q3 revenue", "Q3 EPS", "Q3 gross margin", "Q4 revenue guide"],
    "c1_values": [3.0, (29.43 / 28.67 - 1) * 100, 66.4 - 67.0, 6.5],
}


class SurpriseFmt:
    """Percent for revenue/EPS/guide, percentage points for the margin line (the only negative bar)."""
    def format(self, v):
        return f"{v:+.1f}pp" if v < 0 else f"{v:+.1f}%"


def main(p=PARAMS):
    import os
    os.makedirs(p["out"], exist_ok=True)
    sc.setup_fonts()
    df = sc.load_bloomberg_sheet(p["xlsx"])
    df = df[df["eps"].notna()].reset_index(drop=True)

    # Chart 1
    c1 = f"{p['out']}/TSM_chart1_surprises.png"
    sc.bar_chart(c1, p["c1_labels"], p["c1_values"],
                 "TSM: Q3 2026 results and Q4 guide vs. consensus",
                 "Surprise vs. pre-results consensus, % (gross margin in percentage points)",
                 sc.source_line("Bloomberg, company filings, analyst research notes", p["asof"],
                                "Revenue and gross-margin consensus approximate",
                                "Q4 guide midpoint USD 53.3bn vs. prior consensus, middle of the 5-8% range"),
                 fmt=SurpriseFmt(), ylabel="Surprise vs. consensus")
    sc.crop_for_pdf(c1, f"{p['out']}/c1_crop.png", "bar")

    # Chart 2: USD only. Bloomberg's BEst EPS for TSM US is in TWD per ADR; restate it in USD per ADR with the
    # exchange rate Bloomberg itself uses in the P/E (EPS_USD = price / P/E), so price, EPS and P/E stay consistent
    c2 = f"{p['out']}/TSM_chart2_price_eps_pe.png"
    d2 = df[df["date"] >= p["c2_start"]].dropna(subset=["pe"]).copy()
    d2["eps"] = d2["price"] / d2["pe"]
    d2 = d2.reset_index(drop=True)
    stats = sc.price_eps_pe_chart(
        c2, d2, "TSM", "TSM: share price vs. consensus earnings and valuation",
        sc.source_line("Bloomberg", p["asof"], "TSM US Equity (ADR), weekly", "BEst 12m-forward consensus EPS per ADR in USD",
                       "40-week simple MA", "Log scale",
                       "P/E shaded above (orange) / below (blue) its 2010-26 average"),
        ccy="USD")
    sc.crop_for_pdf(c2, f"{p['out']}/c2_crop.png", "price_eps_pe")
    print(stats)
    return stats


if __name__ == "__main__":
    main()
