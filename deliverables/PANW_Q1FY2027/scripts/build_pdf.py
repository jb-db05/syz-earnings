"""Fill template -> PDF -> PNG pages, and write fill.json for the PPTX. python3 build_pdf.py"""
import sys, json, html, re
sys.path.insert(0, "/home/claude/panw"); import content as c
from PIL import Image
OUT = "/home/claude/out"; import os; os.makedirs(OUT, exist_ok=True)
STEM = "Earnings_Update_PANW_Q1FY2027"
P = lambda t: f"<p>{t}</p>"
quote_block = (f'<div class="quote"><p>&ldquo;{c.QUOTE}&rdquo;</p><div class="who">{c.QUOTE_WHO}</div></div>' if c.QUOTE else "")
tk = "\n".join(f'<li><span class="tag {t}">{l}</span><span class="t">{x}</span></li>' for t, l, x in c.TAKEAWAYS)
kp = "\n".join(f'<td><div class="lbl">{l}</div><div class="val">{v}</div><div class="sub {s}">{u}</div></td>' for l, v, u, s in c.KPIS)
fill = dict(DOC_TYPE=c.DOC_TYPE, DATE=c.DATE, TITLE=c.TITLE, QUOTE_BLOCK=quote_block, COMPANY_INTRO=c.COMPANY_INTRO,
    TAKEAWAYS=tk, KPI_TILES=kp, H_P1=c.H_P1, P1_PARAGRAPH=P(c.P1), C1_TITLE=c.C1_TITLE, C1_SUB=c.C1_SUB,
    C1_IMG="/home/claude/c1_crop.png", C1_COMMENT=P(c.C1_COMMENT), BASE_CASE=c.BASE_CASE,
    UP_HEAD="What would strengthen our view", DOWN_HEAD="What would change our view", UPSIDE=c.UPSIDE, DOWNSIDE=c.DOWNSIDE,
    P2_TITLE=c.P2_TITLE, H_A1=c.H_A1, A1_PARAGRAPHS="\n".join(P(x) for x in c.A1), H_A2=c.H_A2, A2_PARAGRAPHS=P(c.A2),
    H_C2=c.H_C2, C2_TITLE=c.C2_TITLE, C2_SUB=c.C2_SUB, C2_IMG="/home/claude/c2_crop.png", C2_COMMENT=P(c.C2_COMMENT),
    SOURCE_LINE=c.SOURCE_LINE, W1=c.W1, W2=c.W2)
tpl = open("/home/claude/template.html").read()
h = tpl
for k, v in fill.items(): h = h.replace("{{" + k + "}}", str(v))
assert "{{" not in h and "—" not in h
open(f"{OUT}/doc.html", "w").write(h)
from weasyprint import HTML; HTML(f"{OUT}/doc.html").write_pdf(f"{OUT}/{STEM}.pdf")
from pdf2image import convert_from_path
pages = convert_from_path(f"{OUT}/{STEM}.pdf", dpi=100)
for i, p in enumerate(pages): p.save(f"{OUT}/page{i+1}.png")
print("pages:", len(pages))

# fill.json for build_pptx.js (plain text)
u = lambda s: html.unescape(s).replace("−", "-")
disc = [u(re.sub(r"<.*?>", "", p)).strip() for p in re.findall(r'<div class="legal">.*?</div>\s*<div class="disc-head">Disclaimer</div>(.*?)</div>', tpl, re.S)[0].strip().split("\n") if p.strip()]
asp = lambda f: (lambda im: im.size[1] / im.size[0])(Image.open(f))
J = dict(LOGO="/home/claude/syz_logo_hq.png", GRADBAR="/home/claude/syz_gradbar.png", DOC_TYPE=c.DOC_TYPE, DATE=c.DATE,
    TITLE=u(c.TITLE), QUOTE=u(c.QUOTE), QUOTE_WHO=u(c.QUOTE_WHO), COMPANY_INTRO=u(c.COMPANY_INTRO),
    TAKEAWAYS=[dict(tag=t, label=l, text=u(x)) for t, l, x in c.TAKEAWAYS],
    KPIS=[dict(label=l, value=u(v), sub=u(s2), sign=s) for l, v, s2, s in c.KPIS],
    H_P1=u(c.H_P1), P1_PARAGRAPH=u(c.P1), C1_TITLE=u(c.C1_TITLE), C1_SUB=u(c.C1_SUB), C1_IMG="/home/claude/c1_crop.png",
    C1_ASPECT=asp("/home/claude/c1_crop.png"), W1=c.W1_PPT, C1_COMMENT=u(c.C1_COMMENT), BASE_CASE=u(c.BASE_CASE),
    UPSIDE=u(c.UPSIDE), DOWNSIDE=u(c.DOWNSIDE), UPSIDE_HEAD="What would strengthen our view", DOWNSIDE_HEAD="What would change our view",
    P2_TITLE=c.P2_TITLE, H_A1=u(c.H_A1), A1_PARAGRAPHS=[u(x) for x in c.A1], H_A2=u(c.H_A2), A2_PARAGRAPH=u(c.A2),
    H_C2=u(c.H_C2), C2_TITLE=u(c.C2_TITLE), C2_SUB=u(c.C2_SUB), C2_IMG="/home/claude/c2_crop.png",
    C2_ASPECT=asp("/home/claude/c2_crop.png"), W2=c.W2_PPT, C2_COMMENT=u(c.C2_COMMENT), SOURCE_LINE=u(c.SOURCE_LINE), DISCLAIMER=disc)
assert len(disc) == 7, len(disc)
json.dump(J, open(f"{OUT}/fill.json", "w"), ensure_ascii=False, indent=1)
