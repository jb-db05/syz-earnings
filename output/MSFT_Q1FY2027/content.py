"""content.py: all text for the Microsoft Q1 FY2027 Earnings update (HTML entities)."""
P = lambda s: f"<p>{s}</p>"

DOC_TYPE = "Earnings update"
DATE = "29 October 2026"
TITLE = "Microsoft Q1 FY2027: faster Azure, costlier capacity"

QUOTE = ("In closing, based on the demand we see, the strength of our products, and the efficiency we are "
         "driving across the stack, I&rsquo;ve never been more confident in the long-term returns for our investments.")
QUOTE_WHO = "Satya Nadella, Chairman and CEO, Q1 FY2027 earnings call, 28 October 2026"

COMPANY_INTRO = ("Microsoft sells cloud infrastructure (Azure), workplace software (Microsoft 365, Copilot), Windows, "
                 "Xbox and LinkedIn worldwide. Its Agents and Infra segment earned 83% of quarterly revenue of "
                 "USD 92.3bn. Listed on Nasdaq.")

TAKEAWAYS = [
    ("pos", "Beat", "Revenue of USD 92.3bn beat consensus by 1.8%; Azure grew 48%, three points ahead of expectations."),
    ("pos", "Raised", "The Q2 Azure guide of 49% to 50% tops consensus of about 45%, despite delayed capacity."),
    ("neg", "Reaction", "Shares only 1% higher pre-market on 29 October: a Q2 margin near 47% and capex weighed."),
    ("neu", "Valuation", "25.2x forward earnings, down from 30.6x a year ago: earnings did the work, not the multiple."),
]

KPIS = [
    ("Revenue", "USD 92.3bn", "+1.8% vs. consensus", "pos"),
    ("Adj. EPS", "USD 4.89", "+3.4% vs. consensus", "pos"),
    ("Azure growth", "48%", "+3 pts vs. consensus", "pos"),
    ("Q2 Azure guide (cc)", "49&ndash;50%", "+4.5 pts vs. consensus", "pos"),
]

H_P1 = "Capacity, not demand, sets the pace"
P1_PARAGRAPH = P(
    "Revenue beat consensus by 1.8%, operating income by 4.2% and EPS by 3.4%, and the Azure guide cleared "
    "expectations by about 4.5 points, yet the shares were only 1% higher pre-market on 29 October, after an "
    "after-hours gain of about 4%. Demand still exceeds supply; what investors now weigh is the cost of the "
    "capacity, not a lack of customers.")

C1_TITLE = "MSFT: Q1 FY2027 results and Q2 guide vs. consensus"
C1_SUB = ("Reported vs. pre-results consensus, % &middot; Q2 revenue guide at the midpoint &middot; adj. EPS excludes "
          "the OpenAI impact &middot; RPO: remaining performance obligation")
C1_COMMENT = P(
    "Every reported line beat, and the Q2 revenue guide midpoint sits 1.0% above consensus. The one miss is the "
    "commercial order backlog, USD 677bn against an estimated USD 706bn, with bookings down 12% against a large "
    "prior-year Azure contract. We read this as timing: the part due within 12 months still grew 29%.")

BASE_CASE = (
    "We are constructive on Microsoft. We underwrite Azure growth near "
    "50% in the first half and Microsoft 365 commercial cloud picking up from 18%, which points to upgrades to the "
    "USD 21.2 forward EPS consensus. The debate has moved from demand to returns on USD 170bn of 2026 capex. At "
    "25.2x, below the five-year average of 28.0x, the multiple does not price the pick-up. Next test: the Q2 print "
    "in late January.")
UPSIDE = ("Azure growth at or above 50% in Q2 with Microsoft Cloud gross margin holding at 65%; delayed GPU "
          "capacity arriving on time in the second half; a Copilot seat count showing consumption beyond GitHub.")
