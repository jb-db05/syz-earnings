"""Epiroc Q3 2026: data -> charts (standalone PNGs with header/footnote + PDF crops)."""
import sys
sys.path.insert(0, "/home/claude")
import contextlib
import matplotlib.axes
import pandas as pd
import syz_charts
from syz_charts import setup_fonts, price_eps_pe_chart, bar_chart, crop_for_pdf, source_line

PARAMS = {
    "xlsx": "EPIROC.xlsx",  # Bloomberg daily export (not in the repository)
    "ticker": "EPI A", "ccy": "SEK",
    "window_start": "2018-06-18",          # listing date, first consensus EPS
    "asof": "28 Oct 2026",
    # release 28 Oct 10:30 UTC; reaction SEK 239.20 vs. 252.00 close at 13:27 GMT (StreetAccount)
    "prev_close": 252.00, "reaction_price": 239.20, "reaction_date": "28 October 2026", "market_pct": None,
    # surprises vs. consensus in % (orders consensus from analyst first takes; EPS basic vs. adjusted consensus)
    "c1_labels": ["Orders\nvs. consensus", "Revenue\nvs. consensus", "Adjusted EBIT\nvs. consensus",
                  "EPS\nvs. consensus"],
    "c1_values": [(17467 / 17742 - 1) * 100, (16775 / 17289 - 1) * 100, (3426 / 3497 - 1) * 100,
                  (2.00 / 2.14 - 1) * 100],
}


def load_daily_to_weekly(path):
    """Bloomberg daily export (Date | Last Price | BEst P/E | BEst EPS | SMAVG(40) | SMAVG(200)), newest first,
    all in SEK. Weekly Friday closes; the 40-week MA is computed on the weekly closes."""
    df = pd.read_excel(path).dropna(how="all")
    cols = {c: c.lower() for c in df.columns}
    pick = lambda *keys: next(c for c, l in cols.items() if all(k in l for k in keys))
    d = pd.DataFrame({"date": pd.to_datetime(df[pick("date")]),
                      "price": pd.to_numeric(df[pick("last price")], errors="coerce"),
                      "eps": pd.to_numeric(df[pick("best eps")], errors="coerce"),
                      "pe": pd.to_numeric(df[pick("p/e")], errors="coerce")}).sort_values("date").set_index("date")
    w = d.resample("W-FRI").last().dropna(subset=["price", "pe"])
    w.index = [min(i, d.index[-1]) for i in w.index]          # last, partial week dated at the last row
    w["ma40"] = w["price"].rolling(40).mean()
    return w.rename_axis("date").reset_index()


_log_ticks_kit = syz_charts._log_ticks


def _log_ticks_dense(ax, lo, hi, subs=(1, 2, 5)):
    """EPS spans less than one decade: denser ladder so the axis gets 3+ ticks."""
    _log_ticks_kit(ax, lo, hi, subs=(1, 2, 3, 4, 5, 6, 8) if hi / lo < 5 else subs)


@contextlib.contextmanager
def chart_tweaks(swap_labels):
    """Optional swap of the kit's (10, 10) / (10, -22) end-label offsets, plus the denser log ladder."""
    orig = matplotlib.axes.Axes.annotate
    swap = {(10, 10): (10, -22), (10, -22): (10, 10)} if swap_labels else {}
    swap[(10, -4)] = (10, -16)          # P/E end label sits on its average line: move it below

    def annotate(self, text, xy, *a, **kw):
        if kw.get("xytext") in swap:
            kw["xytext"] = swap[kw["xytext"]]
        return orig(self, text, xy, *a, **kw)
    matplotlib.axes.Axes.annotate = annotate
    syz_charts._log_ticks = _log_ticks_dense
    try:
        yield
    finally:
        matplotlib.axes.Axes.annotate = orig
        syz_charts._log_ticks = _log_ticks_kit


def main(swap_labels=False):
    setup_fonts()
    df = load_daily_to_weekly(PARAMS["xlsx"])
    df = df[df["date"] >= PARAMS["window_start"]].reset_index(drop=True)
    with chart_tweaks(swap_labels):
        stats = price_eps_pe_chart(
            "EPI_price_eps_pe.png", df, "EPI A", "EPI A: share price vs. consensus earnings and valuation",
            source_line("Bloomberg", PARAMS["asof"], "EPIA SS, weekly", "BEst 12m-forward consensus",
                        "40-week simple MA", "Log scale", "P/E shaded vs. its 2018-26 average",
                        "Last price 28 Oct intraday"),
            ccy=PARAMS["ccy"])
    crop_for_pdf("EPI_price_eps_pe.png", "c2_crop.png", "price_eps_pe")

    bar_chart("EPI_q3_surprise.png", PARAMS["c1_labels"], PARAMS["c1_values"],
              "EPI A: Q3 2026 vs. consensus", "Surprise in %",
              source_line("Bloomberg, company filings", PARAMS["asof"],
                          "Consensus: orders SEK 17.74bn, revenue SEK 17.29bn, adj. EBIT SEK 3.50bn, adj. EPS SEK 2.14",
                          "Orders consensus from analyst first takes"),
              ylabel="% vs. consensus")
    crop_for_pdf("EPI_q3_surprise.png", "c1_crop.png", "bar")
    print({k: round(v, 3) if isinstance(v, float) else v for k, v in stats.items()})
    print([round(v, 1) for v in PARAMS["c1_values"]], "reaction %.1f%%" % ((PARAMS["reaction_price"] / PARAMS["prev_close"] - 1) * 100))


if __name__ == "__main__":
    main(swap_labels="--no-swap" not in sys.argv)   # EPS ends above the price: swap by default
