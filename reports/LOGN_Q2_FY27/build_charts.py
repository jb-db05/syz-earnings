"""Logitech Q2 FY27: data -> charts (standalone PNGs with header/footnote + PDF crops)."""
import sys
sys.path.insert(0, "/home/claude")
import contextlib
import matplotlib.axes
import pandas as pd
from syz_charts import setup_fonts, price_eps_pe_chart, bar_chart, crop_for_pdf, source_line

PARAMS = {
    "xlsx": "Logitech_Shareprice.xlsx",  # Bloomberg daily export (not in the repository)
    "ticker": "LOGN", "ccy": "CHF",
    # P/E reaches 59x in 2010 on post-crisis earnings: window starts in 2015
    "window_start": "2015-01-01",
    "asof": "28 Oct 2026",
    # results published after the SIX close on 27 Oct: reaction day is 28 Oct (export price, early trading)
    "reaction_date": "28 October 2026", "market_pct": None,
    # surprises in % (sales and EPS vs. consensus; Q2 operating income vs. guide midpoint USD 197.5m)
    "c1_labels": ["Q2 sales\nvs. consensus", "Q2 EPS\nvs. consensus", "Q2 operating income\nvs. guide midpoint",
                  "Q3 sales guide\nvs. consensus", "Q3 operating income\nguide vs. consensus"],
    "c1_values": [0.6,  # USD 1.22bn reported, 0.6% above consensus (stated in the results summary)
                  (1.51 / 1.31 - 1) * 100, (231 / 197.5 - 1) * 100,
                  (1395 / 1317.5 - 1) * 100, -0.7],
}


def load_daily_to_weekly(path):
    """Bloomberg daily export (Date | Last Price | BEst EPS | BEst P/E | SMAVG(40) | SMAVG(200)), newest first.
    BEst EPS is in USD while the price is in CHF: EPS is taken in CHF as price / P/E, consistent with the
    Bloomberg P/E. Weekly Friday closes; the 40-week MA is computed on the weekly closes."""
    df = pd.read_excel(path).dropna(how="all")
    cols = {c: c.lower() for c in df.columns}
    pick = lambda *keys: next(c for c, l in cols.items() if all(k in l for k in keys))
    d = pd.DataFrame({"date": pd.to_datetime(df[pick("date")]),
                      "price": pd.to_numeric(df[pick("last price")], errors="coerce"),
                      "pe": pd.to_numeric(df[pick("p/e")], errors="coerce")}).sort_values("date").set_index("date")
    w = d.resample("W-FRI").last().dropna()
    w.index = [min(i, d.index[-1]) for i in w.index]          # last, partial week dated at the last row
    w["ma40"] = w["price"].rolling(40).mean()
    w["eps"] = w["price"] / w["pe"]
    return w.rename_axis("date").reset_index()


@contextlib.contextmanager
def swapped_end_labels():
    """EPS ends above the price here: swap the kit's (10, 10) / (10, -22) end-label offsets to avoid a collision."""
    orig = matplotlib.axes.Axes.annotate
    swap = {(10, 10): (10, -22), (10, -22): (10, 10)}

    def annotate(self, text, xy, *a, **kw):
        if kw.get("xytext") in swap:
            kw["xytext"] = swap[kw["xytext"]]
        return orig(self, text, xy, *a, **kw)
    matplotlib.axes.Axes.annotate = annotate
    try:
        yield
    finally:
        matplotlib.axes.Axes.annotate = orig


def main():
    setup_fonts()
    df = load_daily_to_weekly(PARAMS["xlsx"])
    df = df[df["date"] >= PARAMS["window_start"]].reset_index(drop=True)

    with swapped_end_labels():
        stats = price_eps_pe_chart(
            "LOGN_price_eps_pe.png", df, "LOGN", "LOGN: share price vs. consensus earnings and valuation",
            source_line("Bloomberg", PARAMS["asof"], "LOGN SW, weekly", "BEst 12m-forward consensus in CHF (price / P/E)",
                        "40-week simple MA", "Log scale", "P/E shaded vs. its 2015-26 average", "Last price 28 Oct, early trading"),
            ccy=PARAMS["ccy"])
    crop_for_pdf("LOGN_price_eps_pe.png", "c2_crop.png", "price_eps_pe")

    bar_chart("LOGN_q2_surprise.png", PARAMS["c1_labels"], PARAMS["c1_values"],
              "LOGN: Q2 FY27 results and Q3 guide vs. consensus",
              "Surprise in %; guide = midpoint of the range",
              source_line("Bloomberg, company filings", PARAMS["asof"],
                          "Consensus: Q2 sales USD 1,210.7m, EPS USD 1.31; Q3 sales USD 1,317.5m",
                          "Q3 operating income vs. consensus from analyst first takes"),
              ylabel="% vs. reference")
    crop_for_pdf("LOGN_q2_surprise.png", "c1_crop.png", "bar")
    print({k: round(v, 3) if isinstance(v, float) else v for k, v in stats.items()})
    print([round(v, 1) for v in PARAMS["c1_values"]], "eps range", df.eps.min(), df.eps.max(), df.price.min(), df.price.max())


if __name__ == "__main__":
    main()
