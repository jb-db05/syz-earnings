"""content.py: all text for the Galp Q3 2026 Earnings update (HTML entities; fill.json is derived from it)."""

DOC_TYPE = "Earnings update"
THEME = "Integrated oil and gas"
DATE = "26 October 2026"
TITLE = "Galp Q3 2026: Moeve collapse hits the stock, not the case"

QUOTE = ("While discussions with Moeve regarding a potential combination of our downstream businesses have "
         "concluded without an agreement, Galp&rsquo;s strategic direction and investment proposition remain unchanged.")
QUOTE_WHO = "Maria Jo&atilde;o Carioca and Jo&atilde;o Marques da Silva, co-CEOs, Q3 2026 results release, 26 October 2026"

TAKEAWAYS = [
    ("neg", "Deal", "The Moeve downstream merger ended after ten months of talks, removing c.EUR 1.1 per share of synergies."),
    ("pos", "Beat", "Q3 RCA EBITDA of EUR 1,522m rose 67%, 3.5% above consensus, on Bacalhau and refining."),
    ("pos", "Raised", "Full-year EBITDA guidance lifted to c.EUR 5bn from c.EUR 4bn, operating cash flow to c.EUR 3.9bn."),
    ("neu", "Valuation", "The 8.8% fall, nearly twice the synergy value, leaves 8.4x forward earnings, 27% below average."),
]

KPIS = [
    ("Lost synergies per share", "c.EUR 1.1", "EUR 750 to 800m in total", "neg"),
    ("Results-day share move", "&minus;8.8%", "&minus;EUR 2.03 per share", "neg"),
    ("RCA EBITDA", "EUR 1,522m", "+3.5% vs. consensus", "pos"),
    ("FY26 EBITDA guide", "c.EUR 5.0bn", "+25% vs. prior guide", "pos"),
]

H_P1 = "The deal, not the quarter, drove the stock"
P1 = ("The quarter was good: RCA (replacement cost adjusted) EBITDA beat consensus by 3.5% and full-year guidance rose "
      "25%. The share price followed the deal: on results day Galp confirmed that ten months of talks to merge its "
      "Iberian refining and retail businesses with Moeve (formerly Cepsa) had ended without agreement. The shares fell "
      "8.8%, about EUR 2.0 per share, close to twice the c.EUR 1.1 of synergy value analysts had assigned. The market is "
      "pricing a lost strategic option.")

C1_TITLE = "GALP: results-day share price fall vs. lost synergy value"
C1_SUB = ("EUR per share &middot; synergies: analyst estimates of EUR 750 to 800m &middot; share price fall: "
          "23 October close to the 26 October results-day print")
C1_COMMENT = ("The shares lost EUR 2.03 on results day, almost twice the c.EUR 1.1 "
              "of synergies analysts had assigned to the deal. We read the extra EUR 0.9 as the "
              "lost option to shrink Galp&rsquo;s refining exposure: Galp would have kept only 20% of the combined "
              "refineries, moving it closer to an upstream growth story.")

BASE_CASE = ("We stay positive on Galp and would add on the results-day weakness. The sell-off prices the failed merger "
             "as a permanent loss of value, too harshly in our view: the synergies were worth about EUR 1.1 per share, "
             "the shares lost EUR 2.0, and Galp keeps a standalone downstream that earned EUR 639m of EBITDA in Q3. We "
             "underwrite the new c.EUR 5bn EBITDA and c.EUR 3.9bn cash flow guidance, with a proposed "
             "10% dividend rise to EUR 0.70 and the EUR 250m buyback. Management still backs consolidation; the next test "
             "is whether it sets out another route for downstream at full-year results.")

UPSIDE = ("A new route for downstream at full-year results, such as a Sines partner or a smaller retail deal; Moeve or another party returns on revised terms; Q4 EBITDA beats the c.EUR 1.26bn implied by "
          "guidance; a larger 2027 buyback.")
DOWNSIDE = ("Galp turns buyer and raises its refining exposure through a large acquisition; refining margins fall back "
            "towards the USD 13 per barrel of the original guidance, cutting the value of the standalone business; Brazil "
            "makes its temporary oil export tax permanent.")

