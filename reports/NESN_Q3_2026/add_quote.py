"""add_quote.py: insert a management quote block on page 1 of an existing Syz update PDF (no HTML source).
The quote is typeset by WeasyPrint with the template's own CSS (same @page), then stamped between the dateline
and "Key takeaways"; the rest of page 1 moves down by the block height, header and footer stay in place.
Each stamped piece keeps only its own text, so the text layer reads once, in order.
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
W, H = p1.rect.width, p1.rect.height
text_of = lambda b: " ".join(s["text"] for l in b["lines"] for s in l["spans"])
blocks = [b for b in p1.get_text("dict")["blocks"] if "lines" in b]
kicker_title, dateline = text_of(blocks[0]), text_of(blocks[1])
kicker = kicker_title.split(" Nestl")[0]
head = (f'<div class="gradbar"></div><div class="kicker">{kicker}</div>'
        f'<h1>{kicker_title[len(kicker) + 1:]}</h1><div class="dateline">{dateline}</div>')
quote = f'<div class="quote"><p>&ldquo;{QUOTE}&rdquo;</p><div class="who">{WHO}</div></div>'
HIDE = ("body > :not(.quote) { visibility: hidden; } "
        "@page { @top-right { content: none; } @bottom-left { content: none; } @bottom-right { content: none; } }")


def render(with_quote, quote_only=False):
    """Header (+ quote) + first heading. quote_only: everything but the quote is laid out but not painted."""
    body = head + (quote if with_quote else "") + '<div class="sec first"><h2>Key takeaways</h2></div>'
    style = css + (HIDE if quote_only else "")
    pdf = HTML(string=f"<html><head><meta charset='utf-8'><style>{style}</style></head><body>{body}</body></html>").write_pdf()
    return fitz.open("pdf", pdf)


def heading_y(page):
    return next(b["bbox"][1] for b in page.get_text("dict")["blocks"] if "lines" in b and text_of(b) == "Key takeaways")


y_orig = heading_y(p1)
y_ref = heading_y(render(False)[0])
assert abs(y_ref - y_orig) < 0.5, (y_ref, y_orig)             # the rebuilt header matches the original layout
dy = heading_y(render(True)[0]) - y_ref
qdoc = render(True, quote_only=True)

ycut = (blocks[1]["bbox"][3] + y_orig) / 2                      # whitespace between dateline and the heading
body_bottom = max(b["bbox"][3] for b in blocks if b["bbox"][3] < 800)
foot_top = min(b["bbox"][1] for b in blocks if b["bbox"][1] > 800) - 4
assert body_bottom + dy < foot_top - 10, "page 1 would overflow"
print(f"quote block {dy:.1f}pt, body bottom {body_bottom:.1f} -> {body_bottom + dy:.1f}, footer at {foot_top:.1f}")


def piece(keep):
    """Copy of page 1 with the text outside `keep` removed (vectors and images untouched; they are clipped)."""
    d = fitz.open(); d.insert_pdf(src, from_page=0, to_page=0); pg = d[0]
    for r in (fitz.Rect(0, 0, W, keep.y0), fitz.Rect(0, keep.y1, W, H)):
        if not r.is_empty:
            pg.add_redact_annot(r)
    pg.apply_redactions(images=fitz.PDF_REDACT_IMAGE_NONE, graphics=fitz.PDF_REDACT_LINE_ART_NONE)
    return d


top = fitz.Rect(0, 0, W, ycut)
body = fitz.Rect(0, ycut, W, body_bottom + 4)
foot = fitz.Rect(0, foot_top, W, H)
qr = fitz.Rect(0, ycut, W, ycut + dy)

out = fitz.open()
pg = out.new_page(width=W, height=H)
pg.show_pdf_page(top, piece(top), 0, clip=top)
pg.show_pdf_page(qr, qdoc, 0, clip=qr)
pg.show_pdf_page(body + (0, dy, 0, dy), piece(body), 0, clip=body)
pg.show_pdf_page(foot, piece(foot), 0, clip=foot)
out.insert_pdf(src, from_page=1)
out.set_metadata(src.metadata)
out.save(OUT, garbage=4, deflate=True)
print("written", OUT, "pages", len(out))
