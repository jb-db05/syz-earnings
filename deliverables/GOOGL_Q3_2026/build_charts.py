"""build_charts.py: Alphabet (GOOGL) Q3 2026 Earnings update charts. Edit PARAMS for the next quarter."""
import sys
sys.path.insert(0, "/home/claude")
import pandas as pd
import syz_charts as sc

PARAMS = {
    "xlsx": "/home/claude/Alphabet_Shareprice.xlsx",
    "ticker": "GOOGL",
    "ccy": "USD",
    "window_start": "2010-01-01",      # post-IPO years (2005 to 2007) ran at 40x to 57x and distort the P/E average
    "asof": "28 Oct 2026",
    "reaction_pct": -10.0,              # pre-market, 29 Oct 2026 ("down over 10%"), close to be confirmed
    "reaction_date": "29 October 2026",
    "market_pct": None,
    # Chart 1: reported vs. consensus (USD bn, EPS in USD), consensus as quoted in the results coverage
    "surprises": [
        ("Revenue", 127.58, 128.22),
        ("Search", 63.35, 64.99),
        ("YouTube ads", 11.21, 11.40),
        ("Cloud revenue", 30.71, 29.15),
        ("Cloud profit", 11.10, 9.75),
        ("EPS", 2.12, 3.01),
        ("Op. cash flow", 42.30, 52.72),
    ],
}


def load_daily_to_weekly(path):
    """This export is daily (Date | Last Price | BEst P/E Ratio | BEst EPS | SMAVG (40) | SMAVG (200)), so the kit
    loader does not apply: resample to Friday weeks (last trading day kept as the date) and compute the 40-week MA."""
    raw = pd.read_excel(path)
    cols = {c: c.lower() for c in raw.columns}
    pick = lambda *keys: next(c for c, l in cols.items() if all(k in l for k in keys))
    d = pd.DataFrame({
        "date": pd.to_datetime(raw[pick("date")]),
        "price": pd.to_numeric(raw[pick("last price")], errors="coerce"),
        "eps": pd.to_numeric(raw[pick("best eps")], errors="coerce"),
        "pe": pd.to_numeric(raw[pick("best p/e")], errors="coerce"),
    }).dropna(subset=["date", "price"]).sort_values("date")
    d["last_day"] = d["date"]
    w = d.set_index("date").resample("W-FRI").last().dropna(subset=["price"])
    w["date"] = w["last_day"]
    w = w.reset_index(drop=True)[["date", "price", "eps", "pe"]]
    w["ma40"] = w["price"].rolling(40).mean()
    return w


def _style_ax_with_headroom(ax, grid_axis="y", _orig=sc.style_ax):
    """Kit style plus 10% vertical margin, so the EPS bar label clears the x axis."""
    _orig(ax, grid_axis)
    ax.margins(y=0.10)


def main():
    p = PARAMS
    sc.setup_fonts()
    df = load_daily_to_weekly(p["xlsx"])
    df = df[df["eps"].notna() & (df["date"] >= p["window_start"])].reset_index(drop=True)

    # Chart 1: surprise vs. consensus by line
    sc.style_ax = _style_ax_with_headroom
    labels = [s[0] for s in p["surprises"]]
    vals = [(r / c - 1) * 100 for _, r, c in p["surprises"]]
    sc.bar_chart("/home/claude/work/c1.png", labels, vals,
                 f"{p['ticker']}: Q3 2026 results vs. consensus",
                 "Reported vs. consensus before the release, %",
                 sc.source_line("Bloomberg, company filings", p["asof"], "Consensus as quoted in results coverage",
                                "Cloud profit = Google Cloud operating income",
                                "EPS includes a USD 0.55 loss on equity securities"),
                 ylabel="% vs. consensus")
    sc.crop_for_pdf("/home/claude/work/c1.png", "/home/claude/work/c1_crop.png", "bar")
    sc.style_ax = _style_ax_with_headroom.__defaults__[1]

    # Chart 2: price vs. consensus EPS and P/E
    stats = sc.price_eps_pe_chart(
        "/home/claude/work/c2.png", df, "Alphabet",
        f"{p['ticker']}: share price vs. consensus earnings and valuation",
        sc.source_line("Bloomberg", p["asof"], "GOOGL US Equity, weekly", "BEst 12m-forward consensus",
                       "40-week simple MA", "Log scale", "P/E shaded above (orange) / below (blue) its 2010-26 average"),
        ccy=p["ccy"], price_lbl=(10, -16), eps_lbl=(10, 10))   # EPS line ends above the price line
    sc.crop_for_pdf("/home/claude/work/c2.png", "/home/claude/work/c2_crop.png", "price_eps_pe")

    last = df.iloc[-1]
    yr = df[df["date"] > last["date"] - pd.Timedelta(days=365)]
    ago = df[df["date"] <= last["date"] - pd.Timedelta(days=365)].iloc[-1]
    stats.update({
        "window": f"{df['date'].iloc[0]:%d %b %Y} to {last['date']:%d %b %Y}",
        "pe_1y_avg": float(yr["pe"].mean()),
        "pe_peak_1y": (f"{yr.loc[yr['pe'].idxmax(), 'date']:%b %Y}", float(yr["pe"].max())),
        "price_12m_pct": (last["price"] / ago["price"] - 1) * 100,
        "eps_12m_pct": (last["eps"] / ago["eps"] - 1) * 100,
        "surprises_pct": dict(zip(labels, [round(v, 1) for v in vals])),
        "premarket_level": last["price"] * (1 + p["reaction_pct"] / 100),
        "premarket_pe": last["price"] * (1 + p["reaction_pct"] / 100) / last["eps"],
    })
    for k, v in stats.items():
        print(f"{k}: {v}")


if __name__ == "__main__":
    main()
