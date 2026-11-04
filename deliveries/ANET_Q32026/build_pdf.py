"""build_pdf.py: fill the Syz template from content.py, render the PDF, rasterise, write fill.json."""
import sys, json, html, re
sys.path.insert(0, "/home/claude/work")
import content as c
from PIL import Image

OUT = "/home/claude/work"
PDF = f"{OUT}/Earnings_Update_ANET_Q32026.pdf"
W1 = int(sys.argv[1]) if len(sys.argv) > 1 else c.W1
W2 = int(sys.argv[2]) if len(sys.argv) > 2 else c.W2
C1, C2 = f"{OUT}/c1_crop.png", f"{OUT}/c2_crop.png"

quote_block = (f'<div class="quote"><p>&ldquo;{c.QUOTE}&rdquo;</p><div class="who">{c.QUOTE_WHO}</div></div>'
               if c.QUOTE else "")
tk = "\n".join(f'<li><span class="tag {t}">{l}</span><span class="t">{x}</span></li>' for t, l, x in c.TAKEAWAYS)
kp = "\n".join(f'<td><div class="lbl">{a}</div><div class="val">{b}</div><div class="sub {s}">{d}</div></td>'
               for a, b, d, s in c.KPIS)
P = lambda xs: "\n".join(f"<p>{x}</p>" for x in xs)
fill = dict(DOC_TYPE=c.DOC_TYPE, DATE=c.DATE, TITLE=c.TITLE, QUOTE_BLOCK=quote_block, COMPANY_INTRO=c.COMPANY_INTRO,
            TAKEAWAYS=tk, KPI_TILES=kp, H_P1=c.H_P1, P1_PARAGRAPH=P([c.P1_PARAGRAPH]), C1_TITLE=c.C1_TITLE,
            C1_SUB=c.C1_SUB, C1_IMG=C1, C1_COMMENT=P([c.C1_COMMENT]), BASE_CASE=c.BASE_CASE, UP_HEAD=c.UP_HEAD,
            DOWN_HEAD=c.DOWN_HEAD, UPSIDE=c.UPSIDE, DOWNSIDE=c.DOWNSIDE, P2_TITLE=c.P2_TITLE, H_A1=c.H_A1,
            A1_PARAGRAPHS=P(c.A1_PARAGRAPHS), H_A2=c.H_A2, A2_PARAGRAPHS=P(c.A2_PARAGRAPHS), H_C2=c.H_C2,
            C2_TITLE=c.C2_TITLE, C2_SUB=c.C2_SUB, C2_IMG=C2, C2_COMMENT=P([c.C2_COMMENT]), SOURCE_LINE=c.SOURCE_LINE,
            W1=W1, W2=W2)

tpl = open("/home/claude/template.html").read()
h = tpl
for k, v in fill.items():
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

# ---- fill.json for the PowerPoint (plain text)
u = lambda s: html.unescape(s).replace("−", "-")
disc = re.findall(r'<div class="disc-head">Disclaimer</div>(.*?)</div>', tpl, re.S)[0]
disc = [u(x).strip() for x in re.findall(r"<p>(.*?)</p>", disc, re.S)]
asp = lambda p: (lambda im: im.size[1] / im.size[0])(Image.open(p))
fj = dict(LOGO="/home/claude/syz_logo_hq.png", GRADBAR="/home/claude/syz_gradbar.png", DOC_TYPE=c.DOC_TYPE,
          DATE=c.DATE, TITLE=u(c.TITLE), QUOTE=u(c.QUOTE), QUOTE_WHO=u(c.QUOTE_WHO), COMPANY_INTRO=u(c.COMPANY_INTRO),
          TAKEAWAYS=[dict(tag=t, label=l, text=u(x)) for t, l, x in c.TAKEAWAYS],
          KPIS=[dict(label=u(a), value=u(b), sub=u(d), sign=s) for a, b, d, s in c.KPIS],
          H_P1=u(c.H_P1), P1_PARAGRAPH=u(c.P1_PARAGRAPH), C1_TITLE=u(c.C1_TITLE), C1_SUB=u(c.C1_SUB), C1_IMG=C1,
          C1_ASPECT=asp(C1), W1=66, C1_COMMENT=u(c.C1_COMMENT), BASE_CASE=u(c.BASE_CASE), UPSIDE=u(c.UPSIDE),
          DOWNSIDE=u(c.DOWNSIDE), UPSIDE_HEAD=c.UP_HEAD, DOWNSIDE_HEAD=c.DOWN_HEAD, P2_TITLE=c.P2_TITLE,
          H_A1=u(c.H_A1), A1_PARAGRAPHS=[u(x) for x in c.A1_PARAGRAPHS], H_A2=u(c.H_A2),
          A2_PARAGRAPH=u(" ".join(c.A2_PARAGRAPHS)), H_C2=u(c.H_C2), C2_TITLE=u(c.C2_TITLE), C2_SUB=u(c.C2_SUB),
          C2_IMG=C2, C2_ASPECT=asp(C2), W2=88, C2_COMMENT=u(c.C2_COMMENT), SOURCE_LINE=u(c.SOURCE_LINE),
          DISCLAIMER=disc)
json.dump(fj, open(f"{OUT}/fill.json", "w"), ensure_ascii=False, indent=1)
print("disclaimer paragraphs:", len(disc))
