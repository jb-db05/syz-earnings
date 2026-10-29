"""content.py: all text for the Eli Lilly Q3 2026 Earnings update (HTML entities; fill.json is derived from it)."""

DATE = "29 October 2026"

TITLE = "Eli Lilly Q3 2026: volume drives a beat and raise at 26x"

QUOTE = ("Lilly had another strong quarter, exceeding our prior expectations and allowing us to raise our "
         "full-year outlook. Revenue growth was driven by broad global consumer demand for Mounjaro and Zepbound&hellip;")
QUOTE_WHO = "David A. Ricks, chair and CEO, Q3 2026 results release, 29 October 2026"

COMPANY_INTRO = ("Eli Lilly develops medicines for diabetes, obesity, cancer, immune disorders and Alzheimer&rsquo;s disease. "
                 "Mounjaro and Zepbound made up 66% of Q3 2026 revenue of USD 24.4bn; the US accounts for 62%. "
                 "Listed in New York.")

TAKEAWAYS = [
    ("pos", "Beat", "Revenue USD 24.4bn (+8% vs. consensus) and EPS USD 7.48 (+32%); shares up 8.2% intraday on 29 October."),
    ("pos", "Raised", "2026 revenue guide raised by USD 5.5bn to USD 91 to 92bn; the implied Q4 looks cautious."),
    ("neg", "Watch", "About USD 0.9bn of one-offs flattered revenue, and realised prices fell 15% as cheaper channels grow."),
    ("neu", "Valuation", "26.2x 12m-forward earnings, in line with the 26.3x average since 2018, for 39% revenue growth."),
]

KPIS = [
    ("Revenue", "USD 24.4bn", "+8.0% vs. consensus", "pos"),
    ("Non-GAAP EPS", "USD 7.48", "+31.7% vs. consensus", "pos"),
    ("Gross margin (non-GAAP)", "84.4%", "+100bp vs. expectations", "pos"),
    ("2026 revenue guide", "USD 91&ndash;92bn", "+USD 5.5bn at midpoint", "pos"),
]

H_P1 = "Volume carries the quarter and the guidance"
P1_PARAGRAPH = ("Revenue beat consensus by 8% and non-GAAP EPS by 32%, and the shares rose 8.2% intraday on 29 October "
                "to a record USD 1,393. The move matches the size of the beat and of the USD 5.5bn guidance raise. "
                "Volume grew 53% and absorbed a 15% fall in realised prices: demand for Mounjaro and Zepbound keeps "
                "widening the earnings base faster than price erodes it.")

C1_TITLE = "LLY: Q3 2026 results vs. consensus"
C1_SUB = ("Surprise vs. consensus, % &middot; ex one-offs strips about USD 0.9bn of non-recurring revenue "
          "&middot; FY26 guide: midpoint vs. prior guide")
C1_COMMENT = ("Half of the revenue beat came from one-offs: USD 410m of Jardiance milestones, the last ones, and about "
              "USD 490m of rebate and discount adjustments. Stripped of both, revenue still beat by 4%. "
              "International Mounjaro gave the cleanest upside, 8% above consensus. Foundayo, the new oral GLP-1, "
              "missed by 20% at USD 184m.")

BASE_CASE = ("The case remains very constructive and the risk/reward skewed to the upside. We underwrite 2026 revenue "
             "in the top half of the USD 91 to 92bn range and EPS of about USD 35.50 after USD 4.57 per share of acquired "
             "research charges. For 2027 the open point is price: volume has to keep outrunning price cuts as Medicare "
             "and lower-priced channels expand. The retatrutide filing in Q1 2027 is the next catalyst, and the Q4 print "
             "with first 2027 guidance is the next test.")
UPSIDE = ("Q4 revenue above USD 24.8bn, the top of the implied range; international Mounjaro adding another USD 0.5bn "
          "on Q3; the retatrutide filing on time in Q1 2027; realised price declines easing below 10% a year.")
