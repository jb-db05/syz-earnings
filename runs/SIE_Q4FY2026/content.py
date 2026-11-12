"""content.py: all text for the Siemens Q4 FY2026 Earnings update (HTML entities; fill.json is unescaped from this)."""

DOC_TYPE = "Earnings update"
DATE = "12 November 2026"
TITLE = "Siemens Q4 FY2026: record orders, higher targets, full price"

QUOTE = ("We see significant opportunities ahead. Driven by powerful secular growth trends and the strengths of our "
         "core markets, we are raising our mid-term targets.")
QUOTE_WHO = "Roland Busch, CEO, Q4 FY2026 earnings call, 12 November 2026"

COMPANY_INTRO = ("Siemens supplies factory automation and software, electrification, building technology and rail "
                 "systems, and controls Siemens Healthineers. Fiscal 2026 revenue EUR 83.4bn; Frankfurt-listed, "
                 "market value about EUR 220bn.")

TAKEAWAYS = [
    ("pos", "Beat", "Q4 orders EUR 34.8bn, 29% above consensus; industrial profit EUR 3.9bn, 5% ahead, at a 16.8% margin."),
    ("pos", "Raised", "Mid-term revenue growth target lifted to 7% to 11% from 6% to 9%; EPS growth now double digit."),
    ("neg", "Watch", "Mobility&rsquo;s record orders convert mostly after fiscal 2028; China automation orders softened in September."),
    ("neu", "Valuation", "21.6x forward earnings, 43% above the 2015 to 2026 average of 15.1x: the quality is priced."),
]

KPIS = [
    ("Q4 orders", "EUR 34.8bn", "+29% vs. consensus", "pos"),
    ("Q4 revenue", "EUR 23.7bn", "+1% vs. consensus", "pos"),
    ("Q4 industrial profit", "EUR 3.9bn", "+5% vs. consensus", "pos"),
    ("FY27 EPS guide", "EUR 10.20&ndash;10.80", "+13% at midpoint, ex SHL", "neu"),
]

H_P1 = "Orders reset the growth path, not the rating"
P1_PARAGRAPH = ("Orders beat consensus by 29% and industrial profit by 5%, and the shares rose about 3% in early trading on "
                "12 November, with the DAX higher. What changes is the growth path: management lifted the mid-term "
                "revenue target to 7% to 11% and EPS growth to double digit, backed by a data centre backlog above EUR 7bn "
                "and record free cash flow of EUR 12.1bn.")

C1_TITLE = "SIE: Q4 FY2026 results vs. consensus"
C1_SUB = ("Reported vs. consensus, % &middot; Consensus: analyst estimates before the release &middot; "
          "Free cash flow: fiscal year; other lines: fiscal Q4")
C1_COMMENT = ("The orders beat is large but mixed in quality: Mobility booked more than EUR 10bn, much of it long-dated "
              "rolling stock and service contracts, while Smart Infrastructure orders rose 39% on data centres. Revenue was "
              "only 1% ahead, so the profit beat came from margins, led by Digital Industries at 21.9% before severance.")

BASE_CASE = ("Siemens has moved from a cyclical recovery story to a structural growth one."
             " We underwrite fiscal 2027 EPS of EUR 10.20 to 10.80 excluding Healthineers, up 13% at the midpoint, "
             "with upside if US and China automation keep their pace. The case remains constructive, but at 21.6x forward earnings the "
             "risk/reward is balanced: further gains need upgrades, not a higher multiple. The next tests are the "
             "10 December spin-off report, setting out how Siemens shareholders receive Healthineers shares, and the "
             "February votes approving it.")
UP_HEAD = "What would strengthen our view"
DOWN_HEAD = "What would change our view"
UPSIDE = ("Digital Industries Q1 growth inside its 8% to 12% range despite October pre-buying; data centre orders "
          "rising again in fiscal 2027; the EPS guide raised at the half year in May.")
DOWNSIDE = ("Data centre orders stalling for two quarters on power access or permits; China automation slowing once price-led "
            "pre-buying fades; the Healthineers spin-off slipping beyond the planned May 2027 date.")

P2_TITLE = "Beyond the key takeaways"
H_A1 = "Results: margins carried the profit beat"
A1_PARAGRAPHS = [
    ("Comparable revenue rose 10% to EUR 23.7bn and industrial business profit 22% to EUR 3.9bn, a 16.8% margin, 150bp "
     "higher year on year. Digital Industries did most of the margin work: orders rose 15% and revenue 10%, and the "
     "margin before severance reached 21.9% on automation volumes, a better mix and some currency help, with software "
     "revenue and annual recurring revenue both up 12%. Smart Infrastructure grew revenue 15% at a 20.3% margin, of which "
     "50bp came from US tariff refunds, a one-off we strip from the run rate. Mobility&rsquo;s 9.5% margin reflected a "
     "favourable mix, and quarterly free cash flow reached EUR 5.6bn."),
    ("Surprise and reaction are aligned, but the move is modest for a 29% orders beat: the shares rose about 3% in early "
     "trading on 12 November, with the DAX also higher. Two confirmed facts temper the headline. Mobility&rsquo;s record "
     "orders convert progressively, with many projects starting only beyond fiscal 2028, and China automation orders, up "
     "8%, softened in September, while October was lifted by buying ahead of announced price increases. We think "
     "positioning also played a part: the shares traded at 20.2x forward earnings into the print, against a 15.1x "
     "average since 2015, so the beat confirms rather than changes the expected path."),
]
H_A2 = "Outlook: a 13% EPS step without Healthineers"
A2_PARAGRAPHS = [
    ("For fiscal 2027, excluding Siemens Healthineers, Siemens guides comparable revenue growth of 9% to 11%, a "
     "book-to-bill above 1 and EPS before purchase price allocation of EUR 10.20 to 10.80, up 13% at the midpoint. Digital Industries 8% to 12% at a 20% to 22% margin; Smart Infrastructure 11% to 13% at 19.5% to 20.5%, carried by electrification; Mobility 6% to 8% "
     "at 8% to 10%, held back by Mermec integration costs. Management expects about 70% of the data centre backlog to "
     "convert in fiscal 2027. In late spring 2027 Siemens will hand a 34.1% "
     "Healthineers stake directly to its shareholders, one Healthineers share for every two Siemens shares."),
]
H_C2 = "Valuation: earnings must now do the work"
C2_TITLE = "SIE: share price vs. consensus earnings and valuation"
C2_SUB = ("Weekly, Jun 2015 to 12 Nov 2026 &middot; Bloomberg 12m-forward consensus EPS, includes Healthineers &middot; "
          "40-week MA &middot; log scale &middot; last price is a results-day level")
C2_COMMENT = ("Over 12 months the share price rose 19% against 13% for consensus EPS: the "
              "12m-forward P/E stands at 21.6x, 43% above its 15.1x average since 2015 and close to the 23.1x peak of July "
              "2026, with the price 9% above its 40-week moving average. Since early August, EPS rose 3% "
              "while the price was broadly flat, a mild derating. At the long-run average multiple the price would be "
              "about EUR 197, and a 10% upgrade at an unchanged price still leaves 19.6x. Consensus includes Healthineers, "
              "so the series will reset once the stake is reported as discontinued.")

SOURCE_LINE = ("Source: Syz Research, Bloomberg, company filings, Siemens Q4 FY2026 earnings release and call of "
               "12 November 2026, analyst research notes of 12 November 2026")

W1, W2 = 72, 94            # PDF chart widths, % of text width
W1_PPTX, W2_PPTX = 66, 88  # PPTX chart widths
