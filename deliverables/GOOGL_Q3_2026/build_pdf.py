"""build_pdf.py: fill the Syz template from content.py, render the PDF, rasterise, write fill.json for the PPTX."""
import html, json, re, sys
sys.path.insert(0, "/home/claude/work")
from PIL import Image
import content as c

OUT = "Earnings_Update_GOOGL_Q32026"
W1, W2 = 74, 94            # PDF chart widths, % of text width
W1_PPTX, W2_PPTX = 66, 88  # PowerPoint chart widths
C1_IMG, C2_IMG = "/home/claude/work/c1_crop.png", "/home/claude/work/c2_crop.png"

tpl = open("/home/claude/template.html").read()
quote_block = (f'<div class="quote"><p>&ldquo;{c.QUOTE}&rdquo;</p><div class="who">{c.QUOTE_WHO}</div></div>'
               if c.QUOTE else "")
takeaways = "\n".join(f'<li><span class="tag {t}">{l}</span><span class="t">{x}</span></li>' for t, l, x in c.TAKEAWAYS)
tiles = "\n".join(f'<td><div class="lbl">{l}</div><div class="val">{v}</div><div class="sub {s}">{u}</div></td>'
                  for l, v, u, s in c.KPIS)
P = lambda s: f"<p>{s}</p>"
fill = {
    "DOC_TYPE": c.DOC_TYPE, "DATE": c.DATE, "TITLE": c.TITLE, "QUOTE_BLOCK": quote_block,
    "COMPANY_INTRO": c.COMPANY_INTRO, "TAKEAWAYS": takeaways, "KPI_TILES": tiles,
    "H_P1": c.H_P1, "P1_PARAGRAPH": P(c.P1_PARAGRAPH),
    "C1_TITLE": c.C1_TITLE, "C1_SUB": c.C1_SUB, "C1_IMG": C1_IMG, "C1_COMMENT": P(c.C1_COMMENT),
    "BASE_CASE": c.BASE_CASE, "UPSIDE": c.UPSIDE, "DOWNSIDE": c.DOWNSIDE,
    "P2_TITLE": c.P2_TITLE, "H_A1": c.H_A1, "A1_PARAGRAPHS": "\n".join(P(p) for p in c.A1_PARAGRAPHS),
    "H_A2": c.H_A2, "A2_PARAGRAPHS": P(c.A2_PARAGRAPH),
    "H_C2": c.H_C2, "C2_TITLE": c.C2_TITLE, "C2_SUB": c.C2_SUB, "C2_IMG": C2_IMG, "C2_COMMENT": P(c.C2_COMMENT),
    "W1": W1, "W2": W2, "SOURCE_LINE": c.SOURCE_LINE,
}
doc = tpl
for k, v in fill.items():
    doc = doc.replace("{{" + k + "}}", str(v))
assert "{{" not in doc, "unfilled placeholder"
assert "—" not in doc, "em dash"
open("doc.html", "w").write(doc)

from weasyprint import HTML
HTML("doc.html").write_pdf(OUT + ".pdf")
from pdf2image import convert_from_path
pages = convert_from_path(OUT + ".pdf", dpi=100)
for i, p in enumerate(pages):
    p.save(f"page{i+1}.png")
print("pages:", len(pages))

# fill.json for build_pptx.js: plain text, same content
u = lambda s: html.unescape(s).replace("−", "-")
legal = re.search(r'<div class="legal">(.*?)</div>\s*</body>', tpl, re.S).group(1)
disclaimer = [u(p) for p in re.findall(r"<p>(.*?)</p>", legal, re.S)]
assert len(disclaimer) == 7
aspect = lambda p: (lambda im: im.size[1] / im.size[0])(Image.open(p))
fj = {
    "LOGO": "/home/claude/syz_logo_hq.png", "GRADBAR": "/home/claude/syz_gradbar.png",
    "DOC_TYPE": c.DOC_TYPE, "DATE": c.DATE, "TITLE": u(c.TITLE), "QUOTE": u(c.QUOTE), "QUOTE_WHO": u(c.QUOTE_WHO),
    "COMPANY_INTRO": u(c.COMPANY_INTRO),
    "TAKEAWAYS": [{"tag": t, "label": l, "text": u(x)} for t, l, x in c.TAKEAWAYS],
    "KPIS": [{"label": l, "value": u(v), "sub": u(s), "sign": g} for l, v, s, g in c.KPIS],
    "H_P1": u(c.H_P1), "P1_PARAGRAPH": u(c.P1_PARAGRAPH),
    "C1_TITLE": u(c.C1_TITLE), "C1_SUB": u(c.C1_SUB), "C1_IMG": C1_IMG, "C1_ASPECT": aspect(C1_IMG), "W1": W1_PPTX,
    "C1_COMMENT": u(c.C1_COMMENT), "BASE_CASE": u(c.BASE_CASE), "UPSIDE": u(c.UPSIDE), "DOWNSIDE": u(c.DOWNSIDE),
    "P2_TITLE": c.P2_TITLE, "H_A1": u(c.H_A1), "A1_PARAGRAPHS": [u(p) for p in c.A1_PARAGRAPHS],
    "H_A2": u(c.H_A2), "A2_PARAGRAPH": u(c.A2_PARAGRAPH), "H_C2": u(c.H_C2),
    "C2_TITLE": u(c.C2_TITLE), "C2_SUB": u(c.C2_SUB), "C2_IMG": C2_IMG, "C2_ASPECT": aspect(C2_IMG), "W2": W2_PPTX,
    "C2_COMMENT": u(c.C2_COMMENT), "SOURCE_LINE": u(c.SOURCE_LINE), "DISCLAIMER": disclaimer,
}
json.dump(fj, open("fill.json", "w"), ensure_ascii=False, indent=1)
print("fill.json written")
