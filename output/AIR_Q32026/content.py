"""content.py: all text for the Airbus Q3 2026 Earnings update (HTML entities)."""
P = lambda s: f"<p>{s}</p>"

DOC_TYPE = "Earnings update"
DATE = "29 October 2026"
TITLE = "Airbus Q3 2026: the guide holds, Q4 must deliver"

QUOTE = ("Overall, we feel comfortable with the ramp up. As you see, we are confirming the outlook for this year. "
         "We were comfortable enough at the Farnborough Airshow to give a 2029 mid-term target.")
QUOTE_WHO = "Guillaume Faury, CEO, Q3 2026 earnings call, 28 October 2026"

COMPANY_INTRO = ("Airbus builds commercial aircraft (A220, A320, A330, A350), helicopters and defence and space "
                 "systems. Commercial aircraft were 73% of Q3 revenue; nine-month revenue EUR 50.6bn. Listed in "
                 "Paris, Frankfurt and Madrid.")

TAKEAWAYS = [
    ("neu", "In line", "Q3 adjusted EBIT of EUR 1.77bn matched consensus; revenue missed by 5% on fewer deliveries."),
    ("pos", "Reaction", "Shares closed 3.3% higher on 29 October, against 0.8% for the Stoxx Europe 600."),
    ("neg", "Watch", "The unchanged guide needs about 323 Q4 deliveries and EUR 5.8bn of Q4 free cash flow."),
    ("neu", "Valuation", "23.5x forward earnings, 35% above the 17.4x average since 2005, below January&rsquo;s 27.7x."),
]

KPIS = [
    ("Q3 adjusted EBIT", "EUR 1.77bn", "+1.0% vs. consensus", "pos"),
    ("Q3 revenue", "EUR 17.5bn", "&minus;5.0% vs. consensus", "neg"),
    ("Q3 free cash flow", "EUR &minus;0.10bn", "vs. EUR +0.33bn consensus", "neg"),
    ("2026 EBIT guide", "EUR 7.5bn", "Held, 2.5% below consensus", "neu"),
]

H_P1 = "Relief on the guide, the cash test is Q4"
P1_PARAGRAPH = P(
    "Q3 adjusted EBIT matched consensus while revenue missed by 5% and free cash flow by about EUR 0.4bn, yet the "
    "shares closed 3.3% higher on 29 October, against 0.8% for the Stoxx Europe 600. The guide and the buyback plan "
    "held, and orders keep building: 1,105 net orders in nine months, double last year. The case now rests on delivering Q4.")

C1_TITLE = "AIR: Q3 2026 results and 2026 guide vs. consensus"
C1_SUB = ("Q3 reported vs. Q3 consensus &middot; maintained 2026 guide vs. 2026 consensus, % &middot; free cash flow "
          "before customer financing")
C1_COMMENT = P(
    "The misses are volume and cash, not margin: commercial EBIT held up as fewer aircraft left the line. The "
    "maintained 2026 guide sits 2.5% below consensus on EBIT and 6% below on free cash flow, a gap that already "
    "existed before the release; the delivery guide is slightly above consensus.")

BASE_CASE = (
    "We are constructive on Airbus. We underwrite about 870 deliveries this year, adjusted EBIT of about EUR 7.5bn "
    "and a 2027 ramp paced by engines, backed by a backlog of 9,310 aircraft. Forward EPS of EUR 8.4 is 15% above "
    "its 2019 peak, and defence orders, up 70%, add a second leg. The debate has moved from demand to execution: the Spirit integration and the cash release from "
    "about EUR 10bn of extra inventory. At 23.5x, delivery must follow. Next test: the full-year results in February.")
UPSIDE = ("Q4 deliveries at or above 323 with free cash flow before customer financing of at least EUR 4.5bn; the "
          "EUR 5bn buyback launched before year-end; Project Bromo signed in 2026 as planned.")
