"""TSMC Q3 2026 Earnings update: all text (HTML entities). Shared by the PDF and the PPTX build."""

TICKER, PERIOD = "TSM", "Q32026"

FILL = {
    "DOC_TYPE": "Earnings update",
    "THEME": "Semiconductors",
    "DATE": "15 October 2026",
    "TITLE": "TSMC Q3 2026: AI demand lifts the bar again, 2nm is the margin cost",
    "QUOTE": "",          # no transcript or release quote available at the time of writing
    "QUOTE_WHO": "",
    "W1": 76,
    "W2": 94,
    "P2_TITLE": "Beyond the key takeaways",
    "SOURCE_LINE": "Source: Syz Research, Bloomberg, company filings, TSMC Q3 2026 results of 15 October 2026, "
                   "analyst research notes of 12 to 15 October 2026",
}

TAKEAWAYS = [
    ("pos", "Beat", "Revenue of TWD 1,494bn, up 51% on the year and 2.2% above consensus, on AI datacentre demand."),
    ("pos", "Raised", "The fourth-quarter guide of 12% to 16% sequential growth lifts 2026 growth to about 44%."),
    ("neg", "Watch", "Gross margin of 66.4% sat within guidance but below the 67% to 68% expected, on 2nm dilution."),
    ("neu", "Valuation", "19.7x forward earnings: 16% above the 2010 to 2026 average, well below the 23.3x one-year mean."),
]

KPIS = [
    ("Revenue", "TWD 1,494bn", "+2.2% vs. consensus", "pos"),
    ("Gross margin", "66.4%", "Below 67&ndash;68% expected", "neg"),
    ("Q4 revenue guide", "+12&ndash;16% q/q", "Midpoint +14% q/q", "neu"),
    ("2026 revenue growth", "c. 44%", "3&ndash;4% above prior estimates", "pos"),
]

H_P1 = "The debate moves from demand to margins"
P1 = ("TSMC remains the bottleneck of the artificial intelligence (AI) build-out. Revenue cleared the top of "
      "guidance by 2% to 3%, and management now expects 2026 growth of &ldquo;slightly above 40%&rdquo;, up from "
      "&ldquo;above 30%&rdquo;. Demand is not the question: the gap between supply and demand for leading-edge "
      "wafers is still described as large. The question is the cost of growth, as the 2nm ramp, overseas "
      "fabs and rising investment hold the gross margin below its second-quarter peak.")

C1_TITLE = "TSM: Q3 2026 revenue vs. consensus and history"
C1_SUB = "Quarterly revenue, TWD bn &middot; Q3 2026 consensus is the pre-results estimate &middot; Q3 2026 reported in orange"
C1_COMMENT = ("Third-quarter revenue rose 51% on the year and 17.6% on the quarter, TWD 32bn above the pre-results "
              "estimate. High-performance computing, the platform that carries AI accelerators, grew 22% "
              "sequentially, smartphones 10% and automotive 23% on electric-vehicle and driver-assistance demand. "
              "The beat came from the leading edge: 3nm capacity is still tight and the 2nm ramp is steeper "
              "than planned.")

BASE_CASE = ("We stay positive on TSMC and would add on the 13% pullback from the 2 October record. We back "
             "the AI-led earnings path: consensus 12-month forward EPS has risen 86% in a year, and the "
             "fourth-quarter guide should lift 2026 estimates by a further 2% to 3%. The debate has moved from "
             "demand to the margin cost of growth, with 2nm dilution and overseas fabs keeping gross margin in "
             "a 66% to 68% band. At 19.7x forward earnings the stock sits below its one-year average after "
             "a 39% rise, so earnings, not the multiple, carry the return. The next test is the "
             "January 2027 print and the 2027 capex guide.")

UPSIDE = ("A first-quarter 2027 gross margin guide at 67% or above despite the 2nm ramp; a 2027 capex budget "
          "of USD 80bn or more backed by customer commitments; confirmation of 2027 risk production for the "
          "next-generation A14 node.")
DOWNSIDE = ("Gross margin below 65% as 2nm and overseas fab dilution compound; capex heading for USD 100bn "
            "without matching price increases; any sign that hyperscaler AI budgets for 2027 stall, or new US "
            "tariffs on Taiwan-made chips.")

H_A1 = "Results: volume beat, margin held in range"
A1 = [
    ("Revenue of TWD 1,494bn beat the TWD 1,462bn pre-results estimate by TWD 32bn and exceeded the top of "
     "the guided range by 2% to 3%. The quarter added TWD 224bn of revenue on the second quarter and TWD 504bn "
     "on a year ago. The mix tells the story: high-performance computing grew more than twice as fast as "
     "smartphones on the quarter, as datacentre accelerators for NVIDIA, AMD and the hyperscalers absorbed "
     "most leading-edge output, while automotive added a cyclical leg. Supply, not demand, capped the "
     "quarter: N3 capacity remains tight, and a steeper N2 ramp than planned is what lifted revenue above "
     "the guided range."),
    ("Gross margin came in at 66.4%, within guidance and 695bp above the 59.5% of Q3 2025, but 130bp below "
     "the 67.7% of Q2 2026 and short of the 67% to 68% expected. The dilution is N2: a new node "
     "carries heavy depreciation before it scales. On reported revenue, the margin implies gross "
     "profit of about TWD 992bn, 2% above the TWD 973bn estimate, so the revenue beat more than offset the "
     "margin shortfall in absolute profit. We read the margin as the price of the node transition, not "
     "a loss of pricing power."),
]

H_A2 = "Outlook: capacity, not demand, sets the pace"
A2 = ("The fourth-quarter guide of 12% to 16% sequential growth, 14% at the midpoint, rests on continued "
      "high-performance computing strength and flagship smartphone builds and implies about 44% growth for "
      "2026, 3% to 4% above prior estimates. The 2026 capex budget of USD 60bn to 64bn was reiterated, with "
      "&ldquo;significantly higher&rdquo; spending flagged for 2027 and 2028; analyst estimates run to USD 80bn "
      "to 85bn in 2027 and up to USD 100bn in 2028. The A14 node has been pulled in, with risk production in "
      "2027 and volume manufacturing in 2028, and customer activity already above N2 at the same stage. "
      "Advanced packaging moves to 9x reticle sizes in 2027.")

H_C2 = "Valuation: earnings have outrun the price"
C2_TITLE = "TSM: share price vs. consensus earnings and valuation"
C2_SUB = ("TSM US (ADR), weekly, Jan 2010 to 15 Oct 2026 &middot; Price in USD, consensus 12m-forward EPS in TWD "
          "per ADR &middot; 40-week MA &middot; Log scale &middot; Last price on results day")
C2_COMMENT = ("Over 12 months the ADR has risen 39% while consensus 12-month forward EPS rose 86%, so the "
              "multiple has compressed from 24.9x a year ago and a 26.4x peak in June to 19.7x, its lowest since "
              "June 2025. That is still 16% above the 16.9x average since 2010, but below the 23.3x one-year "
              "average. The price stands 3.4% above its 40-week moving average of USD 397 after a 9.3% "
              "weekly fall. A further 16% of upgrades at an unchanged price would take "
              "the multiple back to its long-run average; analysts put the stock at about 16x 2027 earnings.")
