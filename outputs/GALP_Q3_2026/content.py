"""content.py: all text for the Galp Q3 2026 Earnings update (HTML entities; fill.json is derived from it)."""

DOC_TYPE = "Earnings update"
THEME = "Integrated oil and gas"
DATE = "26 October 2026"
TITLE = "Galp Q3 2026: guidance raised, deal dropped, the sell-off goes too far"

QUOTE = ("While discussions with Moeve regarding a potential combination of our downstream businesses have "
         "concluded without an agreement, Galp&rsquo;s strategic direction and investment proposition remain unchanged.")
QUOTE_WHO = "Maria Jo&atilde;o Carioca and Jo&atilde;o Marques da Silva, co-CEOs, Q3 2026 results release, 26 October 2026"

TAKEAWAYS = [
    ("pos", "Beat", "RCA EBITDA of EUR 1,522m rose 67% and came in 3.5% above consensus, led by Bacalhau and refining."),
    ("pos", "Raised", "Full-year EBITDA guidance lifted to c.EUR 5bn from c.EUR 4bn, operating cash flow to c.EUR 3.9bn."),
    ("neg", "Watch", "Moeve downstream talks ended without a deal, removing c.EUR 1.1 per share of expected synergy value."),
    ("neu", "Valuation", "The 8.8% results-day fall leaves 8.4x forward earnings, 27% below the 2022 to 2026 average."),
]

KPIS = [
    ("RCA EBITDA", "EUR 1,522m", "+3.5% vs. consensus", "pos"),
    ("RCA net income", "EUR 682m", "+68% year on year", "pos"),
    ("FY26 EBITDA guide", "c.EUR 5.0bn", "+25% vs. prior guide", "pos"),
    ("Net debt", "EUR 1.43bn", "0.35x EBITDA", "neu"),
]

H_P1 = "The debate moves from earnings to Brazil risk"
P1 = ("Operationally, this was one of Galp&rsquo;s strongest quarters: the Bacalhau field lifted production 14% and a "
      "refining margin of USD 34 per barrel, triple last year&rsquo;s, drove a 25% guidance upgrade. The market looked past it. The shares fell 8.8% on results day as the end of the "
      "Moeve talks removed a catalyst and Brazil&rsquo;s election-year fiscal noise raised the risk premium on "
      "its offshore assets. We think the price now discounts more than the lost deal.")

C1_TITLE = "GALP: Q3 2026 RCA EBITDA vs. consensus and history"
C1_SUB = ("EUR m &middot; replacement cost adjusted (RCA) EBITDA, which strips out inventory gains and one-offs "
          "&middot; consensus: pre-results analyst estimates")
C1_COMMENT = ("RCA EBITDA rose 67% year on year and 20% on the previous quarter to EUR 1,522m, 3.5% ahead of consensus. "
              "Upstream contributed EUR 708m and Industrial &amp; Midstream EUR 639m, double last year despite EUR 172m of "
              "refining hedge losses. Commercial grew 24% and Renewables tripled to EUR 48m. The beat came from volumes "
              "and margins, not one-offs.")

BASE_CASE = ("We stay positive on Galp and would use the results-day weakness to add, sized for Brazil political risk. "
             "We underwrite the new 2026 guidance of c.EUR 5bn EBITDA and c.EUR 3.9bn operating cash flow, with net debt at "
             "0.35x EBITDA funding a proposed 10% dividend increase to EUR 0.70 and the EUR 250m buyback. The debate is now how much of "
             "those earnings Brazil keeps. The 8.8% drop, about EUR 2.0 per share, already exceeds the c.EUR 1.1 of deal "
             "value the market had assigned. The next test is Brazil&rsquo;s post-election stance on the oil export tax.")

UPSIDE = ("Brazil lets the temporary oil export tax lapse after the run-off; Bacalhau holds about 160,000 barrels a day "
          "gross through the fourth quarter; Q4 EBITDA beats the c.EUR 1.26bn implied by guidance; a larger 2027 buyback "
          "at full-year results.")
