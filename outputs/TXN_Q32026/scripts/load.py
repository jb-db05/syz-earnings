"""Daily Bloomberg export -> weekly frame in the shape syz_charts expects (date, price, eps, ma40, pe)."""
import pandas as pd

def load_daily_as_weekly(path):
    raw = pd.read_excel(path).dropna(how="all")
    cols = {c: c.lower() for c in raw.columns}
    pick = lambda *k: next(c for c, l in cols.items() if all(x in l for x in k))
    d = pd.DataFrame({
        "date": pd.to_datetime(raw[pick("date")]),
        "price": pd.to_numeric(raw[pick("last price")], errors="coerce"),
        "eps": pd.to_numeric(raw[pick("best eps")], errors="coerce"),
        "pe": pd.to_numeric(raw[pick("best p/e")], errors="coerce"),
    }).sort_values("date").set_index("date")
    d["eps"] = d["eps"].ffill()            # BEst EPS has gaps on some days
    w = d.resample("W-FRI").last()
    w["lastdate"] = d["price"].resample("W-FRI").apply(lambda s: s.dropna().index.max())
    w = w.dropna(subset=["price"])
    w["ma40"] = w["price"].rolling(40).mean()   # 40-week simple MA on weekly closes
    w = w.reset_index(drop=True).rename(columns={"lastdate": "date"})
    w = w[w["eps"].notna() & w["ma40"].notna()].reset_index(drop=True)
    return w[["date", "price", "eps", "ma40", "pe"]], d
