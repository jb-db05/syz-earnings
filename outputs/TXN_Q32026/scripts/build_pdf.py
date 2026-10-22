"""build_pdf.py: fill the Syz template from content.py, render the PDF, rasterise, write fill.json."""
import sys, re, json, html as H
sys.path.insert(0, "/home/claude/txn")
from PIL import Image
import content as c

OUT = f"Earnings_Update_{c.TICKER}_{c.Q}"
tpl = open("/home/claude/template.html").read()
disc = [H.unescape(re.sub(r"<.*?>", "", p)) for p in re.findall(r"<p>(.*?)</p>", tpl.split('class="disc-head"')[1], re.S)]

quote = "" if not c.QUOTE else (f'<div class="quote"><p>&ldquo;{c.QUOTE}&rdquo;</p><div class="who">{c.QUOTE_WHO}</div></div>')
fill = {
    "DOC_TYPE": "Earnings update", "THEME": c.THEME, "DATE": c.DATE, "TITLE": c.TITLE, "QUOTE_BLOCK": quote,
    "TAKEAWAYS": "\n".join(f'<li><span class="tag {t}">{l}</span><span class="t">{x}</span></li>' for t, l, x in c.TAKEAWAYS),
    "KPI_TILES": "\n".join(f'<td><div class="lbl">{l}</div><div class="val">{v}</div><div class="sub {s}">{u}</div></td>' for l, v, u, s in c.KPIS),
    "H_P1": c.H_P1, "P1_PARAGRAPH": f"<p>{c.P1}</p>",
    "C1_TITLE": c.C1_TITLE, "C1_SUB": c.C1_SUB, "C1_IMG": "/home/claude/txn/c1_crop.png", "C1_COMMENT": f"<p>{c.C1_COMMENT}</p>",
    "BASE_CASE": c.BASE_CASE, "UPSIDE": c.UPSIDE, "DOWNSIDE": c.DOWNSIDE, "P2_TITLE": c.P2_TITLE,
    "H_A1": c.H_A1, "A1_PARAGRAPHS": "".join(f"<p>{p}</p>" for p in c.A1),
    "H_A2": c.H_A2, "A2_PARAGRAPHS": f"<p>{c.A2}</p>",
    "H_C2": c.H_C2, "C2_TITLE": c.C2_TITLE, "C2_SUB": c.C2_SUB, "C2_IMG": "/home/claude/txn/c2_crop.png",
    "C2_COMMENT": f"<p>{c.C2_COMMENT}</p>", "SOURCE_LINE": c.SOURCE_LINE, "W1": c.W1, "W2": c.W2,
}
doc = tpl
for k, v in fill.items():
    doc = doc.replace("{{" + k + "}}", str(v))
assert "{{" not in doc, "unfilled placeholder"
assert "—" not in doc, "em dash"
open("doc.html", "w").write(doc)
from weasyprint import HTML; HTML("doc.html").write_pdf(OUT + ".pdf")
from pdf2image import convert_from_path
pages = convert_from_path(OUT + ".pdf", dpi=100)
for i, p in enumerate(pages): p.save(f"page{i+1}.png")
print("pages:", len(pages))

u = lambda s: H.unescape(s).replace("−", "-")
asp = lambda p: (lambda im: im.size[1] / im.size[0])(Image.open(p))
pptx = {
    "LOGO": "/home/claude/syz_logo_hq.png", "GRADBAR": "/home/claude/syz_gradbar.png",
    "DOC_TYPE": "Earnings update", "THEME": c.THEME, "DATE": c.DATE, "TITLE": u(c.TITLE),
    "QUOTE": u(c.QUOTE), "QUOTE_WHO": u(c.QUOTE_WHO),
    "TAKEAWAYS": [{"tag": t, "label": l, "text": u(x)} for t, l, x in c.TAKEAWAYS],
    "KPIS": [{"label": l, "value": v, "sub": u(s2), "sign": s} for l, v, s2, s in c.KPIS],
    "H_P1": u(c.H_P1), "P1_PARAGRAPH": u(c.P1), "C1_TITLE": u(c.C1_TITLE), "C1_SUB": u(c.C1_SUB),
    "C1_IMG": fill["C1_IMG"], "C1_ASPECT": asp(fill["C1_IMG"]), "W1": c.W1_PPTX, "C1_COMMENT": u(c.C1_COMMENT),
    "BASE_CASE": u(c.BASE_CASE), "UPSIDE": u(c.UPSIDE), "DOWNSIDE": u(c.DOWNSIDE), "P2_TITLE": c.P2_TITLE,
    "H_A1": u(c.H_A1), "A1_PARAGRAPHS": [u(p) for p in c.A1], "H_A2": u(c.H_A2), "A2_PARAGRAPH": u(c.A2),
    "H_C2": u(c.H_C2), "C2_TITLE": u(c.C2_TITLE), "C2_SUB": u(c.C2_SUB), "C2_IMG": fill["C2_IMG"],
    "C2_ASPECT": asp(fill["C2_IMG"]), "W2": c.W2_PPTX, "C2_COMMENT": u(c.C2_COMMENT),
    "SOURCE_LINE": u(c.SOURCE_LINE), "DISCLAIMER": disc,
}
json.dump(pptx, open("fill.json", "w"), indent=1, ensure_ascii=False)
print("disclaimer paragraphs:", len(disc))
