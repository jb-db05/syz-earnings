"""content.py: all text for the Safran Q3 2026 Earnings update (HTML entities; fill.json is derived from it)."""
OUT = "/home/claude/saf"
TICKER, Q = "SAF", "Q32026"

C = {
"DOC_TYPE": "Earnings update",
"THEME": "Aerospace and defence",
"DATE": "23 October 2026",
"P2_TITLE": "Beyond the key takeaways",
"W1": 72, "W2": 94,
"TITLE": "Safran Q3 2026: a solid engine, no fuel for upgrades",

"QUOTE": "This [the jet fuel price increase] will eat into the profits of the airlines in 2026, but globally, when we compound all the profits of all the airlines, we believe, overall, they are going to stay positive.",
"QUOTE_WHO": "Olivier Andri&egrave;s, Chief Executive Officer, Q3 2026 revenue call, 23 October 2026",

"TAKEAWAYS": [
 ("pos", "Solid", "Revenue of EUR 9.0bn was in line and civil spare parts rose 17%: the aftermarket holds."),
 ("neg", "No raise", "Unchanged targets offer no upgrade catalyst: consensus operating income sits 2.1% above the guided midpoint."),
 ("neg", "Watch", "Jet fuel above $100, a longer French surtax and GE&rsquo;s caution feed workscope and pricing fears."),
 ("neu", "Valuation", "The shares fell 6.2% to 27.0x forward earnings, below their five-year average of 30.0x."),
],
"KPIS": [
 ("Q3 revenue", "EUR 9.0bn", "+13.4% organic, in line", "neu"),
 ("Civil spare parts (USD)", "+17%", "Q4 guided mid to high 20s", "pos"),
 ("LEAP deliveries, 9 months", "1,565", "+26% y/y, FY above 2,100", "neu"),
 ("FY26 op. income guide", "EUR 6.4&ndash;6.5bn", "&minus;2.1% vs. consensus", "neg"),
],

"H_P1": "What the quarter means for the investment case",
"P1_PARAGRAPH": "<p>The shares fell 6.2% today, and 9.7% over two sessions, although the quarter was solid: revenue matched consensus and the civil aftermarket kept growing. But unchanged guidance offers no catalyst for upgrades, with consensus operating income already above the range. Near term, jet fuel at $100 or more, the proposed extension of the French surtax and GE&rsquo;s caution feed fears of workscope compression and weaker pricing. The call pushed back: management expects workscopes to &ldquo;remain at this high level next year&rdquo;.</p>",

"C1_TITLE": "SAF: Q3 2026 revenue and 2026 guidance vs. consensus",
"C1_SUB": "% vs. consensus &middot; Q3: company-compiled consensus &middot; FY26: guidance midpoints vs. consensus per analyst first takes",
"C1_COMMENT": "<p>Group revenue matched the company-compiled consensus within 0.1% and Equipment &amp; Defense beat by 2.5% on guided bombs, optronics, navigation and missile seekers. Aircraft Interiors missed by 1.3%, as seat certification still paces deliveries. The two bars on the right carry the message: confirmed targets sit about 2% below consensus, so estimates edge down rather than up.</p>",

"BASE_CASE": "We stay positive on Safran: the structural case is intact. The earnings path we underwrite holds: 2026 operating income of EUR 6.4bn to EUR 6.5bn reached without the LEAP-1B profit release, which now adds to 2027, and a 2028 target of EUR 7bn to EUR 7.5bn that management said in July may be revisited. The debate has moved to the durability of aftermarket pricing and workscopes. The catalyst is 2027 guidance at the full-year results in February. Until then, geopolitics, jet fuel and the French surtax can keep the shares weak.",
"UPSIDE": "2027 guidance in February implying operating income growth above 10%, helped by the LEAP-1B profit release; Q4 spare parts up in the mid to high 20s as guided; advance payments on India&rsquo;s 114 Rafale order; a good price for the cabin business.",
"DOWNSIDE": "Evidence of workscope compression or softer CFM56 pricing in Q4 as airlines absorb jet fuel at $100 or more; the French surtax kept at the 2026 rate, worth EUR 500m or more in 2027; capex above 6% of sales eroding cash conversion.",

"H_A1": "Results: the aftermarket still carries the group",
"A1_PARAGRAPHS": "<p>Revenue reached EUR 9.0bn, up 14.7% reported and 13.4% organically, in line with the EUR 8.99bn company-compiled consensus; currency added 1.1 points and scope was neutral. Propulsion revenue rose 13% organically to EUR 4.6bn. Civil engine spare parts grew 17% in dollars, showing &ldquo;no sign of deceleration&rdquo; according to management: the gap with 24% over nine months reflects a strong Q3 2025 base, and sales rose 4% on Q2. Services grew 19%, led by LEAP maintenance contracts, while military engines declined on the Rafale delivery schedule. LEAP deliveries reached 535, up 5%, and 1,565 over nine months, up 26%, on track for more than 2,100 this year.</p>"
                 "<p>Equipment &amp; Defense revenue rose 16% organically to EUR 3.6bn, ahead of the EUR 3.53bn expected, on strong demand for Hammer guided bombs, optronics, inertial navigation and missile seekers. Aircraft Interiors grew 6% to EUR 751m, against EUR 761m expected; certification still paces seat deliveries and may push some into early 2027. Safran has launched the sale of its cabin business, about EUR 2bn of revenue with positive operating profit and cash flow. Airbus selected the SkyNaute inertial navigation system for the A220, Safran&rsquo;s entry into commercial navigation. No profit figures are reported at the third quarter.</p>",

"H_A2": "Outlook: 2026 held, 2027 rests on price and LEAP",
"A2_PARAGRAPHS": "<p>Safran confirmed its 2026 targets: revenue growth in the mid-teens, recurring operating income of EUR 6.4bn to EUR 6.5bn and free cash flow of EUR 4.7bn to EUR 4.9bn, despite moving a LEAP-1B profit release in the low hundreds of millions of euros to 2027. Demand for shop visits still &ldquo;exceeds the available capacity&rdquo; and no airline has asked to defer deliveries. For 2027, management expects CFM56 shop visits flat at 2,400 and workscopes stable at today&rsquo;s high level, so growth comes from price and LEAP. Capex will exceed 6% of sales every year, and the draft 2027 budget extends the surtax, at a cost of around EUR 400m.</p>",

"H_C2": "Valuation: the multiple has done the adjusting",
"C2_TITLE": "SAF: share price vs. consensus earnings and valuation",
"C2_SUB": "Weekly, Sep 2005 to 23 Oct 2026 &middot; Bloomberg BEst 12m-forward EPS &middot; 40-week MA &middot; Log scale &middot; Last price: 23 October, intraday, after the release",
"C2_COMMENT": "<p>Over 12 months the share price fell 7.9% while consensus forward EPS rose 27.9%: earnings kept rising and the multiple absorbed the whole correction. At 27.0x forward earnings the stock trades 27% above its 21.3x average since 2005, but below its one-year average of 31.7x and its five-year average of 30.0x. The multiple has fallen from 34.9x at the record high of EUR 363.6 on 12 August, and the price sits 10% below its 40-week average of EUR 317. Even a 5% cut to consensus EPS at today&rsquo;s price would leave the multiple at 28.5x, still below its five-year average.</p>",

"SOURCE_LINE": "Source: Syz Research, Bloomberg, Safran Q3 2026 revenue call of 23 October 2026, Safran H1 2026 earnings call of 28 July 2026, company-compiled consensus, analyst research notes of 23 October 2026",
}
