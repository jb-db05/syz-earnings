import re, sys
# usage: python3 render_test.py P1 C1 BASE UPDOWN A1 A2 C2 W1 W2   (word budgets, then chart widths in %)
# e.g.    python3 render_test.py 75 60 100 40 108 100 92 76 92
def para(n):
    w = ("Orders of EUR 7.1bn beat consensus by 12% and the EUV share rose to 58%, the highest since Q2 2024, while gross margin reached 53.4% against a guide of 51 to 53%. We read the mix shift as structural rather than cyclical, and the guidance for Q4 implies a run-rate above the FY27 consensus. The debate now moves from demand to capacity. ").split()
    out = []
    while len(out) < n: out += w
    return " ".join(out[:n]) + "."
P = lambda n: f"<p>{para(n)}</p>"
B = dict(p1=int(sys.argv[1]), c1=int(sys.argv[2]), bc=int(sys.argv[3]), ud=int(sys.argv[4]),
         a1=int(sys.argv[5]), a2=int(sys.argv[6]), c2=int(sys.argv[7]), w1=sys.argv[8], w2=sys.argv[9])
fill = {
 "DOC_TYPE": "Earnings update", "THEME": "Semiconductors", "DATE": "14 October 2026",
 "TITLE": "ASML Q3 2026: orders confirm the upcycle, valuation leaves little slack",
 "QUOTE_BLOCK": '<div class="quote"><p>&ldquo;Illustrative management quote of about twenty to thirty words that captures the tone of the call and the key message to investors.&rdquo;</p><div class="who">Illustrative Name, CEO, Q3 2026 earnings call, 14 October 2026</div></div>',
 "TAKEAWAYS": "\n".join([
   '<li><span class="tag pos">Beat</span><span class="t">Revenue EUR 9.2bn (+4% vs. consensus) and EPS EUR 7.85 (+6%), driven by EUV mix and services.</span></li>',
   '<li><span class="tag pos">Raised</span><span class="t">FY26 revenue guide lifted to the top of the EUR 34 to 36bn range; gross margin 52 to 53%.</span></li>',
   '<li><span class="tag neg">Watch</span><span class="t">China fell to 22% of system sales from 29%, and export-licence timing remains the main swing factor.</span></li>',
   '<li><span class="tag neu">Valuation</span><span class="t">30.6x forward earnings, 18% above the 2010 to 2026 average: the upcycle is priced, not the next leg.</span></li>']),
 "KPI_TILES": "\n".join([
   '<td><div class="lbl">Revenue</div><div class="val">EUR 9.2bn</div><div class="sub pos">+4.1% vs. consensus</div></td>',
   '<td><div class="lbl">EPS</div><div class="val">EUR 7.85</div><div class="sub pos">+5.6% vs. consensus</div></td>',
   '<td><div class="lbl">Gross margin</div><div class="val">53.4%</div><div class="sub pos">+80bp vs. consensus</div></td>',
   '<td><div class="lbl">Q4 revenue guide</div><div class="val">EUR 9.6bn</div><div class="sub neg">-2.3% vs. consensus</div></td>']),
 "H_P1": "What the quarter means for the investment case",
 "P1_PARAGRAPH": P(B['p1']),
 "C1_TITLE": "ASML Q3 2026 &ndash; results vs. consensus", "C1_SUB": "Surprise vs. Bloomberg consensus, % &middot; guidance midpoint vs. consensus &middot; illustrative numbers",
 "C1_IMG": "/home/claude/c1_crop.png", "C1_COMMENT": P(B['c1']),
 "BASE_CASE": para(B['bc']),
 "UPSIDE": para(B['ud']), "DOWNSIDE": para(B['ud']),
 "H_A1": "Results: the beat was mix, not volume", "A1_PARAGRAPHS": P(B['a1']) + P(B['a1']-10),
 "H_A2": "Outlook: guidance leans on EUV and services", "A2_PARAGRAPHS": P(B['a2']),
 "H_C2": "Valuation: the upcycle is priced, the next leg is not",
 "C2_TITLE": "ASML &ndash; share price vs. consensus earnings and valuation",
 "C2_SUB": "ASML NA Equity, weekly &middot; BEst 12m-forward consensus &middot; 40-week simple MA &middot; log scale &middot; P/E shaded above (orange) / below (blue) its 2010 to 2026 average",
 "C2_IMG": "/home/claude/c2_crop.png", "C2_COMMENT": P(B['c2']),
 "P2_TITLE": "Beyond the key takeaways",
 "W1": B['w1'], "W2": B['w2'],
 "SOURCE_LINE": "Source: Syz Research, Bloomberg, company filings",
}
html = open("template.html").read()
for k, v in fill.items(): html = html.replace("{{"+k+"}}", str(v))
assert "{{" not in html, re.findall(r"\{\{(\w+)\}\}", html)
open("doc.html","w").write(html)
from weasyprint import HTML; HTML("doc.html").write_pdf("test.pdf")
from pdf2image import convert_from_path
pages = convert_from_path("test.pdf", dpi=100)
for i,p in enumerate(pages): p.save(f"page{i+1}.png")
print("pages:", len(pages))
