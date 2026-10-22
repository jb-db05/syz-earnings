"""add_quote.py: insert a management quote block on page 1 of an existing Syz update PDF (no HTML source).
The quote is typeset by WeasyPrint with the template's own CSS (same @page), then stamped between the dateline and
"Key takeaways"; the rest of page 1 moves down by the block height, header and footer stay in place.
Usage: python3 add_quote.py in.pdf out.pdf"""
import re, sys
import pymupdf as fitz
from weasyprint import HTML

SRC, OUT = sys.argv[1], sys.argv[2]
QUOTE = ("This gives me confidence that we are on the right path. I am pleased with our progress, "
         "but I am not satisfied.")
WHO = "Philipp Navratil, CEO"

tpl = open("/home/claude/template.html").read()
css = re.search(r"<style>(.*?)</style>", tpl, re.S).group(1)
src = fitz.open(SRC); p1 = src[0]
blocks = [b for b in p1.get_text("dict")["blocks"] if "lines" in b]
text_of = lambda b: " ".join(s["text"] for l in b["lines"] for s in l["spans"])
head = lambda: f"""<div class="gradbar"></div><div class="kicker">{text_of(blocks[0]).split(' Nestl')[0]}</div>
<h1>{text_of(blocks[0])[len(text_of(blocks[0]).split(' Nestl')[0]) + 1:]}</h1><div class="dateline">{text_of(blocks[1])}</div>"""
quote = f'<div class="quote"><p>&ldquo;{QUOTE}&rdquo;</p><div class="who">{WHO}</div></div>'

def render(with_quote):
    body = head() + (quote if with_quote else "") + '<div class="sec first"><h2>Key takeaways</h2></div>'
    pdf = HTML(string=f"<html><head><meta charset='utf-8'><style>{css}</style></head><body>{body}</body></html>").write_pdf()
    d = fitz.open("pdf", pdf)
    y = next(b["bbox"][1] for b in d[0].get_text("dict")["blocks"] if "lines" in b and text_of(b) == "Key takeaways")
    return d, y

ref, y_ref = render(False)
qdoc, y_q = render(True)
y_orig = next(b["bbox"][1] for b in blocks if text_of(b) == "Key takeaways")
assert abs(y_ref - y_orig) < 0.5, (y_ref, y_orig)          # the rebuilt header matches the original layout
dy = y_q - y_ref
date_bottom = blocks[1]["bbox"][3]
ycut = (date_bottom + y_orig) / 2                             # whitespace between dateline and the heading
body_bottom = max(b["bbox"][3] for b in blocks if b["bbox"][3] < 800)
foot_top = min(b["bbox"][1] for b in blocks if b["bbox"][1] > 800) - 4
assert body_bottom + dy < foot_top - 10, "page 1 would overflow"
print(f"quote block {dy:.1f}pt, body bottom {body_bottom:.1f} -> {body_bottom + dy:.1f}, footer at {foot_top:.1f}")

out = fitz.open()
W, H = p1.rect.width, p1.rect.height
pg = out.new_page(width=W, height=H)
top = fitz.Rect(0, 0, W, ycut)
body = fitz.Rect(0, ycut, W, body_bottom + 4)
foot = fitz.Rect(0, foot_top, W, H)
pg.show_pdf_page(top, src, 0, clip=top)
pg.show_pdf_page(body + (0, dy, 0, dy), src, 0, clip=body)
pg.show_pdf_page(foot, src, 0, clip=foot)
qr = fitz.Rect(0, ycut, W, ycut + dy)
pg.show_pdf_page(qr, qdoc, 0, clip=qr)
out.insert_pdf(src, from_page=1)
out.set_metadata(src.metadata)
out.save(OUT, garbage=4, deflate=True)
print("written", OUT, "pages", len(out))
