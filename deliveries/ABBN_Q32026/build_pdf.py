"""build_pdf.py: fill the template from content.py, render the PDF, rasterise, write fill.json."""
import html, json, re, sys
from PIL import Image
from weasyprint import HTML
from pdf2image import convert_from_path
import content as c

OUT = "/home/claude/abb"
W1, W2 = 76, 92                 # PDF chart widths, % of text width
W1_PPTX, W2_PPTX = 70, 88       # PPTX chart widths
C1, C2 = f"{OUT}/c1_crop.png", f"{OUT}/c2_crop.png"
NAME = f"Earnings_Update_{c.TICKER}_{c.PERIOD}"

if len(sys.argv) > 1:
    W1, W2, W1_PPTX, W2_PPTX = map(int, sys.argv[1:5])


def paras(*ps):
    return "\n".join(f"<p>{p}</p>" for p in ps)


quote_block = "" if not c.QUOTE else (
    f'<div class="quote"><p>&ldquo;{c.QUOTE}&rdquo;</p><div class="who">{c.QUOTE_WHO}</div></div>')

fill = {
    "DOC_TYPE": c.DOC_TYPE, "THEME": c.THEME, "DATE": c.DATE, "TITLE": c.TITLE,
    "QUOTE_BLOCK": quote_block,
    "TAKEAWAYS": "\n".join(f'<li><span class="tag {t}">{lbl}</span><span class="t">{txt}</span></li>'
                           for t, lbl, txt in c.TAKEAWAYS),
    "KPI_TILES": "\n".join(f'<td><div class="lbl">{l}</div><div class="val">{v}</div>'
                           f'<div class="sub {s}">{sub}</div></td>' for l, v, sub, s in c.KPIS),
    "H_P1": c.H_P1, "P1_PARAGRAPH": paras(c.P1_PARAGRAPH),
    "C1_TITLE": c.C1_TITLE, "C1_SUB": c.C1_SUB, "C1_IMG": C1, "C1_COMMENT": paras(c.C1_COMMENT),
    "BASE_CASE": c.BASE_CASE, "UPSIDE": c.UPSIDE, "DOWNSIDE": c.DOWNSIDE,
    "P2_TITLE": c.P2_TITLE, "H_A1": c.H_A1, "A1_PARAGRAPHS": paras(*c.A1_PARAGRAPHS),
    "H_A2": c.H_A2, "A2_PARAGRAPHS": paras(c.A2_PARAGRAPH),
    "H_C2": c.H_C2, "C2_TITLE": c.C2_TITLE, "C2_SUB": c.C2_SUB, "C2_IMG": C2,
    "C2_COMMENT": paras(c.C2_COMMENT),
    "W1": W1, "W2": W2, "SOURCE_LINE": c.SOURCE_LINE,
}

tpl = open("/home/claude/template.html").read()
doc = tpl
for k, v in fill.items():
    doc = doc.replace("{{" + k + "}}", str(v))
assert "{{" not in doc, "unfilled placeholder"
assert "—" not in doc, "em dash"
open(f"{OUT}/doc.html", "w").write(doc)
HTML(f"{OUT}/doc.html").write_pdf(f"{OUT}/{NAME}.pdf")
pages = convert_from_path(f"{OUT}/{NAME}.pdf", dpi=100)
for i, p in enumerate(pages):
    p.save(f"{OUT}/page{i+1}.png")
print("pages:", len(pages))

# ---- fill.json for the PPTX (plain text)
plain = lambda s: html.unescape(s).replace("−", "-")
disclaimer = [plain(re.sub(r"<.*?>", "", p)) for p in
              re.findall(r'<div class="disc-head">Disclaimer</div>(.*?)</div>', tpl, re.S)[0].split("</p>") if p.strip()]
disclaimer = [d.strip() for d in disclaimer]
assert len(disclaimer) == 7
aspect = lambda p: (lambda im: im.size[1] / im.size[0])(Image.open(p))
fj = {
    "LOGO": "/home/claude/syz_logo_hq.png", "GRADBAR": "/home/claude/syz_gradbar.png",
    "DOC_TYPE": c.DOC_TYPE, "THEME": c.THEME, "DATE": c.DATE, "TITLE": plain(c.TITLE),
    "QUOTE": plain(c.QUOTE), "QUOTE_WHO": plain(c.QUOTE_WHO),
    "TAKEAWAYS": [{"tag": t, "label": lbl, "text": plain(txt)} for t, lbl, txt in c.TAKEAWAYS],
    "KPIS": [{"label": l, "value": plain(v), "sub": plain(sub), "sign": s} for l, v, sub, s in c.KPIS],
    "H_P1": plain(c.H_P1), "P1_PARAGRAPH": plain(c.P1_PARAGRAPH),
    "C1_TITLE": plain(c.C1_TITLE), "C1_SUB": plain(c.C1_SUB), "C1_IMG": C1, "C1_ASPECT": aspect(C1),
    "W1": W1_PPTX, "C1_COMMENT": plain(c.C1_COMMENT),
    "BASE_CASE": plain(c.BASE_CASE), "UPSIDE": plain(c.UPSIDE), "DOWNSIDE": plain(c.DOWNSIDE),
    "P2_TITLE": c.P2_TITLE, "H_A1": plain(c.H_A1), "A1_PARAGRAPHS": [plain(p) for p in c.A1_PARAGRAPHS],
    "H_A2": plain(c.H_A2), "A2_PARAGRAPH": plain(c.A2_PARAGRAPH),
    "H_C2": plain(c.H_C2), "C2_TITLE": plain(c.C2_TITLE), "C2_SUB": plain(c.C2_SUB), "C2_IMG": C2,
    "C2_ASPECT": aspect(C2), "W2": W2_PPTX, "C2_COMMENT": plain(c.C2_COMMENT),
    "SOURCE_LINE": plain(c.SOURCE_LINE), "DISCLAIMER": disclaimer,
}
json.dump(fj, open(f"{OUT}/fill.json", "w"), ensure_ascii=False, indent=1)
print("fill.json written")