DOWNSIDE = ("Azure growth below 45% in Q2 as efficiency gains fade; an operating margin below 46% on capacity costs; "
            "fiscal 2027 capex above USD 200bn funded with debt, without a matching rise in the near-term backlog.")

P2_TITLE = "Beyond the key takeaways"
H_A1 = "Results: Azure and efficiency carried it"
A1_PARAGRAPHS = [
    P("Revenue rose 19% to USD 92.3bn, above the top of Microsoft&rsquo;s own USD 89.9bn to 91.0bn guide. Agents and "
      "Infra, the new segment holding the cloud, grew 25% to USD 76.8bn and Microsoft Cloud 30% to USD 63.9bn. Azure "
      "accelerated to 48%: engineering work freed GPU capacity that went to Foundry, whose revenue more than tripled, "
      "token prices were higher than planned, and idle CPU capacity was monetised. Opex rose only 6%, so operating "
      "income grew 21% and the margin held near 50%. Devices and Consumer fell 3%: Windows OEM dropped 27% on "
      "the Windows 10 end-of-support comparison and high inventory, while search and advertising ex traffic "
      "acquisition costs grew 12%."),
    P("The surprise was broad, the reaction small: shares were 1% higher pre-market on 29 October, against an "
      "after-hours gain of about 4%. Confirmed drivers temper the beat: the Q2 cost guide implies an "
      "operating margin near 46.8%, from 49.8%; Microsoft Cloud gross margin fell to 66%; bookings fell 12% and the "
      "order backlog came in 4% below the estimate; and management raised external funding. We think "
      "positioning explains the rest: the shares had risen 15% since the July results to a record USD 535 in early "
      "October. Alphabet&rsquo;s near 10% after-hours fall that evening is consistent with, not proof of, "
      "a sector drag."),
]
H_A2 = "Outlook: faster Azure, thinner margins"
A2_PARAGRAPHS = P(
    "Q2 guidance calls for revenue of USD 96.0bn to 97.1bn, up 18% to 19%, 1.0% above consensus at the "
    "midpoint, with Azure growth of 49% to 50% in constant currency against about 45% expected. The guide leans on "
    "more efficiency gains to offset GPU contracts delayed to the second half, and token "
    "pricing is a variable. Costs rise faster: cost of goods sold up 26% to 27% and opex up 9%, "
    "with the voluntary exit offer. Capex exceeds USD 50bn in Q2 and reaches about USD 170bn for calendar "
    "2026, accelerating in the second half. Windows OEM and Devices is guided down in the mid-30s; free cash flow "
    "stays positive.")

H_C2 = "Valuation: earnings outran the share price"
C2_TITLE = "MSFT: share price vs. consensus earnings and valuation"
C2_SUB = ("MSFT US Equity, weekly, April 2005 to October 2026 &middot; BEst 12m-forward consensus &middot; 40-week "
          "simple MA &middot; log scale &middot; P/E shaded vs. its 2005 to 2026 average &middot; last price USD 533.9 "
          "is a 29 October pre-market level, after the release")
C2_COMMENT = P(
    "Earnings did the work: over 12 months consensus forward EPS rose 25% to USD 21.2 while the share "
    "price gained 3%, so the forward P/E fell from 30.6x to 25.2x. The multiple troughed at 19.1x in June 2026 and "
    "re-rated after the July results, with the price up 15% against 6% for EPS. At 25.2x it trades 25% above "
    "its 20.1x average since 2005, but below the five-year average of 28.0x and the 35.1x peak of November 2021. "
    "The price is 22% above its 40-week average. A 10% EPS upgrade at an unchanged price would take the multiple "
    "to 22.9x.")

SOURCE_LINE = ("Source: Syz Research, Bloomberg, company filings, Microsoft Q1 FY2027 earnings release and call of "
               "28 October 2026, analyst research notes of 29 October 2026")
W1, W2 = 72, 92            # PDF chart widths, % of text width
W1_PPTX, W2_PPTX = 66, 88
