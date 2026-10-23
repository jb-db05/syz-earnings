"""content.py: all text for the Safran Q3 2026 Earnings update (HTML entities; fill.json is derived from it)."""
OUT = "/home/claude/saf"
TICKER, Q = "SAF", "Q32026"

C = {
"DOC_TYPE": "Earnings update",
"THEME": "Aerospace and defence",
"DATE": "23 October 2026",
"P2_TITLE": "Beyond the key takeaways",
"W1": 76, "W2": 94,
"TITLE": "Safran Q3 2026: no upgrade, the de-rating overshoots",

"QUOTE": "",
"QUOTE_WHO": "",

"TAKEAWAYS": [
 ("pos", "In line", "Q3 revenue of EUR 9.0bn was in line; propulsion aftermarket rose 18.7% and defence beat."),
 ("neg", "No raise", "Targets were only confirmed: the EUR 6.45bn operating income midpoint sits 2.1% below consensus."),
 ("neg", "Watch", "Jet fuel above $100 and a French surtax worth about EUR 500m this year cloud 2027."),
 ("neu", "Valuation", "The shares fell 6.2% to 27.0x forward earnings, below their five-year average of 30.0x."),
],
"KPIS": [
 ("Q3 revenue", "EUR 9.0bn", "+13.4% organic, in line", "neu"),
 ("Propulsion aftermarket", "+18.7%", "Original equipment +3.5%", "pos"),
 ("LEAP deliveries", "535", "+5% y/y", "neu"),
 ("FY26 op. income guide", "EUR 6.4&ndash;6.5bn", "&minus;2.1% vs. consensus", "neg"),
],

"H_P1": "What the quarter means for the investment case",
"P1_PARAGRAPH": "<p>The quarter itself was sound: revenue matched consensus, the engine aftermarket kept growing close to 20% and defence equipment beat. What disappointed was the absence of a second guidance upgrade after July&rsquo;s raise, with operating income held at EUR 6.4bn to EUR 6.5bn while consensus already sat above the range. With jet fuel above $100, a French surtax likely to be extended and a cautious read-across from GE, investors now question how long airlines keep spending heavily on engine maintenance.</p>",

"C1_TITLE": "SAF: Q3 2026 revenue and 2026 guidance vs. consensus",
"C1_SUB": "% vs. consensus &middot; Q3: company-compiled consensus &middot; FY26: guidance midpoints vs. consensus per analyst first takes",
"C1_COMMENT": "<p>The reported lines were in line or better: group revenue matched the company-compiled consensus within 0.1% and Equipment &amp; Defense beat by 2.5%. Aircraft Interiors missed by 1.3%, as seat certification delays flagged in July persist. The two bars on the right carry the message: confirmed targets sit about 2% below consensus, so estimates edge down rather than up into the full-year results.</p>",

"BASE_CASE": "We stay positive on Safran and would build positions on this weakness. The earnings path we underwrite is intact: 2026 operating income of EUR 6.4bn to EUR 6.5bn, a 2028 target of EUR 7bn to EUR 7.5bn that management said in July may be revisited, and profits on LEAP-1B maintenance contracts recognised from early 2027, which moves earnings into next year rather than removing them. The debate has moved from engine deliveries to the durability of heavy maintenance spending. The catalyst is 2027 guidance at the full-year results in February 2027. Near term, jet fuel and French tax headlines can keep the shares under pressure.",
"UPSIDE": "2027 guidance in February implying operating income growth above 10%; heavy CFM56 shop visits holding, as management expected in July; advance payments on India&rsquo;s 114 Rafale order, which are not in guidance; LEAP deliveries reaching high-teens growth for 2026.",
"DOWNSIDE": "Evidence of workscope compression, with airlines deferring heavy CFM56 shop visits while jet fuel stays above $100; the French surtax extended into 2027 at the 2026 level; LEAP delivery growth short of the high-teens target, pointing to supply-chain strain.",

"H_A1": "Results: the aftermarket still carries the group",
"A1_PARAGRAPHS": "<p>Revenue reached EUR 9.0bn, up 14.7% reported and 13.4% organically, in line with the EUR 8.99bn company-compiled consensus. Propulsion grew 13.2% organically. The mix remains the story: aftermarket revenue rose 18.7% and services 19.0% in dollars, while original equipment grew only 3.5%. LEAP deliveries reached 535 engines, up 5%, a sharp slowdown after 41% growth in the first half, which leaves a heavy fourth quarter to meet the high-teens target for the year. Aftermarket-led growth is good for profit: in the first half it lifted the propulsion margin to a record 24.5%, above the 22% to 24% range, and the group margin to 18.4%.</p>"
                 "<p>Equipment &amp; Defense revenue rose 16% organically to EUR 3.62bn, against EUR 3.53bn expected, the strongest division in the quarter. Reported growth is flattered by the integration of the Collins actuation business and by the transfer of Safran Ventilation Systems from Aircraft Interiors at the start of 2026. Aircraft Interiors grew 6% organically to EUR 751m, against EUR 761m expected; seat deliveries remain capped by certification delays that management in July called an industry issue. Safran reports no profit figures at the third quarter, so the margin read waits for February.</p>",

"H_A2": "Outlook: guidance held, upside pushed to 2027",
"A2_PARAGRAPHS": "<p>Safran confirmed the 2026 targets raised in July: revenue growth in the mid-teens, recurring operating income of EUR 6.4bn to EUR 6.5bn and free cash flow of EUR 4.7bn to EUR 4.9bn, including about EUR 500m of French surtax. The midpoints sit 2.1% and 1.8% below consensus, so estimates should drift lower. Profit recognition on LEAP-1B maintenance contracts is now expected in early 2027 rather than late 2026: a timing shift that removes a 2026 upside and adds to 2027. In July, management expected heavy CFM56 workscopes to last through 2027 and 2028.</p>",

"H_C2": "Valuation: the multiple has done the adjusting",
"C2_TITLE": "SAF: share price vs. consensus earnings and valuation",
"C2_SUB": "Weekly, Sep 2005 to 23 Oct 2026 &middot; Bloomberg BEst 12m-forward EPS &middot; 40-week MA &middot; Log scale &middot; Last price: 23 October, intraday, after the release",
"C2_COMMENT": "<p>Over 12 months the share price fell 7.9% while consensus forward EPS rose 27.9%: earnings kept rising and the multiple absorbed the whole correction. At 27.0x forward earnings the stock trades 27% above its 21.3x average since 2005, but below its one-year average of 31.7x and its five-year average of 30.0x. The multiple has fallen from 34.9x at the record high of EUR 363.6 on 12 August, and the price sits 10% below its 40-week average of EUR 317. Even a 5% cut to consensus EPS at today&rsquo;s price would leave the multiple at 28.5x, still below its five-year average.</p>",

"SOURCE_LINE": "Source: Syz Research, Bloomberg, Safran Q3 2026 revenue release of 23 October 2026, Safran H1 2026 earnings call of 28 July 2026, analyst research notes of 23 October 2026",
}
