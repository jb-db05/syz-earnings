import pandas as pd, numpy as np
def load_galp(path):
    """Bloomberg daily export (newest first): Date | Last Price | BEst EPS | BEst P/E | SMAVG(40) | SMAVG(200).
    Resampled to weekly (last trading day of each week, real date kept). The 200-day MA stands in for the 40-week MA."""
    raw = pd.read_excel(path).dropna(how="all")
    cols = {c: c.lower() for c in raw.columns}
    pick = lambda *k: next(c for c, l in cols.items() if all(x in l for x in k))
    d = pd.DataFrame({"date": pd.to_datetime(raw[pick("date")]),
                      "price": pd.to_numeric(raw[pick("last price")], errors="coerce"),
                      "eps": pd.to_numeric(raw[pick("best eps")], errors="coerce"),
                      "pe": pd.to_numeric(raw[pick("best p/e")], errors="coerce"),
                      "ma40": pd.to_numeric(raw[pick("smavg (200)")], errors="coerce")})
    d = d.dropna(subset=["date"]).sort_values("date").reset_index(drop=True)
    d["eps"] = d["eps"].ffill()
    d["wk"] = d["date"].dt.to_period("W-FRI")
    w = d.groupby("wk").last().reset_index(drop=True)
    w = w[w["eps"].notna() & w["pe"].notna() & w["ma40"].notna()].reset_index(drop=True)
    return d, w
