"""content.py: all text for the Apple fiscal Q4 2026 Earnings update (HTML entities; fill.json is derived from it)."""

DOC_TYPE = "Earnings update"
DATE = "3 November 2026"
TITLE = "Apple Q4 2026: price beats, memory caps the margin"

QUOTE = ("What we&rsquo;re seeing with memory pricing right now is unprecedented. &hellip; For the December "
         "quarter, we expect even higher memory costs, partly offset by a few factors.")
QUOTE_WHO = "John Ternus, CEO, fiscal Q4 2026 earnings call, 2 November 2026"

COMPANY_INTRO = ("Apple sells the iPhone, about half of revenue, plus Mac, iPad, wearables and services such as the "
                 "App Store, across over 2.5bn active devices. Fiscal 2026 revenue USD 479bn; Nasdaq-listed, worth "
                 "about USD 5tn.")

TAKEAWAYS = [
    ("pos", "Beat", "Revenue USD 114.5bn (+1% vs. consensus) and EPS USD 2.10 (+5.5%), led by iPhone and Mac pricing."),
    ("neg", "Reaction", "Shares fell 3.5% after hours on 2 November: a 45% to 46% margin guide undercut the beat."),
    ("neg", "Watch", "Services growth guided to 8% to 9%, from 10%, as licensing and App Store changes bite."),
    ("neu", "Valuation", "35.2x forward earnings, near the highest since 2010: little room for further margin slippage."),
]

KPIS = [
    ("Q4 revenue", "USD 114.5bn", "+1.0% vs. consensus", "pos"),
    ("Q4 diluted EPS", "USD 2.10", "+5.5%, +3.0% ex refunds", "pos"),
    ("Dec-quarter revenue guide", "+7&ndash;10% y/y", "+2.4pt vs. consensus", "pos"),
    ("Dec-quarter margin guide", "45&ndash;46%", "&minus;80bp vs. consensus", "neg"),
]

H_P1 = "The debate moves from demand to cost"
P1_PARAGRAPH = ("<p>Revenue beat consensus by 1% and EPS by 5.5%, yet the shares fell 3.5% after hours on 2 November. "
                "The beat leaned on price rises and a USD 0.05 tariff refund; the December-quarter margin guide of "
                "45% to 46% is 80bp below consensus. Demand is not the issue: Apple is short of supply. "
                "The question is how much memory inflation pricing can absorb.</p>")

C1_TITLE = "AAPL: Q4 2026 results and December-quarter guide vs. consensus"
C1_SUB = ("Surprise vs. LSEG consensus of 2 November 2026 &middot; sales and EPS in %, margins and growth guide in "
          "points &middot; *ex tariff refunds &middot; guides at midpoint")
C1_COMMENT = ("<p>Hardware carried the quarter: Mac beat by 12% and iPhone by 2%, both supply-constrained after price "
              "increases. iPad and wearables missed by 7% and 8% on tough comparisons. Ex tariff refunds, EPS beat by 3% and gross margin fell about 60bp short. The guide splits the "
              "same way: sales above consensus, margin below.</p>")

BASE_CASE = ("The investment case is intact, but the multiple leaves little slack. Apple has so far passed memory "
             "inflation on without hurting demand, and fiscal 2026 EPS rose 20% to USD 8.98. "
             "Consensus forward EPS of USD 9.58 implies only 7% growth from here, which we see as achievable with gross margin at "
             "45% to 46%. At 35.2x, that delivery is priced and the risk/reward is balanced. iPhone "
             "Duo supply is the catalyst; the next test is the December-quarter margin in early 2027.")
UP_HEAD = "What would strengthen our view"
DOWN_HEAD = "What would change our view"
UPSIDE = ("December-quarter gross margin at or above 46%; iPhone Duo supply in balance with demand by spring "
          "2027; Services back to 10% growth as Siri AI lifts paid subscriptions and iCloud+.")
DOWNSIDE = ("A March-quarter margin guide below 45%; unit declines once the September iPhone price rise works "
            "through; further App Store rulings taking Services growth below 8%.")

P2_TITLE = "Beyond the key takeaways"
H_A1 = "Results: price and the Mac did the work"
A1_PARAGRAPHS = [
    ("<p>Revenue rose 12% to USD 114.5bn, above the 9% to 11% guide, despite nearly 2 points of sequential currency "
     "headwind. iPhone grew 17% to USD 57.6bn, a September-quarter record, with record upgraders in the US, mainland "
     "China and India; Mac grew 24% to USD 10.8bn on MacBook Neo and MacBook Pro. Both were supply-constrained, mainly "
     "by advanced-node chip availability. iPad fell 10% and wearables 8% against launches a year ago. Services rose "
     "10% to USD 31.6bn, in line, with paid subscriptions above 1.5bn. Operating expenses rose 21% on research spending, "
     "so operating income grew 10%, and buybacks lifted EPS growth to 14%.</p>"),
    ("<p>The beat and the 3.5% after-hours fall on 2 November diverge, and the confirmed drivers sit in the margin "
     "line. Without the 1-point tariff refund, gross margin was about 46.9%, 60bp below consensus, and EPS beat by 3% "
     "rather than 5.5%. Management guided the December-quarter margin to 45% to 46% against 46.3% expected, said memory "
     "prices keep rising beyond December and disclosed USD 33bn of additional purchase obligations since June. We "
     "think positioning added to the move: the shares had risen 25% in twelve months against 16% for forward "
     "earnings, and traded at 35.2x into the print.</p>"),
]
H_A2 = "Outlook: record sales, thinner margin"
A2_PARAGRAPHS = ("<p>Apple guides December-quarter revenue up 7% to 10%, on top of 16% growth a year ago and against "
                 "6.1% expected: the midpoint implies about USD 156bn, which management expects to be the best quarter "
                 "in its history. The guide reflects constrained supply: iPhone Duo is short of demand, and Mac and iPad "
                 "are now limited by memory. Services should grow 8% to 9%, slowed by third-party licensing, App Store "
                 "changes and currency. Gross margin of 45% to 46% compares with 48.2% a year ago, with most of the "
                 "decline from memory plus Siri AI ramp costs. Management says it "
                 "is too early to read price elasticity.</p>")

H_C2 = "Valuation: a peak multiple on slower growth"
C2_TITLE = "AAPL: share price vs. consensus earnings and valuation"
C2_SUB = ("Weekly, January 2010 to 2 November 2026 &middot; Bloomberg BEst 12m-forward EPS &middot; 40-week simple MA "
          "&middot; log scale &middot; P/E vs. its 2010 to 2026 average &middot; last price: 2 November close, pre-release")
C2_COMMENT = ("<p>The shares have run ahead of earnings: up 25% over twelve months against 16% for consensus forward "
              "EPS. The 12-month forward P/E of 35.2x is 83% above its 19.3x average since 2010, close to the 36.1x "
              "peak of 23 October and above the one-year average of 32.1x. The price sits 13% above its 40-week "
              "average of USD 301. Consensus EPS slipped 0.4% to USD 9.58 on 3 November; a further 5% cut at an "
              "unchanged price would take the multiple to 37x. A return to the one-year average needs a 10% upgrade, "
              "which the margin guide does not support.</p>")

SOURCE_LINE = ("Source: Syz Research, Bloomberg, LSEG consensus, company filings, Apple fiscal Q4 2026 results release "
               "and earnings call of 2 November 2026, analyst research notes of 3 November 2026")

W1, W2 = 70, 94            # PDF chart widths (% of text width)
W1_PPTX, W2_PPTX = 66, 88  # PPTX chart widths
