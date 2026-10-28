"""Epiroc Q3 2026: content.py -> HTML template -> PDF (+ page PNGs) and fill.json for build_pptx.js."""
import html, json, re
from PIL import Image
import content as c

OUT_PDF = "Earnings_Update_EPIA_Q32026.pdf"
W1, W2 = 74, 94          # PDF chart widths (% of text width)
W1_PPTX, W2_PPTX = 66, 88
TEMPLATE = "/home/claude/template.html"

li = "\n".join(f'<li><span class="tag {t}">{lab}</span><span class="t">{txt}</span></li>' for t, lab, txt in c.TAKEAWAYS)
tiles = "\n".join(f'<td><div class="lbl">{l}</div><div class="val">{v}</div><div class="sub {s}">{sub}</div></td>'
                  for l, v, sub, s in c.KPIS)
quote = (f'<div class="quote"><p>&ldquo;{c.QUOTE}&rdquo;</p><div class="who">{c.QUOTE_WHO}</div></div>'
         if c.QUOTE else "")
P = lambda t: f"<p>{t}</p>"

fill = {
    "DOC_TYPE": "Earnings update", "DATE": c.DATE, "TITLE": c.TITLE, "QUOTE_BLOCK": quote,
    "COMPANY_INTRO": c.COMPANY_INTRO, "TAKEAWAYS": li, "KPI_TILES": tiles,
    "H_P1": c.H_P1, "P1_PARAGRAPH": P(c.P1), "C1_TITLE": c.C1_TITLE, "C1_SUB": c.C1_SUB,
    "C1_IMG": "/home/claude/epi/c1_crop.png", "C1_COMMENT": P(c.C1_COMMENT),
    "BASE_CASE": c.BASE_CASE, "UPSIDE": c.UPSIDE, "DOWNSIDE": c.DOWNSIDE, "P2_TITLE": c.P2_TITLE,
    "H_A1": c.H_A1, "A1_PARAGRAPHS": "".join(P(p) for p in c.A1), "H_A2": c.H_A2, "A2_PARAGRAPHS": P(c.A2),
    "H_C2": c.H_C2, "C2_TITLE": c.C2_TITLE, "C2_SUB": c.C2_SUB, "C2_IMG": "/home/claude/epi/c2_crop.png",
    "C2_COMMENT": P(c.C2_COMMENT), "W1": W1, "W2": W2, "SOURCE_LINE": c.SOURCE_LINE,
}

tpl = open(TEMPLATE).read()
doc = tpl
for k, v in fill.items():
    doc = doc.replace("{{" + k + "}}", str(v))
assert "{{" not in doc, "unfilled placeholder"
assert "—" not in doc, "em dash"
open("doc.html", "w").write(doc)

from weasyprint import HTML
HTML("doc.html").write_pdf(OUT_PDF)
from pdf2image import convert_from_path
pages = convert_from_path(OUT_PDF, dpi=100)
for i, p in enumerate(pages):
    p.save(f"page{i + 1}.png")
print("pages:", len(pages))

# ---- fill.json for the PowerPoint (plain text)
def plain(s):
    s = html.unescape(re.sub(r"<[^>]+>", "", s))
    return s.replace("−", "-")

aspect = lambda p: Image.open(p).size[1] / Image.open(p).size[0]
disc = re.findall(r'<div class="disc-head">Disclaimer</div>(.*?)</div>', tpl, re.S)[0]
fj = {
    "LOGO": "/home/claude/syz_logo_hq.png", "GRADBAR": "/home/claude/syz_gradbar.png",
    "DOC_TYPE": "Earnings update", "DATE": c.DATE, "TITLE": plain(c.TITLE), "QUOTE": plain(c.QUOTE),
    "QUOTE_WHO": plain(c.QUOTE_WHO), "COMPANY_INTRO": plain(c.COMPANY_INTRO),
    "TAKEAWAYS": [{"tag": t, "label": lab, "text": plain(txt)} for t, lab, txt in c.TAKEAWAYS],
    "KPIS": [{"label": plain(l), "value": plain(v), "sub": plain(s), "sign": g} for l, v, s, g in c.KPIS],
    "H_P1": c.H_P1, "P1_PARAGRAPH": plain(c.P1), "C1_TITLE": plain(c.C1_TITLE), "C1_SUB": plain(c.C1_SUB),
    "C1_IMG": fill["C1_IMG"], "C1_ASPECT": aspect(fill["C1_IMG"]), "W1": W1_PPTX, "C1_COMMENT": plain(c.C1_COMMENT),
    "BASE_CASE": plain(c.BASE_CASE), "UPSIDE": plain(c.UPSIDE), "DOWNSIDE": plain(c.DOWNSIDE),
    "P2_TITLE": c.P2_TITLE, "H_A1": c.H_A1, "A1_PARAGRAPHS": [plain(p) for p in c.A1], "H_A2": c.H_A2,
    "A2_PARAGRAPH": plain(c.A2), "H_C2": c.H_C2, "C2_TITLE": plain(c.C2_TITLE), "C2_SUB": plain(c.C2_SUB),
    "C2_IMG": fill["C2_IMG"], "C2_ASPECT": aspect(fill["C2_IMG"]), "W2": W2_PPTX, "C2_COMMENT": plain(c.C2_COMMENT),
    "SOURCE_LINE": plain(c.SOURCE_LINE),
    "DISCLAIMER": [plain(p) for p in re.findall(r"<p>(.*?)</p>", disc, re.S)],
}
assert len(fj["DISCLAIMER"]) == 7
json.dump(fj, open("fill.json", "w"), ensure_ascii=False, indent=1)
print("fill.json written")
