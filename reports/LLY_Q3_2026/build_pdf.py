"""build_pdf.py: fill the Syz template from content.py, render the PDF, rasterise, write fill.json.
Run after build_charts.py:  python3 build_pdf.py"""
import html, json, re, sys
from PIL import Image
import content as C

ROOT = "/home/user/syz-earnings"
OUT_PDF = "Earnings_Update_LLY_Q32026.pdf"
DOC_TYPE = "Earnings update"


def words(s):
    return len(re.sub(r"&\w+;", " ", s).split())


budgets = {"QUOTE": (C.QUOTE, 20, 35), "COMPANY_INTRO": (C.COMPANY_INTRO, 25, 36), "P1": (C.P1_PARAGRAPH, 55, 65),
           "C1": (C.C1_COMMENT, 50, 55), "BASE": (C.BASE_CASE, 80, 90), "UP": (C.UPSIDE, 34, 38),
           "DOWN": (C.DOWNSIDE, 34, 38), "A1a": (C.A1_PARAGRAPHS[0], 100, 115), "A1b": (C.A1_PARAGRAPHS[1], 90, 105),
           "A2": (C.A2_PARAGRAPHS[0], 95, 110), "C2": (C.C2_COMMENT, 85, 100)}
for k, (t, lo, hi) in budgets.items():
    n = words(t)
    print(f"{k:14s} {n:4d}  [{lo}-{hi}]" + ("" if lo <= n <= hi else "  <-- out of budget"))
for _, label, t in C.TAKEAWAYS:
    print(f"takeaway {label:10s} {words(t)} words")

P = lambda s: f"<p>{s}</p>"
fill = {
    "DOC_TYPE": DOC_TYPE, "DATE": C.DATE, "TITLE": C.TITLE,
    "QUOTE_BLOCK": (f'<div class="quote"><p>&ldquo;{C.QUOTE}&rdquo;</p><div class="who">{C.QUOTE_WHO}</div></div>'
                    if C.QUOTE else ""),
    "COMPANY_INTRO": C.COMPANY_INTRO,
    "TAKEAWAYS": "\n".join(f'<li><span class="tag {c}">{l}</span><span class="t">{t}</span></li>' for c, l, t in C.TAKEAWAYS),
    "KPI_TILES": "\n".join(f'<td><div class="lbl">{l}</div><div class="val">{v}</div><div class="sub {s}">{d}</div></td>'
                           for l, v, d, s in C.KPIS),
    "H_P1": C.H_P1, "P1_PARAGRAPH": P(C.P1_PARAGRAPH),
    "C1_TITLE": C.C1_TITLE, "C1_SUB": C.C1_SUB, "C1_IMG": "/home/claude/c1_crop.png", "C1_COMMENT": P(C.C1_COMMENT),
    "BASE_CASE": C.BASE_CASE, "UPSIDE": C.UPSIDE, "DOWNSIDE": C.DOWNSIDE,
    "P2_TITLE": C.P2_TITLE,
    "H_A1": C.H_A1, "A1_PARAGRAPHS": "".join(P(p) for p in C.A1_PARAGRAPHS),
    "H_A2": C.H_A2, "A2_PARAGRAPHS": "".join(P(p) for p in C.A2_PARAGRAPHS),
    "H_C2": C.H_C2, "C2_TITLE": C.C2_TITLE, "C2_SUB": C.C2_SUB, "C2_IMG": "/home/claude/c2_crop.png",
    "C2_COMMENT": P(C.C2_COMMENT),
    "W1": C.W1, "W2": C.W2, "SOURCE_LINE": C.SOURCE_LINE,
}

tpl = open(f"{ROOT}/template.html").read()
doc = tpl
for k, v in fill.items():
    doc = doc.replace("{{" + k + "}}", str(v))
assert "{{" not in doc, re.findall(r"\{\{(\w+)\}\}", doc)
assert "—" not in doc, "em dash"
open("doc.html", "w").write(doc)

from weasyprint import HTML
HTML("doc.html").write_pdf(OUT_PDF)
from pdf2image import convert_from_path
pages = convert_from_path(OUT_PDF, dpi=100)
for i, p in enumerate(pages):
    p.save(f"page{i+1}.png")
print("pages:", len(pages))

# ---- fill.json for the PowerPoint (plain text)
U = lambda s: html.unescape(s).replace("−", "-")
disc = re.findall(r'<div class="disc-head">Disclaimer</div>(.*?)</div>', tpl, re.S)[0]
disc = [U(re.sub(r"\s+", " ", p).strip()) for p in re.findall(r"<p>(.*?)</p>", disc, re.S)]
assert len(disc) == 7
aspect = lambda p: (lambda im: im.size[1] / im.size[0])(Image.open(p))
fj = {
    "LOGO": "/home/claude/syz_logo_hq.png", "GRADBAR": "/home/claude/syz_gradbar.png",
    "DOC_TYPE": DOC_TYPE, "DATE": C.DATE, "TITLE": U(C.TITLE),
    "QUOTE": U(C.QUOTE), "QUOTE_WHO": U(C.QUOTE_WHO), "COMPANY_INTRO": U(C.COMPANY_INTRO),
    "TAKEAWAYS": [{"tag": c, "label": l, "text": U(t)} for c, l, t in C.TAKEAWAYS],
    "KPIS": [{"label": U(l), "value": U(v), "sub": U(d), "sign": s} for l, v, d, s in C.KPIS],
    "H_P1": U(C.H_P1), "P1_PARAGRAPH": U(C.P1_PARAGRAPH),
    "C1_TITLE": U(C.C1_TITLE), "C1_SUB": U(C.C1_SUB), "C1_IMG": "/home/claude/c1_crop.png",
    "C1_ASPECT": aspect("/home/claude/c1_crop.png"), "W1": C.W1_PPTX, "C1_COMMENT": U(C.C1_COMMENT),
    "BASE_CASE": U(C.BASE_CASE), "UPSIDE": U(C.UPSIDE), "DOWNSIDE": U(C.DOWNSIDE),
    "P2_TITLE": C.P2_TITLE, "H_A1": U(C.H_A1), "A1_PARAGRAPHS": [U(p) for p in C.A1_PARAGRAPHS],
    "H_A2": U(C.H_A2), "A2_PARAGRAPH": U(C.A2_PARAGRAPHS[0]),
    "H_C2": U(C.H_C2), "C2_TITLE": U(C.C2_TITLE), "C2_SUB": U(C.C2_SUB), "C2_IMG": "/home/claude/c2_crop.png",
    "C2_ASPECT": aspect("/home/claude/c2_crop.png"), "W2": C.W2_PPTX, "C2_COMMENT": U(C.C2_COMMENT),
    "SOURCE_LINE": U(C.SOURCE_LINE), "DISCLAIMER": disc,
}
json.dump(fj, open("fill.json", "w"), indent=1, ensure_ascii=False)
print("fill.json written")
