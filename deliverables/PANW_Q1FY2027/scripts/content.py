"""PANW fiscal Q1 2027 Earnings update: all text (HTML entities)."""
DOC_TYPE = "Earnings update"
DATE = "19 November 2026"
TITLE = "Palo Alto Networks Q1 FY27: beat, raise and a bet on AI"
QUOTE = ("NGS ARR was up 66%, and we delivered one of the largest NGS ARR beats "
         "in our history. &hellip; That momentum gives us confidence to materially raise our guidance for the year.")
QUOTE_WHO = "Nikesh Arora, Chairman and Chief Executive Officer, fiscal Q1 2027 earnings call, 18 November 2026"
COMPANY_INTRO = ("Palo Alto Networks sells cybersecurity platforms for networks, security operations and identity, sold as "
                 "subscriptions to enterprises and governments. Network and AI security is two thirds of revenue. Listed on "
                 "Nasdaq, worth about USD 300bn.")
TAKEAWAYS = [
    ("pos", "Beat", "Revenue USD 3.44bn beat consensus by 4% and EPS by 8%; shares rose 5.4% intraday on 19 November."),
    ("pos", "Raised", "Fiscal 2027 guide raised: revenue USD 14.52 to 14.57bn, +2.8% at midpoint; EPS USD 4.26 to 4.30."),
    ("neg", "Watch", "The USD 4.5bn Applied Compute deal costs up to 200bp of operating margin in fiscal 2028."),
    ("neu", "Valuation", "80.5x forward earnings, 63% above the 2016 to 2026 average: the price has run ahead of earnings."),
]
KPIS = [
    ("Q1 revenue", "USD 3.44bn", "+3.9% vs. consensus", "pos"),
    ("Q1 non-GAAP EPS", "USD 1.05", "+8.2% vs. consensus", "pos"),
    ("Q1 NGS ARR", "USD 9.73bn", "+1.8% vs. top of guide", "pos"),
    ("FY27 revenue guide", "USD 14.55bn", "+2.8% vs. prior guide", "pos"),
]
H_P1 = "AI-driven threats are turning into budgets"
P1 = ("Revenue beat consensus by 4% and EPS by 8%, and the shares rose 5.4% intraday on 19 November after a 9.6% "
      "pre-market jump: surprise and reaction are aligned. The quarter shows AI-assisted attacks turning into spending, with "
      "a record 170 customers consolidating onto the platform. The case now has two engines: consolidation and a "
      "costly bet on AI models.")
C1_TITLE = "PANW: Q1 beat and fiscal 2027 guidance raise"
C1_SUB = ("Q1 vs. consensus (revenue, EPS) and vs. top of guide (NGS ARR) &middot; FY27 guidance midpoints vs. prior guidance, % "
          "&middot; Non-GAAP")
C1_COMMENT = ("Every line beat, but the beat sits mainly in earnings rather than recurring revenue: EPS "
              "beat by 8%, while next-generation security annualised recurring revenue (NGS ARR), came "
              "1.8% above the top of the guide. The fiscal 2027 revenue raise, USD 395m at the midpoint, is three times the Q1 beat.")
BASE_CASE = ("The investment case remains constructive: AI raises both the volume of attacks and the cost of fragmented defences, "
             "and Palo Alto is the main consolidator. We underwrite the fiscal 2027 guide of USD 4.26 to 4.30 of EPS and 26% to 27% "
             "revenue growth, with Applied Compute an option on secure enterprise AI. At 80.5x forward "
             "earnings the risk/reward is balanced: the multiple already pays for upgrades. Next test: the fiscal Q2 print in February.")
UPSIDE = ("NGS ARR above the USD 10.22bn top of the Q2 guide; operating margin held at 29.5% despite component costs; "
          "Applied Compute closing in fiscal Q3 2027 with early ARR visibility.")
DOWNSIDE = ("Net-new platform consolidations back below 100 a quarter; gross margin under 74% on SaaS mix and memory costs; "
            "deal margin dilution beyond the 200bp guided for fiscal 2028.")
P2_TITLE = "Beyond the key takeaways"
H_A1 = "Results: every platform accelerated"
A1 = [
    ("Revenue rose 39% to USD 3.44bn, lifted by the CyberArk acquisition, now the Idira identity segment, and growth "
     "accelerated in all three segments. Network and AI security, two thirds of revenue, grew 20% to USD 2.3bn, with secure "
     "access service edge (SASE) ARR up 30% and software firewall ARR up 34%, a third consecutive acceleration. Cortex, the "
     "security operations platform, grew 53% (40% pro forma), with XSIAM ARR up over 65% to about USD 800m. Idira grew 23% "
     "pro forma and logged more than 100 cross-sell wins from the core base. Prisma AIRS, the AI security product, reached "
     "about USD 170m of ARR within five quarters, the fastest ramp in company history."),
    ("The reaction is aligned. EPS of USD 1.05 beat consensus of USD 0.97 by 8% and the guide by USD 0.08, "
     "and the shares rose 5.4% intraday on 19 November, against a 9.6% gain pre-market, so part of the move faded. The "
     "confirmed drivers are the guidance raise and NGS ARR growth of 66%, with net-new ARR more than doubling. The beat is of "
     "good quality: operating margin rose 50bp to 30.7% even as gross margin fell 170bp to 75.2% on component costs and SaaS "
     "mix. We think the fade reflects the margin cost of the Applied Compute deal rather than the quarter itself."),
]
H_A2 = "Outlook: guide raised, the AI deal adds cost"
A2 = ("The fiscal 2027 guide, excluding Applied Compute, is now revenue USD 14.52 to 14.57bn "
      "(26% to 27% growth), NGS ARR USD 11.475 to 11.525bn, EPS USD 4.26 to 4.30, operating margin 29.5% and adjusted "
      "free cash flow margin 38%. The Q2 guide is revenue of USD 3.53 to 3.55bn and EPS of USD 1.01 to 1.03. Applied "
      "Compute, a USD 4.5bn all-stock deal with USD 100m of annualised revenue, should add USD 1bn of NGS ARR by "
      "fiscal 2029. The cost is up to 100bp of operating margin in fiscal 2027 and 200bp in fiscal 2028, plus under USD 3bn "
      "of capital spending through fiscal 2030.")
H_C2 = "Valuation: the multiple ran ahead of earnings"
C2_TITLE = "PANW: share price vs. consensus earnings and valuation"
C2_SUB = ("Weekly, January 2016 to 19 November 2026 &middot; Bloomberg 12m-forward consensus EPS &middot; 40-week simple moving "
          "average &middot; Log scale &middot; Last price intraday on 19 November")
C2_COMMENT = ("The share price rose 75% over 12 months while 12m-forward consensus EPS rose 13%: the rerating, not earnings, did "
              "most of the work. At 80.5x, the forward P/E sits 63% above its 49.5x average since 2016, below the 97.1x peak of "
              "9 October 2026 but well above the 63.1x one-year average. Since mid-August, before the previous results, EPS has "
              "risen 7% and the price has fallen 7%, so the derating has started. The price is 26% above its 40-week average. At "
              "an unchanged price, EPS would need to rise 28% to bring the multiple back to its one-year average.")
SOURCE_LINE = ("Source: Syz Research, Bloomberg, company filings, Palo Alto Networks fiscal Q1 2027 earnings call of "
               "18 November 2026, analyst research notes of 16 to 19 November 2026")
W1, W2 = 72, 94
W1_PPT, W2_PPT = 66, 88
