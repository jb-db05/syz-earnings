"""build_pdf.py: fill the Syz template from content.py, render the PDF, rasterise pages, write fill.json for the PPTX."""
import sys, re, json, html as H
sys.path.insert(0, "/home/claude/vrtx")
import content as c
from PIL import Image

OUT = "/home/claude/vrtx/Earnings_Update_VRTX_Q32026.pdf"
C1_IMG, C2_IMG = "/home/claude/vrtx/c1_crop.png", "/home/claude/vrtx/c2_crop.png"
P = lambda t: f"<p>{t}</p>"

fill = {
    "DOC_TYPE": "Earnings update", "DATE": c.DATE, "TITLE": c.TITLE,
    "QUOTE_BLOCK": (f'<div class="quote"><p>&ldquo;{c.QUOTE}&rdquo;</p><div class="who">{c.QUOTE_WHO}</div></div>' if c.QUOTE else ""),
    "COMPANY_INTRO": c.COMPANY_INTRO,
    "TAKEAWAYS": "\n".join(f'<li><span class="tag {t}">{l}</span><span class="t">{x}</span></li>' for t, l, x in c.TAKEAWAYS),
    "KPI_TILES": "\n".join(f'<td><div class="lbl">{l}</div><div class="val">{v}</div><div class="sub {s}">{u}</div></td>' for l, v, u, s in c.KPIS),
    "H_P1": c.H_P1, "P1_PARAGRAPH": P(c.P1),
    "C1_TITLE": c.C1_TITLE, "C1_SUB": c.C1_SUB, "C1_IMG": C1_IMG, "C1_COMMENT": P(c.C1),
    "BASE_CASE": c.BASE_CASE, "UPSIDE": c.UPSIDE, "DOWNSIDE": c.DOWNSIDE,
    "UP_HEAD": "What would strengthen our view", "DOWN_HEAD": "What would change our view",
    "P2_TITLE": "Beyond the key takeaways",
    "H_A1": c.H_A1, "A1_PARAGRAPHS": "".join(P(x) for x in c.A1),
    "H_A2": c.H_A2, "A2_PARAGRAPHS": P(c.A2),
    "H_C2": c.H_C2, "C2_TITLE": c.C2_TITLE, "C2_SUB": c.C2_SUB, "C2_IMG": C2_IMG, "C2_COMMENT": P(c.C2),
    "W1": c.W1, "W2": c.W2, "SOURCE_LINE": c.SOURCE_LINE,
}
tpl = open("/home/claude/template.html").read()
html = tpl
for k, v in fill.items():
    html = html.replace("{{" + k + "}}", str(v))
assert "{{" not in html, re.findall(r"\{\{(\w+)\}\}", html)
assert "—" not in html, "em dash"
open("/home/claude/vrtx/doc.html", "w").write(html)
from weasyprint import HTML
HTML("/home/claude/vrtx/doc.html").write_pdf(OUT)
from pdf2image import convert_from_path
pages = convert_from_path(OUT, dpi=100)
for i, p in enumerate(pages):
    p.save(f"/home/claude/vrtx/page{i+1}.png")
print("pages:", len(pages))

# ---- fill.json for build_pptx.js (plain text, no entities)
u = lambda s: H.unescape(s).replace("−", "-")
disc = re.findall(r"<p>(This communication has been issued.*?)</p>.*?</div>", tpl, re.S)[0]
DISC = [u(re.sub(r"<[^>]+>", "", p)) for p in re.findall(r"<p>(.*?)</p>", tpl.split('<div class="disc-head">Disclaimer</div>')[1], re.S)]
asp = lambda p: (lambda im: im.size[1] / im.size[0])(Image.open(p))
fj = {
    "LOGO": "/home/claude/syz_logo_hq.png", "GRADBAR": "/home/claude/syz_gradbar.png",
    "DOC_TYPE": "Earnings update", "DATE": c.DATE, "TITLE": u(c.TITLE), "QUOTE": u(c.QUOTE), "QUOTE_WHO": u(c.QUOTE_WHO),
    "COMPANY_INTRO": u(c.COMPANY_INTRO),
    "TAKEAWAYS": [{"tag": t, "label": l, "text": u(x)} for t, l, x in c.TAKEAWAYS],
    "KPIS": [{"label": u(l), "value": u(v), "sub": u(s2), "sign": s} for l, v, s2, s in c.KPIS],
    "H_P1": u(c.H_P1), "P1_PARAGRAPH": u(c.P1),
    "C1_TITLE": u(c.C1_TITLE), "C1_SUB": u(c.C1_SUB), "C1_IMG": C1_IMG, "C1_ASPECT": asp(C1_IMG), "W1": c.W1_PPTX,
    "C1_COMMENT": u(c.C1), "BASE_CASE": u(c.BASE_CASE), "UPSIDE": u(c.UPSIDE), "DOWNSIDE": u(c.DOWNSIDE),
    "P2_TITLE": "Beyond the key takeaways", "H_A1": u(c.H_A1), "A1_PARAGRAPHS": [u(x) for x in c.A1],
    "H_A2": u(c.H_A2), "A2_PARAGRAPH": u(c.A2), "H_C2": u(c.H_C2), "C2_TITLE": u(c.C2_TITLE), "C2_SUB": u(c.C2_SUB),
    "C2_IMG": C2_IMG, "C2_ASPECT": asp(C2_IMG), "W2": c.W2_PPTX, "C2_COMMENT": u(c.C2),
    "SOURCE_LINE": u(c.SOURCE_LINE), "DISCLAIMER": DISC,
}
assert len(DISC) == 7
json.dump(fj, open("/home/claude/vrtx/fill.json", "w"), indent=1, ensure_ascii=False)
print("fill.json written")
