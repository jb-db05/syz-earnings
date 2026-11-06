import re, sys, json, html, subprocess
sys.path.insert(0, "/home/user/syz-earnings"); sys.path.insert(0, ".")
from content import C
W1, W2 = int(sys.argv[1]), int(sys.argv[2])
tmpl = open("/home/user/syz-earnings/template.html").read()
P = lambda t: f"<p>{t}</p>"
fill = {
 "DOC_TYPE": "Earnings update", "DATE": C["DATE"], "COMPANY_INTRO": C["COMPANY_INTRO"], "TITLE": C["TITLE"], "QUOTE_BLOCK": "",
 "TAKEAWAYS": "\n".join(f'<li><span class="tag {t}">{l}</span><span class="t">{x}</span></li>' for t, l, x in C["TAKEAWAYS"]),
 "KPI_TILES": "\n".join(f'<td><div class="lbl">{l}</div><div class="val">{v}</div><div class="sub {s}">{x}</div></td>' for l, v, x, s in C["KPIS"]),
 "H_P1": C["H_P1"], "P1_PARAGRAPH": P(C["P1"]), "C1_TITLE": C["C1_TITLE"], "C1_SUB": C["C1_SUB"],
 "C1_IMG": "/home/claude/c1_crop.png", "C1_COMMENT": P(C["C1"]), "BASE_CASE": C["BC"],
 "UPSIDE": C["UP"], "DOWNSIDE": C["DOWN"], "UP_HEAD": C["UP_HEAD"], "DOWN_HEAD": C["DOWN_HEAD"],
 "H_A1": C["H_A1"], "A1_PARAGRAPHS": "".join(P(a) for a in C["A1"]), "H_A2": C["H_A2"], "A2_PARAGRAPHS": P(C["A2"]),
 "H_C2": C["H_C2"], "C2_TITLE": C["C2_TITLE"], "C2_SUB": C["C2_SUB"], "C2_IMG": "/home/claude/c2_crop.png", "C2_COMMENT": P(C["C2"]),
 "P2_TITLE": "Beyond the key takeaways", "W1": W1, "W2": W2, "SOURCE_LINE": C["SOURCE_LINE"],
}
h = tmpl
for k, v in fill.items(): h = h.replace("{{" + k + "}}", str(v))
assert "{{" not in h, re.findall(r"\{\{(\w+)\}\}", h)
open("doc.html", "w").write(h)
from weasyprint import HTML
HTML("doc.html", base_url="/").write_pdf("Earnings_Update_MCK_Q2-2027.pdf")
from pdf2image import convert_from_path
pages = convert_from_path("Earnings_Update_MCK_Q2-2027.pdf", dpi=100)
for i, p in enumerate(pages): p.save(f"/home/claude/page{i+1}.png")
print("pages:", len(pages))
# fill.json (plain text)
un = lambda s: html.unescape(s).replace("‑", "-")
disc = [un(re.sub(r"<[^>]+>", "", m)) for m in re.findall(r"<p>(This .*?|Past .*?|Nothing .*?|Should .*?)</p>", tmpl, re.S) if True]
leg = re.search(r'<div class="legal">(.*)</div>', tmpl, re.S).group(1)
disc = [un(m) for m in re.findall(r"<p>(.*?)</p>", leg, re.S)]
j = {"LOGO": "/home/claude/syz_logo_hq.png", "GRADBAR": "/home/claude/syz_gradbar.png", "DOC_TYPE": "Earnings update", "DATE": C["DATE"],
 "TITLE": C["TITLE"], "QUOTE": "", "QUOTE_WHO": "", "COMPANY_INTRO": C["COMPANY_INTRO"],
 "TAKEAWAYS": [{"tag": t, "label": l, "text": un(x)} for t, l, x in C["TAKEAWAYS"]],
 "KPIS": [{"label": l, "value": v, "sub": un(x), "sign": s} for l, v, x, s in C["KPIS"]],
 "H_P1": C["H_P1"], "P1_PARAGRAPH": un(C["P1"]), "C1_TITLE": un(C["C1_TITLE"]), "C1_SUB": un(C["C1_SUB"]),
 "C1_IMG": "/home/claude/c1_crop.png", "C1_ASPECT": 0.312, "W1": 66, "C1_COMMENT": un(C["C1"]), "BASE_CASE": un(C["BC"]),
 "UPSIDE_HEAD": C["UP_HEAD"], "DOWNSIDE_HEAD": C["DOWN_HEAD"], "UPSIDE": un(C["UP"]), "DOWNSIDE": un(C["DOWN"]),
 "H_A1": C["H_A1"], "A1_PARAGRAPHS": [un(a) for a in C["A1"]], "H_A2": C["H_A2"], "A2_PARAGRAPH": un(C["A2"]),
 "H_C2": C["H_C2"], "C2_TITLE": un(C["C2_TITLE"]), "C2_SUB": un(C["C2_SUB"]), "C2_IMG": "/home/claude/c2_crop.png", "C2_ASPECT": 0.5984,
 "W2": 88, "C2_COMMENT": un(C["C2"]), "P2_TITLE": "Beyond the key takeaways", "SOURCE_LINE": C["SOURCE_LINE"], "DISCLAIMER": disc}
json.dump(j, open("fill.json", "w"), indent=1, ensure_ascii=False)
