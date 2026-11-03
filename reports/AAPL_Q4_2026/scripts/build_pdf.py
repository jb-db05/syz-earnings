"""build_pdf.py: fill the Syz template from content.py, render the PDF, rasterise, write fill.json for the PPTX."""
import sys, json, html, re
sys.path.insert(0, "/home/claude/aapl")
from PIL import Image
import content as C

OUT = "/home/claude/aapl/Earnings_Update_AAPL_Q4_2026"
C1, C2 = "/home/claude/aapl/c1_crop.png", "/home/claude/aapl/c2_crop.png"
DISC_TPL = "/home/claude/template.html"

tags = "\n".join(f'<li><span class="tag {c}">{l}</span><span class="t">{t}</span></li>' for c, l, t in C.TAKEAWAYS)
tiles = "\n".join(f'<td><div class="lbl">{l}</div><div class="val">{v}</div><div class="sub {s}">{u}</div></td>'
                  for l, v, u, s in C.KPIS)
quote = (f'<div class="quote"><p>&ldquo;{C.QUOTE}&rdquo;</p><div class="who">{C.QUOTE_WHO}</div></div>'
         if C.QUOTE else "")
fill = {
    "DOC_TYPE": C.DOC_TYPE, "DATE": C.DATE, "TITLE": C.TITLE, "QUOTE_BLOCK": quote, "COMPANY_INTRO": C.COMPANY_INTRO,
    "TAKEAWAYS": tags, "KPI_TILES": tiles, "H_P1": C.H_P1, "P1_PARAGRAPH": C.P1_PARAGRAPH,
    "C1_TITLE": C.C1_TITLE, "C1_SUB": C.C1_SUB, "C1_IMG": C1, "C1_COMMENT": C.C1_COMMENT,
    "BASE_CASE": C.BASE_CASE, "UP_HEAD": C.UP_HEAD, "DOWN_HEAD": C.DOWN_HEAD, "UPSIDE": C.UPSIDE, "DOWNSIDE": C.DOWNSIDE,
    "P2_TITLE": C.P2_TITLE, "H_A1": C.H_A1, "A1_PARAGRAPHS": "\n".join(C.A1_PARAGRAPHS), "H_A2": C.H_A2,
    "A2_PARAGRAPHS": C.A2_PARAGRAPHS, "H_C2": C.H_C2, "C2_TITLE": C.C2_TITLE, "C2_SUB": C.C2_SUB, "C2_IMG": C2,
    "C2_COMMENT": C.C2_COMMENT, "SOURCE_LINE": C.SOURCE_LINE, "W1": C.W1, "W2": C.W2,
}
tpl = open(DISC_TPL).read()
doc = tpl
for k, v in fill.items():
    doc = doc.replace("{{" + k + "}}", str(v))
assert "{{" not in doc, "unfilled placeholder"
assert "—" not in doc, "em dash"
open("/home/claude/aapl/doc.html", "w").write(doc)

from weasyprint import HTML
HTML("/home/claude/aapl/doc.html").write_pdf(OUT + ".pdf")
from pdf2image import convert_from_path
pages = convert_from_path(OUT + ".pdf", dpi=100)
for i, p in enumerate(pages):
    p.save(f"/home/claude/aapl/page{i+1}.png")
print("pages:", len(pages))

# ---- fill.json for build_pptx.js (plain text, no entities)
def plain(s):
    s = re.sub(r"</?p>", "", s)
    return html.unescape(s).replace("−", "-").strip()
disc = [plain(p) for p in re.findall(r'<div class="legal">.*?</div>\s*<div class="disc-head">Disclaimer</div>(.*?)</div>',
                                    tpl, re.S)[0].split("</p>") if p.strip()]
assert len(disc) == 7
asp = lambda p: (lambda im: im.size[1] / im.size[0])(Image.open(p))
fj = {
    "LOGO": "/home/claude/syz_logo_hq.png", "GRADBAR": "/home/claude/syz_gradbar.png",
    "DOC_TYPE": C.DOC_TYPE, "DATE": C.DATE, "TITLE": plain(C.TITLE), "QUOTE": plain(C.QUOTE),
    "QUOTE_WHO": plain(C.QUOTE_WHO), "COMPANY_INTRO": plain(C.COMPANY_INTRO),
    "TAKEAWAYS": [{"tag": c, "label": l, "text": plain(t)} for c, l, t in C.TAKEAWAYS],
    "KPIS": [{"label": plain(l), "value": plain(v), "sub": plain(u), "sign": s} for l, v, u, s in C.KPIS],
    "H_P1": plain(C.H_P1), "P1_PARAGRAPH": plain(C.P1_PARAGRAPH), "C1_TITLE": plain(C.C1_TITLE),
    "C1_SUB": plain(C.C1_SUB), "C1_IMG": C1, "C1_ASPECT": asp(C1), "W1": C.W1_PPTX, "C1_COMMENT": plain(C.C1_COMMENT),
    "BASE_CASE": plain(C.BASE_CASE), "UPSIDE": plain(C.UPSIDE), "DOWNSIDE": plain(C.DOWNSIDE),
    "UPSIDE_HEAD": C.UP_HEAD, "DOWNSIDE_HEAD": C.DOWN_HEAD, "P2_TITLE": C.P2_TITLE,
    "H_A1": plain(C.H_A1), "A1_PARAGRAPHS": [plain(p) for p in C.A1_PARAGRAPHS], "H_A2": plain(C.H_A2),
    "A2_PARAGRAPH": plain(C.A2_PARAGRAPHS), "H_C2": plain(C.H_C2), "C2_TITLE": plain(C.C2_TITLE),
    "C2_SUB": plain(C.C2_SUB), "C2_IMG": C2, "C2_ASPECT": asp(C2), "W2": C.W2_PPTX, "C2_COMMENT": plain(C.C2_COMMENT),
    "SOURCE_LINE": plain(C.SOURCE_LINE), "DISCLAIMER": disc,
}
json.dump(fj, open("/home/claude/aapl/fill.json", "w"), ensure_ascii=False, indent=1)
print("fill.json written")