DOWNSIDE = ("US realised price falling faster than 7% a year without matching volume; Foundayo missing consensus again in Q4; "
            "a retatrutide filing slipping beyond Q1 2027; new US rules capping obesity drug prices in Medicare.")

P2_TITLE = "Beyond the key takeaways"

H_A1 = "Results: volume did the work"
A1_PARAGRAPHS = [
    ("Worldwide volume rose 53% and realised prices fell 15%. In the US, volume grew 41% at a 7% lower price; "
     "outside the US, volume rose 76% at a 29% lower price, as launches reach lower-priced markets. Mounjaro sales "
     "reached USD 10.7bn (+65%), of which USD 5.7bn came from outside the US (+93%), more than USD 570m above Q2 and "
     "USD 415m above consensus. Zepbound added USD 5.4bn (+49%) on wider US coverage and a ramp in Medicare. Key "
     "products in oncology, immunology and neuroscience doubled. Non-GAAP gross margin reached 84.4%, 80bp above "
     "Q3 2025 and about 100bp above expectations, the main reason EPS beat by more than revenue."),
    ("Revenue beat consensus by 8% and EPS by 32%, and the shares rose 8.2% intraday on 29 October against the "
     "28 October close of USD 1,288: surprise and reaction are aligned. The confirmed drivers are the USD 5.5bn raise "
     "to revenue guidance and a 250bp lift to the performance margin guide, now 52.0 to 52.5%. About USD 0.9bn of revenue will not repeat, and no further Jardiance milestones remain. EPS of "
     "USD 7.48 already absorbs USD 4.57 per share of acquired research charges. We read the rally as a response to "
     "the underlying trend, with revenue 4% ahead of consensus after one-offs."),
]

H_A2 = "Outlook: the raised guide still looks cautious"
A2_PARAGRAPHS = [
    ("Lilly now guides 2026 revenue at USD 91 to 92bn, from USD 85 to 87bn, and non-GAAP EPS at USD 35.00 to 36.00, "
     "from USD 35.50 to 36.50. The lower EPS range reflects the Q3 research charge of USD 4.57 per share; on our "
     "arithmetic the underlying EPS outlook rose by about USD 4. Against nine-month revenue of USD 67.2bn, the "
     "midpoint implies Q4 revenue of about USD 24.3bn, flat on Q3, and Q4 EPS of about USD 11.10, below the USD 12.05 "
     "Q3 figure before research charges. A higher tax rate guide of 19 to 20% explains part of that gap."),
]

H_C2 = "Valuation: earnings carried the rally"
C2_TITLE = "LLY: share price vs. consensus earnings and valuation"
C2_SUB = ("LLY US Equity, weekly from November 2018 (first consensus EPS) &middot; BEst 12m-forward consensus &middot; "
          "40-week simple MA &middot; log scale &middot; P/E shaded above (orange) / below (blue) its 2018 to 2026 average "
          "&middot; last point is the 29 October intraday price, after the release")
C2_COMMENT = ("The shares trade at a record USD 1,393, 69% above the level of a year ago and 27% above the 40-week moving "
              "average of USD 1,097. The 12m-forward P/E stands at 26.2x on Bloomberg data, in line with the 26.3x average "
              "since 2018 and the 26.0x one-year average, and well below the 31.0x peak of January 2021. A year ago the "
              "multiple stood at 25.2x, so earnings growth delivered most of the gain. On the 2026 EPS guidance midpoint "
              "of USD 35.50 the shares trade at 39x, a multiple that 2027 growth has to bring down quickly.")

SOURCE_LINE = ("Source: Syz Research, Bloomberg, company filings, Eli Lilly results release of 29 October 2026, "
               "analyst research notes of 5 August to 29 October 2026")

W1, W2 = 74, 94            # PDF chart widths, % of text width
W1_PPTX, W2_PPTX = 66, 88  # PPTX chart widths
