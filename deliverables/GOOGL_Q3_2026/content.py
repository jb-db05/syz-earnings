"""content.py: all text for the Alphabet (GOOGL) Q3 2026 Earnings update (HTML entities)."""

DOC_TYPE = "Earnings update"
DATE = "29 October 2026"
TITLE = "Alphabet Q3 2026: Cloud doubles, capex drains cash flow"

QUOTE = ("Google Cloud revenues grew 103%, powered by huge demand for our AI infrastructure and AI solutions. "
         "We&rsquo;re also seeing strong demand for our TPU systems across a wide range of customers.")
QUOTE_WHO = "Sundar Pichai, CEO, Alphabet Q3 2026 results, 28 October 2026"

COMPANY_INTRO = ("Alphabet owns Google Search, YouTube, Android and Google Cloud. Google Services, mostly advertising, "
                 "brings in 75% of revenue and Google Cloud 24%. Revenue now runs above USD 500bn a year; "
                 "the shares trade on Nasdaq.")

TAKEAWAYS = [
    ("neg", "Miss", "EPS of USD 2.12 missed consensus by 30%; a USD 8.7bn equity-stake loss explains 60% of the gap."),
    ("pos", "Beat", "Google Cloud revenue doubled to USD 30.7bn, 5% above consensus, and its operating margin reached 36%."),
    ("neg", "Reaction", "Shares are down over 10% pre-market on 29 October: margins fell and free cash flow turned negative."),
    ("neu", "Valuation", "Near USD 292, the stock trades on 17.7x forward earnings, 10% below its 2010 to 2026 average."),
]

KPIS = [
    ("Revenue", "USD 127.6bn", "&minus;0.5% vs. consensus", "neg"),
    ("EPS", "USD 2.12", "&minus;29.6% vs. consensus", "neg"),
    ("Google Cloud revenue", "USD 30.7bn", "+5.4% vs. consensus", "pos"),
    ("Free cash flow", "USD &minus;9.1bn", "Consensus USD &minus;2.7bn", "neg"),
]

H_P1 = "The debate moves to the return on capex"
P1_PARAGRAPH = ("Revenue missed consensus by 0.5% and EPS by 30%, and the shares are down over 10% pre-market on "
                "29 October, below USD 300. The fall is larger than the operating miss of about 6%. We read it as a "
                "verdict on the investment cycle: free cash flow was &minus;USD 9.1bn, share buybacks stopped and "
                "capital expenditure (capex) of USD 51.4bn absorbed 40% of revenue.")

C1_TITLE = "GOOGL: Q3 2026 results vs. consensus"
C1_SUB = ("Reported vs. consensus before the release, % &middot; Cloud profit = Google Cloud operating income "
          "&middot; EPS includes a USD 0.55 loss on equity securities")
C1_COMMENT = ("The quarter splits in two. Google Cloud beat consensus by 5% on revenue and by 14% on operating income. "
              "Advertising fell short, with Search 2.5% and YouTube ads 1.7% below estimates. Excluding the USD 0.55 "
              "equity loss, EPS of USD 2.67 sits 11% under consensus, and operating cash flow came in 20% short.")

BASE_CASE = ("The investment case remains intact and the risk/reward has improved with the fall. We underwrite revenue "
             "growth of around 20% into 2027, led by Cloud, and expect consensus EPS to come down as depreciation rises. "
             "The debate has moved from AI demand to the payback on capex, with a Cloud backlog of USD 561bn as support. "
             "Near USD 292, the stock trades 10% below its long-run multiple. The next test is the Q4 report in early "
             "February and the 2027 capex plan.")
UPSIDE = ("Google Cloud margin above 30% in Q4 despite third-party capacity costs; Search growth back to 15% or "
          "more; buybacks resuming in Q4; TPU contracts turning into the revenue management expects for 2027.")
DOWNSIDE = ("Free cash flow negative again in Q4 with no restart of buybacks; Search growth below 10% as retail media "
            "takes budget; a 2027 capex plan well above 2026 without a matching rise in the Cloud backlog.")

P2_TITLE = "Beyond the key takeaways"
H_A1 = "Results: Cloud carried, advertising slowed"
A1_PARAGRAPHS = [
    ("Revenue rose 25% to USD 127.6bn and operating income 30% to USD 40.6bn. Google Cloud did most of the work: "
     "revenue grew 103% to USD 30.7bn on demand for AI infrastructure, enterprise AI tools and the first TPU system "
     "sales, and operating income more than tripled to USD 11.1bn, a 36.2% margin. Google Services revenue of "
     "USD 96.3bn missed by 2.2% and its operating income of USD 39.2bn by 3.9%. Search grew 12% to USD 63.4bn, down "
     "from 17% in Q2; management cited currency and a Q2 lifted by the FIFA World Cup. YouTube ads grew 9% to "
     "USD 11.2bn. Net income fell 25% to USD 26.2bn."),
    ("The miss and the pre-market fall of more than 10% on 29 October point the same way, though the move goes "
     "beyond the operating shortfall. Most of the EPS gap is non-operating: a USD 8.7bn loss on equity stakes, "
     "mainly SpaceX, cost USD 0.55 per share. The confirmed drivers sit elsewhere. The operating margin fell to 31.8% "
     "from 34.0% in Q2 as depreciation rose, free cash flow was &minus;USD 9.1bn against &minus;USD 2.7bn expected, "
     "and no shares were bought back. The stock had already lost 8% since 13 October. We think investors now "
     "question the payback on capex, and the buyback halt removes a support."),
]
H_A2 = "Outlook: heavier spending, TPU revenue in 2027"
A2_PARAGRAPH = ("Management flagged near-term pressure on Cloud margins as higher-cost third-party capacity fills gaps "
                "in its own supply, with the cost rising in Q4. Capex reached USD 51.4bn in Q3, up 114%, taking the "
                "nine-month total to about USD 132bn. The full-year plan of USD 195bn to 205bn, set in July, implies "
                "USD 63bn to 73bn in Q4. The Cloud backlog stands at USD 561bn, and management expects the vast "
                "majority of TPU system revenue in 2027. Usage keeps climbing: first-party models process 32 billion "
                "tokens per minute and the Gemini app has one billion users. Cash and "
                "securities of USD 265.1bn cover long-term debt of USD 125.1bn twice.")
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

SOURCE_LINE = ("Source: Syz Research, Bloomberg, company filings, Alphabet Q3 2026 results of 28 October 2026, "
               "analyst research notes of 29 October 2026")
