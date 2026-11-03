"""content.py: all text for the Apple Q4 FY2025 Earnings update (HTML entities; fill.json is derived from it)."""

DOC_TYPE = "Earnings update"
DATE = "31 October 2025"
TICKER, PERIOD = "AAPL", "Q4FY2025"

TITLE = "Apple Q4 FY2025: strong guide, fully priced stock"

QUOTE = ("In September, we were thrilled to launch our best iPhone lineup ever, including iPhone 17, "
         "iPhone 17 Pro and Pro Max, and iPhone Air.")
QUOTE_WHO = "Tim Cook, CEO, Apple Q4 FY2025 results release, 30 October 2025"

COMPANY_INTRO = ("Apple designs the iPhone, Mac, iPad and wearables and earns a rising share from services. "
                 "iPhone made 50% of fiscal 2025 revenue of USD 416bn, Services 26%. Listed on Nasdaq, worth about USD 4tn.")

TAKEAWAYS = [
    ("pos", "Beat", "Revenue USD 102.5bn and EPS USD 1.85 beat consensus by 0.2% and 4.5%, led by Services and margin."),
    ("pos", "Guide", "December-quarter guide of 10&ndash;12% growth sits 4% above consensus, with iPhone up double digits."),
    ("neg", "Reaction", "Shares slipped 0.4% on 31 October as the Nasdaq rose 0.6%: iPhone revenue missed consensus by 2.3%."),
    ("neu", "Valuation", "32.7x forward earnings, 20% above the five-year average and close to the 33.9x peak of December 2024."),
]

KPIS = [
    ("Revenue", "USD 102.5bn", "+0.2% vs. consensus", "pos"),
    ("Diluted EPS", "USD 1.85", "+4.5% vs. consensus", "pos"),
    ("Gross margin", "47.2%", "+80bp vs. consensus", "pos"),
    ("Dec-Q revenue guide", "+10&ndash;12% y/y", "+4.3% vs. consensus", "pos"),
]

H_P1 = "The iPhone 17 cycle is real and supply-bound"
P1_PARAGRAPH = ("<p>Apple beat consensus by 4.5% on EPS and guided December-quarter revenue about 4% above expectations, "
                "yet the shares slipped 0.4% on 31 October while the Nasdaq rose 0.6%. The confirmed drag was iPhone "
                "revenue, 2.3% short of consensus as supply of several models fell short. We read the muted "
                "move as positioning after an 11% run into the print.</p>")

C1_TITLE = "AAPL: Q4 FY2025 surprises vs. consensus"
C1_SUB = ("Reported vs. LSEG consensus in % &middot; gross margin in margin points (bp) &middot; "
          "December-quarter guide at the 11% midpoint vs. USD 132.3bn consensus")
C1_COMMENT = ("<p>Every line beat except iPhone. Services, up 15% to a record USD 28.8bn, and an 80bp gross margin beat "
              "did the work, despite USD 1.1bn of tariff costs. The guide is the bigger surprise: 11% growth at the midpoint "
              "implies about USD 138bn of revenue against USD 132.3bn expected, with iPhone back to double-digit growth.</p>")

BASE_CASE = ("The investment case remains constructive, but the multiple leaves little slack. We underwrite double-digit "
             "December-quarter growth and 12m-forward consensus EPS of USD 8.3, rising as iPhone 17 supply catches up with "
             "demand. The debate has moved from demand to supply, memory costs and the return on higher AI spending. "
             "At 32.7x, after an 11% run into the print, we see the risk/reward as balanced rather than skewed to the upside. "
             "The next test is the December-quarter report in late January 2026.")
UP_HEAD, DOWN_HEAD = "What would strengthen our view", "What would change our view"
UPSIDE = ("iPhone 17 supply catching up by January with Greater China back to growth; gross margin at the top of the "
          "47&ndash;48% guide despite memory costs; EPS upgrades above 5% after the print.")
