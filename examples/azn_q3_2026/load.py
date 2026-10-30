import pandas as pd
def load_weekly(path, window_start=None):
    """Bloomberg daily export (Date | Last Price | BEst P/E | BEst EPS | SMAVG 40 | SMAVG 200), newest first.
    Resampled to weekly (last trading day of the week); 40-week MA computed on the weekly closes."""
    df = pd.read_excel(path)
    cols = {c: c.lower() for c in df.columns}
    pick = lambda *k: next(c for c, l in cols.items() if all(x in l for x in k))
    d = pd.DataFrame({"date": pd.to_datetime(df[pick("date")]),
                      "price": pd.to_numeric(df[pick("last price")], errors="coerce"),
                      "eps": pd.to_numeric(df[pick("best eps")], errors="coerce"),
                      "pe": pd.to_numeric(df[pick("best p/e")], errors="coerce")})
    d = d.dropna(subset=["price"]).sort_values("date").set_index("date")
    w = d.resample("W-FRI").last()
    w["last_day"] = d["price"].resample("W-FRI").apply(lambda s: s.index.max())
    w = w.dropna(subset=["price"])
    w["ma40"] = w["price"].rolling(40).mean()
    w = w.reset_index()
    w = w[w["eps"].notna()]
    if window_start: w = w[w["date"] >= window_start]
    return w.reset_index(drop=True)
