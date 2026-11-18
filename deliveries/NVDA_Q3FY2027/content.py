"""content.py: all text for the NVIDIA Q3 FY2027 Earnings update (HTML entities; fill.json is unescaped from it)."""

DOC_TYPE = "Earnings update"
DATE = "18 November 2026"
TITLE = "NVIDIA Q3 FY2027: earnings intact, governance sets the price"

QUOTE = ("Our momentum is real. Our demand is accelerating. Our supply is growing. Our customers and our "
         "partners are with us, and employees are committed. We&rsquo;ve got this.")
QUOTE_WHO = "Colette Kress, Interim CEO and CFO, Q3 FY2027 earnings call, 17 November 2026"

COMPANY_INTRO = ("NVIDIA designs accelerated computing systems, chips, networking and software for AI data centres. "
                 "Data centre was 93% of Q3 FY2027 revenue, hyperscalers 52%. Listed on Nasdaq, market value about USD 3.7tn.")

TAKEAWAYS = [
    ("pos", "Beat", "Revenue of USD 115.8bn beat consensus by 6.1% and EPS of USD 2.68 by 8.5%."),
    ("pos", "Raised", "Q4 guide of USD 130bn is 4% above consensus; FY2028 growth lifted to about 75%."),
    ("neg", "Watch", "Free cash flow of USD 43.8bn missed by 23%, and USD 2.4bn of China Hopper sales stop."),
    ("neu", "Valuation", "10.6x forward earnings, the lowest since 2014: the market prices governance risk, not earnings."),
]

KPIS = [
    ("Revenue", "USD 115.8bn", "+6.1% vs. consensus", "pos"),
    ("EPS (adjusted)", "USD 2.68", "+8.5% vs. consensus", "pos"),
    ("Gross margin (adjusted)", "74.9%", "+80bp vs. consensus", "pos"),
    ("Q4 revenue guide", "USD 130bn", "+4.0% vs. consensus", "pos"),
]

H_P1 = "Earnings are not the problem, the CEO seat is"
P1_PARAGRAPH = ("Revenue beat consensus by 6.1% and EPS by 8.5%, and the shares rose 4% after hours on 17 November, "
                "a modest move after a 34% fall from the 2 October high. It settles the operating question: "
                "Vera Rubin delivered nearly USD 20bn in its first production quarter and FY2028 growth was raised to "
                "about 75%. Governance, China and customer financing remain open.")

C1_TITLE = "NVDA: Q3 FY2027 results and Q4 guide vs. consensus"
C1_SUB = ("Surprise vs. Bloomberg consensus, % &middot; gross margin in points, labelled in bp &middot; "
          "free cash flow vs. about USD 57bn expected")
C1_COMMENT = ("The beat was broad: revenue, data centre, margin and EPS all cleared consensus, and the Q4 guide beat "
              "by 4% with no China Hopper sales in it. The outlier is cash: free cash flow of USD 43.8bn fell 23% short "
              "as receivables rose almost a third to USD 81bn. Earnings quality is the next debate.")

BASE_CASE = ("We keep the position and would add on governance-driven weakness: at 10.6x forward earnings, the "
             "market prices a lasting governance discount rather than a weaker franchise. We underwrite FY2028 revenue "
             "growth of about 75% and consensus EPS near USD 16.3, with gross margin back to 72&ndash;73% after the Q4 "
             "trough. The debate has moved from demand to leadership and China. The catalyst is a "
             "credible permanent CEO; the USD 227bn buyback cushions the wait. The next test is the Q4 report in February 2027.")

UP_HEAD = "What would strengthen our view"
DOWN_HEAD = "What would change our view"
UPSIDE = ("A credible permanent CEO named before the Q4 report; the December congressional hearings passing without "
          "new restrictions; receivables falling from USD 81bn as cash conversion recovers.")
DOWNSIDE = ("A Q4 gross margin below 71% or an FY2028 margin under 72%; AI cloud customers failing to secure "
            "financing; export rules widened beyond China to other Asian buyers.")

P2_TITLE = "Beyond the key takeaways"

H_A1 = "Results: Rubin and networking did the work"
A1_PARAGRAPHS = [
    ("Data centre revenue rose 21% quarter on quarter to USD 108bn. Hyperscale grew 23% to USD 60bn on the Vera "
     "Rubin ramp and continued Grace Blackwell volumes; AI clouds, industrial and enterprise rose 18% to USD 47bn, "
     "nearly tripling year on year but slightly below analyst expectations. Networking exceeded USD 21bn, pulled "
     "through by full-rack deployments, and hyperscalers brought Rubin into production in about a month, half the "
     "Grace Blackwell lead time. Adjusted gross margin of 74.9% beat the 74% guide on mix, while adjusted operating "
     "expenses rose 7%. Q3 included USD 2.4bn of licensed Hopper sales to China, now stopped."),
    ("Surprise and reaction are aligned, but the move is small: a 6.1% revenue beat and a guide 4% above consensus "
     "lifted the shares only 4% after hours on 17 November. The confirmed drags are free cash flow of USD 43.8bn "
     "against about USD 57bn expected, receivables up almost a third, the end of China Hopper shipments and USD 518bn "
     "of total commitments, including USD 118bn of guarantees. The most likely reading, in our view, is that "
     "investors now price leadership and policy risk rather than earnings: the board took no questions on the "
     "resignation, and Congress holds hearings in December."),
]

H_A2 = "Outlook: 75% growth, a margin trough in Q4"
A2_PARAGRAPH = ("The Q4 guide of USD 130bn &plusmn;3% implies 12% sequential growth, or 15% excluding China Hopper, "
                "but Q4 carries an extra week: mechanically, a 13-week quarter would grow about 4%, or 6.5% ex China. "
                "Gross margin troughs at 71&ndash;72% as memory costs rise and legacy orders ship at old prices, then "
                "recovers to 72&ndash;73% in FY2028 under new pricing. Growth of about 75% implies some USD 726bn of FY2028 "
                "revenue on the USD 415bn FY2027 consensus base, 2.5% above FY2028 consensus. Purchase commitments of USD "
                "390bn, up over USD 100bn, and a USD 2.5tn cloud backlog support it."
                "")

H_C2 = "Valuation: the cheapest multiple since 2014"
C2_TITLE = "NVDA: share price vs. consensus earnings and valuation"
C2_SUB = ("Weekly, Sep 2014 to 18 Nov 2026 &middot; Bloomberg 12m-forward consensus EPS &middot; 40-week MA "
          "&middot; log scale &middot; last price before the post-results session")
C2_COMMENT = ("Price and earnings have decoupled: 12m-forward EPS is up 134% over 12 months to USD 14.8, while the share "
              "price is down 18% to USD 155. The forward P/E has fallen to 10.6x, the lowest reading since the series "
              "starts in 2014, a 67% discount to the 32.1x average and about half the one-year average of 20.3x. The "
              "stock trades 23% below its 40-week moving average of USD 203. Even a 25% cut to consensus EPS would leave "
              "the multiple at 14x, under half the long-run average: the price discounts governance, not growth.")

SOURCE_LINE = ("Source: Syz Research, Bloomberg, company filings, NVIDIA Q3 FY2027 earnings call transcript of "
               "17 November 2026, Financial Times of 18 November 2026, analyst research notes of 16 to 18 November 2026")

W1, W2 = 74, 94            # PDF chart widths, % of text width
W1_PPTX, W2_PPTX = 66, 88  # PPTX chart widths
