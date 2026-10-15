"""build_pdf.py: fill the Syz template from content.py, render the PDF, rasterise pages, write fill.json."""
import html, json, re, sys
from PIL import Image
import content as C

OUT = "/home/claude/out"
REPO = "/home/user/syz-earnings"
PDF = f"{OUT}/Earnings_Update_{C.TICKER}_{C.QUARTER}.pdf"


def words(s):
    return len(re.sub(r"<[^>]+>", " ", html.unescape(s)).split())


def budgets():
    rows = [("H_P1", C.P1_PARAGRAPH, 65, 85), ("C1", C.C1_COMMENT, 55, 65), ("BASE", C.BASE_CASE, 95, 110),
            ("UP", C.UPSIDE, 36, 45), ("DOWN", C.DOWNSIDE, 36, 45), ("A1a", C.A1_PARAGRAPHS[0], 100, 115),
            ("A1b", C.A1_PARAGRAPHS[1], 90, 105), ("A2", C.A2_PARAGRAPH, 95, 110), ("C2", C.C2_COMMENT, 85, 100)]
    for n, t, lo, hi in rows:
        w = words(t); print(f"{n:5s} {w:4d}  [{lo}-{hi}] {'OK' if lo <= w <= hi else '<<<'}")
    for _, l, t in C.TAKEAWAYS:
        print(f"TK {l:9s} {words(t):3d} (<=18)")


def fill():
    f = dict(C.FILL)
    f["QUOTE_BLOCK"] = (f'<div class="quote"><p>&ldquo;{C.QUOTE}&rdquo;</p><div class="who">{C.QUOTE_WHO}</div></div>'
                        if C.QUOTE else "")
    f["TAKEAWAYS"] = "\n".join(f'<li><span class="tag {c}">{l}</span><span class="t">{t}</span></li>' for c, l, t in C.TAKEAWAYS)
    f["KPI_TILES"] = "\n".join(f'<td><div class="lbl">{a}</div><div class="val">{b}</div><div class="sub {d}">{c}</div></td>'
                               for a, b, c, d in C.KPIS)
    f.update(H_P1=C.H_P1, P1_PARAGRAPH=C.P1_PARAGRAPH, C1_TITLE=C.C1_TITLE, C1_SUB=C.C1_SUB, C1_COMMENT=C.C1_COMMENT,
             BASE_CASE=C.BASE_CASE, UPSIDE=C.UPSIDE, DOWNSIDE=C.DOWNSIDE, H_A1=C.H_A1,
             A1_PARAGRAPHS="\n".join(C.A1_PARAGRAPHS), H_A2=C.H_A2, A2_PARAGRAPHS=C.A2_PARAGRAPH, H_C2=C.H_C2,
             C2_TITLE=C.C2_TITLE, C2_SUB=C.C2_SUB, C2_COMMENT=C.C2_COMMENT)
    return f


def render(f):
    h = open(f"{REPO}/template.html").read()
    for k, v in f.items():
        h = h.replace("{{" + k + "}}", str(v))
    assert "{{" not in h, "unfilled placeholder"
    assert "—" not in h, "em dash"
    open(f"{OUT}/doc.html", "w").write(h)
    from weasyprint import HTML
    HTML(f"{OUT}/doc.html").write_pdf(PDF)
    from pdf2image import convert_from_path
    pages = convert_from_path(PDF, dpi=100)
    for i, p in enumerate(pages):
        p.save(f"{OUT}/page{i+1}.png")
    print("pages:", len(pages))
    return h


def plain(s):
    s = re.sub(r"</p>\s*<p>", "\n", s)
    return html.unescape(re.sub(r"<[^>]+>", "", s)).replace("−", "-").strip()


def write_fill_json(h, w1=70, w2=88):
    disc = [plain(p) for p in re.findall(r"<p>(.*?)</p>", h.split('class="disc-head"')[1], re.S)]
    assert len(disc) == 7
    asp = lambda p: (lambda im: im.size[1] / im.size[0])(Image.open(p))
    j = {"LOGO": "/home/claude/syz_logo_hq.png", "GRADBAR": "/home/claude/syz_gradbar.png",
         **{k: plain(str(v)) for k, v in C.FILL.items() if k not in ("W1", "W2")},
         "QUOTE": plain(C.QUOTE), "QUOTE_WHO": plain(C.QUOTE_WHO),
         "TAKEAWAYS": [{"tag": c, "label": l, "text": plain(t)} for c, l, t in C.TAKEAWAYS],
         "KPIS": [{"label": plain(a), "value": plain(b), "sub": plain(c), "sign": d} for a, b, c, d in C.KPIS],
         "H_P1": plain(C.H_P1), "P1_PARAGRAPH": plain(C.P1_PARAGRAPH), "C1_TITLE": plain(C.C1_TITLE),
         "C1_SUB": plain(C.C1_SUB), "C1_IMG": C.FILL["C1_IMG"], "C1_ASPECT": asp(C.FILL["C1_IMG"]), "W1": w1,
         "C1_COMMENT": plain(C.C1_COMMENT), "BASE_CASE": plain(C.BASE_CASE), "UPSIDE": plain(C.UPSIDE),
         "DOWNSIDE": plain(C.DOWNSIDE), "H_A1": plain(C.H_A1), "A1_PARAGRAPHS": [plain(p) for p in C.A1_PARAGRAPHS],
         "H_A2": plain(C.H_A2), "A2_PARAGRAPH": plain(C.A2_PARAGRAPH), "H_C2": plain(C.H_C2),
         "C2_TITLE": plain(C.C2_TITLE), "C2_SUB": plain(C.C2_SUB), "C2_IMG": C.FILL["C2_IMG"],
         "C2_ASPECT": asp(C.FILL["C2_IMG"]), "W2": w2, "C2_COMMENT": plain(C.C2_COMMENT), "DISCLAIMER": disc}
    json.dump(j, open(f"{OUT}/fill.json", "w"), ensure_ascii=False, indent=1)


if __name__ == "__main__":
    budgets()
    h = render(fill())
    w1, w2 = (int(a) for a in sys.argv[1:3]) if len(sys.argv) > 2 else (70, 88)
    write_fill_json(h, w1, w2)
