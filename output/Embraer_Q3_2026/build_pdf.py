"""build_pdf.py: fill the template, render the PDF, rasterise, write fill.json. Run after build_charts.py."""
import json, html, re, sys
from PIL import Image
import content as c

OUT = "/home/claude/Earnings_Update_EMBJ3_Q32026"
W1, W2 = int(sys.argv[1]) if len(sys.argv) > 1 else 74, int(sys.argv[2]) if len(sys.argv) > 2 else 92
TEMPLATE = "/home/claude/template.html"

def p(t): return f"<p>{t}</p>"
tk = "\n".join(f'<li><span class="tag {g}">{l}</span><span class="t">{t}</span></li>' for g, l, t in c.TAKEAWAYS)
kp = "\n".join(f'<td><div class="lbl">{l}</div><div class="val">{v}</div><div class="sub {g}">{s}</div></td>'
               for l, v, s, g in c.KPIS)
quote = (f'<div class="quote"><p>&ldquo;{c.QUOTE}&rdquo;</p><div class="who">{c.QUOTE_WHO}</div></div>' if c.QUOTE else "")
fill = {
    "DOC_TYPE": "Earnings update", "DATE": c.DATE, "TITLE": c.TITLE, "QUOTE_BLOCK": quote,
    "COMPANY_INTRO": c.COMPANY_INTRO, "TAKEAWAYS": tk, "KPI_TILES": kp, "H_P1": c.H_P1, "P1_PARAGRAPH": p(c.P1),
    "C1_TITLE": c.C1_TITLE, "C1_SUB": c.C1_SUB, "C1_IMG": "/home/claude/c1_crop.png", "C1_COMMENT": p(c.C1_COMMENT),
    "BASE_CASE": c.BASE_CASE, "UP_HEAD": "What would strengthen our view", "DOWN_HEAD": "What would change our view",
    "UPSIDE": c.UPSIDE, "DOWNSIDE": c.DOWNSIDE, "P2_TITLE": c.P2_TITLE, "H_A1": c.H_A1,
    "A1_PARAGRAPHS": "\n".join(p(a) for a in c.A1), "H_A2": c.H_A2, "A2_PARAGRAPHS": p(c.A2), "H_C2": c.H_C2,
    "C2_TITLE": c.C2_TITLE, "C2_SUB": c.C2_SUB, "C2_IMG": "/home/claude/c2_crop.png", "C2_COMMENT": p(c.C2_COMMENT),
    "SOURCE_LINE": c.SOURCE_LINE, "W1": W1, "W2": W2,
}
tpl = open(TEMPLATE).read()
doc = tpl
for k, v in fill.items():
    doc = doc.replace("{{" + k + "}}", str(v))
assert "{{" not in doc, "unfilled placeholder"
assert "—" not in doc, "em dash"
open("/home/claude/doc.html", "w").write(doc)
from weasyprint import HTML
HTML("/home/claude/doc.html").write_pdf(OUT + ".pdf")
from pdf2image import convert_from_path
pages = convert_from_path(OUT + ".pdf", dpi=100)
for i, pg in enumerate(pages): pg.save(f"/home/claude/page{i+1}.png")
print("pages:", len(pages))

# ---- fill.json for the PPTX (plain text)
u = lambda s: html.unescape(s).replace("−", "-")
disc = [u(re.sub(r"<.*?>", "", m)) for m in re.findall(r'<div class="legal">.*?</div>\s*</body>', tpl, re.S)[0].split("<p>")[1:]]
disc = [d.strip() for d in disc]
asp = lambda f: (lambda im: im.size[1] / im.size[0])(Image.open(f))
fj = {
    "LOGO": "/home/claude/syz_logo_hq.png", "GRADBAR": "/home/claude/syz_gradbar.png", "DOC_TYPE": "Earnings update",
    "DATE": c.DATE, "TITLE": u(c.TITLE), "QUOTE": u(c.QUOTE), "QUOTE_WHO": u(c.QUOTE_WHO), "COMPANY_INTRO": u(c.COMPANY_INTRO),
    "TAKEAWAYS": [{"tag": g, "label": l, "text": u(t)} for g, l, t in c.TAKEAWAYS],
    "KPIS": [{"label": u(l), "value": u(v), "sub": u(s), "sign": g} for l, v, s, g in c.KPIS],
    "H_P1": u(c.H_P1), "P1_PARAGRAPH": u(c.P1), "C1_TITLE": u(c.C1_TITLE), "C1_SUB": u(c.C1_SUB),
    "C1_IMG": "/home/claude/c1_crop.png", "C1_ASPECT": asp("/home/claude/c1_crop.png"), "W1": 66,
    "C1_COMMENT": u(c.C1_COMMENT), "BASE_CASE": u(c.BASE_CASE), "UPSIDE": u(c.UPSIDE), "DOWNSIDE": u(c.DOWNSIDE),
    "P2_TITLE": c.P2_TITLE, "H_A1": u(c.H_A1), "A1_PARAGRAPHS": [u(a) for a in c.A1], "H_A2": u(c.H_A2),
    "A2_PARAGRAPH": u(c.A2), "H_C2": u(c.H_C2), "C2_TITLE": u(c.C2_TITLE), "C2_SUB": u(c.C2_SUB),
    "C2_IMG": "/home/claude/c2_crop.png", "C2_ASPECT": asp("/home/claude/c2_crop.png"), "W2": 88,
    "C2_COMMENT": u(c.C2_COMMENT), "SOURCE_LINE": u(c.SOURCE_LINE), "DISCLAIMER": disc,
}
json.dump(fj, open("/home/claude/fill.json", "w"), ensure_ascii=False, indent=1)
print("disclaimer paragraphs:", len(disc))
