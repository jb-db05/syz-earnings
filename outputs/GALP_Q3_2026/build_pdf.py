"""build_pdf.py: fill the Syz template from content.py, render the PDF, rasterise, write fill.json for the PPTX."""
import sys, re, json, html as H
sys.path.insert(0, "/home/claude/galp")
import content as C
from PIL import Image

OUT = "/home/claude/galp"
TAG = "Earnings_Update_GALP_Q32026"
P = lambda t: f"<p>{t}</p>"
words = lambda t: len(re.sub(r"<[^>]+>|&\w+;", " ", t).split())

budget = {"QUOTE": (C.QUOTE, 20, 35), "P1": (C.P1, 65, 85), "C1": (C.C1_COMMENT, 55, 65),
          "BASE": (C.BASE_CASE, 95, 110), "UP": (C.UPSIDE, 36, 45), "DOWN": (C.DOWNSIDE, 36, 45),
          "A1a": (C.A1[0], 100, 115), "A1b": (C.A1[1], 90, 105), "A2": (C.A2, 95, 110), "C2": (C.C2_COMMENT, 85, 100)}
for k, (t, lo, hi) in budget.items():
    n = words(t); print(f"{k:5s} {n:4d}  [{lo}-{hi}] {'OK' if lo <= n <= hi else 'OUT'}")
for _, lbl, t in C.TAKEAWAYS:
    print(f"take  {words(t):4d}  [<=18] {lbl}")

fill = {
    "DOC_TYPE": C.DOC_TYPE, "THEME": C.THEME, "DATE": C.DATE, "TITLE": C.TITLE,
    "QUOTE_BLOCK": (f'<div class="quote"><p>&ldquo;{C.QUOTE}&rdquo;</p><div class="who">{C.QUOTE_WHO}</div></div>'
                    if C.QUOTE else ""),
    "TAKEAWAYS": "\n".join(f'<li><span class="tag {c}">{l}</span><span class="t">{t}</span></li>' for c, l, t in C.TAKEAWAYS),
    "KPI_TILES": "\n".join(f'<td><div class="lbl">{l}</div><div class="val">{v}</div><div class="sub {s}">{u}</div></td>'
                           for l, v, u, s in C.KPIS),
    "H_P1": C.H_P1, "P1_PARAGRAPH": P(C.P1),
    "C1_TITLE": C.C1_TITLE, "C1_SUB": C.C1_SUB, "C1_IMG": f"{OUT}/c1_crop.png", "C1_COMMENT": P(C.C1_COMMENT),
    "BASE_CASE": C.BASE_CASE, "UPSIDE": C.UPSIDE, "DOWNSIDE": C.DOWNSIDE,
    "P2_TITLE": C.P2_TITLE, "H_A1": C.H_A1, "A1_PARAGRAPHS": "".join(P(t) for t in C.A1),
    "H_A2": C.H_A2, "A2_PARAGRAPHS": P(C.A2),
    "H_C2": C.H_C2, "C2_TITLE": C.C2_TITLE, "C2_SUB": C.C2_SUB, "C2_IMG": f"{OUT}/c2_crop.png",
    "C2_COMMENT": P(C.C2_COMMENT), "W1": C.W1, "W2": C.W2, "SOURCE_LINE": C.SOURCE_LINE,
}
tpl = open("/home/claude/template.html").read()
for k, v in fill.items():
    tpl = tpl.replace("{{" + k + "}}", str(v))
assert "{{" not in tpl, re.findall(r"\{\{(\w+)\}\}", tpl)
assert "—" not in tpl, "em dash"
open(f"{OUT}/doc.html", "w").write(tpl)
from weasyprint import HTML
HTML(f"{OUT}/doc.html").write_pdf(f"{OUT}/{TAG}.pdf")
from pdf2image import convert_from_path
pages = convert_from_path(f"{OUT}/{TAG}.pdf", dpi=100)
for i, p in enumerate(pages):
    p.save(f"{OUT}/page{i + 1}.png")
print("pages:", len(pages))

# ---- fill.json for build_pptx.js (plain text)
u = lambda t: H.unescape(re.sub(r"<[^>]+>", "", t)).replace("−", "-")
disc = re.findall(r"<p>(.*?)</p>", tpl.split('<div class="disc-head">Disclaimer</div>')[1], re.S)
asp = lambda p: (lambda im: im.size[1] / im.size[0])(Image.open(p))
fj = {
    "LOGO": "/home/claude/syz_logo_hq.png", "GRADBAR": "/home/claude/syz_gradbar.png",
    "DOC_TYPE": C.DOC_TYPE, "THEME": C.THEME, "DATE": C.DATE, "TITLE": u(C.TITLE),
    "QUOTE": u(C.QUOTE), "QUOTE_WHO": u(C.QUOTE_WHO),
    "TAKEAWAYS": [{"tag": c, "label": l, "text": u(t)} for c, l, t in C.TAKEAWAYS],
    "KPIS": [{"label": u(l), "value": u(v), "sub": u(s), "sign": g} for l, v, s, g in C.KPIS],
    "H_P1": u(C.H_P1), "P1_PARAGRAPH": u(C.P1),
    "C1_TITLE": u(C.C1_TITLE), "C1_SUB": u(C.C1_SUB), "C1_IMG": f"{OUT}/c1_crop.png", "C1_ASPECT": asp(f"{OUT}/c1_crop.png"),
    "W1": C.W1_PPTX, "C1_COMMENT": u(C.C1_COMMENT), "BASE_CASE": u(C.BASE_CASE),
    "UPSIDE": u(C.UPSIDE), "DOWNSIDE": u(C.DOWNSIDE), "P2_TITLE": C.P2_TITLE,
    "H_A1": u(C.H_A1), "A1_PARAGRAPHS": [u(t) for t in C.A1], "H_A2": u(C.H_A2), "A2_PARAGRAPH": u(C.A2),
    "H_C2": u(C.H_C2), "C2_TITLE": u(C.C2_TITLE), "C2_SUB": u(C.C2_SUB), "C2_IMG": f"{OUT}/c2_crop.png",
    "C2_ASPECT": asp(f"{OUT}/c2_crop.png"), "W2": C.W2_PPTX, "C2_COMMENT": u(C.C2_COMMENT),
    "SOURCE_LINE": u(C.SOURCE_LINE), "DISCLAIMER": [u(" ".join(p.split())) for p in disc],
}
assert len(fj["DISCLAIMER"]) == 7
json.dump(fj, open(f"{OUT}/fill.json", "w"), ensure_ascii=False, indent=1)
print("fill.json written")
