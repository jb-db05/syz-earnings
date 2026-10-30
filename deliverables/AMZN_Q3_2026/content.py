"""content.py: all text for the Amazon Q3 2026 earnings update (HTML entities; fill.json is derived from it)."""

DOC_TYPE = "Earnings update"
DATE = "30 October 2026"
TITLE = "Amazon Q3 2026: AWS speeds up, capex weighs on the shares"

QUOTE = ("Our AWS investment in functionality and infrastructure is working &hellip; There has never been a "
         "trillion dollar revenue business, and we may have two of them in the next 5-10 years.")
QUOTE_WHO = "Andy Jassy, President and CEO, Amazon Q3 2026 results release, 29 October 2026"

COMPANY_INTRO = ("Amazon runs online stores, an advertising business and the AWS cloud platform. AWS earned 63% of "
                 "Q3 operating income on 23% of sales. 2025 revenue USD 717bn; Nasdaq market value around USD 2.6trn.")

TAKEAWAYS = [
    ("pos", "Beat", "AWS revenue +39.3%, a sixth quarter of acceleration; operating income USD 28.1bn at a record 13.9% margin."),
    ("neg", "Reaction", "Shares down 7% pre-market on 30 October: Q4 guide below consensus, USD 33.5bn quarterly cash outflow."),
    ("neg", "Watch", "2026 capex of about USD 220bn and more in 2027; free cash flow &minus;USD 42.4bn over twelve months."),
    ("neu", "Valuation", "26.1x forward earnings before the release, near the 26.3x average since 2018; about 24x after the drop."),
]

KPIS = [
    ("Revenue", "USD 201.9bn", "&minus;0.2% vs. consensus", "neg"),
    ("AWS revenue", "USD 46.0bn", "+39.3% y/y vs. +38% consensus", "pos"),
    ("Operating income", "USD 28.1bn", "+6% vs. top of guide", "pos"),
    ("Q4 operating income guide", "USD 28.5&ndash;33.5bn", "Midpoint below consensus", "neg"),
]

H_P1 = "Record profit meets a softer Q4 guide"
P1_PARAGRAPH = ("Operating income beat the top of guidance by USD 1.6bn and AWS growth beat consensus by 1.3 points, yet "
                "the shares were down 7% pre-market on 30 October, after a 4.2% fall on 29 October. "
                "The Q4 guide, softer advertising and a USD 33.5bn free cash outflow drove the reaction. AWS earnings "
                "power improved; the cash return on the build-out lies further out.")

C1_TITLE = "AMZN: Q3 2026 operating income vs. guidance and prior year"
C1_SUB = "USD bn &middot; Q3 2025 and Q3 2026 reported &middot; Q3 2026 guidance range from the Q2 2026 release"
C1_COMMENT = ("Operating income rose 61% to USD 28.1bn, 6% above the top of the USD 22.5bn to 26.5bn range. AWS "
              "contributed USD 17.8bn at a 38.7% margin, and the North America margin rose to 7.7% from 4.5%. Mix, "
              "lower cost per unit shipped and marketing leverage drove the beat, with revenue 0.2% below consensus.")

BASE_CASE = ("The investment case remains constructive. We underwrite AWS growth near 40% in 2027, supported by a "
             "USD 578bn backlog against about USD 200bn a year ago, and a return to positive free cash flow in Q4 as "
             "capex timing evens out. The share price now depends on the return on USD 220bn of annual capex, most of it for AWS. At about 24x forward earnings after the drop, "
             "expectations have reset. The next test is the Q4 report in early February 2027.")
UPSIDE = ("AWS growth above 40% in Q4, with quarterly dollar additions back above USD 4.6bn; positive Q4 free cash "
          "flow; advertising growth back in the high teens in Q4, as guided.")
DOWNSIDE = ("AWS dollar additions below USD 3.8bn for a second quarter; a 2027 capex guide far above USD 220bn "
            "without a step-up in backlog; new debt ahead of a free cash flow recovery.")

P2_TITLE = "Beyond the key takeaways"
H_A1 = "Results: AWS mix and unit costs drove margin"
A1_PARAGRAPHS = [
    ("Revenue rose 12% to USD 201.9bn (13% excluding currency), 0.2% below the USD 202.3bn consensus and at the top "
     "of the USD 197bn to 202bn guide. Growth slowed 8 points from Q2 as Prime Day fell in Q2 this year. AWS revenue of USD 46.0bn grew 39.3%, ahead of the 38% consensus, with operating income up 55% to USD 17.8bn. North America sales rose 6% to USD 112.9bn at "
     "a 7.7% margin, helped by lower fulfilment and shipping cost per unit. Stores unit growth reached 17%, the "
     "highest since the pandemic lockdowns. EPS was USD 1.89 against USD 1.95, as non-operating items and tax "
     "absorbed the operating gain."),
    ("The shares were down 7% pre-market on 30 October against an operating beat of 15% on the guide midpoint: "
     "price and results diverged. Confirmed drivers: the Q4 midpoints of USD 243.5bn for revenue and USD 31.0bn for "
     "operating income sit below consensus; advertising grew 12% excluding currency, short of expectations; free "
     "cash flow was about &minus;USD 33.5bn against an analyst estimate near &minus;USD 15bn, on "
     "USD 75.9bn of cash capex. We think, without confirmation from the company, that expectations ran high into "
     "the print: the stock rose 15.3% after the Q2 results to a USD 284 record, and investors looked "
     "for AWS growth near 42%."),
]
H_A2 = "Outlook: capacity sets the AWS pace into 2027"
A2_PARAGRAPH = ("Q4 guidance calls for revenue of USD 240bn to 247bn, up 12% to 16%, and "
                "operating income of USD 28.5bn to 33.5bn against USD 25.0bn a year earlier. Management kept 2026 cash "
                "capex at about USD 220bn and pointed to meaningfully more in 2027. The company "
                "expects AWS growth above 40% in 2027 and 2028 and advertising growth back in the high teens. AWS "
                "dollar additions slowed to USD 3.8bn from USD 4.6bn in Q2, consistent with capacity limits. Long-term "
                "debt stands at USD 173bn against USD 66bn at the end of 2025; analysts see no need for equity and a "
                "possible further USD 50bn of debt late in 2027.")

H_C2 = "Valuation: at the long-run average multiple"
C2_TITLE = "AMZN: share price vs. consensus earnings and valuation"
C2_SUB = ("Weekly, November 2018 (first consensus EPS) to 29 October 2026 &middot; Bloomberg BEst 12m-forward EPS and "
          "P/E &middot; 40-week MA from weekly closes &middot; log scale &middot; last price is the 29 October close, "
          "before the release")
C2_COMMENT = ("The share price closed at USD 243.79 on 29 October, flat over twelve months, as consensus 12m-forward "
              "EPS rose 8.8% over the same period and 3.0% since the Q2 print. Bloomberg&rsquo;s forward P/E stood at "
              "26.1x, 1% below its 26.3x average since 2018, in line with the one-year average of 26.0x and well below "
              "the 31.0x peak of January 2021. The price sat on its 40-week average of USD 243.4. A 7% fall at "
              "unchanged estimates takes the multiple to about 24.3x, 8% below the long-run average and above the "
              "22.6x low of December 2025.")

SOURCE_LINE = ("Source: Syz Research, Bloomberg, company filings, Amazon.com Q3 2026 results release of 29 October 2026, "
               "analyst research notes of 30 October 2026")
