"""content.py: all text of the Novartis Q3 2026 Earnings update (HTML entities; fill.json is derived from it)."""

DOC_TYPE = "Earnings update"
DATE = "27 October 2026"
TICKER = "NOVN"
QUARTER = "Q3 2026"

TITLE = "Novartis Q3 2026: the beat is costs, the debate is pipeline"

QUOTE = ("Novartis delivered solid sales growth in Q3, as priority brands and launches more than offset generic "
         "erosion, demonstrating the replacement power of the business.")
QUOTE_WHO = "Vas Narasimhan, CEO, Q3 2026 results release, 27 October 2026"

COMPANY_INTRO = ("Novartis is a Basel-based innovative medicines company in cardiovascular, immunology, neuroscience "
                 "and oncology. Its top 20 brands made up 83% of third-quarter sales of USD 14.5bn. Listed on SIX, "
                 "market value around CHF 240bn.")

TAKEAWAYS = [
    ("pos", "Beat", "Core earnings per share (EPS) of USD 2.46 beat consensus by 7%, driven by costs rather than sales."),
    ("pos", "Raised", "2026 core operating income guidance raised to flat to low single-digit growth, from a "
                      "decline."),
    ("neg", "Watch", "Two late-stage trial failures triggered a USD 1.9bn impairment; reported net income fell 71%."),
    ("neu", "Valuation", "17.4x forward earnings, 33% above the 2005 to 2026 average: much pipeline success is "
                         "already priced."),
]

KPIS = [
    ("Net sales", "USD 14.5bn", "In line, +0.6% vs. consensus", "neu"),
    ("Core EPS", "USD 2.46", "+7% vs. consensus", "pos"),
    ("Core operating margin", "41.6%", "+270bp vs. consensus", "pos"),
    ("2026 core profit guide", "Raised", "To flat to +low single digit", "pos"),
]

H_P1 = "Replacement power holds, costs do the rest"
P1_PARAGRAPH = ("Core EPS beat consensus by 7% on in-line sales, and the shares were indicated 1.2% higher before the "
                "open on 27 October, at CHF 129.05: aligned but muted, with the close not yet available. Priority "
                "brands lifted sales 4% despite Entresto falling 38% to generics, which supports the replacement "
                "story; the beat came from costs, not demand.")

C1_TITLE = "NOVN: Q3 2026 results vs. consensus"
C1_SUB = ("Reported vs. pre-results consensus, % &middot; Group lines and selected brands &middot; Consensus: "
          "analyst estimates compiled in first takes of 27 Oct 2026")
C1_COMMENT = ("Group profit lines beat by 7% to 8% on a sales line that only matched expectations. Selling, general "
              "and administrative costs ran 9% below estimates, while two growth brands fell short: Pluvicto, the "
              "prostate cancer radioligand, and Scemblix, for leukaemia. Rhapsido, the new urticaria pill, beat by "
              "16% and is the early launch to watch.")

BASE_CASE = ("We stay constructive on Novartis and keep the position, but would not chase the shares at 17.4x forward "
             "earnings; we would add on pipeline-driven weakness towards the 200-day average near CHF 121. We "
             "underwrite flat to low single-digit core operating income growth in 2026, around 3% consensus EPS "
             "upgrades and faster sales growth in 2027 as generic erosion fades. The debate has moved from the patent "
             "cliff to the pipeline. Next test: the 19 November management event and its 2031 outlook.")

UPSIDE = ("A 19 November outlook that keeps sales growing through the 2029 to 2031 patent expiries of Cosentyx, "
          "Kisqali and Kesimpta; fourth-quarter sales growth near 9%; positive abelacimab Phase III data in atrial "
          "fibrillation by mid-2027.")
DOWNSIDE = ("Another late-stage failure or impairment, above all abelacimab; a fourth-quarter core margin back below "
            "38%, showing the third-quarter savings were timing; Pluvicto still missing estimates if the new "
            "prostate cancer label fails to lift US demand.")

P2_TITLE = "Beyond the key takeaways"