DOWNSIDE = ("The export tax becomes permanent or is raised above 12%, or royalties are reopened under a "
            "resource-nationalism agenda; refining margins fall back towards the USD 13 per barrel of the original "
            "guidance; capital is redirected into a large, dilutive acquisition after Moeve.")

P2_TITLE = "Beyond the key takeaways"
H_A1 = "Results: Bacalhau and refining did the work"
A1 = [
    ("Upstream RCA EBITDA rose 53% to EUR 708m. Working-interest production averaged 131 kboe/d, up 14%, as the "
     "Bacalhau FPSO ramped up with four producer wells connected, reaching about 160 kboe/d gross in September and more "
     "than offsetting planned turnarounds. Oil realisations rose 32% to USD 87.3/bbl, although the discount to Brent "
     "widened to USD 9.7/bbl on freight and softer Asian demand for Brazilian crude. Industrial &amp; Midstream EBITDA "
     "doubled to EUR 639m: the refining margin reached USD 34.0/boe against USD 9.5/boe a year ago, on diesel cracks of "
     "USD 590/t, with Sines running close to full availability. Margin hedges cost EUR 172m and supply pricing-formula "
     "lags a further EUR 125m."),
    ("Commercial EBITDA rose 24% to EUR 147m on B2B sales in Spain; Renewables tripled to EUR 48m on newly acquired "
     "wind assets. RCA net income of EUR 682m, about EUR 0.94 "
     "per share on our count, rose 68% despite RCA taxes up 79% to EUR 493m, which include Brazil&rsquo;s temporary oil "
     "export tax. IFRS net income was EUR 201m after EUR 453m of special items, mostly derivative mark-to-market. "
     "Operating cash flow of EUR 1,223m (+63%) covered EUR 646m of capex, including EUR 420m for Spanish wind, and the "
     "EUR 253m interim dividend, leaving net debt at EUR 1.43bn."),
]

H_A2 = "Outlook: the upgrade leans on the macro deck"
A2 = ("Management raised 2026 RCA EBITDA guidance to c.EUR 5bn from c.EUR 4bn and operating cash flow to c.EUR 3.9bn "
      "from c.EUR 3bn, on Brent at USD 90/bbl (from 80) and a realised refining "
      "margin of c.USD 25/boe (from 13). The guide implies Q4 EBITDA of about EUR 1.26bn and, on our "
      "arithmetic, a Q4 Brent near USD 78/bbl against USD 97 in Q3. The risk sits in Brazil: the temporary 12% crude export tax costs up to EUR 100m, and the polarised run-off widened "
      "the risk premium on pre-salt assets, which in our view complicated valuation talks with Moeve&rsquo;s shareholders.")

H_C2 = "Valuation: earnings ran ahead of the price"
C2_TITLE = "GALP: share price vs. consensus earnings and valuation"
C2_SUB = ("GALP PL Equity, weekly from January 2022 (the 2020 earnings collapse lifted the P/E above 130x) &middot; BEst "
          "12m-forward consensus &middot; 200-day (c. 40-week) simple MA &middot; log scale &middot; P/E shaded vs. its "
          "2022 to 2026 average &middot; last price is the 26 October results-day print; consensus EPS not yet revised")
C2_COMMENT = ("Earnings have run well ahead of the share price. Over 12 months, consensus 12m-forward EPS rose 87% to "
              "EUR 2.48 while the price gained 24%, so the forward P/E fell from 12.7x to 8.4x, 27% below its 11.6x "
              "average since 2022 and under the 10.9x one-year average; results day alone took it down from 9.2x. The "
              "price is 10% below its September high of EUR 23.18 but still 6% above its 40-week average. Even if "
              "consensus EPS were cut 10% for the export tax, the stock would trade on 9.4x, 19% below its 2022 to 2026 "
              "average.")

SOURCE_LINE = ("Source: Syz Research, Bloomberg, company filings, Galp Q3 2026 results release of 26 October 2026, "
               "analyst research notes of 23 October 2026")

W1, W2 = 74, 92            # PDF chart widths (% of text width)
W1_PPTX, W2_PPTX = 66, 88  # PPTX chart widths
