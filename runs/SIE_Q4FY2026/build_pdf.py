"""build_pdf.py: content.py -> PDF (WeasyPrint) + page PNGs + fill.json for build_pptx.js."""
import html, json, os, re
from PIL import Image
import content as C

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = "Earnings_Update_SIE_Q42026"
P = lambda f: os.path.join(HERE, f)


def wc(s):
    return len(re.sub(r"&\w+;", " ", s).split())


def plain(s):
    return html.unescape(s).replace("−", "-")


# ---- word budgets
budget = {
    "QUOTE": (C.QUOTE, 20, 35), "COMPANY_INTRO": (C.COMPANY_INTRO, 25, 36), "P1": (C.P1_PARAGRAPH, 55, 65),
    "C1_COMMENT": (C.C1_COMMENT, 50, 55), "BASE_CASE": (C.BASE_CASE, 80, 90), "UPSIDE": (C.UPSIDE, 30, 38),
    "DOWNSIDE": (C.DOWNSIDE, 30, 38), "A1a": (C.A1_PARAGRAPHS[0], 100, 115), "A1b": (C.A1_PARAGRAPHS[1], 90, 105),
    "A2": (C.A2_PARAGRAPHS[0], 95, 110), "C2_COMMENT": (C.C2_COMMENT, 85, 100),
}
for k, (t, lo, hi) in budget.items():
    n = wc(t)
    print(f"{k:14s} {n:4d}  [{lo}-{hi}] {'OK' if lo <= n <= hi else '<<<'}")
for tag, lab, t in C.TAKEAWAYS:
    print(f"takeaway {lab:10s} {wc(t):3d} {'OK' if wc(t) <= 18 else '<<<'}")
print("upside chars", len(plain(C.UPSIDE)), "downside chars", len(plain(C.DOWNSIDE)))

# ---- HTML fill
quote_block = (f'<div class="quote"><p>&ldquo;{C.QUOTE}&rdquo;</p><div class="who">{C.QUOTE_WHO}</div></div>'
               if C.QUOTE else "")
fill = {
    "DOC_TYPE": C.DOC_TYPE, "DATE": C.DATE, "TITLE": C.TITLE, "QUOTE_BLOCK": quote_block,
    "COMPANY_INTRO": C.COMPANY_INTRO,
    "TAKEAWAYS": "\n".join(f'<li><span class="tag {g}">{l}</span><span class="t">{t}</span></li>' for g, l, t in C.TAKEAWAYS),
    "KPI_TILES": "\n".join(f'<td><div class="lbl">{l}</div><div class="val">{v}</div><div class="sub {g}">{s}</div></td>'
                           for l, v, s, g in C.KPIS),
    "H_P1": C.H_P1, "P1_PARAGRAPH": f"<p>{C.P1_PARAGRAPH}</p>",
    "C1_TITLE": C.C1_TITLE, "C1_SUB": C.C1_SUB, "C1_IMG": P("c1_crop.png"), "C1_COMMENT": f"<p>{C.C1_COMMENT}</p>",
    "BASE_CASE": C.BASE_CASE, "UP_HEAD": C.UP_HEAD, "DOWN_HEAD": C.DOWN_HEAD, "UPSIDE": C.UPSIDE, "DOWNSIDE": C.DOWNSIDE,
    "P2_TITLE": C.P2_TITLE, "H_A1": C.H_A1, "A1_PARAGRAPHS": "\n".join(f"<p>{p}</p>" for p in C.A1_PARAGRAPHS),
    "H_A2": C.H_A2, "A2_PARAGRAPHS": "\n".join(f"<p>{p}</p>" for p in C.A2_PARAGRAPHS),
    "H_C2": C.H_C2, "C2_TITLE": C.C2_TITLE, "C2_SUB": C.C2_SUB, "C2_IMG": P("c2_crop.png"),
    "C2_COMMENT": f"<p>{C.C2_COMMENT}</p>", "SOURCE_LINE": C.SOURCE_LINE, "W1": C.W1, "W2": C.W2,
}
tpl = open(P("template.html")).read()
doc = tpl
for k, v in fill.items():
    doc = doc.replace("{{" + k + "}}", str(v))
assert "{{" not in doc, "unfilled placeholder"
assert "—" not in doc and "&mdash;" not in doc, "em dash"
open(P("doc.html"), "w").write(doc)
from weasyprint import HTML
HTML(P("doc.html")).write_pdf(P(OUT + ".pdf"))
from pdf2image import convert_from_path
pages = convert_from_path(P(OUT + ".pdf"), dpi=100)
for i, pg in enumerate(pages):
    pg.save(P(f"page{i+1}.png"))
print("pages:", len(pages))

# ---- fill.json for the PPTX (plain text)
disc = re.findall(r"<p>(This communication has been issued.*?)</p>", tpl, re.S)
legal = re.findall(r'<div class="disc-head">Disclaimer</div>(.*?)</div>', tpl, re.S)[0]
disc = [plain(re.sub(r"\s+", " ", p)) for p in re.findall(r"<p>(.*?)</p>", legal, re.S)]
assert len(disc) == 7
aspect = lambda f: (lambda im: im.size[1] / im.size[0])(Image.open(P(f)))
fj = {
    "LOGO": "/home/claude/syz_logo_hq.png", "GRADBAR": "/home/claude/syz_gradbar.png",
    "DOC_TYPE": C.DOC_TYPE, "DATE": C.DATE, "TITLE": plain(C.TITLE), "QUOTE": plain(C.QUOTE), "QUOTE_WHO": plain(C.QUOTE_WHO),
    "COMPANY_INTRO": plain(C.COMPANY_INTRO),
    "TAKEAWAYS": [{"tag": g, "label": l, "text": plain(t)} for g, l, t in C.TAKEAWAYS],
    "KPIS": [{"label": plain(l), "value": plain(v), "sub": plain(s), "sign": g} for l, v, s, g in C.KPIS],
    "H_P1": plain(C.H_P1), "P1_PARAGRAPH": plain(C.P1_PARAGRAPH),
    "C1_TITLE": plain(C.C1_TITLE), "C1_SUB": plain(C.C1_SUB), "C1_IMG": P("c1_crop.png"), "C1_ASPECT": aspect("c1_crop.png"),
    "W1": C.W1_PPTX, "C1_COMMENT": plain(C.C1_COMMENT),
    "BASE_CASE": plain(C.BASE_CASE), "UPSIDE": plain(C.UPSIDE), "DOWNSIDE": plain(C.DOWNSIDE),
    "UPSIDE_HEAD": C.UP_HEAD, "DOWNSIDE_HEAD": C.DOWN_HEAD,
    "P2_TITLE": C.P2_TITLE, "H_A1": plain(C.H_A1), "A1_PARAGRAPHS": [plain(p) for p in C.A1_PARAGRAPHS],
    "H_A2": plain(C.H_A2), "A2_PARAGRAPH": plain(C.A2_PARAGRAPHS[0]),
    "H_C2": plain(C.H_C2), "C2_TITLE": plain(C.C2_TITLE), "C2_SUB": plain(C.C2_SUB), "C2_IMG": P("c2_crop.png"),
    "C2_ASPECT": aspect("c2_crop.png"), "W2": C.W2_PPTX, "C2_COMMENT": plain(C.C2_COMMENT),
    "SOURCE_LINE": plain(C.SOURCE_LINE), "DISCLAIMER": disc,
}
json.dump(fj, open(P("fill.json"), "w"), ensure_ascii=False, indent=1)
print("fill.json written")
