"""build_pdf.py: content.py + charts -> Earnings update PDF (WeasyPrint), page PNGs, fill.json and PPTX.
Usage: python3 build_charts.py && python3 build_pdf.py"""
import html
import json
import os
import re
import shutil
import subprocess
import sys

from PIL import Image

import content as C

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", ".."))
OUT = os.path.join(HERE, "out")
NAME = f"Earnings_Update_{C.TICKER}_{C.QUARTER.replace(' ', '')}"
OUT_PDF = os.path.join(OUT, NAME + ".pdf")
OUT_PPTX = os.path.join(OUT, NAME + ".pptx")
C1_IMG, C2_IMG = os.path.join(OUT, "c1_crop.png"), os.path.join(OUT, "c2_crop.png")


def words(s):
    return len(html.unescape(re.sub(r"<[^>]+>", " ", s)).split())


def check_budgets():
    texts = {"QUOTE": C.QUOTE, "COMPANY_INTRO": C.COMPANY_INTRO, "P1_PARAGRAPH": C.P1_PARAGRAPH,
             "C1_COMMENT": C.C1_COMMENT, "BASE_CASE": C.BASE_CASE, "UPSIDE": C.UPSIDE, "DOWNSIDE": C.DOWNSIDE,
             "A1_0": C.A1_PARAGRAPHS[0], "A1_1": C.A1_PARAGRAPHS[1], "A2_PARAGRAPH": C.A2_PARAGRAPH,
             "C2_COMMENT": C.C2_COMMENT}
    ok = True
    for k, t in texts.items():
        lo, hi = C.BUDGETS[k]
        n = words(t)
        flag = "" if lo <= n <= hi else "  <-- OUT OF BUDGET"
        ok &= not flag
        print(f"{k:14s} {n:4d}  ({lo}-{hi}){flag}")
    for tag, label, t in C.TAKEAWAYS:
        n = words(t)
        print(f"takeaway {label:9s} {n:3d}  (<=18){'  <-- OUT OF BUDGET' if n > 18 else ''}")
        ok &= n <= 18
    return ok


def p(s):
    return f"<p>{s}</p>"


def html_fill():
    quote = (f'<div class="quote"><p>&ldquo;{C.QUOTE}&rdquo;</p><div class="who">{C.QUOTE_WHO}</div></div>'
             if C.QUOTE else "")
    take = "\n".join(f'<li><span class="tag {t}">{l}</span><span class="t">{x}</span></li>' for t, l, x in C.TAKEAWAYS)
    kpi = "\n".join(f'<td><div class="lbl">{l}</div><div class="val">{v}</div><div class="sub {s}">{sub}</div></td>'
                    for l, v, sub, s in C.KPIS)
    return {
        "DOC_TYPE": C.DOC_TYPE, "DATE": C.DATE, "TITLE": C.TITLE, "QUOTE_BLOCK": quote,
        "COMPANY_INTRO": C.COMPANY_INTRO, "TAKEAWAYS": take, "KPI_TILES": kpi,
        "H_P1": C.H_P1, "P1_PARAGRAPH": p(C.P1_PARAGRAPH),
        "C1_TITLE": C.C1_TITLE, "C1_SUB": C.C1_SUB, "C1_IMG": C1_IMG, "C1_COMMENT": p(C.C1_COMMENT),
        "BASE_CASE": C.BASE_CASE, "UPSIDE": C.UPSIDE, "DOWNSIDE": C.DOWNSIDE,
        "P2_TITLE": C.P2_TITLE, "H_A1": C.H_A1, "A1_PARAGRAPHS": "\n".join(p(x) for x in C.A1_PARAGRAPHS),
        "H_A2": C.H_A2, "A2_PARAGRAPHS": p(C.A2_PARAGRAPH),
        "H_C2": C.H_C2, "C2_TITLE": C.C2_TITLE, "C2_SUB": C.C2_SUB, "C2_IMG": C2_IMG, "C2_COMMENT": p(C.C2_COMMENT),
        "W1": C.W1, "W2": C.W2, "SOURCE_LINE": C.SOURCE_LINE,
    }


