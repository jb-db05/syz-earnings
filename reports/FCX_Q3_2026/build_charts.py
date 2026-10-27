"""FCX Q3 2026: data -> charts (standalone PNGs with header/footnote + PDF crops)."""
import sys
sys.path.insert(0, "/home/claude")
import contextlib
import numpy as np
import pandas as pd
import matplotlib.axes
import syz_charts
from syz_charts import (setup_fonts, load_bloomberg_sheet, price_eps_pe_chart, bar_chart,
                        crop_for_pdf, source_line)

PARAMS = {
    "xlsx": "FCX_US.xlsx",  # Bloomberg weekly export (not in the repository)
    "ticker": "FCX", "ccy": "USD",
    # P/E on trough earnings exceeds 100x in 2009 and 2020: window starts after the Covid trough
    "window_start": "2021-01-01",
    "asof": "27 Oct 2026",
    # publication-day reaction: release before the open on 27 Oct; intraday (export) vs. 26 Oct close
    "prev_close": 65.16, "reaction_date": "27 October 2026", "market_pct": None,
    # surprises, favourable (+) / unfavourable (-)
    "c1_labels": ["Revenue\nvs. consensus", "Adjusted EPS\nvs. consensus", "Unit net cash cost\nvs. July estimate",
                  "2026 copper sales\nvs. July guide", "2027 copper sales\nvs. July guide", "2027 capex\nvs. July estimate"],
    "c1_values": [(7.55 / 7.36 - 1) * 100, (0.88 / 0.80 - 1) * 100, -(2.07 / 2.00 - 1) * 100, -2.0, -2.5,
                  -(5.2 / 4.8 - 1) * 100],
}


_log_ticks_kit = syz_charts._log_ticks


def _log_ticks_dense(ax, lo, hi, subs=(1, 2, 5)):
    """FCX EPS and price span less than one decade in the window: denser ladder so each axis gets 3+ ticks."""
    _log_ticks_kit(ax, lo, hi, subs=(1, 2, 3, 4, 5, 6, 8) if hi / lo < 5 else subs)


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
    syz_charts._log_ticks = _log_ticks_dense
    try:
        yield
    finally:
        matplotlib.axes.Axes.annotate = orig
        syz_charts._log_ticks = _log_ticks_kit


def main():
    setup_fonts()
    df = load_bloomberg_sheet(PARAMS["xlsx"])
    df = df[df["eps"].notna() & (df["date"] >= PARAMS["window_start"])].reset_index(drop=True)
    PARAMS["reaction_pct"] = (df["price"].iloc[-1] / PARAMS["prev_close"] - 1) * 100

    with swapped_end_labels():
        stats = price_eps_pe_chart(
            "FCX_price_eps_pe.png", df, "FCX", "FCX: share price vs. consensus earnings and valuation",
            source_line("Bloomberg", PARAMS["asof"], "FCX US, weekly", "BEst 12m-forward consensus",
                        "40-week simple MA", "Log scale", "P/E shaded above (orange) / below (blue) its 2021-26 average",
                        "Last price intraday 27 Oct"),
            ccy=PARAMS["ccy"])
    crop_for_pdf("FCX_price_eps_pe.png", "c2_crop.png", "price_eps_pe")

    bar_chart("FCX_q3_surprise.png", PARAMS["c1_labels"], PARAMS["c1_values"],
              "FCX: Q3 2026 vs. consensus and vs. the July guidance",
              "Favourable (+) / unfavourable (-) in %; cost and capex shown as unfavourable when above estimate",
              source_line("Bloomberg, company filings", PARAMS["asof"],
                          "Consensus: EPS USD 0.80, revenue USD 7.36bn (pre-results)",
                          "Copper sales revisions as stated by management (approx.)"),
              ylabel="% vs. reference")
    crop_for_pdf("FCX_q3_surprise.png", "c1_crop.png", "bar")

    print({k: round(v, 3) if isinstance(v, float) else v for k, v in stats.items()})
    print("reaction %.2f%%" % PARAMS["reaction_pct"], [round(v, 1) for v in PARAMS["c1_values"]])


if __name__ == "__main__":
    main()
