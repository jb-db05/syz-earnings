"""Fill the template, render PDF, rasterise, write fill.json. python3 build_pdf.py"""
import sys, json, html as H, re
sys.path.insert(0, "/home/claude/rwe"); import content as c
from PIL import Image
OUT = "Earnings_Update_RWE_Q32026"
P = lambda ps: "".join(f"<p>{p}</p>" for p in ps)
fill = {
 "DOC_TYPE": "Earnings update", "DATE": c.DATE, "TITLE": c.TITLE,
 "QUOTE_BLOCK": f'<div class="quote"><p>&ldquo;{c.QUOTE}&rdquo;</p><div class="who">{c.QUOTE_WHO}</div></div>' if c.QUOTE else "",
 "COMPANY_INTRO": c.COMPANY_INTRO,
 "TAKEAWAYS": "\n".join(f'<li><span class="tag {t}">{l}</span><span class="t">{x}</span></li>' for t, l, x in c.TAKEAWAYS),
 "KPI_TILES": "\n".join(f'<td><div class="lbl">{a}</div><div class="val">{b}</div><div class="sub {s}">{d}</div></td>' for a, b, d, s in c.KPIS),
 "H_P1": c.H_P1, "P1_PARAGRAPH": P(c.P1), "C1_TITLE": c.C1_TITLE, "C1_SUB": c.C1_SUB,
 "C1_IMG": "/home/claude/rwe/c1_crop.png", "C1_COMMENT": P(c.C1_COMMENT),
 "BASE_CASE": c.BASE_CASE, "UPSIDE": c.UPSIDE, "DOWNSIDE": c.DOWNSIDE, "UP_HEAD": c.UP_HEAD, "DOWN_HEAD": c.DOWN_HEAD,
 "P2_TITLE": "Beyond the key takeaways", "H_A1": c.H_A1, "A1_PARAGRAPHS": P(c.A1), "H_A2": c.H_A2, "A2_PARAGRAPHS": P(c.A2),
 "H_C2": c.H_C2, "C2_TITLE": c.C2_TITLE, "C2_SUB": c.C2_SUB, "C2_IMG": "/home/claude/rwe/c2_crop.png", "C2_COMMENT": P(c.C2_COMMENT),
 "W1": c.W1, "W2": c.W2, "SOURCE_LINE": c.SOURCE_LINE,
}
tpl = open("/home/claude/tpl.html").read()
doc = tpl
for k, v in fill.items(): doc = doc.replace("{{" + k + "}}", str(v))
assert "{{" not in doc, re.findall(r"\{\{(\w+)\}\}", doc)
assert "—" not in doc and "&mdash;" not in doc
open("doc.html", "w").write(doc)
from weasyprint import HTML; HTML("doc.html").write_pdf(OUT + ".pdf")
from pdf2image import convert_from_path
pages = convert_from_path(OUT + ".pdf", dpi=100)
for i, p in enumerate(pages): p.save(f"page{i+1}.png")
print("pages:", len(pages))
# fill.json for the PPTX
u = lambda s: H.unescape(s).replace("−", "-")
disc = [u(re.sub(r"<.*?>", "", p)) for p in re.findall(r'<div class="legal">.*?</div>\s*<div class="disc-head">Disclaimer</div>(.*?)</div>', tpl, re.S)[0].split("</p>") if p.strip()]
asp = lambda f: (lambda w, h: h / w)(*Image.open(f).size)
fj = {
 "LOGO": "/home/claude/syz_logo_hq.png", "GRADBAR": "/home/claude/syz_gradbar.png",
 "DOC_TYPE": "Earnings update", "DATE": c.DATE, "TITLE": u(c.TITLE), "QUOTE": u(c.QUOTE), "QUOTE_WHO": u(c.QUOTE_WHO),
 "COMPANY_INTRO": u(c.COMPANY_INTRO),
 "TAKEAWAYS": [{"tag": t, "label": l, "text": u(x)} for t, l, x in c.TAKEAWAYS],
 "KPIS": [{"label": u(a), "value": u(b), "sub": u(d), "sign": s} for a, b, d, s in c.KPIS],
 "H_P1": u(c.H_P1), "P1_PARAGRAPH": u(c.P1[0]), "C1_TITLE": u(c.C1_TITLE), "C1_SUB": u(c.C1_SUB),
 "C1_IMG": fill["C1_IMG"], "C1_ASPECT": asp(fill["C1_IMG"]), "W1": 66, "C1_COMMENT": u(c.C1_COMMENT[0]),
 "BASE_CASE": u(c.BASE_CASE), "UPSIDE": u(c.UPSIDE), "DOWNSIDE": u(c.DOWNSIDE), "UPSIDE_HEAD": c.UP_HEAD, "DOWNSIDE_HEAD": c.DOWN_HEAD,
 "P2_TITLE": "Beyond the key takeaways", "H_A1": u(c.H_A1), "A1_PARAGRAPHS": [u(p) for p in c.A1],
 "H_A2": u(c.H_A2), "A2_PARAGRAPH": u(c.A2[0]), "H_C2": u(c.H_C2), "C2_TITLE": u(c.C2_TITLE), "C2_SUB": u(c.C2_SUB),
 "C2_IMG": fill["C2_IMG"], "C2_ASPECT": asp(fill["C2_IMG"]), "W2": 88, "C2_COMMENT": u(c.C2_COMMENT[0]),
 "SOURCE_LINE": u(c.SOURCE_LINE), "DISCLAIMER": disc,
}
assert len(disc) == 7, len(disc)
json.dump(fj, open("fill.json", "w"), ensure_ascii=False, indent=1)
print("fill.json written")
