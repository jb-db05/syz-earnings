"""build_charts.py: ABB Q3 2026 earnings update charts. Update PARAMS for the next quarter."""
import sys
sys.path.insert(0, "/home/claude")
import pandas as pd
import syz_charts as sc

PARAMS = {
    "xlsx": "/root/.claude/uploads/2cb30792-c374-5f3b-89e1-e5a7b4b4f3e9/f74888e0-Copy_of_ABB_Bloomberg.xlsx",
    "ticker": "ABBN",
    "asof": "20 Oct 2026",
    "out": "/home/claude/abb",
    # Chart 1: Q3 2026 reported vs. pre-results consensus, %
    "c1_labels": ["Orders", "Electrification\norders", "Automation\norders", "Revenue",
                  "Operational\nEBITA", "Basic EPS", "Free cash\nflow"],
    "c1_values": [
        8.0,                         # orders USD 12.06bn, c.8% above consensus
        16.0,                        # Electrification orders c.16% above consensus
        -9.0,                        # Automation orders c.9% below consensus
        (9.70 / 9.74 - 1) * 100,     # revenue USD 9.70bn vs. 9.74bn consensus
        2.0,                         # operational EBITA c.2% above consensus
        (0.65 / 0.78 - 1) * 100,     # basic EPS USD 0.65 vs. midpoint of 0.77-0.79
        29.0,                        # free cash flow USD 1.58bn, c.29% above consensus
    ],
}


def load_weekly(path):
    """This export is daily with SMAVG columns: resample to the last trading day of each week and
    compute the 40-week simple MA on the weekly closes. EPS starts the window."""
    raw = pd.read_excel(path)
    cols = {c: c.lower() for c in raw.columns}
    pick = lambda *k: next(c for c, l in cols.items() if all(x in l for x in k))
    d = pd.DataFrame({"date": pd.to_datetime(raw[pick("date")]),
                      "price": pd.to_numeric(raw[pick("last price")], errors="coerce"),
                      "eps": pd.to_numeric(raw[pick("best eps")], errors="coerce"),
                      "pe": pd.to_numeric(raw[pick("best p/e")], errors="coerce")})
    d = d.dropna(subset=["date"]).sort_values("date")
    d = d[d["eps"].notna()]
    w = d.groupby(d["date"].dt.to_period("W-FRI")).last().reset_index(drop=True)
    w["ma40"] = w["price"].rolling(40).mean()
    return w


if __name__ == "__main__":
    P = PARAMS
    sc.setup_fonts()
    out = P["out"]

    # Chart 1
    c1 = f"{out}/ABBN_q3_vs_consensus.png"
    sc.bar_chart(c1, P["c1_labels"], P["c1_values"],
                 f"{P['ticker']}: Q3 2026 results vs. consensus",
                 "Reported vs. pre-results consensus, %",
                 sc.source_line("Bloomberg, company filings", P["asof"],
                                "Pre-results consensus", "EPS vs. midpoint of USD 0.77-0.79",
                                "Segment and EBITA surprises approximate"),
                 fmt="{:+.1f}%", ylim=(-22, 34))
    sc.crop_for_pdf(c1, f"{out}/c1_crop.png", "bar")

    # Chart 2
    w = load_weekly(P["xlsx"])
    c2 = f"{out}/ABBN_price_eps_pe.png"
    stats = sc.price_eps_pe_chart(
        c2, w, "ABB", f"{P['ticker']}: share price vs. consensus earnings and valuation",
        sc.source_line("Bloomberg", P["asof"], "ABBN SW Equity, weekly", "BEst EPS, current fiscal year",
                       "40-week simple MA", "Log scale", "P/E shaded vs. its 2006-26 average"),
        ccy="CHF", eps_ccy="USD", eps_desc="Consensus EPS, current fiscal year",
        p1_title="Share price and consensus EPS, current fiscal year (log scale)",
        p2_title="Consensus P/E, current fiscal year",
        pe_label="Consensus P/E", price_off=(10, -16), eps_off=(10, 6))
    sc.crop_for_pdf(c2, f"{out}/c2_crop.png", "price_eps_pe")
    print(stats)
