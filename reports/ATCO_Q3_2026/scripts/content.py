"""content.py: all text for the Atlas Copco Q3 2026 Earnings update (HTML entities; fill.json is derived from it)."""
OUT = "/home/claude/atco"
TICKER, Q = "ATCO", "Q32026"

C = {
"DOC_TYPE": "Earnings update",
"THEME": "Industrial machinery",
"DATE": "22 October 2026",
"P2_TITLE": "Beyond the key takeaways",
"W1": 72, "W2": 94,
"TITLE": "Atlas Copco Q3 2026: vacuum boom, compressor squeeze",

"QUOTE": "What we see now with the semi customers, the biggest priority now is that we focus on output. And I think the biggest discussions between ourselves and our customers is output, output.",
"QUOTE_WHO": "Vagner Rego, President and CEO, Q3 2026 earnings call, 22 October 2026",

"TAKEAWAYS": [
 ("pos", "Beat", "Organic orders rose 25% against 20% expected, lifted by an 82% jump in vacuum for chipmakers."),
 ("neg", "Watch", "The compressor margin fell to 23.6% from 25.3%: currency, mix and costlier components hit the core."),
 ("neu", "Outlook", "Activity is seen stable, but chip orders after a record quarter are hard to call into Q4."),
 ("neu", "Valuation", "The shares fell 7.1% to 29.2x forward earnings, below their one-year average of 31.0x."),
],
"KPIS": [
 ("Orders received", "SEK 52.3bn", "+25% organic vs. 20% exp.", "pos"),
 ("Revenue", "SEK 47.9bn", "Record, +11% organic", "pos"),
 ("Adj. operating margin", "21.3%", "Flat y/y, below expectations", "neg"),
 ("Compressor margin", "23.6%", "&minus;170bp y/y", "neg"),
],

"H_P1": "What the quarter means for the investment case",
"P1_PARAGRAPH": "<p>Atlas Copco now runs at two speeds. Vacuum Technique is riding the semiconductor investment cycle: organic orders up 82%, revenue up 28% and the margin up to 22.2% despite ramp-up costs. Compressor Technique, the profit engine, grew orders by only 6% and gave up 1.7 points of margin. The shares fell 7.1% on the day: the beat rested on vacuum orders partly pulled forward, compressor prices will lag cost inflation, and a crowded stock close to its record needed more.</p>",

"C1_TITLE": "ATCO: Q3 2026 organic order growth by business area",
"C1_SUB": "Organic growth in orders received, Q3 2026 vs. Q3 2025 &middot; Group consensus: pre-results analyst expectations &middot; Source: company, Bloomberg",
"C1_COMMENT": "<p>Every region grew, with Asia and North America both up 39%, and three of the four business areas posted double-digit order growth. The beat is nonetheless concentrated in vacuum, where management acknowledged some pre-ordering by customers keen to secure capacity. Compressors, which carry the highest margin in the group, delivered the weakest growth, held back by a flat Europe.</p>",

"BASE_CASE": "We stay positive on Atlas Copco and would add gradually on the results-day fall. The earnings path we underwrite rests on vacuum: lead times beyond the usual three to six months and a new US dry pump plant moving to full pump assembly in Q4 should carry double-digit revenue growth into 2027, while the compressor margin stabilises around 24% as price increases work through the order book. The debate has moved to compressor profitability. Crowded positioning means the de-rating can run further near term. The next test is the Q4 report in late January 2027.",
"UPSIDE": "Compressor orders back above 10% organic growth, with the margin recovering towards 25% by mid-2027; vacuum orders holding close to the Q3 level in Q4 despite seasonality; clearly higher prices as semiconductor supply agreements come up for renewal in 2027.",
"DOWNSIDE": "A compressor margin below 23% in Q4, showing that price increases do not offset component inflation; vacuum orders falling more than seasonally as customers digest Q3 pre-orders; European weakness spreading to North American compressor demand in early 2027.",

"H_A1": "Results: vacuum volume, compressor costs",
"A1_PARAGRAPHS": "<p>Orders reached a record SEK 52.3bn, up 29% in total: 25% organic, 3% from acquisitions and a small currency tailwind. Revenue was also a record at SEK 47.9bn, up 11% organically. The reported operating margin of 20.8% includes a SEK 132m restructuring charge for German operations in Industrial Technique; the adjusted margin of 21.3% was flat year on year and slightly below analyst expectations. Volume and price drove a good organic drop-through, offset by currency, mainly a stronger Korean won, and mildly dilutive acquisitions. A 21% tax rate, helped by tax credits, lifted profit to SEK 7.7bn from SEK 6.7bn and basic EPS by 15% to SEK 1.58. Working capital absorbed only SEK 87m.</p>"
                 "<p>In Vacuum Technique, revenue rose 28% organically and the margin improved again to 22.2%, despite ramp-up costs and currency. Pricing gains are slow: customers are few and powerful, and supply agreements expire at staggered dates. Compressor Technique grew revenue 5% organically, but its margin slipped to 23.6% on the won, product and regional mix and dearer electronics, aluminium castings and oil. Long-cycle projects with up to a year of lead time were priced before the inflation. Industrial Technique orders rose 12%, revenue only 2%, with a 20.6% adjusted margin helped by lower tariff costs. Power Technique orders grew 13% and the margin rose to 18.3%.</p>",

"H_A2": "Outlook: stable activity, a hard call on chips",
"A2_PARAGRAPHS": "<p>The guidance is the usual sequential one: customer activity, excluding large orders, currency and seasonality, should remain at the current level for most segments. Management stressed the seasonal dip from Q3 to Q4 and declined to call semiconductor orders after a record intake, noting that customers now focus on output rather than new orders. Further vacuum margin expansion is expected, but at a slower pace than in the last two quarters. For compressors, price increases will reach the income statement only gradually and the new European cooling acquisition dilutes the margin. Currency should add about SEK 0.5bn to Q4 profit and the tax rate should rise to around 22.5%.</p>",

"H_C2": "Valuation: the premium is being tested",
"C2_TITLE": "ATCO: share price vs. consensus earnings and valuation",
"C2_SUB": "Weekly, Oct 2005 to 22 Oct 2026 &middot; Bloomberg BEst 12m-forward EPS &middot; 40-week MA &middot; Log scale &middot; Last price: 22 October close, after the release",
"C2_COMMENT": "<p>Over 12 months the share price rose 8.0% while consensus forward EPS rose 9.7%: earnings did the work. At 29.2x forward earnings the stock trades at a 54% premium to its 18.9x average since 2005, but it sits below its one-year average of 31.0x. The multiple has fallen from 35.2x at the record high of SEK 213.4 on 6 October, and the price is now below its 40-week average of SEK 190. A 5% EPS upgrade at an unchanged price would take the multiple to 27.8x. Analyst price targets set after the release range from SEK 235 to SEK 260.</p>",

"SOURCE_LINE": "Source: Syz Research, Bloomberg, Atlas Copco Q3 2026 interim report and earnings call of 22 October 2026, analyst research notes of 22 October 2026",
}
