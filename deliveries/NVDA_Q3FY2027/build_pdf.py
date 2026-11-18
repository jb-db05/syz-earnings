"""build_pdf.py: fill the Syz template from content.py, render the PDF, rasterise, write fill.json, check budgets."""
import html, json, re, sys
from PIL import Image
sys.path.insert(0, "/home/claude/nvda")
import content as C

OUT = "/home/claude/nvda/Earnings_Update_NVDA_Q3FY2027"
TPL = "/home/claude/template.html"
C1, C2 = "/home/claude/nvda/c1_crop.png", "/home/claude/nvda/c2_crop.png"

def words(s): return len(re.sub(r"&\w+;", " ", s).split())

def budgets():
    chk = {"quote": (C.QUOTE, 20, 35), "intro": (C.COMPANY_INTRO, 25, 36), "P1": (C.P1_PARAGRAPH, 55, 65),
           "C1": (C.C1_COMMENT, 50, 55), "base": (C.BASE_CASE, 80, 90), "A1a": (C.A1_PARAGRAPHS[0], 100, 115),
           "A1b": (C.A1_PARAGRAPHS[1], 90, 105), "A2": (C.A2_PARAGRAPH, 95, 110), "C2": (C.C2_COMMENT, 85, 100), "CS": (C.CS_COMMENT, 55, 75)}
    for k, (t, lo, hi) in chk.items():
        n = words(t); print(f"{k:6s} {n:4d}  [{lo}-{hi}]", "" if lo <= n <= hi else "<-- OUT")
    for k, t in [("up", C.UPSIDE), ("down", C.DOWNSIDE)]:
        n = len(html.unescape(t)); print(f"{k:6s} {n:4d} chars [<=200]", "" if n <= 205 else "<-- OUT")
    for _, _, t in C.TAKEAWAYS:
        n = words(t); print(f"take   {n:4d}  [<=18]", "" if n <= 18 else "<-- OUT")

def fill():
    p = lambda t: f"<p>{t}</p>"
    quote = (f'<div class="quote"><p>&ldquo;{C.QUOTE}&rdquo;</p><div class="who">{C.QUOTE_WHO}</div></div>'
             if C.QUOTE else "")
    tk = "\n".join(f'<li><span class="tag {c}">{l}</span><span class="t">{t}</span></li>' for c, l, t in C.TAKEAWAYS)
    kp = "\n".join(f'<td><div class="lbl">{l}</div><div class="val">{v}</div><div class="sub {s}">{u}</div></td>'
                   for l, v, u, s in C.KPIS)
    return {"DOC_TYPE": C.DOC_TYPE, "DATE": C.DATE, "TITLE": C.TITLE, "QUOTE_BLOCK": quote,
            "COMPANY_INTRO": C.COMPANY_INTRO, "TAKEAWAYS": tk, "KPI_TILES": kp, "H_P1": C.H_P1,
            "P1_PARAGRAPH": p(C.P1_PARAGRAPH), "C1_TITLE": C.C1_TITLE, "C1_SUB": C.C1_SUB, "C1_IMG": C1,
            "C1_COMMENT": p(C.C1_COMMENT), "BASE_CASE": C.BASE_CASE, "UP_HEAD": C.UP_HEAD, "DOWN_HEAD": C.DOWN_HEAD,
            "UPSIDE": C.UPSIDE, "DOWNSIDE": C.DOWNSIDE, "P2_TITLE": C.P2_TITLE, "H_A1": C.H_A1,
            "A1_PARAGRAPHS": "\n".join(p(x) for x in C.A1_PARAGRAPHS), "H_A2": C.H_A2,
            "A2_PARAGRAPHS": p(C.A2_PARAGRAPH), "H_C2": C.H_C2, "C2_TITLE": C.C2_TITLE, "C2_SUB": C.C2_SUB,
            "C2_IMG": C2, "C2_COMMENT": p(C.C2_COMMENT), "SOURCE_LINE": C.SOURCE_LINE, "W1": C.W1, "W2": C.W2}