def plain(s):
    return html.unescape(s).replace("−", "-")


def build_fill_json(template):
    disc = [" ".join(plain(re.sub(r"<[^>]+>", "", x)).split()) for x in re.findall(r'<div class="disc-head">Disclaimer</div>(.*?)</div>',
                                                                  template, re.S)[0].split("</p>") if x.strip()]
    aspect = lambda f: (lambda im: im.size[1] / im.size[0])(Image.open(f))
    return {
        "LOGO": "/home/claude/syz_logo_hq.png", "GRADBAR": "/home/claude/syz_gradbar.png",
        "DOC_TYPE": C.DOC_TYPE, "DATE": C.DATE, "TITLE": plain(C.TITLE),
        "QUOTE": plain(C.QUOTE), "QUOTE_WHO": plain(C.QUOTE_WHO), "COMPANY_INTRO": plain(C.COMPANY_INTRO),
        "TAKEAWAYS": [{"tag": t, "label": l, "text": plain(x)} for t, l, x in C.TAKEAWAYS],
        "KPIS": [{"label": plain(l), "value": plain(v), "sub": plain(s), "sign": g} for l, v, s, g in C.KPIS],
        "H_P1": plain(C.H_P1), "P1_PARAGRAPH": plain(C.P1_PARAGRAPH),
        "C1_TITLE": plain(C.C1_TITLE), "C1_SUB": plain(C.C1_SUB), "C1_IMG": C1_IMG, "C1_ASPECT": aspect(C1_IMG),
        "W1": C.W1_PPTX, "C1_COMMENT": plain(C.C1_COMMENT),
        "BASE_CASE": plain(C.BASE_CASE), "UPSIDE": plain(C.UPSIDE), "DOWNSIDE": plain(C.DOWNSIDE),
        "P2_TITLE": C.P2_TITLE, "H_A1": plain(C.H_A1), "A1_PARAGRAPHS": [plain(x) for x in C.A1_PARAGRAPHS],
        "H_A2": plain(C.H_A2), "A2_PARAGRAPH": plain(C.A2_PARAGRAPH),
        "H_C2": plain(C.H_C2), "C2_TITLE": plain(C.C2_TITLE), "C2_SUB": plain(C.C2_SUB),
        "C2_IMG": C2_IMG, "C2_ASPECT": aspect(C2_IMG), "W2": C.W2_PPTX, "C2_COMMENT": plain(C.C2_COMMENT),
        "SOURCE_LINE": plain(C.SOURCE_LINE), "DISCLAIMER": disc,
    }


def main():
    ok = check_budgets()
    if not ok and "--force" not in sys.argv:
        sys.exit("word budgets exceeded (rerun with --force to render anyway)")
    template = open(os.path.join(REPO, "template.html")).read()
    doc = template
    for k, v in html_fill().items():
        doc = doc.replace("{{" + k + "}}", str(v))
    assert "{{" not in doc, "unfilled placeholder"
    assert "—" not in doc, "em dash"
    open(os.path.join(OUT, "doc.html"), "w").write(doc)
    from weasyprint import HTML
    HTML(os.path.join(OUT, "doc.html")).write_pdf(OUT_PDF)
    from pdf2image import convert_from_path
    pages = convert_from_path(OUT_PDF, dpi=100)
    for i, pg in enumerate(pages):
        pg.save(os.path.join(OUT, f"page{i + 1}.png"))
    print("pages:", len(pages))

    fill = build_fill_json(template)
    assert len(fill["DISCLAIMER"]) == 7, len(fill["DISCLAIMER"])
    fj = os.path.join(OUT, "fill.json")
    json.dump(fill, open(fj, "w"), indent=1, ensure_ascii=False)
    shutil.copy(os.path.join(REPO, "build_pptx.js"), "/home/claude/build_pptx.js")
    subprocess.run(["node", "/home/claude/build_pptx.js", fj, OUT_PPTX], check=True)


if __name__ == "__main__":
    main()