DOWNSIDE = ("Deliveries below 850, the low end of the range; free cash flow short of EUR 4bn as inventory fails to "
            "unwind; Spirit costs above the guided effect; fewer engines than planned for 2027.")

P2_TITLE = "Beyond the key takeaways"
H_A1 = "Results: fewer deliveries, firmer margins"
A1_PARAGRAPHS = [
    P("Q3 revenue fell 2% to EUR 17.5bn and adjusted EBIT 9% to EUR 1.77bn on 196 deliveries. Commercial Aircraft "
      "revenue fell 2% to EUR 12.8bn and its adjusted EBIT 12% to EUR 1.38bn, a 10.8% margin against the 10.4% "
      "analysts expected, on fewer deliveries, a less favourable mix and the integration of the former Spirit "
      "AeroSystems work packages, which also cost EUR 112m in charges below adjusted EBIT. Helicopters fell 17% to "
      "EUR 205m and Defence and Space rose 19% to EUR 185m. Free cash flow before customer financing was EUR "
      "&minus;102m, as inventory rose about EUR 10bn since January to support the ramp. Net cash fell to EUR 7.0bn "
      "from EUR 12.2bn at end-2025."),
    P("The reaction diverged from the misses: the shares closed 3.3% higher on 29 October, against 0.8% for the "
      "Stoxx Europe 600. Confirmed drivers: the guide held; management said the A321 stringer issue would not push "
      "deliveries toward the low end of the 850 to 890 range nor affect 2027; commercial margins beat; and the CFO "
      "said the plan to start the EUR 5bn buyback in the second half was unchanged. We think relief did the rest: "
      "the shares went into the print 12% below their January peak, at 22.9x, under the one-year average of 24.2x."),
]
H_A2 = "Outlook: a heavy fourth quarter"
A2_PARAGRAPHS = P(
    "The unchanged guide of about 870 deliveries, EUR 7.5bn of adjusted EBIT and EUR 4.5bn of free cash flow before "
    "customer financing leaves a heavy Q4: about 323 deliveries, 37 more than a year earlier; about EUR 3.0bn of "
    "EBIT, roughly flat as the A220 mix, Spirit costs and back-loaded R&amp;D absorb the volume; and about EUR 5.8bn "
    "of cash, which depends on unwinding the inventory built this year. Engines pace 2027, and "
    "Airbus will not build extra airframes ahead of them. An A350 rate above 12 is under review, and the 2029 target "
    "set in July, EUR 12bn to 13bn of adjusted EBIT at USD 1.22, stands.")

H_C2 = "Valuation: a premium to history, not to 2026"
C2_TITLE = "AIR: share price vs. consensus earnings and valuation"
C2_SUB = ("AIR FP Equity, weekly, April 2005 to October 2026 &middot; BEst 12m-forward consensus &middot; 40-week "
          "simple MA &middot; log scale &middot; P/E shaded vs. its 2005 to 2026 average &middot; last price EUR "
          "198.30 is the 29 October close, the first session after the release")
C2_COMMENT = P(
    "Earnings have outrun the price: over 12 months consensus forward EPS rose 8% to EUR 8.4 while the shares fell "
    "7%, so the forward P/E fell from 27.5x to 23.5x. That is 35% above the 17.4x average since 2005 and above the "
    "ten-year average of 20.8x, but below the one-year average of 24.2x and the 27.7x reached at the January record "
    "of EUR 217. The 2021 peak of 35.8x reflected depressed post-pandemic earnings. The price is 6% above its "
    "40-week average. A 10% EPS upgrade at an unchanged price would take the multiple to 21.4x, the five-year "
    "average.")

SOURCE_LINE = ("Source: Syz Research, Bloomberg, company filings, Airbus nine-month 2026 release and call of "
               "28 October 2026, analyst research notes of 29 October 2026")
W1, W2 = 80, 92            # PDF chart widths, % of text width
W1_PPTX, W2_PPTX = 66, 88