DOWNSIDE = ("December-quarter growth below 10% or Greater China down again; memory or tariff costs pushing gross margin below 47%; "
            "operating expenses above USD 18.5bn with no visible AI payoff in 2026.")

P2_TITLE = "Beyond the key takeaways"
H_A1 = "Results: Services and margin carried the beat"
A1_PARAGRAPHS = [
    ("<p>Revenue rose 8% to a September-quarter record of USD 102.5bn, 0.2% above consensus, and fiscal 2025 closed at "
     "USD 416bn. iPhone grew 6% to USD 49.0bn, also a September-quarter record, but missed consensus of USD 50.2bn: "
     "management said several iPhone 17 models were supply-constrained and the quarter ended with very lean channel "
     "inventory. Services rose 15% to an all-time high of USD 28.8bn, 2% above consensus, with records in advertising, "
     "the App Store, cloud, music, payments and video, and passed USD 100bn for the year. Mac grew 13% to USD 8.7bn, "
     "while iPad (USD 7.0bn) and wearables (USD 9.0bn) were flat.</p>"),
    ("<p>Gross margin of 47.2% beat consensus by 80bp despite USD 1.1bn of tariff costs, and net income reached "
     "USD 27.5bn. EPS of USD 1.85 beat consensus by 4.5% and rose 13% on an adjusted basis, excluding a one-off "
     "EU state aid tax charge a year earlier. Against that, the shares fell 0.4% on 31 October, the first session "
     "after the release, while the Nasdaq gained 0.6%. The confirmed drivers of the gap are the iPhone "
     "shortfall and Greater China, down 4% to USD 14.5bn. Our interpretation is that a pre-results multiple of 33.1x "
     "and an 11% run-up had already discounted a strong guide.</p>"),
]
H_A2 = "Outlook: double-digit growth, higher costs"
A2_PARAGRAPHS = ("<p>For the December quarter, management guided revenue growth of 10&ndash;12%, with iPhone up double "
                 "digits, against a consensus that implied about 6%. Gross margin is guided at 47&ndash;48%, including "
                 "an estimated USD 1.4bn of tariff costs, up from USD 1.1bn. Operating expenses step up to "
                 "USD 18.1&ndash;18.5bn from USD 15.9bn, about 18% above a year earlier at the midpoint, as research and "
                 "development spending on AI rises. Management attributed the China decline to supply, not demand, and "
                 "expects a return to growth this quarter. The open questions are on supply: advanced-node capacity for "
                 "Apple silicon and rising memory prices, which we see as the main risk to margins in 2026.</p>")
H_C2 = "Valuation: priced for the cycle, not beyond"
C2_TITLE = "AAPL: share price vs. consensus earnings and valuation"
C2_SUB = ("Weekly Friday closes sampled from daily Bloomberg data, 1 Jan 2010 to 31 Oct 2025 &middot; BEst 12m-forward "
          "consensus EPS &middot; 40-week simple MA &middot; log scale &middot; last price is the 31 October close, "
          "the first session after the release")
C2_COMMENT = ("<p>Price has run well ahead of earnings: the shares are up 21% over twelve months against 11% for "
              "12m-forward consensus EPS, and up 34% since the Q3 print against 7% for EPS. The multiple has expanded from "
              "26.1x in early August to 32.7x, 77% above the 18.4x average since 2010 and 20% above the five-year average "
              "of 27.3x, close to the 33.9x peak of December 2024. The price sits 21% above its 40-week average. A 10% EPS "
              "upgrade at an unchanged price would take the multiple to 29.7x, the one-year average: from here, earnings "
              "have to do the work.</p>")

SOURCE_LINE = ("Source: Syz Research, Bloomberg, company filings, Apple results release and earnings call of 30 Oct 2025, "
               "LSEG consensus via press coverage, analyst research notes of 31 Oct 2025")

W1, W2 = 74, 94            # PDF chart widths (% of text width)
W1_PPTX, W2_PPTX = 66, 88  # PPTX chart widths
