"""TSMC Q3 2026 Earnings update: fill the template, render the PDF, rasterise, write fill.json."""
import html, json, re, sys
sys.path.insert(0, "/home/claude")
from content import *

OUT = f"Earnings_Update_{TICKER}_{PERIOD}"
TEMPLATE = "/home/claude/template.html"

def words(s):
    return len(re.sub(r"<[^>]+>", "", html.unescape(s)).split())

budget = {"P1": (P1, 65, 85), "C1": (C1_COMMENT, 55, 65), "BASE": (BASE_CASE, 95, 110),
          "UP": (UPSIDE, 36, 45), "DOWN": (DOWNSIDE, 36, 45), "A1a": (A1[0], 100, 115),
          "A1b": (A1[1], 90, 105), "A2": (A2, 95, 110), "C2": (C2_COMMENT, 85, 100)}
for k, (t, lo, hi) in budget.items():
    n = words(t); print(f"{k:5s} {n:4d}  [{lo}-{hi}]{'  <-- OUT' if not lo <= n <= hi else ''}")
for _, lbl, t in TAKEAWAYS:
    n = words(t); print(f"take  {n:4d}  [<=18]{'  <-- OUT' if n > 18 else ''}  {lbl}")

p = lambda t: f"<p>{t}</p>"
fill = dict(FILL)
fill.update({
    "QUOTE_BLOCK": (f'<div class="quote"><p>&ldquo;{FILL["QUOTE"]}&rdquo;</p><div class="who">{FILL["QUOTE_WHO"]}</div></div>'
                    if FILL["QUOTE"] else ""),
    "TAKEAWAYS": "\n".join(f'<li><span class="tag {c}">{l}</span><span class="t">{t}</span></li>' for c, l, t in TAKEAWAYS),
    "KPI_TILES": "\n".join(f'<td><div class="lbl">{l}</div><div class="val">{v}</div><div class="sub {c}">{s}</div></td>'
                           for l, v, s, c in KPIS),
    "H_P1": H_P1, "P1_PARAGRAPH": p(P1),
    "C1_TITLE": C1_TITLE, "C1_SUB": C1_SUB, "C1_IMG": "/home/claude/c1_crop.png", "C1_COMMENT": p(C1_COMMENT),
    "BASE_CASE": BASE_CASE, "UPSIDE": UPSIDE, "DOWNSIDE": DOWNSIDE,
    "H_A1": H_A1, "A1_PARAGRAPHS": "".join(p(t) for t in A1),
    "H_A2": H_A2, "A2_PARAGRAPHS": p(A2),
    "H_C2": H_C2, "C2_TITLE": C2_TITLE, "C2_SUB": C2_SUB, "C2_IMG": "/home/claude/c2_crop.png", "C2_COMMENT": p(C2_COMMENT),
})
doc = open(TEMPLATE).read()
for k, v in fill.items():
    doc = doc.replace("{{" + k + "}}", str(v))
assert "{{" not in doc, "unfilled placeholder"
assert "—" not in doc, "em dash"
open("doc.html", "w").write(doc)

from weasyprint import HTML
HTML("doc.html").write_pdf(OUT + ".pdf")
from pdf2image import convert_from_path
pages = convert_from_path(OUT + ".pdf", dpi=100)
for i, pg in enumerate(pages):
    pg.save(f"/tmp/claude-0/-home-user-syz-earnings/65291476-479b-5ca1-a099-11073929894d/scratchpad/page{i+1}.png")
print("pages:", len(pages))

# ---- fill.json for build_pptx.js (plain text)
from PIL import Image
u = lambda s: html.unescape(s).replace("−", "-")
legal = re.search(r'<div class="disc-head">Disclaimer</div>(.*?)</div>', doc, re.S).group(1)
ar = lambda f: (lambda im: im.size[1] / im.size[0])(Image.open(f))
pp = {
    "LOGO": "/home/claude/syz_logo_hq.png", "GRADBAR": "/home/claude/syz_gradbar.png",
    "DOC_TYPE": u(FILL["DOC_TYPE"]), "THEME": u(FILL["THEME"]), "DATE": FILL["DATE"], "TITLE": u(FILL["TITLE"]),
    "QUOTE": u(FILL["QUOTE"]), "QUOTE_WHO": u(FILL["QUOTE_WHO"]),
    "TAKEAWAYS": [{"tag": c, "label": l, "text": u(t)} for c, l, t in TAKEAWAYS],
    "KPIS": [{"label": u(l), "value": u(v), "sub": u(s), "sign": c} for l, v, s, c in KPIS],
    "H_P1": u(H_P1), "P1_PARAGRAPH": u(P1),
    "C1_TITLE": u(C1_TITLE), "C1_SUB": u(C1_SUB), "C1_IMG": "/home/claude/c1_crop.png",
    "C1_ASPECT": ar("/home/claude/c1_crop.png"), "W1": int(sys.argv[1]) if len(sys.argv) > 1 else 66,
    "C1_COMMENT": u(C1_COMMENT), "BASE_CASE": u(BASE_CASE), "UPSIDE": u(UPSIDE), "DOWNSIDE": u(DOWNSIDE),
    "P2_TITLE": u(FILL["P2_TITLE"]), "H_A1": u(H_A1), "A1_PARAGRAPHS": [u(t) for t in A1],
    "H_A2": u(H_A2), "A2_PARAGRAPH": u(A2), "H_C2": u(H_C2),
    "C2_TITLE": u(C2_TITLE), "C2_SUB": u(C2_SUB), "C2_IMG": "/home/claude/c2_crop.png",
    "C2_ASPECT": ar("/home/claude/c2_crop.png"), "W2": int(sys.argv[2]) if len(sys.argv) > 2 else 90,
    "C2_COMMENT": u(C2_COMMENT), "SOURCE_LINE": u(FILL["SOURCE_LINE"]),
    "DISCLAIMER": [u(t) for t in re.findall(r"<p>(.*?)</p>", legal, re.S)],
}
assert len(pp["DISCLAIMER"]) == 7
json.dump(pp, open("fill.json", "w"), ensure_ascii=False, indent=1)
