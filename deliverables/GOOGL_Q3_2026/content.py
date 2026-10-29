"""content.py: all text for the Alphabet (GOOGL) Q3 2026 Earnings update (HTML entities)."""

DOC_TYPE = "Earnings update"
DATE = "29 October 2026"
TITLE = "Alphabet Q3 2026: good for AI growth, tough on margins"

QUOTE = ("The significant increase in our investment in technical infrastructure will continue to weigh on the P&amp;L "
         "in the form of higher depreciation expenses and related data center operations costs, such as energy.")
QUOTE_WHO = "Anat Ashkenazi, CFO, Alphabet Q3 2026 earnings call, 28 October 2026"

COMPANY_INTRO = ("Alphabet owns Google Search, YouTube, Android and Google Cloud. Google Services, mostly advertising, "
                 "brings in 75% of revenue and Google Cloud 24%. Revenue now runs above USD 500bn a year; "
                 "the shares trade on Nasdaq.")

TAKEAWAYS = [
    ("neg", "Miss", "EPS of USD 2.12 missed consensus by 30%, mostly on a USD 0.55 loss on the SpaceX stake."),
    ("neg", "Margin", "Operating margin fell to 31.8% from 34.0% as depreciation rose; operating profit missed by about 6%."),
    ("pos", "Growth", "Revenue grew 25% and Google Cloud doubled to USD 30.7bn, with USD 561bn of contracts booked."),
    ("neg", "Reaction", "Shares are down over 10% pre-market on 29 October, to about 17.7x forward earnings, below average."),
]

KPIS = [
    ("EPS", "USD 2.12", "&minus;29.6% vs. consensus", "neg"),
    ("Operating margin", "31.8%", "34.0% in Q2 2026", "neg"),
    ("Google Cloud revenue", "USD 30.7bn", "+5.4% vs. consensus", "pos"),
    ("Free cash flow", "USD &minus;9.1bn", "Consensus USD &minus;2.7bn", "neg"),
]

H_P1 = "Margins explain the fall better than EPS"
P1_PARAGRAPH = ("EPS missed consensus by 30% and the shares are down over 10% pre-market on 29 October, below USD 300. "
                "The EPS miss says little about Search, YouTube or Cloud: most of it is a loss on the SpaceX stake. "
                "The margin matters more. It fell to 31.8% from 34.0% in Q2 as depreciation on the AI build-out rose, "
                "and operating profit missed by about 6%.")

C1_TITLE = "GOOGL: Q3 2026 results vs. consensus"
C1_SUB = ("Reported vs. consensus before the release, % &middot; Cloud profit = Google Cloud operating income "
          "&middot; EPS includes a USD 0.55 loss on equity securities")
C1_COMMENT = ("Google Cloud beat consensus by 5% on revenue and by 14% on operating income. Advertising fell short: "
              "total ads of USD 82bn came in 1.8% below estimates, with Search 2.5% and YouTube 1.7% below. Excluding "
              "the equity loss, EPS of USD 2.67 sits 11% under consensus, and operating cash flow was 20% short.")

BASE_CASE = ("The investment case remains intact: good for AI growth, tough on near-term earnings. "
             "We underwrite revenue growth of around 20% into 2027, led by Cloud, whose USD 561bn backlog is just "
             "over 55% due within 24 months. Consensus EPS should come down as depreciation rises and capex grows "
             "again in 2027. Near USD 292, the stock trades 10% below its long-run multiple and the risk/reward has "
             "improved. The next test is the Q4 report in early February.")
UPSIDE = ("Ads in AI Mode closing the monetisation gap as they roll out abroad; Search growth holding in Q4 despite "
          "FX; Cloud margin above 30% through the third-party capacity ramp; buybacks resuming.")
DOWNSIDE = ("Free cash flow negative again in Q4 without a fine payment; Search slowing further as AI Mode takes "
            "queries; 2027 capex rising faster than the USD 561bn Cloud backlog turns into revenue.")

P2_TITLE = "Beyond the key takeaways"
H_A1 = "Results: Search slowed on FX and AI Mode"
A1_PARAGRAPHS = [
    ("Revenue rose 25% to USD 127.6bn and operating income 30% to USD 40.6bn. Google Cloud revenue grew 103% to "
     "USD 30.7bn and its operating income more than tripled to USD 11.1bn, a 36.2% margin. Search grew 12% to "
     "USD 63.3bn, down from 17% in Q2. Management named FX the single largest driver of that slowdown, followed by "
     "APAC retailers hit by the end of the EU de minimis exemption and World Cup budgets spent in June. It added "
     "that AI Mode, growing fast, monetises less. The FX comment covers the slowdown versus Q2 and leaves the miss "
     "versus consensus open. Management did not cite competition from OpenAI; we treat that as a separate risk."),
    ("The miss and the pre-market fall of more than 10% on 29 October point the same way, and the size of the move "
     "tracks the margin. Confirmed drivers: higher depreciation and a USD 7.7bn Alphabet-level operating loss, "
     "mainly from shared AI research. The 36.2% Cloud margin excludes those shared costs, so we judge the offset on group "
     "profit and cash. Free cash flow of &minus;USD 9.1bn reflected capex, TPU inventory and a USD 5.2bn payment for "
     "a 2018 EC fine; without the fine it would be about &minus;USD 3.9bn, our calculation. No shares were bought "
     "back. We think investors now question the payback on capex."),
]
H_A2 = "Outlook: capex unchanged, costs rise in Q4"
A2_PARAGRAPH = ("Management kept the 2026 capex range of USD 195bn to 205bn, which implies USD 63bn to 73bn in Q4 "
                "after USD 51.4bn in Q3, and expects capex to rise significantly in 2027. Third-party compute came "
                "online at the very end of Q3 and ramps in Q4, and the CFO expects near-term margin headwinds from it. "
                "FX should weigh more in Q4, mainly on Search and YouTube. To lift Search monetisation, Google is "
                "scaling ads in AI Mode and AI Overviews, taking them abroad for the first time and adding multi-turn "
                "ads in the US. TPU system revenue should ramp meaningfully in 2027.")
H_C2 = "Valuation: the premium is gone"
C2_TITLE = "GOOGL: share price vs. consensus earnings and valuation"
C2_SUB = ("Weekly, 2010 to 28 Oct 2026 &middot; Bloomberg 12m-forward consensus EPS &middot; 40-week MA "
          "&middot; Log scale &middot; Last price is the 28 October close, before the release")
C2_COMMENT = ("At the 28 October close of USD 324.9, before the release, the stock traded on 19.7x 12-month forward "
              "EPS of USD 16.5, in line with its 19.6x average since 2010 and far below the 28.2x peak of January "
              "2026. Over 12 months the price rose 25% and consensus EPS 46%, so earnings did the work and the "
              "multiple compressed. The price sat 5% below its 40-week average of USD 340.8. Near USD 292 "
              "pre-market, the multiple drops to 17.7x, 10% below average. A 5% cut to consensus EPS at that price "
              "would lift it to 18.6x, still under the average.")

SOURCE_LINE = ("Source: Syz Research, Bloomberg, company filings, Alphabet Q3 2026 earnings call of 28 October 2026, "
               "press coverage and analyst research notes of 29 October 2026")
