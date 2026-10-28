"""build_pdf.py: content.py -> PDF (WeasyPrint) + page PNGs + fill.json for build_pptx.js.
Run from /home/claude after build_charts.py: python3 build_pdf.py"""
import sys, re, json, html as H
from PIL import Image
HERE = "/home/user/syz-earnings/reports/SDZ_Q3_2026"
sys.path.insert(0, HERE)
import content as C

OUT_PDF = f"{HERE}/Earnings_Update_SDZ_Q32026.pdf"
C1_IMG, C2_IMG = "/home/claude/sdz/c1_crop.png", "/home/claude/sdz/c2_crop.png"
tpl = open("/home/claude/template.html").read()

P = lambda s: f"<p>{s}</p>"
quote_block = (f'<div class="quote"><p>&ldquo;{C.QUOTE}&rdquo;</p><div class="who">{C.QUOTE_WHO}</div></div>'
               if C.QUOTE else "")
fill = {
    "DOC_TYPE": C.DOC_TYPE, "DATE": C.DATE, "TITLE": C.TITLE, "QUOTE_BLOCK": quote_block,
    "COMPANY_INTRO": C.COMPANY_INTRO,
    "TAKEAWAYS": "\n".join(f'<li><span class="tag {c}">{l}</span><span class="t">{t}</span></li>' for c, l, t in C.TAKEAWAYS),
    "KPI_TILES": "\n".join(f'<td><div class="lbl">{l}</div><div class="val">{v}</div><div class="sub {s}">{u}</div></td>'
                           for l, v, u, s in C.KPIS),
    "H_P1": C.H_P1, "P1_PARAGRAPH": P(C.P1_PARAGRAPH),
    "C1_TITLE": C.C1_TITLE, "C1_SUB": C.C1_SUB, "C1_IMG": C1_IMG, "C1_COMMENT": P(C.C1_COMMENT),
    "BASE_CASE": C.BASE_CASE, "UPSIDE": C.UPSIDE, "DOWNSIDE": C.DOWNSIDE,
    "P2_TITLE": C.P2_TITLE, "H_A1": C.H_A1, "A1_PARAGRAPHS": "".join(map(P, C.A1_PARAGRAPHS)),
    "H_A2": C.H_A2, "A2_PARAGRAPHS": "".join(map(P, C.A2_PARAGRAPHS)),
    "H_C2": C.H_C2, "C2_TITLE": C.C2_TITLE, "C2_SUB": C.C2_SUB, "C2_IMG": C2_IMG, "C2_COMMENT": P(C.C2_COMMENT),
    "W1": C.W1, "W2": C.W2, "SOURCE_LINE": C.SOURCE_LINE,
}

# ---- word budgets
wc = lambda s: len(re.sub(r"&\w+;", " ", s).split())
budgets = {"COMPANY_INTRO": (C.COMPANY_INTRO, 25, 36), "P1": (C.P1_PARAGRAPH, 55, 65), "C1": (C.C1_COMMENT, 50, 55),
           "BASE": (C.BASE_CASE, 80, 90), "UP": (C.UPSIDE, 34, 38), "DOWN": (C.DOWNSIDE, 34, 38),
           "A1a": (C.A1_PARAGRAPHS[0], 100, 115), "A1b": (C.A1_PARAGRAPHS[1], 90, 105),
           "A2": (C.A2_PARAGRAPHS[0], 95, 110), "C2": (C.C2_COMMENT, 85, 100)}
for k, (s, lo, hi) in budgets.items():
    n = wc(s); print(f"{k:14s} {n:4d}  [{lo}-{hi}] {'OK' if lo <= n <= hi else '<-- OUT'}")
for c, l, t in C.TAKEAWAYS:
    print(f"takeaway {l:10s} {wc(t):3d} {'OK' if wc(t) <= 18 else '<-- OUT'}")
print("title chars", len(H.unescape(C.TITLE)))

html = tpl
for k, v in fill.items():
    html = html.replace("{{" + k + "}}", str(v))
assert "{{" not in html, "unfilled placeholder"
assert "—" not in html, "em dash"
open("/home/claude/sdz/doc.html", "w").write(html)
from weasyprint import HTML; HTML("/home/claude/sdz/doc.html").write_pdf(OUT_PDF)
from pdf2image import convert_from_path
pages = convert_from_path(OUT_PDF, dpi=100)
for i, p in enumerate(pages): p.save(f"/home/claude/sdz/page{i+1}.png")
print("pages:", len(pages))

# ---- fill.json for the PPTX (plain text, same content)
u = lambda s: H.unescape(s).replace("−", "-")
disc = re.search(r'<div class="disc-head">Disclaimer</div>(.*?)</div>', tpl, re.S).group(1)
asp = lambda p: (lambda im: im.size[1] / im.size[0])(Image.open(p))
pj = {
    "LOGO": "/home/claude/syz_logo_hq.png", "GRADBAR": "/home/claude/syz_gradbar.png",
    "DOC_TYPE": C.DOC_TYPE, "DATE": C.DATE, "TITLE": u(C.TITLE), "QUOTE": u(C.QUOTE), "QUOTE_WHO": u(C.QUOTE_WHO),
    "COMPANY_INTRO": u(C.COMPANY_INTRO),
    "TAKEAWAYS": [{"tag": c, "label": l, "text": u(t)} for c, l, t in C.TAKEAWAYS],
    "KPIS": [{"label": u(l), "value": u(v), "sub": u(s2), "sign": s} for l, v, s2, s in C.KPIS],
    "H_P1": u(C.H_P1), "P1_PARAGRAPH": u(C.P1_PARAGRAPH),
    "C1_TITLE": u(C.C1_TITLE), "C1_SUB": u(C.C1_SUB), "C1_IMG": C1_IMG, "C1_ASPECT": asp(C1_IMG), "W1": C.W1_PPTX,
    "C1_COMMENT": u(C.C1_COMMENT), "BASE_CASE": u(C.BASE_CASE), "UPSIDE": u(C.UPSIDE), "DOWNSIDE": u(C.DOWNSIDE),
    "P2_TITLE": C.P2_TITLE, "H_A1": u(C.H_A1), "A1_PARAGRAPHS": [u(p) for p in C.A1_PARAGRAPHS],
    "H_A2": u(C.H_A2), "A2_PARAGRAPH": u(C.A2_PARAGRAPHS[0]),
    "H_C2": u(C.H_C2), "C2_TITLE": u(C.C2_TITLE), "C2_SUB": u(C.C2_SUB), "C2_IMG": C2_IMG, "C2_ASPECT": asp(C2_IMG),
    "W2": C.W2_PPTX, "C2_COMMENT": u(C.C2_COMMENT), "SOURCE_LINE": u(C.SOURCE_LINE),
    "DISCLAIMER": [u(re.sub(r"\s+", " ", p)) for p in re.findall(r"<p>(.*?)</p>", disc, re.S)],
}
assert len(pj["DISCLAIMER"]) == 7
json.dump(pj, open(f"{HERE}/fill.json", "w"), ensure_ascii=False, indent=1)
print("fill.json written")
