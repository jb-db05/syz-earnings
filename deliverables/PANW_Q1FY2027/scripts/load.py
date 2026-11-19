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
