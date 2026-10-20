"""content_v2.py: user-supplied text for the ABB Q3 2026 Earnings update PPTX (plain text)."""
import json, sys
sys.path.insert(0, "/home/claude/abb")
base = json.load(open("/home/claude/abb/fill.json"))

F = dict(base)
F.update({
 "TITLE": "ABB Q3 2026: record orders, a higher bar",
 "QUOTE": "", "QUOTE_WHO": "",
 "TAKEAWAYS": [
  {"tag": "pos", "label": "Beat", "text": "Orders surged 40% to a record $12.1bn, 8% above consensus, driven by exceptional data centre demand."},
  {"tag": "neg", "label": "Miss", "text": "Basic EPS of $0.65 missed consensus by approximately 17%, partly due to a $115m non-cash hedge charge."},
  {"tag": "neg", "label": "Watch", "text": "Electrification is driving growth, while Automation orders remained flat and Motion margins declined."},
  {"tag": "neu", "label": "Valuation", "text": "At 25.6x consensus earnings, 36% above its long-term average, ABB needs sustained earnings upgrades to justify its premium."},
 ],
 "KPIS": [
  {"label": "Orders", "value": "$12.1bn", "sub": "+8% vs. consensus", "sign": "pos"},
  {"label": "Operational EBITA", "value": "$2.0bn", "sub": "+2% vs. consensus", "sign": "pos"},
  {"label": "Basic EPS", "value": "$0.65", "sub": "−17% vs. consensus", "sign": "neg"},
  {"label": "Free cash flow", "value": "$1.58bn", "sub": "+29% vs. consensus", "sign": "pos"},
 ],
 "H_P1": "The case now rests on electrification",
 "P1_PARAGRAPHS": [
  "ABB delivered record orders in Q3, but the market was less impressed than the headline figures suggest. Order intake surged 40% year-on-year to $12.1bn, driven by triple-digit growth in data centre demand. Revenues rose 14% to $9.7bn, while operational EBITA increased 24%, lifting the margin by 160 basis points to 20.8%. Yet the shares fell 5.7% following the release. Reported earnings missed expectations, the guidance upgrade was relatively modest, and the results coincided with pressure on AI-related industrial stocks.",
  "The strength was concentrated in Electrification, where orders grew 70% organically to $7.7bn and the backlog reached a record $16bn, up 83% year-on-year. This provides substantial revenue visibility into 2027 and 2028. Elsewhere, momentum was less convincing: Motion orders increased 12%, but margins declined, while Automation orders remained flat. With much of ABB’s growth potential already reflected in its valuation, the next test is whether exceptional demand can translate into sustained earnings growth.",
 ],
 "C1_TITLE": "ABBN: Q3 2026 results vs. consensus",
 "C1_COMMENT": "Orders and free cash flow exceeded expectations by 8% and 29%, respectively, while revenues were broadly in line and operational EBITA beat by approximately 2%. Reported EPS was the main disappointment. The $115m non-cash currency hedge revaluation linked to the Rotork acquisition explains part of the shortfall, but the modest underlying earnings surprise also highlights the increasingly demanding expectations facing ABB.",
 "BASE_CASE": "We remain constructive on ABB’s long-term fundamentals, supported by structural electrification demand, record order visibility and improving profitability. However, the 5.7% share price decline illustrates how much growth was already priced in. At the current valuation, we would favour maintaining exposure and look for further weakness or stronger evidence of 2027 earnings upgrades before adding. The investment case remains attractive, but the next challenge is converting exceptional orders into sustainable profits.",
 "UPSIDE": "Continued double-digit Electrification growth, successful conversion of the $16bn backlog into revenues, and a recovery in Automation orders would reinforce our conviction. Sustained margins above 20% and meaningful upward revisions to 2027 earnings would provide further support.",
 "DOWNSIDE": "A slowdown in data centre investment, project delays or cancellations, and margin pressure as large orders move into production would challenge the thesis. Persistent weakness in traditional industrial markets or disappointing returns from acquisitions would also undermine the premium valuation.",
 "P2_TITLE": "Beyond the key takeaways",
 "H_A1": "Results: Electrification drives another record",
 "A1_PARAGRAPHS": [
  "Electrification was the standout, with orders up 70% organically to $7.7bn, 16% above consensus, supported by triple-digit growth in data centres. Revenues increased 21% to $5.4bn, while operational EBITA rose 27% to $1.4bn, lifting the margin to 25.6%. The Americas was particularly strong, with orders up 117%, while utilities, semiconductors and electrical infrastructure also contributed.",
  "The opportunity extends to the architecture of future data centres. AI workloads require higher power density and more efficient electrical systems, accelerating interest in 800-volt direct current technology. ABB’s new Infinitus portfolio addresses this transition, including a solid-state transformer expected to become commercially available in the second half of 2027. Combined with continued grid investment, this provides several structural sources of demand.",
  "Performance elsewhere was mixed. Motion orders grew 12% organically, supported by electrical grids, HVAC, marine and industrial demand, although its margin declined 100 basis points to 19.1%, partly due to the acquired Gamesa Electric business. Automation orders were flat at $2.1bn, approximately 9% below consensus, reflecting weaker process industries and the timing of project bookings. Its margin nevertheless improved 90 basis points to 14.8%.",
  "At group level, operational EBITA margin expanded to 20.8%, supported by higher volumes and efficiency gains. However, gross margin declined 60 basis points to 40.6%, mainly due to unrealised FX and commodity derivative effects. Pricing contributed just above 2%, broadly offsetting cost inflation. Free cash flow reached $1.58bn, supported by improved working capital management, while net debt declined to $1.3bn, equivalent to just 0.2x EBITDA.",
 ],
 "H_A2": "Outlook: stronger visibility, modest upgrades",
 "A2_PARAGRAPHS": [
  "Management narrowed its full-year comparable revenue growth outlook to the low teens and now expects reported operational EBITA margin to improve by at least 270 basis points year-on-year. For Q4, revenue growth should remain broadly similar to Q3, while margins are expected to soften sequentially by less than the usual seasonal pattern.",
  "The guidance improvement requires some qualification. Reported margins will benefit from property disposals, including approximately CHF240m expected in Q4. Excluding this contribution, the underlying upgrade is more modest. The stronger implication concerns 2027, when the exceptional Electrification backlog should increasingly translate into revenues and earnings.",
  "ABB is also reshaping its portfolio towards higher-margin electrical and automation businesses. The Robotics divestment is expected to close in late 2026, while the Rotork acquisition, scheduled for the first half of 2027, will expand its presence in electric actuation and intelligent flow control. ABB also announced a $495m investment for a controlling 51% stake in a joint venture with Mitsubishi Electric’s low-voltage power distribution business. The transaction will strengthen ABB’s position in Japan, with management targeting an operational EBITA margin of at least 20% within five years.",
 ],
 "H_C2": "Valuation: the premium needs earnings growth",
 "C2_TITLE": "ABBN: share price vs. consensus earnings and valuation",
 "C2_PARAGRAPHS": [
  "ABB trades at approximately 25.6x consensus earnings, compared with a long-term average of 18.8x since 2006. The multiple remains 36% above its historical average, despite the recent correction. The premium reflects ABB’s exposure to electrification, improving profitability and the visibility provided by its expanding order backlog.",
  "The valuation also explains the market’s demanding response to Q3. Strong orders support future growth, but expectations were already elevated, and the earnings surprise was relatively modest. Consensus 2026 EPS has risen approximately 15% since January, but only 1% since the July results, suggesting that earnings revisions have recently slowed.",
  "The potential for further upgrades remains, particularly as Electrification orders convert into revenues during 2027 and 2028. However, the current multiple leaves limited room for disappointment if data centre demand moderates, project execution becomes more costly or weaker industrial activity weighs on other divisions. Future share price performance will increasingly depend on earnings growth rather than further multiple expansion.",
 ],
 "SOURCE_LINE": "Source: Syz Research, Bloomberg, company filings",
 "W1": 48, "W2": 90,
})
for k in ["P1_PARAGRAPH", "A2_PARAGRAPH", "C2_COMMENT"]:
    F.pop(k, None)
assert not any("—" in json.dumps(v, ensure_ascii=False) for v in F.values()), "em dash"
json.dump(F, open("fill_v2.json", "w"), ensure_ascii=False, indent=1)
print("ok")
