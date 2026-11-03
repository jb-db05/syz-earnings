"""build_charts.py: Apple Q4 FY2025 Earnings update charts. Edit PARAMS for the next quarter."""
import sys, json
sys.path.insert(0, "/home/claude")
import pandas as pd
import syz_charts as sc

PARAMS = {
    "xlsx": "/home/claude/aapl/apple.xlsx",
    "ticker": "AAPL",
    "ccy": "USD",
    "window_start": "2010-01-01",     # same window as the other reference instances
    "window_end": "2025-10-31",       # publication-day close (results 30 Oct after the close, reaction 31 Oct)
    "asof": "31 Oct 2025",
    "reaction_pct": -0.38,            # 31 Oct 2025 close 270.37 vs 30 Oct close 271.40 (Bloomberg export)
    "reaction_date": "31 October 2025",
    "market_pct": 0.6,                # Nasdaq Composite, 31 Oct 2025 (S&P 500 +0.3%), press coverage
    # Chart 1: reported vs. LSEG consensus (CNBC, 30 Oct 2025); gross margin in margin points
    "c1_labels": ["Revenue", "iPhone", "Services", "Gross margin", "EPS", "Dec-Q guide"],
    "c1_values": [102.466 / 102.24 * 100 - 100, 49.025 / 50.19 * 100 - 100, 28.750 / 28.17 * 100 - 100,
                  47.2 - 46.4, 1.85 / 1.77 * 100 - 100, 124.300 * 1.11 / 132.31 * 100 - 100],
}


class Labels:
    """bar_chart calls fmt.format(v) once per bar: hand it a label list (gross margin in bp)."""
    def __init__(self, labels): self.it = iter(labels)
    def format(self, v): return next(self.it)


def load_daily_as_weekly(path):
    """This Apple export is daily (Date | Last Price | BEst P/E | BEst EPS | SMAVG (40) | SMAVG (200)), so
    the kit loader (which looks for 'moving average') does not apply: sample Friday closes and compute the
    40-week simple MA on the weekly closes (it matches Bloomberg's 200-day SMAVG within 0.1%)."""
    raw = pd.read_excel(path)
    cols = {c: c.lower() for c in raw.columns}
    pick = lambda *k: next(c for c, l in cols.items() if all(x in l for x in k))
    d = pd.DataFrame({"date": pd.to_datetime(raw[pick("date")]),
                      "price": pd.to_numeric(raw[pick("last price")], errors="coerce"),
                      "eps": pd.to_numeric(raw[pick("best eps")], errors="coerce"),
                      "pe": pd.to_numeric(raw[pick("best p/e")], errors="coerce")})
    d = d.dropna(subset=["price"]).sort_values("date").set_index("date")
    w = d.resample("W-FRI").last()
    w["ma40"] = w["price"].rolling(40).mean()
    return w.reset_index()


def main():
    P = PARAMS
    sc.setup_fonts()
    w = load_daily_as_weekly(P["xlsx"])
    df = w[(w["date"] >= P["window_start"]) & (w["date"] <= P["window_end"])]
    df = df[df["eps"].notna()].reset_index(drop=True)

    vals = P["c1_values"]
    lbls = [f"{v:+.1f}%" if i != 3 else f"{v * 100:+.0f}bp" for i, v in enumerate(vals)]
    sc.bar_chart("/home/claude/aapl/c1.png", P["c1_labels"], vals,
                 f"{P['ticker']}: Q4 FY2025 surprises vs. consensus",
                 "Reported vs. LSEG consensus in %, gross margin in margin points, December-quarter guide at the 11% midpoint",
                 sc.source_line("Apple results release of 30 Oct 2025, LSEG consensus via press coverage", P["asof"],
                                "Gross margin 47.2% vs. 46.4% consensus", "Dec-Q guide midpoint USD 138.0bn vs. USD 132.3bn consensus"),
                 fmt=Labels(lbls), ylabel="Surprise vs. consensus (%)")
    sc.crop_for_pdf("/home/claude/aapl/c1.png", "/home/claude/aapl/c1_crop.png", "bar")

    stats = sc.price_eps_pe_chart(
        "/home/claude/aapl/c2.png", df, P["ticker"], f"{P['ticker']}: share price vs. consensus earnings and valuation",
        sc.source_line("Bloomberg", P["asof"], "AAPL US Equity, weekly (Friday close)",
                       "BEst 12m-forward consensus", "40-week simple MA", "Log scale",
                       "P/E shaded above (orange) / below (blue) its 2010-25 average"),
        ccy=P["ccy"], price_lbl=(10, -16), eps_lbl=(10, 10))   # EPS ends above the price line: labels swapped
    sc.crop_for_pdf("/home/claude/aapl/c2.png", "/home/claude/aapl/c2_crop.png", "price_eps_pe")

    pe = df["pe"]; last = df.iloc[-1]
    yr = df[df["date"] > df["date"].iloc[-1] - pd.Timedelta(days=365)]
    y5 = df[df["date"] > df["date"].iloc[-1] - pd.Timedelta(days=5 * 365)]
    ago = df[df["date"] <= df["date"].iloc[-1] - pd.Timedelta(days=364)].iloc[-1]
    q3 = df[df["date"] <= "2025-08-01"].iloc[-1]          # Q3 FY2025 print, 31 Jul 2025 after the close
    stats.update({
        "window": f"{df['date'].iloc[0]:%d %b %Y} to {df['date'].iloc[-1]:%d %b %Y}",
        "pe_1y_avg": float(yr["pe"].mean()), "pe_5y_avg": float(y5["pe"].mean()),
        "pe_peak": float(pe.max()), "pe_peak_date": f"{df.loc[pe.idxmax(), 'date']:%b %Y}",
        "price_12m_pct": (last.price / ago.price - 1) * 100, "eps_12m_pct": (last.eps / ago.eps - 1) * 100,
        "price_since_q3_pct": (last.price / q3.price - 1) * 100, "eps_since_q3_pct": (last.eps / q3.eps - 1) * 100,
        "pe_at_q3": float(q3.pe), "price_vs_ma_pct": (last.price / last.ma40 - 1) * 100,
        "pe_after_10pct_upgrade": float(last.pe / 1.1),
        "c1": dict(zip(P["c1_labels"], [round(v, 2) for v in vals])),
    })
    json.dump(stats, open("/home/claude/aapl/stats.json", "w"), indent=1, default=float)
    print(json.dumps(stats, indent=1, default=float))


if __name__ == "__main__":
    main()
