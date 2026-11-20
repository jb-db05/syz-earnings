import pandas as pd, numpy as np
def load(path="/root/.claude/uploads/07f0e85e-a6f7-5bc3-ba62-89b5e71e0237/5a9ad56c-PaloAlto_Graph.xlsx"):
    df = pd.read_excel(path, sheet_name=0).dropna(how="all")
    cols = {c: c.lower() for c in df.columns}
    pick = lambda *k: next(c for c, l in cols.items() if all(x in l for x in k))
    def todate(v):
        if isinstance(v, (int, float, np.integer, np.floating)):
            return pd.Timestamp("1899-12-30") + pd.Timedelta(days=float(v))
        return pd.Timestamp(v)
    out = pd.DataFrame({"date": df[pick("date")].map(todate),
        "price": pd.to_numeric(df[pick("last price")], errors="coerce"),
        "eps": pd.to_numeric(df[pick("best eps")], errors="coerce"),
        "ma40": pd.to_numeric(df[pick("moving average")], errors="coerce"),
        "pe": pd.to_numeric(df[pick("best p/e")], errors="coerce")}).dropna(subset=["date"]).sort_values("date").reset_index(drop=True)
    return out


# 19 Nov 2026 close from the Bloomberg daily screen supplied by the user (export row was an earlier level, USD 358.30)
CLOSE_19NOV = 361.73
def load_closed(path=None):
    d = load(path) if path else load()
    i = d.index[-1]; assert d.loc[i, "date"] == pd.Timestamp("2026-11-19")
    old = d.loc[i, "price"]
    d.loc[i, "ma40"] += (CLOSE_19NOV - old) / 40
    d.loc[i, "price"] = CLOSE_19NOV
    d.loc[i, "pe"] = CLOSE_19NOV / d.loc[i, "eps"]
    return d
