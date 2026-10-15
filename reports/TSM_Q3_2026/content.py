"""content.py: all text for the TSMC (TSM US) Q3 2026 Syz Earnings update (HTML entities)."""

TICKER, QUARTER = "TSM", "Q32026"

FILL = {
    "DOC_TYPE": "Earnings update",
    "THEME": "Semiconductors",
    "DATE": "15 October 2026",
    "TITLE": "TSMC Q3 2026: AI outruns capacity, margins are the debate",
    "P2_TITLE": "Beyond the key takeaways",
    "W1": 74,
    "W2": 94,
    "C1_IMG": "/home/claude/out/c1_crop.png",
    "C2_IMG": "/home/claude/out/c2_crop.png",
    "SOURCE_LINE": "Source: Syz Research, Bloomberg, company filings, analyst research notes of 15 October 2026",
}

QUOTE = ("Demand is extremely robust.&rdquo; &hellip; &ldquo;There is no ceiling for [TSMC&rsquo;s] profitability.")
QUOTE_WHO = ("C.C. Wei, Chief Executive Officer, Q3 2026 earnings call, 15 October 2026 "
             "(as reproduced in analyst research notes)")

TAKEAWAYS = [
    ("pos", "Beat", "Revenue of USD 46.7bn (+41%) and EPS of USD 4.54 per ADR both beat consensus by about 3%."),
    ("pos", "Raised", "The Q4 guide of USD 52.3&ndash;54.3bn sits 5&ndash;8% above prior consensus, locking in 44% growth for 2026."),
    ("neg", "Watch", "Gross margin of 66.4% missed by 0.6 points on 2nm dilution; overseas fabs cost 3&ndash;4 points in 2027."),
    ("neu", "Valuation", "19.7x forward earnings: 16% above the 2010 to 2026 average, well below the one-year average of 23.3x."),
]

KPIS = [
    ("Q3 revenue", "USD 46.7bn", "+3% vs. consensus", "pos"),
    ("Q3 EPS per ADR", "USD 4.54", "+2.7% vs. consensus", "pos"),
    ("Q3 gross margin", "66.4%", "&minus;0.6pp vs. consensus", "neg"),
    ("Q4 revenue guide", "USD 53.3bn", "+5&ndash;8% vs. consensus", "pos"),
]

H_P1 = "AI now sets the pace, not the cycle"
P1_PARAGRAPH = ("<p>The quarter matters less for the 3% beat than for what management said about the years ahead. "
                "Taiwan Semiconductor Manufacturing Company (TSMC) now expects revenue from artificial intelligence (AI) "
                "accelerators to grow faster than the mid-to-high 50s% annual pace it guided for 2024 to 2029, and plans "
                "to more than double its 2-nanometre (2nm) capacity in 2027. Demand is no longer the question: the debate "
                "has moved to how much of it reaches margins and free cash flow.</p>")

C1_TITLE = "TSM: everything beat except the margin"
C1_SUB = ("Surprise vs. pre-results consensus in %, gross margin in percentage points &middot; Q4 guide at its "
          "USD 53.3bn midpoint vs. prior consensus &middot; EPS per ADR in USD at the 15 October exchange rate &middot; Revenue and margin consensus approximate")
C1_COMMENT = ('<p>The pattern is clear: the top line beat, the margin slipped. Revenue and earnings per share (EPS) both beat consensus by about 3%, and the fourth-quarter guide sits around 6.5% above prior expectations, a 14% sequential step-up. The only miss was gross margin, 0.6 points short at 66.4%, entirely from the 2nm ramp, which should fade as yields improve.</p>')

BASE_CASE = ("We stay positive on TSMC and would add on weakness around the results. We underwrite US dollar revenue "
             "growth of 44% in 2026 and an AI business compounding at more than 50% a year; consensus 12-month forward "
             "EPS is already up 88% in a year. The debate has moved from demand to returns: capital spending "
             "of USD 60&ndash;64bn this year rises sharply in 2027 to 2028, and overseas fabs dilute gross margin by "
             "3&ndash;4 points, which analysts expect pricing to cut to about 1 point. Tactically, the American depositary "
             "receipt (ADR) sits 13% below its 2 October record. The next test is the fourth-quarter release in "
             "mid-January 2027.")

