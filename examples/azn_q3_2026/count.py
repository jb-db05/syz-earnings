import re, html, content as c
def wc(s): return len(html.unescape(re.sub(r"<[^>]+>", " ", s)).split())
for k, lo, hi in [("COMPANY_INTRO",25,36),("P1_PARAGRAPH",55,65),("C1_COMMENT",50,55),("BASE_CASE",80,90),("UPSIDE",34,38),("DOWNSIDE",34,38),("A2_PARAGRAPHS",95,110),("C2_COMMENT",85,100)]:
    n = wc(getattr(c, k)); print(f"{k:14s} {n:4d} [{lo}-{hi}] {'OK' if lo<=n<=hi else '<<'}")
for i,(lo,hi) in enumerate([(100,115),(90,105)]):
    n = wc(c.A1_PARAGRAPHS[i]); print(f"A1[{i}]          {n:4d} [{lo}-{hi}] {'OK' if lo<=n<=hi else '<<'}")
for t in c.TAKEAWAYS: print("take", wc(t[2]))
print("chars up/down", len(c.UPSIDE), len(c.DOWNSIDE))
allt = " ".join(str(v) for k,v in vars(c).items() if k.isupper())
for w in ["while","shift","debate","it is not","What ","robust","notably","underscore","key ","Hold","Buy","Overweight","Kepler","JPMorgan","BofA"," sell","keep","add ","trim"]:
    if w.lower() in allt.lower(): print("FLAG:", w)
