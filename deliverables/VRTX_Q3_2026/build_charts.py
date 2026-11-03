"""build_charts.py: Vertex (VRTX) Q3 2026 earnings update charts. Parameterised for the next quarter via PARAMS."""
import sys; sys.path.insert(0, "/home/claude")
import pandas as pd, numpy as np
import syz_charts as sc

PARAMS = {
    "xlsx": "/home/claude/vrtx/VRTX.xlsx",       # Bloomberg DAILY export (Last Price, BEst P/E, BEst EPS, SMAVG 40/200)
    "ticker": "VRTX", "ccy": "USD",
    "window_start": "2016-01-01",                # first full year of positive 12m-forward EPS (2015 P/E > 30,000x)
    "pe_avg_from": "2020-01-01",                 # Trikafta era (approved Oct 2019): mature-earner regime
    "asof": "2 Nov 2026",
    "reaction_pct": "flat to +1.4%", "reaction_date": "2 Nov 2026 (after hours)", "market_pct": None,
    # Chart 1: surprise vs. consensus, % (reported / consensus - 1)
    "c1": [("Revenue", 3440.8, 3410.0), ("EPS", 4.76, 4.82), ("Alyftrek", 705.8, 652.0),
           ("Casgevy", 99.2, 79.0), ("Journavx", 58.3, 67.0), ("FY26 guide", 13200.0, 13281.0)],
}


def weekly(path, start):
    """Daily Bloomberg export -> weekly Friday closes (last row kept at its own date), 40-week MA from weekly closes."""
    d = pd.read_excel(path)
    cols = {c: c.lower() for c in d.columns}
    pick = lambda *k: next(c for c, l in cols.items() if all(x in l for x in k))
    d = pd.DataFrame({"date": pd.to_datetime(d[pick("date")]), "price": pd.to_numeric(d[pick("last price")], errors="coerce"),
                      "eps": pd.to_numeric(d[pick("best eps")], errors="coerce"), "pe": pd.to_numeric(d[pick("best p/e")], errors="coerce")})
    d = d.dropna(subset=["price"]).sort_values("date").set_index("date")
    w = d.resample("W-FRI").last()
    w.index = [min(i, d.index[-1]) for i in w.index]
    w["ma40"] = w["price"].rolling(40).mean()
    w = w[w.index >= start].reset_index().rename(columns={"index": "date"})
    return w[w["eps"].notna()].reset_index(drop=True)


if __name__ == "__main__":
    sc.setup_fonts()
    P = PARAMS
    # Layout tweaks for VRTX, kit untouched: P/E legend centred (the 2017 peak sits top-left);
    # extra headroom below the bars so the Journavx label clears the axis
    _legend, _header = sc.legend, sc.header
    sc.legend = lambda ax, loc="upper left", ncol=1: _legend(ax, loc="upper center", ncol=ncol)
    def _header_pad(fig, *a, **k):
        for ax in fig.axes[:1]:
            lo, hi = ax.get_ylim(); ax.set_ylim(lo - 0.10 * (hi - lo), hi)
        return _header(fig, *a, **k)
    df = weekly(P["xlsx"], P["window_start"])
    foot2 = sc.source_line("Bloomberg", P["asof"], "VRTX US Equity, daily data sampled weekly", "BEst 12m-forward consensus",
                           "40-week simple MA", "Log scale", "P/E shaded above (orange) / below (blue) its 2020-26 average")
    stats = sc.price_eps_pe_chart("/home/claude/vrtx/c2_full.png", df, "Vertex",
                                  "VRTX: share price vs. consensus earnings and valuation", foot2, ccy="USD",
                                  pe_avg_from=P["pe_avg_from"], price_lbl=(10, -16), eps_lbl=(10, 10))
    print({k: (round(v, 2) if isinstance(v, float) else v) for k, v in stats.items()}, "window", df.date.iloc[0].date(), df.date.iloc[-1].date())

    labels = [l for l, _, _ in P["c1"]]
    vals = [(r / c - 1) * 100 for _, r, c in P["c1"]]
    print([f"{l} {v:+.1f}%" for l, v in zip(labels, vals)])
    foot1 = sc.source_line("company release, consensus as published before the release", P["asof"],
                           "Casgevy vs. midpoint of $76-82m estimates", "FY26 guide = revenue guidance midpoint")
    sc.header = _header_pad
    sc.bar_chart("/home/claude/vrtx/c1_full.png", labels, vals, "VRTX: Q3 2026 results vs. consensus",
                 "Reported vs. consensus, % · FY26 revenue guidance midpoint vs. consensus", foot1, ylabel="% vs. consensus")
    sc.crop_for_pdf("/home/claude/vrtx/c1_full.png", "/home/claude/vrtx/c1_crop.png", "bar")
    sc.crop_for_pdf("/home/claude/vrtx/c2_full.png", "/home/claude/vrtx/c2_crop.png", "price_eps_pe")
