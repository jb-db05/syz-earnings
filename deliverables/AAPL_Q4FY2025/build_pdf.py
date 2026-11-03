"""build_pdf.py: fill the template from content.py, render the PDF, rasterise, write fill.json."""
import html, json, re, sys
sys.path.insert(0, "/home/claude/aapl")
from PIL import Image
import content as C

D = "/home/claude/aapl"
OUT_PDF = f"{D}/Earnings_Update_{C.TICKER}_{C.PERIOD}.pdf"

quote_block = (f'<div class="quote"><p>&ldquo;{C.QUOTE}&rdquo;</p><div class="who">{C.QUOTE_WHO}</div></div>'
               if C.QUOTE else "")
tk = "\n".join(f'<li><span class="tag {c}">{l}</span><span class="t">{t}</span></li>' for c, l, t in C.TAKEAWAYS)
kp = "\n".join(f'<td><div class="lbl">{l}</div><div class="val">{v}</div><div class="sub {s}">{sub}</div></td>'
               for l, v, sub, s in C.KPIS)
fill = {
    "DOC_TYPE": C.DOC_TYPE, "DATE": C.DATE, "TITLE": C.TITLE, "QUOTE_BLOCK": quote_block,
    "COMPANY_INTRO": C.COMPANY_INTRO, "TAKEAWAYS": tk, "KPI_TILES": kp, "H_P1": C.H_P1,
    "P1_PARAGRAPH": C.P1_PARAGRAPH, "C1_TITLE": C.C1_TITLE, "C1_SUB": C.C1_SUB, "C1_IMG": f"{D}/c1_crop.png",
    "C1_COMMENT": C.C1_COMMENT, "BASE_CASE": C.BASE_CASE, "UP_HEAD": C.UP_HEAD, "DOWN_HEAD": C.DOWN_HEAD,
    "UPSIDE": C.UPSIDE, "DOWNSIDE": C.DOWNSIDE, "P2_TITLE": C.P2_TITLE, "H_A1": C.H_A1,
    "A1_PARAGRAPHS": "\n".join(C.A1_PARAGRAPHS), "H_A2": C.H_A2, "A2_PARAGRAPHS": C.A2_PARAGRAPHS,
    "H_C2": C.H_C2, "C2_TITLE": C.C2_TITLE, "C2_SUB": C.C2_SUB, "C2_IMG": f"{D}/c2_crop.png",
    "C2_COMMENT": C.C2_COMMENT, "SOURCE_LINE": C.SOURCE_LINE, "W1": C.W1, "W2": C.W2,
}

# word budgets
wc = lambda s: len(html.unescape(re.sub(r"<[^>]+>", " ", s)).split())
budget = {"QUOTE": (C.QUOTE, 20, 35), "INTRO": (C.COMPANY_INTRO, 25, 36), "P1": (C.P1_PARAGRAPH, 55, 65),
          "C1": (C.C1_COMMENT, 50, 55), "BASE": (C.BASE_CASE, 80, 90), "UP": (C.UPSIDE, 30, 38),
          "DOWN": (C.DOWNSIDE, 30, 38), "A1a": (C.A1_PARAGRAPHS[0], 100, 115), "A1b": (C.A1_PARAGRAPHS[1], 90, 105),
          "A2": (C.A2_PARAGRAPHS, 95, 110), "C2": (C.C2_COMMENT, 85, 100)}
for k, (t, lo, hi) in budget.items():
    n = wc(t); print(f"{k:6s} {n:4d}  [{lo}-{hi}]{'' if lo <= n <= hi else '  <-- OUT'}")
for k in ("UP", "DOWN"):
    print(k, "chars", len(html.unescape(budget[k][0])))
for _, l, t in C.TAKEAWAYS:
    print("takeaway", l, wc(t))

tpl = open(f"{D}/template.html").read()
for k, v in fill.items():
    tpl = tpl.replace("{{" + k + "}}", str(v))
assert "{{" not in tpl, "unfilled placeholder"
assert "—" not in tpl, "em dash"
open(f"{D}/doc.html", "w").write(tpl)
from weasyprint import HTML
HTML(f"{D}/doc.html").write_pdf(OUT_PDF)
from pdf2image import convert_from_path
pages = convert_from_path(OUT_PDF, dpi=100)
for i, p in enumerate(pages):
    p.save(f"{D}/page{i+1}.png")
print("pages:", len(pages))

# fill.json for the PPTX (plain text)
pt = lambda s: html.unescape(re.sub(r"</?p>", "", s)).replace("−", "-")
disc = re.findall(r'<div class="disc-head">Disclaimer</div>(.*?)</div>', open(f"{D}/template.html").read(), re.S)[0]
disc = [pt(p) for p in re.findall(r"<p>(.*?)</p>", disc, re.S)]
asp = lambda p: (lambda im: im.size[1] / im.size[0])(Image.open(p))
F = {
    "LOGO": "/home/claude/syz_logo_hq.png", "GRADBAR": "/home/claude/syz_gradbar.png",
    "DOC_TYPE": C.DOC_TYPE, "DATE": C.DATE, "TITLE": pt(C.TITLE), "QUOTE": pt(C.QUOTE), "QUOTE_WHO": pt(C.QUOTE_WHO),
    "COMPANY_INTRO": pt(C.COMPANY_INTRO),
    "TAKEAWAYS": [{"tag": c, "label": l, "text": pt(t)} for c, l, t in C.TAKEAWAYS],
    "KPIS": [{"label": pt(l), "value": pt(v), "sub": pt(s), "sign": g} for l, v, s, g in C.KPIS],
    "H_P1": pt(C.H_P1), "P1_PARAGRAPH": pt(C.P1_PARAGRAPH), "C1_TITLE": pt(C.C1_TITLE), "C1_SUB": pt(C.C1_SUB),
    "C1_IMG": f"{D}/c1_crop.png", "C1_ASPECT": asp(f"{D}/c1_crop.png"), "W1": C.W1_PPTX,
    "C1_COMMENT": pt(C.C1_COMMENT), "BASE_CASE": pt(C.BASE_CASE), "UPSIDE": pt(C.UPSIDE), "DOWNSIDE": pt(C.DOWNSIDE),
    "UPSIDE_HEAD": C.UP_HEAD, "DOWNSIDE_HEAD": C.DOWN_HEAD, "P2_TITLE": C.P2_TITLE, "H_A1": pt(C.H_A1),
    "A1_PARAGRAPHS": [pt(p) for p in C.A1_PARAGRAPHS], "H_A2": pt(C.H_A2), "A2_PARAGRAPH": pt(C.A2_PARAGRAPHS),
    "H_C2": pt(C.H_C2), "C2_TITLE": pt(C.C2_TITLE), "C2_SUB": pt(C.C2_SUB), "C2_IMG": f"{D}/c2_crop.png",
    "C2_ASPECT": asp(f"{D}/c2_crop.png"), "W2": C.W2_PPTX, "C2_COMMENT": pt(C.C2_COMMENT),
    "SOURCE_LINE": pt(C.SOURCE_LINE), "DISCLAIMER": disc,
}
assert len(disc) == 7
json.dump(F, open(f"{D}/fill.json", "w"), indent=1, ensure_ascii=False)
print("fill.json written")