P2_TITLE = "Beyond the key takeaways"
H_A1 = "Results: Bacalhau and refining did the work"
A1 = [
    ("RCA EBITDA rose 67% to EUR 1,522m. Upstream gained 53% to EUR 708m as the Bacalhau FPSO lifted working-interest "
     "production 14% to 131 kboe/d, with oil realisations up 32% to USD 87.3/bbl. Industrial &amp; Midstream doubled to "
     "EUR 639m: the refining margin reached USD 34.0/boe against USD 9.5/boe a year ago, on diesel cracks of USD 590/t, "
     "despite EUR 172m of hedge losses and EUR 125m of pricing-formula lags. Commercial rose 24% to EUR 147m and "
     "Renewables tripled to EUR 48m. RCA net income rose 68% to EUR 682m, about EUR 0.94 per share on our count, and "
     "operating cash flow of EUR 1,223m (+63%) left net debt at EUR 1.43bn, or 0.35x EBITDA."),
    ("Management raised 2026 RCA EBITDA guidance to c.EUR 5bn from c.EUR 4bn and operating cash flow to c.EUR 3.9bn "
     "from c.EUR 3bn, on Brent at USD 90/bbl (from 80) and a realised refining margin of c.USD 25/boe (from 13). The guide "
     "implies Q4 EBITDA of about EUR 1.26bn and, on our arithmetic, a Q4 Brent near USD 78/bbl against USD 97 in Q3, so "
     "oil leaves room for a beat. Two items temper the read-across: the Sines hydrocracker turnaround that began in late "
     "September, and Brazil&rsquo;s temporary oil export tax, which lifted RCA taxes 79% to EUR 493m."),
]

H_A2 = "The deal: a valuation gap at peak margins"
A2 = ("Announced in January, the plan would have created two Iberian platforms: a 50/50 RetailCo with about 3,500 service "
      "stations, and an IndustrialCo holding the Huelva, C&aacute;diz and Sines refineries, 80% owned by Moeve and 20% by "
      "Galp. Talks failed on valuation. With refining margins high but volatile, the sides could not agree what the "
      "refineries were worth, and Q3&rsquo;s EUR 639m of Industrial EBITDA shows why Galp would not sell at a discount. "
      "Handing Sines, Portugal&rsquo;s only refinery, to a platform controlled by Mubadala and Carlyle also raised "
      "energy-security concerns, and press reports say the Amorim family, Galp&rsquo;s largest shareholder, rejected "
      "some of Moeve&rsquo;s demands.")

H_C2 = "Valuation: earnings ran ahead of the price"
C2_TITLE = "GALP: share price vs. consensus earnings and valuation"
C2_SUB = ("GALP PL Equity, weekly from January 2022 (the 2020 earnings collapse lifted the P/E above 130x) &middot; BEst "
          "12m-forward consensus &middot; 200-day (c. 40-week) simple MA &middot; log scale &middot; P/E shaded vs. its "
          "2022 to 2026 average &middot; last price is the 26 October results-day print; consensus EPS not yet revised")
C2_COMMENT = ("Earnings have run well ahead of the share price. Over 12 months, consensus 12m-forward EPS rose 87% to "
              "EUR 2.48 while the price gained 24%, so the forward P/E fell from 12.7x to 8.4x, 27% below its 11.6x "
              "average since 2022 and under the 10.9x one-year average; results day alone took it down from 9.2x. "
              "Removing the full EUR 1.1 of synergy value from the pre-results EUR 22.96 would leave EUR 21.86, or 8.8x: "
              "the stock now trades below that, though still 6% above its 40-week average.")

SOURCE_LINE = ("Source: Syz Research, Bloomberg, company filings, Galp Q3 2026 results release of 26 October 2026, "
               "analyst research notes, press reports of October 2026")

W1, W2 = 66, 92            # PDF chart widths (% of text width)
W1_PPTX, W2_PPTX = 66, 88  # PPTX chart widths
