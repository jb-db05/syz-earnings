"""build_pdf.py: fill the Syz template from content.py, render the PDF, rasterise, write fill.json for the PPTX."""
import sys, json, html, re
sys.path.insert(0, "/home/claude/saf")
from content import C, OUT, TICKER, Q
from weasyprint import HTML
from pdf2image import convert_from_path

stats = json.load(open(f"{OUT}/stats.json"))
name = f"Earnings_Update_{TICKER}_{Q}"
f = {k: v for k, v in C.items() if isinstance(v, (str, int))}
f["QUOTE_BLOCK"] = (f'<div class="quote"><p>&ldquo;{C["QUOTE"]}&rdquo;</p><div class="who">{C["QUOTE_WHO"]}</div></div>'
                    if C["QUOTE"] else "")
f["TAKEAWAYS"] = "\n".join(f'<li><span class="tag {t}">{l}</span><span class="t">{x}</span></li>' for t, l, x in C["TAKEAWAYS"])
f["KPI_TILES"] = "\n".join(f'<td><div class="lbl">{l}</div><div class="val">{v}</div><div class="sub {s}">{u}</div></td>'
                           for l, v, u, s in C["KPIS"])
f["C1_IMG"], f["C2_IMG"] = f"{OUT}/c1_crop.png", f"{OUT}/c2_crop.png"
f["BASE_CASE"], f["UPSIDE"], f["DOWNSIDE"] = C["BASE_CASE"], C["UPSIDE"], C["DOWNSIDE"]

h = open(f"{OUT}/template.html").read()
for k, v in f.items():
    h = h.replace("{{" + k + "}}", str(v))
assert "{{" not in h, re.findall(r"\{\{\w+\}\}", h)
assert "—" not in h, "em dash"
open(f"{OUT}/doc.html", "w").write(h)
HTML(f"{OUT}/doc.html").write_pdf(f"{OUT}/{name}.pdf")
pages = convert_from_path(f"{OUT}/{name}.pdf", dpi=100)
for i, p in enumerate(pages):
    p.save(f"{OUT}/page{i+1}.png")
print("pages:", len(pages))

# fill.json for build_pptx.js (plain text)
u = lambda s: html.unescape(re.sub(r"</?p>", "", s)).replace("−", "-")
paras = lambda s: [u(p) for p in re.findall(r"<p>(.*?)</p>", s, re.S)]
disc = re.findall(r'<div class="disc-head">Disclaimer</div>(.*?)</div>', h, re.S)[0]
fill = {
    "LOGO": "/home/claude/syz_logo_hq.png", "GRADBAR": "/home/claude/syz_gradbar.png",
    **{k: u(C[k]) for k in ["DOC_TYPE", "THEME", "DATE", "TITLE", "QUOTE", "QUOTE_WHO", "H_P1", "C1_TITLE", "C1_SUB",
                            "BASE_CASE", "UPSIDE", "DOWNSIDE", "P2_TITLE", "H_A1", "H_A2", "H_C2", "C2_TITLE", "C2_SUB",
                            "SOURCE_LINE"]},
    "TAKEAWAYS": [{"tag": t, "label": l, "text": u(x)} for t, l, x in C["TAKEAWAYS"]],
    "KPIS": [{"label": u(l), "value": u(v), "sub": u(s2), "sign": s} for l, v, s2, s in C["KPIS"]],
    "P1_PARAGRAPH": u(C["P1_PARAGRAPH"]), "C1_COMMENT": u(C["C1_COMMENT"]),
    "A1_PARAGRAPHS": paras(C["A1_PARAGRAPHS"]), "A2_PARAGRAPH": u(C["A2_PARAGRAPHS"]),
    "C1_IMG": f["C1_IMG"], "C2_IMG": f["C2_IMG"], "C1_ASPECT": stats["c1_crop_aspect"], "C2_ASPECT": stats["c2_crop_aspect"],
    "W1": int(sys.argv[1]) if len(sys.argv) > 1 else 68, "W2": int(sys.argv[2]) if len(sys.argv) > 2 else 88,
    "C2_COMMENT": u(C["C2_COMMENT"]), "DISCLAIMER": paras(disc),
}
json.dump(fill, open(f"{OUT}/fill.json", "w"), ensure_ascii=False, indent=1)
