import pandas as pd, numpy as np
def load(path="/home/claude/saf/SAF.xlsx"):
    """Bloomberg daily export -> weekly (Friday close, last week ends on the last date), 40-week MA from weekly closes."""
    d = pd.read_excel(path).dropna(how="all")
    cols = {c: c.lower() for c in d.columns}
    pick = lambda *k: next(c for c, l in cols.items() if all(x in l for x in k))
    d = pd.DataFrame({"date": pd.to_datetime(d[pick("date")]),
                      "price": pd.to_numeric(d[pick("last price")], errors="coerce"),
                      "eps": pd.to_numeric(d[pick("best eps")], errors="coerce"),
                      "pe": pd.to_numeric(d[pick("best p/e")], errors="coerce")}).sort_values("date").set_index("date")
    w = d.resample("W-FRI").last()
    w.index = [min(i, d.index[-1]) for i in w.index]
    w["ma40"] = w["price"].rolling(40).mean()
    w = w.reset_index().rename(columns={"index": "date"})
    w = w[w["eps"].notna() & w["ma40"].notna()].reset_index(drop=True)
    return d, w
