"""build_pdf.py: fill the Syz template from content.py, render the PDF, rasterise, and write fill.json for the PPTX."""
import html, json, re, sys
from PIL import Image
import content as C

OUT = "/home/claude/amzn"
PDF = f"{OUT}/Earnings_Update_AMZN_Q32026.pdf"
W1, W2 = (int(a) for a in sys.argv[1:3]) if len(sys.argv) > 2 else (74, 92)
W1_PPTX, W2_PPTX = 66, 88
P = lambda t: f"<p>{t}</p>"


def words(t):
    return len(re.sub(r"&\w+;", " ", t).split())


budgets = {"intro": (C.COMPANY_INTRO, 25, 36), "quote": (C.QUOTE, 20, 35), "p1": (C.P1_PARAGRAPH, 55, 65),
           "c1": (C.C1_COMMENT, 50, 55), "base": (C.BASE_CASE, 80, 90), "up": (C.UPSIDE, 30, 38),
           "down": (C.DOWNSIDE, 30, 38), "a1a": (C.A1_PARAGRAPHS[0], 100, 115), "a1b": (C.A1_PARAGRAPHS[1], 90, 105),
           "a2": (C.A2_PARAGRAPH, 95, 110), "c2": (C.C2_COMMENT, 85, 100)}
for k, (t, lo, hi) in budgets.items():
    n = words(t)
    print(f"{k:6s} {n:4d} [{lo}-{hi}]{'' if lo <= n <= hi else '  <-- OUT'}")
for _, lbl, t in C.TAKEAWAYS:
    print(f"take   {words(t):4d} [<=18] {lbl}")

fill = {
    "DOC_TYPE": C.DOC_TYPE, "DATE": C.DATE, "TITLE": C.TITLE,
    "QUOTE_BLOCK": (f'<div class="quote"><p>&ldquo;{C.QUOTE}&rdquo;</p><div class="who">{C.QUOTE_WHO}</div></div>'
                    if C.QUOTE else ""),
    "COMPANY_INTRO": C.COMPANY_INTRO,
    "TAKEAWAYS": "\n".join(f'<li><span class="tag {c}">{l}</span><span class="t">{t}</span></li>' for c, l, t in C.TAKEAWAYS),
    "KPI_TILES": "\n".join(f'<td><div class="lbl">{l}</div><div class="val">{v}</div><div class="sub {s}">{sub}</div></td>'
                           for l, v, sub, s in C.KPIS),
    "H_P1": C.H_P1, "P1_PARAGRAPH": P(C.P1_PARAGRAPH),
    "C1_TITLE": C.C1_TITLE, "C1_SUB": C.C1_SUB, "C1_IMG": f"{OUT}/c1_crop.png", "C1_COMMENT": P(C.C1_COMMENT),
    "BASE_CASE": C.BASE_CASE, "UPSIDE": C.UPSIDE, "DOWNSIDE": C.DOWNSIDE,
    "P2_TITLE": C.P2_TITLE, "H_A1": C.H_A1, "A1_PARAGRAPHS": "".join(P(p) for p in C.A1_PARAGRAPHS),
    "H_A2": C.H_A2, "A2_PARAGRAPHS": P(C.A2_PARAGRAPH),
    "H_C2": C.H_C2, "C2_TITLE": C.C2_TITLE, "C2_SUB": C.C2_SUB, "C2_IMG": f"{OUT}/c2_crop.png",
    "C2_COMMENT": P(C.C2_COMMENT), "W1": W1, "W2": W2, "SOURCE_LINE": C.SOURCE_LINE,
}

tpl = open("/home/claude/template.html").read()
doc = tpl
for k, v in fill.items():
    doc = doc.replace("{{" + k + "}}", str(v))
assert "{{" not in doc, re.findall(r"\{\{(\w+)\}\}", doc)
assert "—" not in doc, "em dash"
open(f"{OUT}/doc.html", "w").write(doc)
from weasyprint import HTML
HTML(f"{OUT}/doc.html").write_pdf(PDF)
from pdf2image import convert_from_path
pages = convert_from_path(PDF, dpi=100)
for i, p in enumerate(pages):
    p.save(f"{OUT}/page{i + 1}.png")
print("pages:", len(pages))

# ---- fill.json for the PPTX (plain text)
plain = lambda t: html.unescape(t).replace("−", "-")
disc = re.search(r'<div class="disc-head">Disclaimer</div>(.*?)</div>', tpl, re.S).group(1)
aspect = lambda p: (lambda im: im.size[1] / im.size[0])(Image.open(p))
fj = {
    "LOGO": "/home/claude/syz_logo_hq.png", "GRADBAR": "/home/claude/syz_gradbar.png",
    "DOC_TYPE": C.DOC_TYPE, "DATE": C.DATE, "TITLE": plain(C.TITLE),
    "QUOTE": plain(C.QUOTE), "QUOTE_WHO": plain(C.QUOTE_WHO), "COMPANY_INTRO": plain(C.COMPANY_INTRO),
    "TAKEAWAYS": [{"tag": c, "label": l, "text": plain(t)} for c, l, t in C.TAKEAWAYS],
    "KPIS": [{"label": plain(l), "value": plain(v), "sub": plain(s), "sign": g} for l, v, s, g in C.KPIS],
    "H_P1": plain(C.H_P1), "P1_PARAGRAPH": plain(C.P1_PARAGRAPH),
    "C1_TITLE": plain(C.C1_TITLE), "C1_SUB": plain(C.C1_SUB), "C1_IMG": f"{OUT}/c1_crop.png",
    "C1_ASPECT": aspect(f"{OUT}/c1_crop.png"), "W1": W1_PPTX, "C1_COMMENT": plain(C.C1_COMMENT),
    "BASE_CASE": plain(C.BASE_CASE), "UPSIDE": plain(C.UPSIDE), "DOWNSIDE": plain(C.DOWNSIDE),
    "P2_TITLE": C.P2_TITLE, "H_A1": plain(C.H_A1), "A1_PARAGRAPHS": [plain(p) for p in C.A1_PARAGRAPHS],
    "H_A2": plain(C.H_A2), "A2_PARAGRAPH": plain(C.A2_PARAGRAPH), "H_C2": plain(C.H_C2),
    "C2_TITLE": plain(C.C2_TITLE), "C2_SUB": plain(C.C2_SUB), "C2_IMG": f"{OUT}/c2_crop.png",
    "C2_ASPECT": aspect(f"{OUT}/c2_crop.png"), "W2": W2_PPTX, "C2_COMMENT": plain(C.C2_COMMENT),
    "SOURCE_LINE": plain(C.SOURCE_LINE),
    "DISCLAIMER": [plain(p) for p in re.findall(r"<p>(.*?)</p>", disc, re.S)],
}
assert len(fj["DISCLAIMER"]) == 7
json.dump(fj, open(f"{OUT}/fill.json", "w"), ensure_ascii=False, indent=1)
print("fill.json written")