H_A1 = "Results: launches offset generics, costs beat"
A1_PARAGRAPHS = [
    ("Net sales rose 4% in constant currencies (cc) to USD 14.5bn: volume added 14 percentage points, generic "
     "competition took 9 and pricing 1, with no currency effect. Priority brands carried the quarter. Kisqali grew "
     "37% to USD 1.82bn, Kesimpta 22% to USD 1.48bn and Cosentyx 9% to USD 1.86bn, while Scemblix and Leqvio grew 67% "
     "and 63%. Entresto fell 38% to USD 1.17bn and Promacta 61%. Core operating income rose 10% cc to USD 6.04bn, a "
     "41.6% margin, up 2 points cc and 7.6% to 8.1% above consensus depending on the estimate set. Core EPS rose 8% "
     "cc to USD 2.46. The USD 1.9bn del-desiran impairment cut reported net income 71% to USD 1.2bn."),
    ("Surprise and reaction point the same way, but a 1.2% pre-market gain on 27 October is small for a 7% core EPS "
     "beat. Confirmed drivers temper it: sales were only in line, the profit beat came from SG&amp;A costs 9% below "
     "estimates, and Pluvicto and Scemblix missed by 7.7% and 2.1%. Our reading, not confirmed by management, is "
     "that expectations were already high: the shares had recovered 14% from the 8 September low, after the Phase III "
     "failures cut them 10.9% in a day, and slipped 0.4% on 26 October, with the SMI up 0.5%, as detailed "
     "remibrutinib data in multiple sclerosis drew mixed reviews."),
]

H_A2 = "Outlook: the raise needs a strong Q4"
A2_PARAGRAPH = ("Management now expects 2026 core operating income to be flat to up low single digits in cc, from a "
                "low single-digit decline, and keeps net sales growth at low single digits; at late-October rates, "
                "currency adds 1 point to each. With nine-month core profit down 2% cc, the raise implies a "
                "strong fourth quarter: analyst estimates model sales growth near 9% and around 3% upgrades to 2026 "
                "consensus core EPS. The CEO expects sales growth to accelerate in 2027. Next come the 19 November "
                "management event, a US filing for remibrutinib in multiple sclerosis by end-2026 using a priority "
                "review voucher, and abelacimab atrial fibrillation data by mid-2027.")

H_C2 = "Valuation: the multiple did the work"
C2_TITLE = "NOVN: share price vs. consensus earnings and valuation"
C2_SUB = ("Weekly, 21 Jan 2005 to 26 Oct 2026 &middot; Bloomberg 12m-forward consensus EPS in USD, price in CHF "
          "&middot; 200-day MA &middot; P/E vs. its 2005&ndash;26 average &middot; Last price is the 26 October close, "
          "before the release")
C2_COMMENT = ("The shares have run ahead of earnings. Over 12 months the price rose 22.5% to CHF 127.48 while "
              "12m-forward consensus EPS fell 2.0% to USD 8.84, so the whole gain came from the multiple. At 17.4x, "
              "the P/E is 33% above its 13.2x average since 2005 and above the 16.7x one-year average, though below "
              "the 19.1x peak of 27 February 2026. The price sits 5% above its 200-day average and 3% below the 2 "
              "September high. A 3% EPS upgrade at an unchanged price would take the multiple to 16.9x: earnings, "
              "not re-rating, now have to carry the stock.")

SOURCE_LINE = ("Source: Syz Research, Bloomberg, company filings, Novartis Q3 2026 results release of 27 October 2026, "
               "analyst research notes of 26 and 27 October 2026, Finanz und Wirtschaft and finanzen.net of "
               "27 October 2026 (pre-market indication)")

W1, W2 = 74, 94            # PDF chart widths, % of the text width
W1_PPTX, W2_PPTX = 66, 88  # PPTX chart widths

BUDGETS = {  # (min, max) words, from SKILL.md
    "QUOTE": (20, 35), "COMPANY_INTRO": (25, 36), "P1_PARAGRAPH": (55, 65), "C1_COMMENT": (50, 55),
    "BASE_CASE": (80, 90), "UPSIDE": (34, 38), "DOWNSIDE": (34, 38), "A1_0": (100, 115), "A1_1": (90, 105),
    "A2_PARAGRAPH": (95, 110), "C2_COMMENT": (85, 100),
}
