"""Fill the Syz template from content.py, render the PDF, rasterise the pages, write fill.json for the PPTX."""
import html, json, re, sys
from PIL import Image
import content as c

OUT_PDF = "/home/claude/azn/Earnings_Update_AZN_Q32026.pdf"
C1, C2 = "/home/claude/azn/c1_crop.png", "/home/claude/azn/c2_crop.png"
W1 = int(sys.argv[1]) if len(sys.argv) > 1 else c.W1
W2 = int(sys.argv[2]) if len(sys.argv) > 2 else c.W2

quote_block = "" if not c.QUOTE else (f'<div class="quote"><p>&ldquo;{c.QUOTE}&rdquo;</p>'
                                      f'<div class="who">{c.QUOTE_WHO}</div></div>')
takeaways = "\n".join(f'<li><span class="tag {t}">{l}</span><span class="t">{x}</span></li>' for t, l, x in c.TAKEAWAYS)
tiles = "\n".join(f'<td><div class="lbl">{l}</div><div class="val">{v}</div><div class="sub {s}">{u}</div></td>'
                  for l, v, u, s in c.KPIS)
fill = dict(DOC_TYPE=c.DOC_TYPE, DATE=c.DATE, TITLE=c.TITLE, QUOTE_BLOCK=quote_block, COMPANY_INTRO=c.COMPANY_INTRO,
            TAKEAWAYS=takeaways, KPI_TILES=tiles, H_P1=c.H_P1, P1_PARAGRAPH=c.P1_PARAGRAPH, C1_TITLE=c.C1_TITLE,
            C1_SUB=c.C1_SUB, C1_IMG=C1, C1_COMMENT=c.C1_COMMENT, BASE_CASE=c.BASE_CASE, UPSIDE=c.UPSIDE,
            DOWNSIDE=c.DOWNSIDE, P2_TITLE=c.P2_TITLE, H_A1=c.H_A1, A1_PARAGRAPHS="\n".join(c.A1_PARAGRAPHS),
            H_A2=c.H_A2, A2_PARAGRAPHS=c.A2_PARAGRAPHS, H_C2=c.H_C2, C2_TITLE=c.C2_TITLE, C2_SUB=c.C2_SUB,
            C2_IMG=C2, C2_COMMENT=c.C2_COMMENT, SOURCE_LINE=c.SOURCE_LINE, W1=W1, W2=W2)

tpl = open("/home/claude/azn/template.html").read()
doc = tpl
for k, v in fill.items():
    doc = doc.replace("{{" + k + "}}", str(v))
assert "{{" not in doc, "unfilled placeholder"
assert "—" not in doc, "em dash"
open("/home/claude/azn/doc.html", "w").write(doc)
from weasyprint import HTML
HTML("/home/claude/azn/doc.html").write_pdf(OUT_PDF)
from pdf2image import convert_from_path
pages = convert_from_path(OUT_PDF, dpi=100)
for i, p in enumerate(pages):
    p.save(f"/home/claude/azn/page{i+1}.png")
print("pages:", len(pages))

# ---- fill.json for build_pptx.js (plain text)
def plain(s):
    return html.unescape(re.sub(r"<[^>]+>", "", s)).replace("−", "-").strip()
aspect = lambda p: (lambda im: im.size[1] / im.size[0])(Image.open(p))
disc = [plain(p) for p in re.findall(r"<p>(This communication.*?|This information.*?|Past performance.*?|Nothing in.*?|Should a recipient.*?)</p>",
                                     tpl, re.S)]
assert len(disc) == 7, len(disc)
fj = dict(LOGO="/home/claude/syz_logo_hq.png", GRADBAR="/home/claude/syz_gradbar.png", DOC_TYPE=c.DOC_TYPE, DATE=c.DATE,
          TITLE=plain(c.TITLE), QUOTE=plain(c.QUOTE), QUOTE_WHO=plain(c.QUOTE_WHO), COMPANY_INTRO=plain(c.COMPANY_INTRO),
          TAKEAWAYS=[dict(tag=t, label=l, text=plain(x)) for t, l, x in c.TAKEAWAYS],
          KPIS=[dict(label=l, value=v, sub=plain(u), sign=s) for l, v, u, s in c.KPIS],
          H_P1=c.H_P1, P1_PARAGRAPH=plain(c.P1_PARAGRAPH), C1_TITLE=plain(c.C1_TITLE), C1_SUB=plain(c.C1_SUB),
          C1_IMG=C1, C1_ASPECT=aspect(C1), W1=66, C1_COMMENT=plain(c.C1_COMMENT), BASE_CASE=plain(c.BASE_CASE),
          UPSIDE=plain(c.UPSIDE), DOWNSIDE=plain(c.DOWNSIDE), P2_TITLE=c.P2_TITLE, H_A1=c.H_A1,
          A1_PARAGRAPHS=[plain(p) for p in c.A1_PARAGRAPHS], H_A2=c.H_A2, A2_PARAGRAPH=plain(c.A2_PARAGRAPHS),
          H_C2=c.H_C2, C2_TITLE=plain(c.C2_TITLE), C2_SUB=plain(c.C2_SUB), C2_IMG=C2, C2_ASPECT=aspect(C2), W2=88,
          C2_COMMENT=plain(c.C2_COMMENT), SOURCE_LINE=plain(c.SOURCE_LINE), DISCLAIMER=disc)
json.dump(fj, open("/home/claude/azn/fill.json", "w"), ensure_ascii=False, indent=1)
