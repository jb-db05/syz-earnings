"""content.py: all text for the PACCAR Q3 2026 earnings update (HTML entities; fill.json is derived from it)."""

DOC_TYPE = "Earnings update"
DATE = "28 October 2026"
TITLE = "PACCAR Q3 2026: trucks carry the quarter, 2027 rules weigh"

# No verbatim executive quote was available (transcript and release not reachable): quote block omitted.
QUOTE = ""
QUOTE_WHO = ""

COMPANY_INTRO = ("PACCAR designs and builds Kenworth, Peterbilt and DAF heavy trucks, sells aftermarket parts and "
                 "finances customers&rsquo; vehicles. Trucks were 76% of third-quarter truck and parts sales. "
                 "Nasdaq-listed, market value around USD 55bn.")

TAKEAWAYS = [
    ("pos", "Beat", "Truck pretax profit of USD 455m beat estimates by 43%, lifting net income 44% to USD 848m."),
    ("neu", "Reaction", "Shares eased 0.6% on 27 October: EPS met consensus at USD 1.61, sales missed by 1.3%."),
    ("neg", "Watch", "Unfinalised 2027 emission penalties delay orders; supplier shortfalls held deliveries 4.5% below guidance."),
    ("neu", "Valuation", "17.6x forward earnings, down from 23.9x in July while consensus EPS rose 3% over the same period."),
]

KPIS = [
    ("Sales ex financial services", "USD 7.38bn", "&minus;1.3% vs. consensus", "neg"),
    ("Diluted EPS", "USD 1.61", "In line with consensus", "neu"),
    ("Truck pretax profit", "USD 455m", "+43% vs. estimates", "pos"),
    ("Q4 delivery guide", "41,000&ndash;43,000", "Midpoint +4.7% vs. Q3", "neu"),
]

H_P1 = "Earnings recover as the multiple falls"
P1_PARAGRAPH = ("EPS of USD 1.61 met consensus and truck profit beat estimates by 43%, yet sales missed by 1.3% and "
                "the shares eased 0.6% on 27 October, a reaction in line with a mixed print. Higher "
                "deliveries lifted the truck pretax margin to 8.1%. The stock is held back by the unresolved 2027 "
                "emission rules and the timing of a pull-forward in orders.")

C1_TITLE = "PCAR: Q3 2026 results vs. consensus and guidance"
C1_SUB = ("Surprise vs. pre-results consensus or analyst estimates, % &middot; sales of truck, parts and other "
          "&middot; deliveries vs. the ~42,000 company guide")
C1_COMMENT = ("Trucks delivered a 43% profit surprise on revenue up 28% year on year, a "
              "pretax margin of 8.1%. Parts, the steadiest earner, posted record revenue of USD 1.78bn but pretax profit 14% below "
              "estimates. Supplier shortfalls cost about 1,900 deliveries against guidance, which we think explains "
              "most of the sales miss.")

BASE_CASE = ("We keep the position. We underwrite "
             "consensus forward EPS of USD 5.90, 16% above a year ago and 34% below the 2023 peak, "
             "carried by truck margins and record Parts revenue. The debate has moved from the freight recession to "
             "the 2027 rules and the size of a pull-forward in orders. At 17.6x, the July premium is gone and "
             "sentiment is negative, which we think limits the downside. The next test is Q4 deliveries of 41,000 "
             "to 43,000, due in late January 2027.")

UPSIDE = ("Final EPA non-conformance penalties before year-end that release held-back 2027 orders; Q4 deliveries "
          "at the top of the 41,000 to 43,000 range; a Q4 Truck, Parts and Other gross margin at 15%, the top of "
          "guidance.")
DOWNSIDE = ("Q4 deliveries below 41,000, a sign that supplier constraints run into 2027; a gross margin below the "
            "14% low end of guidance; a 2027 US and Canada market heading below 240,000 units if the pull-forward fails "
            "to materialise.")

P2_TITLE = "Beyond the key takeaways"
H_A1 = "Results: truck margins beat, parts slipped"
A1_PARAGRAPHS = [
    ("Consolidated revenue rose 19% to USD 7.94bn and net income 44% to USD 847.5m, or USD 1.61 per diluted share "
     "against USD 1.12 a year ago. Truck revenue grew 28% to USD 5.6bn on deliveries of 40,100, up 26%, which implies "
     "revenue per truck about 2% higher. Truck pretax profit reached USD 454.5m, a margin of 8.1%, against analyst "
     "estimates of USD 317m: operating leverage on higher volumes did the work. Parts revenue grew 3.2% to a record "
     "USD 1.78bn, but pretax profit of USD 404.4m, a 22.7% margin, came in 14% below estimates. Financial Services "
     "added USD 138.1m pretax, up 9.4%, on stable finance margins and a firmer used truck market."),
    ("Against consensus the print was mixed: EPS in line, sales 1.3% short at USD 7.38bn, "
     "truck profit ahead, Parts profit behind. The shares eased 0.6% on 27 October, a move in proportion to that "
     "mix, so surprise and reaction are aligned. The confirmed drivers are the delivery shortfall, which management "
     "attributed to supplier constraints, and an unchanged regulatory picture: customers are still waiting for the "
     "EPA&rsquo;s non-conformance penalties before placing 2027 orders. We think the muted move reflects "
     "expectations that were already low: the stock fell 4.8% in the three sessions before the release and trades "
     "25% below its July high."),
]
H_A2 = "Outlook: Q4 recovers, 2027 hinges on rules"
A2_PARAGRAPHS = [
    ("Management expects Q4 deliveries of 41,000 to 43,000 as supplier performance improves, a midpoint 5% above Q3, "
     "and a Truck, Parts and Other gross margin of 14% to 15%: price-cost is favourable, but production "
     "inefficiencies add cost. The 2026 US and Canada heavy truck market was narrowed to 240,000 to 260,000 units, "
     "and the first 2027 range of 240,000 to 280,000 has a midpoint 4% higher, supported by infrastructure-led "
     "vocational demand, where PACCAR holds a 40% share, and replacement. Europe is seen at 300,000 to 320,000 in both. Capital spending of USD 650m to 700m "
     "and research of USD 460m to 500m in 2027 fund clean-diesel, hybrid and battery-electric powertrains."),
]
H_C2 = "Valuation: earnings up, the multiple derated"
C2_TITLE = "PCAR: share price vs. consensus earnings and valuation"
C2_SUB = ("PCAR US Equity, daily data resampled to weekly, from January 2011 &middot; BEst 12m-forward consensus "
          "&middot; 40-week simple MA &middot; log scale &middot; P/E shaded above (orange) / below (blue) its 2011 "
          "to 2026 average &middot; last price is the 27 October close, after the release")
C2_COMMENT = ("Over 12 months consensus forward EPS has risen 16.4% to USD 5.90 while the share price is up only 2.6%, "
              "so the multiple has done the adjusting. The derating is recent: at the 28 July peak of USD 138.2, "
              "after Q2, the stock traded on 23.9x; it now trades on 17.6x, the lowest since July 2025, 16% above the "
              "15.1x average since 2011 and below the 20.9x one-year average. The price sits 13% below its 40-week "
              "average of USD 120. A 10% upgrade at an unchanged price would take the multiple to 16.0x, close to "
              "the long-run average.")

SOURCE_LINE = ("Source: Syz Research, Bloomberg, company filings, PACCAR results release of 27 October 2026, "
               "analyst research notes of 8 and 27 October 2026")

W1, W2 = 78, 94            # PDF chart widths, % of text width
W1_PPTX, W2_PPTX = 70, 88  # PPTX chart widths