def write_fill_json(tpl):
    u = lambda s: html.unescape(s).replace("−", "-")
    disc = [u(re.sub(r"<[^>]+>", "", x)) for x in re.findall(r'<p>(This communication.*?|This information.*?|'
            r'Past performance.*?|Nothing in.*?|Should a recipient.*?)</p>', tpl, re.S)]
    assert len(disc) == 7, len(disc)
    asp = lambda f: Image.open(f).size[1] / Image.open(f).size[0]
    F = {"LOGO": "/home/claude/syz_logo_hq.png", "GRADBAR": "/home/claude/syz_gradbar.png",
         "DOC_TYPE": C.DOC_TYPE, "DATE": C.DATE, "TITLE": u(C.TITLE), "QUOTE": u(C.QUOTE), "QUOTE_WHO": u(C.QUOTE_WHO),
         "COMPANY_INTRO": u(C.COMPANY_INTRO),
         "TAKEAWAYS": [{"tag": c, "label": l, "text": u(t)} for c, l, t in C.TAKEAWAYS],
         "KPIS": [{"label": l, "value": u(v), "sub": u(s), "sign": g} for l, v, s, g in C.KPIS],
         "H_P1": u(C.H_P1), "P1_PARAGRAPH": u(C.P1_PARAGRAPH), "C1_TITLE": u(C.C1_TITLE), "C1_SUB": u(C.C1_SUB),
         "C1_IMG": C1, "C1_ASPECT": asp(C1), "W1": C.W1_PPTX, "C1_COMMENT": u(C.C1_COMMENT),
         "BASE_CASE": u(C.BASE_CASE), "UPSIDE_HEAD": C.UP_HEAD, "DOWNSIDE_HEAD": C.DOWN_HEAD,
         "UPSIDE": u(C.UPSIDE), "DOWNSIDE": u(C.DOWNSIDE), "P2_TITLE": C.P2_TITLE, "H_A1": u(C.H_A1),
         "A1_PARAGRAPHS": [u(x) for x in C.A1_PARAGRAPHS], "H_A2": u(C.H_A2), "A2_PARAGRAPH": u(C.A2_PARAGRAPH),
         "H_C2": u(C.H_C2), "C2_TITLE": u(C.C2_TITLE), "C2_SUB": u(C.C2_SUB), "C2_IMG": C2, "C2_ASPECT": asp(C2),
         "W2": C.W2_PPTX, "C2_COMMENT": u(C.C2_COMMENT),
         "CS_TITLE": u(C.CS_TITLE), "CS_IMG": "/home/claude/nvda/c2_tall_crop.png",
         "CS_ASPECT": asp("/home/claude/nvda/c2_tall_crop.png"), "CS_LEAD": u(C.CS_LEAD), "CS_COMMENT": u(C.CS_COMMENT),
         "CS_KPIS": [{"label": l, "value": u(v), "sub": u(x), "sign": g} for l, v, x, g in C.CS_KPIS],
         "SOURCE_LINE": u(C.SOURCE_LINE), "DISCLAIMER": disc}
    json.dump(F, open("/home/claude/nvda/fill.json", "w"), ensure_ascii=False, indent=1)

if __name__ == "__main__":
    budgets()
    tpl = open(TPL).read()
    h = tpl
    for k, v in fill().items():
        h = h.replace("{{" + k + "}}", str(v))
    assert "{{" not in h, re.findall(r"{{\w+}}", h)
    assert "—" not in h and "&mdash;" not in h, "em dash"
    open("/home/claude/nvda/doc.html", "w").write(h)
    from weasyprint import HTML
    HTML("/home/claude/nvda/doc.html").write_pdf(OUT + ".pdf")
    from pdf2image import convert_from_path
    pages = convert_from_path(OUT + ".pdf", dpi=100)
    for i, pg in enumerate(pages): pg.save(f"/home/claude/nvda/page{i+1}.png")
    print("pages:", len(pages))
    write_fill_json(tpl)
