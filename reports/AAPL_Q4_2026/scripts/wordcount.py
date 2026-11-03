import re, html, sys
sys.path.insert(0, "/home/claude/aapl")
import content as C
def wc(s): return len(html.unescape(re.sub(r"<[^>]+>", "", s)).replace("&hellip;", "").split())
def cc(s): return len(html.unescape(re.sub(r"<[^>]+>", "", s)))
rows = [("quote 20-35", C.QUOTE), ("intro 25-36", C.COMPANY_INTRO), ("P1 55-65", C.P1_PARAGRAPH),
        ("C1 50-55", C.C1_COMMENT), ("base 80-85(90)", C.BASE_CASE), ("A1a 100-115", C.A1_PARAGRAPHS[0]),
        ("A1b 90-105", C.A1_PARAGRAPHS[1]), ("A2 95-110", C.A2_PARAGRAPHS), ("C2 85-100", C.C2_COMMENT)]
for n, s in rows: print(f"{n:16s} {wc(s)}")
print("upside words/chars", wc(C.UPSIDE), cc(C.UPSIDE), "downside", wc(C.DOWNSIDE), cc(C.DOWNSIDE), "(<=200 chars)")
for t in C.TAKEAWAYS: print("takeaway", wc(t[2]), len(t[1]))
print("title chars", len(C.TITLE))
for h in [C.H_P1, C.H_A1, C.H_A2, C.H_C2]: print("heading", len(h), h)