UPSIDE = ("Fourth-quarter gross margin at or above the 67% top of guidance in January; AI accelerator growth confirmed "
          "above the mid-to-high 50s% pace; 2nm yields fast enough to lift 2027 capacity beyond the planned doubling; "
          "subsidies or customer commitments funding the Dallas complex.")
DOWNSIDE = ("Gross margin below 65%, the bottom of the fourth-quarter guide, and staying there through the 2nm and A14 "
            "ramps; capital spending above USD 100bn in 2027 without matching revenue; higher US tariffs on chips; "
            "an AI derating that takes the multiple below its 16.9x average.")

H_A1 = "Results: volume beat, 2nm dented the margin"
A1_PARAGRAPHS = [
    ("<p>Third-quarter revenue of USD 46.7bn rose 16.2% quarter on quarter, above guidance, and 41% year on "
     "year, about 3% ahead of consensus. High-performance computing (HPC), smartphones and automotive led demand, and the "
     "strength was broad rather than a single product cycle. Operating leverage was strong: the operating margin reached 58.7%, ahead of "
     "expectations, and EPS of USD 4.54 per ADR beat the USD 4.43 consensus by 2.7% and rose 69% year on year, in line with net "
     "income. This is the third consecutive quarter of beat-and-raise, and it came with an upgrade to the multi-year AI "
     "outlook, with agentic AI named as an additional growth engine on top of the cloud AI build-out.</p>"),
    ("<p>Gross margin was the one soft line. At 66.4% it came in about 0.6 points below elevated expectations of 67% and "
     "1.3 points below the 67.7% of the second quarter, a decline management attributes entirely to the dilution from the "
     "2nm ramp. We read this as a cost of leadership rather than pricing pressure: the dilution was limited for a "
     "first-year node, and analysts see it as support for scarcity-driven pricing in 2027. Analyst estimates put 2026 "
     "return on equity near 44%, with a net cash balance sheet, so the margin step-down does not constrain the "
     "investment plan.</p>"),
]

H_A2 = "Outlook: capacity, not demand, is the limit"
A2_PARAGRAPH = ('<p>The fourth-quarter guide of USD 52.3&ndash;54.3bn, with gross margin of 65&ndash;67%, implies 44% US dollar revenue growth for 2026. Capital spending stays at USD 60&ndash;64bn this year, but 2026 to 2028 spending is guided well above the USD 101bn of the previous three years; analyst estimates range from USD 80&ndash;85bn to USD 90bn for 2027 and reach USD 105bn for 2028. Capacity follows: 2nm more than doubles in 2027, Arizona Fab 2 (3nm) starts volume production in the third quarter of 2027, and a Dallas complex could take planned US investment to about USD 530bn. Overseas margin dilution rises from about 2 points in 2026 to 3&ndash;4 points in 2027.</p>')

H_C2 = "Valuation: earnings did the work, not the multiple"
C2_TITLE = "TSM: share price vs. consensus earnings and valuation"
C2_SUB = ("ADR in USD, weekly, January 2010 to 15 October 2026 &middot; Bloomberg 12m-forward consensus EPS per ADR in USD, at Bloomberg&rsquo;s implied exchange rate "
          "&middot; 40-week simple moving average &middot; Log scale &middot; Last price is the 15 October (results day) print")
C2_COMMENT = ('<p>Over 12 months the ADR is up 46% to USD 411 while consensus 12-month forward EPS rose 88% to USD 20.8 per ADR, so the forward price-to-earnings ratio (P/E) fell from 25.3x to 19.7x. That is 16% above the 16.9x average since 2010, but below the one-year average of 23.3x and the 33.9x peak of February 2021. The price is 13% below its 2 October record and 3% above its 40-week moving average of USD 397. Analysts put the stock at about 16x 2027 earnings; a 10% upgrade at an unchanged price takes the multiple to 17.9x, near its average.</p>')
