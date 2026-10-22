"""build_pdf.py: fill the Syz template from content.py, render the PDF, rasterise the pages, write fill.json.
Run: python3 build_pdf.py   (then: node /home/claude/build_pptx.js fill.json <out>.pptx)"""
import html, json, re, sys
from PIL import Image
import content as C

OUT = "/home/claude/galderma"
NAME = f"Earnings_Update_{C.TICKER}_{C.PERIOD}"
C1_IMG, C2_IMG = f"{OUT}/c1_crop.png", f"{OUT}/c2_crop.png"

words = lambda s: len(re.sub(r"&\w+;", "", s).split())
BUDGET = {"QUOTE": (C.QUOTE, 20, 38), "P1": (C.P1, 65, 85), "C1": (C.C1_COMMENT, 55, 65),
          "BASE": (C.BASE_CASE, 95, 110), "UP": (C.UPSIDE, 36, 45), "DOWN": (C.DOWNSIDE, 36, 45),
          "A1a": (C.A1[0], 100, 115), "A1b": (C.A1[1], 90, 105), "A2": (C.A2, 95, 110), "C2": (C.C2_COMMENT, 85, 100)}
for k, (s, lo, hi) in BUDGET.items():
    n = words(s); print(f"{k:5s} {n:4d}  [{lo}-{hi}]{'  <-- OUT' if not lo <= n <= hi else ''}")
for _, _, t in C.TAKEAWAYS:
    assert words(t) <= 18, t

P = lambda s: f"<p>{s}</p>"
fill = {
    "DOC_TYPE": C.DOC_TYPE, "THEME": C.THEME, "DATE": C.DATE, "TITLE": C.TITLE,
    "QUOTE_BLOCK": (f'<div class="quote"><p>&ldquo;{C.QUOTE}&rdquo;</p><div class="who">{C.QUOTE_WHO}</div></div>'
                    if C.QUOTE else ""),
    "TAKEAWAYS": "\n".join(f'<li><span class="tag {c}">{l}</span><span class="t">{t}</span></li>' for c, l, t in C.TAKEAWAYS),
    "KPI_TILES": "\n".join(f'<td><div class="lbl">{l}</div><div class="val">{v}</div><div class="sub {s}">{d}</div></td>'
                           for l, v, d, s in C.KPIS),
    "H_P1": C.H_P1, "P1_PARAGRAPH": P(C.P1),
    "C1_TITLE": C.C1_TITLE, "C1_SUB": C.C1_SUB, "C1_IMG": C1_IMG, "C1_COMMENT": P(C.C1_COMMENT),
    "BASE_CASE": C.BASE_CASE, "UPSIDE": C.UPSIDE, "DOWNSIDE": C.DOWNSIDE,
    "P2_TITLE": C.P2_TITLE, "H_A1": C.H_A1, "A1_PARAGRAPHS": "".join(P(p) for p in C.A1),
    "H_A2": C.H_A2, "A2_PARAGRAPHS": P(C.A2),
    "H_C2": C.H_C2, "C2_TITLE": C.C2_TITLE, "C2_SUB": C.C2_SUB, "C2_IMG": C2_IMG, "C2_COMMENT": P(C.C2_COMMENT),
    "W1": C.W1, "W2": C.W2, "SOURCE_LINE": C.SOURCE_LINE,
}

tpl = open("/home/claude/template.html").read()
doc = tpl
for k, v in fill.items():
    doc = doc.replace("{{" + k + "}}", str(v))
assert "{{" not in doc, re.findall(r"\{\{(\w+)\}\}", doc)
assert "—" not in doc and "&mdash;" not in doc, "em dash"
open(f"{OUT}/doc.html", "w").write(doc)

from weasyprint import HTML
HTML(f"{OUT}/doc.html").write_pdf(f"{OUT}/{NAME}.pdf")
from pdf2image import convert_from_path
pages = convert_from_path(f"{OUT}/{NAME}.pdf", dpi=100)
for i, p in enumerate(pages):
    p.save(f"{OUT}/page{i+1}.png")
print("pages:", len(pages))

# ---- fill.json for the PowerPoint (plain text)
T = lambda s: html.unescape(s).replace("−", "-")
disc = re.findall(r"<p>(This communication.*?|This information.*?|Past performance.*?|Nothing in.*?|Should a.*?)</p>",
                  tpl, re.S)
assert len(disc) == 7, len(disc)
aspect = lambda p: (lambda im: im.size[1] / im.size[0])(Image.open(p))
fj = {
    "LOGO": "/home/claude/syz_logo_hq.png", "GRADBAR": "/home/claude/syz_gradbar.png",
    "DOC_TYPE": C.DOC_TYPE, "THEME": C.THEME, "DATE": C.DATE, "TITLE": T(C.TITLE),
    "QUOTE": T(C.QUOTE), "QUOTE_WHO": T(C.QUOTE_WHO),
    "TAKEAWAYS": [{"tag": c, "label": l, "text": T(t)} for c, l, t in C.TAKEAWAYS],
    "KPIS": [{"label": T(l), "value": T(v), "sub": T(d), "sign": s} for l, v, d, s in C.KPIS],
    "H_P1": C.H_P1, "P1_PARAGRAPH": T(C.P1),
    "C1_TITLE": T(C.C1_TITLE), "C1_SUB": T(C.C1_SUB), "C1_IMG": C1_IMG, "C1_ASPECT": round(aspect(C1_IMG), 4),
    "W1": C.W1_PPTX, "C1_COMMENT": T(C.C1_COMMENT),
    "BASE_CASE": T(C.BASE_CASE), "UPSIDE": T(C.UPSIDE), "DOWNSIDE": T(C.DOWNSIDE),
    "P2_TITLE": C.P2_TITLE, "H_A1": T(C.H_A1), "A1_PARAGRAPHS": [T(p) for p in C.A1],
    "H_A2": T(C.H_A2), "A2_PARAGRAPH": T(C.A2),
    "H_C2": T(C.H_C2), "C2_TITLE": T(C.C2_TITLE), "C2_SUB": T(C.C2_SUB), "C2_IMG": C2_IMG,
    "C2_ASPECT": round(aspect(C2_IMG), 4), "W2": C.W2_PPTX, "C2_COMMENT": T(C.C2_COMMENT),
    "SOURCE_LINE": T(C.SOURCE_LINE), "DISCLAIMER": [T(re.sub(r"\s+", " ", d)) for d in disc],
}
json.dump(fj, open(f"{OUT}/fill.json", "w"), indent=1, ensure_ascii=False)
print("fill.json written")
