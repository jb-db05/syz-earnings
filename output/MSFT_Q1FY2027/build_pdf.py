"""build_pdf.py: fill the Syz template from content.py, render the PDF, rasterise, write fill.json."""
import html, json, re, sys
from PIL import Image
import content as C

OUT = "/home/claude/msft"
TICKER, QTR = "MSFT", "Q1FY2027"
OUT_PDF = f"{OUT}/Earnings_Update_{TICKER}_{QTR}.pdf"
W1 = int(sys.argv[1]) if len(sys.argv) > 1 else C.W1
W2 = int(sys.argv[2]) if len(sys.argv) > 2 else C.W2

quote_block = (f'<div class="quote"><p>&ldquo;{C.QUOTE}&rdquo;</p><div class="who">{C.QUOTE_WHO}</div></div>'
               if C.QUOTE else "")
fill = {
    "DOC_TYPE": C.DOC_TYPE, "DATE": C.DATE, "TITLE": C.TITLE, "QUOTE_BLOCK": quote_block,
    "COMPANY_INTRO": C.COMPANY_INTRO,
    "TAKEAWAYS": "\n".join(f'<li><span class="tag {t}">{l}</span><span class="t">{x}</span></li>'
                           for t, l, x in C.TAKEAWAYS),
    "KPI_TILES": "\n".join(f'<td><div class="lbl">{l}</div><div class="val">{v}</div><div class="sub {s}">{u}</div></td>'
                           for l, v, u, s in C.KPIS),
    "H_P1": C.H_P1, "P1_PARAGRAPH": C.P1_PARAGRAPH,
    "C1_TITLE": C.C1_TITLE, "C1_SUB": C.C1_SUB, "C1_IMG": f"{OUT}/c1_crop.png", "C1_COMMENT": C.C1_COMMENT,
    "BASE_CASE": C.BASE_CASE, "UPSIDE": C.UPSIDE, "DOWNSIDE": C.DOWNSIDE,
    "P2_TITLE": C.P2_TITLE, "H_A1": C.H_A1, "A1_PARAGRAPHS": "".join(C.A1_PARAGRAPHS),
    "H_A2": C.H_A2, "A2_PARAGRAPHS": C.A2_PARAGRAPHS,
    "H_C2": C.H_C2, "C2_TITLE": C.C2_TITLE, "C2_SUB": C.C2_SUB, "C2_IMG": f"{OUT}/c2_crop.png",
    "C2_COMMENT": C.C2_COMMENT, "W1": W1, "W2": W2, "SOURCE_LINE": C.SOURCE_LINE,
}

tpl = open("/home/claude/template.html").read()
doc = tpl
for k, v in fill.items():
    doc = doc.replace("{{" + k + "}}", str(v))
assert "{{" not in doc, "unfilled placeholder"
assert "—" not in doc, "em dash"
open(f"{OUT}/doc.html", "w").write(doc)
from weasyprint import HTML
HTML(f"{OUT}/doc.html").write_pdf(OUT_PDF)
from pdf2image import convert_from_path
pages = convert_from_path(OUT_PDF, dpi=100)
for i, p in enumerate(pages):
    p.save(f"{OUT}/page{i+1}.png")
print("pages:", len(pages))

# ---- fill.json for build_pptx.js (plain text, no entities)
def plain(s):
    return html.unescape(re.sub(r"<[^>]+>", "", s)).replace("−", "-")
paras = lambda s: [plain(p) for p in re.findall(r"<p>(.*?)</p>", s, re.S)]
disc = [plain(p) for p in re.findall(r"<p>(.*?)</p>", tpl.split('<div class="disc-head">')[1], re.S)]
aspect = lambda p: (lambda im: im.size[1] / im.size[0])(Image.open(p))
fj = {
    "LOGO": "/home/claude/syz_logo_hq.png", "GRADBAR": "/home/claude/syz_gradbar.png",
    "DOC_TYPE": C.DOC_TYPE, "DATE": C.DATE, "TITLE": plain(C.TITLE),
    "QUOTE": plain(C.QUOTE), "QUOTE_WHO": plain(C.QUOTE_WHO), "COMPANY_INTRO": plain(C.COMPANY_INTRO),
    "TAKEAWAYS": [{"tag": t, "label": l, "text": plain(x)} for t, l, x in C.TAKEAWAYS],
    "KPIS": [{"label": plain(l), "value": plain(v), "sub": plain(u), "sign": s} for l, v, u, s in C.KPIS],
    "H_P1": plain(C.H_P1), "P1_PARAGRAPH": paras(C.P1_PARAGRAPH)[0],
    "C1_TITLE": plain(C.C1_TITLE), "C1_SUB": plain(C.C1_SUB), "C1_IMG": f"{OUT}/c1_crop.png",
    "C1_ASPECT": aspect(f"{OUT}/c1_crop.png"), "W1": C.W1_PPTX, "C1_COMMENT": paras(C.C1_COMMENT)[0],
    "BASE_CASE": plain(C.BASE_CASE), "UPSIDE": plain(C.UPSIDE), "DOWNSIDE": plain(C.DOWNSIDE),
    "P2_TITLE": C.P2_TITLE, "H_A1": plain(C.H_A1), "A1_PARAGRAPHS": [paras(p)[0] for p in C.A1_PARAGRAPHS],
    "H_A2": plain(C.H_A2), "A2_PARAGRAPH": paras(C.A2_PARAGRAPHS)[0],
    "H_C2": plain(C.H_C2), "C2_TITLE": plain(C.C2_TITLE), "C2_SUB": plain(C.C2_SUB),
    "C2_IMG": f"{OUT}/c2_crop.png", "C2_ASPECT": aspect(f"{OUT}/c2_crop.png"), "W2": C.W2_PPTX,
    "C2_COMMENT": paras(C.C2_COMMENT)[0], "SOURCE_LINE": plain(C.SOURCE_LINE), "DISCLAIMER": disc,
}
assert len(disc) == 7
json.dump(fj, open(f"{OUT}/fill.json", "w"), ensure_ascii=False, indent=1)
print("fill.json written")
