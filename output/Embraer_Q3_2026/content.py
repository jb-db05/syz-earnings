"""content.py: all text for Embraer Q3 2026 (HTML entities). Plain-text fill.json is derived from it."""
DATE = "10 November 2026"
TITLE = "Embraer Q3 2026: operations beat, the profit miss is noise"
QUOTE = ("We delivered record third quarter revenue of $2.3 billion with revenue and margin expansion across all our "
         "businesses. Our backlog reached a new all time high of $35.7 billion for the eighth consecutive quarter.")
QUOTE_WHO = "Francisco Gomes Neto, President and CEO, Q3 2026 earnings call, 10 November 2026"
COMPANY_INTRO = ("Embraer, based in Brazil, builds regional jets, business jets and defence aircraft such as the KC-390, "
                 "and services their fleets. Commercial jets were 30% of Q3 revenue. Listed in S&atilde;o Paulo and New York.")
TAKEAWAYS = [
    ("pos", "Beat", "Revenue USD 2.35bn (+11% vs. consensus) and adjusted EBIT USD 255m (+22%), a 10.9% margin."),
    ("pos", "Raised", "Free cash flow guide lifted to USD 700m or more, from USD 400m; revenue guide also raised."),
    ("pos", "Reaction", "Shares rose 5.9% intraday on 10 November although adjusted net income missed consensus by 50%."),
    ("neu", "Valuation", "13.1x forward earnings, 9% below the 14.3x average since 2014: the upgrades are not yet priced."),
]
KPIS = [
    ("Revenue", "USD 2.35bn", "+11% vs. consensus", "pos"),
    ("Adj. EBIT margin", "10.9%", "+90bp vs. consensus", "pos"),
    ("Adj. net income", "USD 74m", "&minus;50% vs. consensus", "neg"),
    ("FY26 FCF guide", "&ge; USD 700m", "Up from &ge; USD 400m", "pos"),
]
H_P1 = "Cash, not net income, sets the tone"
P1 = ("Revenue beat consensus by 11% and adjusted EBIT by 22%, while adjusted net income fell 50% short, yet the shares "
      "rose 5.9% intraday on 10 November. We read the divergence as justified: the miss came from a non-cash "
      "revaluation of the share-linked incentive plan and higher tax, while USD 628m of free cash flow and the "
      "raised cash guide are recurring.")
C1_TITLE = "EMBJ3: Q3 2026 surprises vs. consensus and guide revisions"
C1_SUB = ("Q3 lines vs. press-reported consensus (revenue and EBIT in USD, net income in BRL) &middot; FY26 guides vs. "
          "the previous guide (revenue midpoint, free cash flow floor)")
C1_COMMENT = ("The operating lines and the cash guide carry the chart; the miss sits below operating profit. "
              "Adjusted net income of USD 74m absorbed USD 159m of net financial costs, mainly the incentive-plan "
              "revaluation, which rises with the share price. Free cash flow of USD 628m, twice last year&rsquo;s, "
              "came from pre-delivery payments.")
BASE_CASE = ("The case remains very constructive and the risk/reward skewed to the upside. We underwrite an adjusted "
             "EBIT margin of about 10% for 2026, rising with mix as business jets and services, at 16% to 17% margins, "
             "outgrow commercial jets at 2.4%. The USD 35.7bn backlog, about four years of revenue, gives visibility "
             "to 2030. At 13.1x forward earnings, below the long-run average, the rerating has room. The next test is "
             "the Q4 print and the 2027 guide.")
UPSIDE = ("Firm orders from the large Indian and European jet campaigns; a Q4 EBIT margin above the implied 9%; "
          "business jet output moving toward the 200-unit target for 2028.")
DOWNSIDE = ("Supply delays leaving Q4 short of the 80 to 85 commercial jets guided; commercial margins sliding back "
            "toward zero; new-programme spending lifting capex above USD 550m.")
P2_TITLE = "Beyond the key takeaways"
H_A1 = "Results: every division widened its margin"
A1 = [
    ("Revenue rose 17% to USD 2.35bn, a record for a third quarter, and adjusted EBIT 48% to USD 255m, lifting the "
     "margin to 10.9% from 8.6%. Commercial aviation grew 13% to USD 696m with a 2.4% margin, helped by supplier "
     "compensation. Business jets grew 12% to USD 655m at 16%, about 430bp higher, on price, mix and the absence of "
     "last year&rsquo;s US import tariffs. Defence grew 22% to USD 341m at 15.7% on KC-390 volumes. Services and "
     "support grew 30% to USD 638m at 17%, about 330bp higher on operating leverage. Nine-month revenue of USD 6.0bn "
     "is above 70% of the guidance midpoint."),
    ("The quarter beat on revenue, operating margin and free cash flow and missed on earnings: adjusted net income of "
     "USD 74m was 13% below last year and about 50% below consensus, yet the shares rose 5.9% by 10:24 on 10 "
     "November. Management named the drivers of the miss: USD 159m of net financial costs, "
     "mainly the mark-to-market of the long-term incentive plan, and higher taxes. Neither touches operations or "
     "cash. The rise is consistent with investors looking through a charge that grows with the share price, but we "
     "cannot confirm positioning: the stock had already gained 16% in the two weeks before the print."),
]
H_A2 = "Outlook: cash guide up 75%, margins held"
A2 = ("Embraer raised its 2026 revenue guide to USD 8.4 to 8.6bn, from 8.2 to 8.5bn, and its adjusted free cash flow "
      "guide, excluding Eve, to USD 700m or more, from USD 400m, the second upgrade this year. The 10.0% to 10.6% EBIT "
      "margin range and the delivery guides, 80 to 85 commercial and 160 to 170 business jets, are unchanged. After "
      "10.7% over nine months, the range implies about 9% in Q4 at the midpoints, partly as defence margins normalise. "
      "Beyond 2026, capex rises to USD 500 to 550m in 2027 and 2028 for the 200-unit business jet target, and Eve, "
      "the air mobility unit, should contribute only after 2029.")
H_C2 = "Valuation: below the long-run multiple"
C2_TITLE = "EMBJ3: share price vs. consensus earnings and valuation"
C2_SUB = ("EMBJ3 BZ, weekly, Sep 2014 to 10 Nov 2026, BRL &middot; Bloomberg 12m-forward consensus &middot; 40-week "
          "simple MA &middot; log scale &middot; Jan 2019 to Jun 2022 earnings trough blanked and excluded from the P/E "
          "average &middot; last price BRL 113.45 is an intraday level on results day")
C2_COMMENT = ("Over 12 months the price rose 31% and consensus EPS 29%, so the move has been earnings-led. At 13.1x "
              "12m-forward earnings, the multiple sits 9% below its 14.3x average since 2014, with the 2019 to 2022 "
              "earnings trough excluded, and above its 11.7x one-year average, but well under the 22.1x peak of July "
              "2025. The price is 31% above its 40-week average, a stretched short-term trend. A return to the "
              "long-run average would add 9% at unchanged earnings; a 10% EPS upgrade at today&rsquo;s price would "
              "take the multiple to 11.9x.")
SOURCE_LINE = ("Source: Syz Research, Bloomberg, company filings, Embraer Q3 2026 earnings call of 10 November 2026, "
               "analyst research notes of 10 November 2026")
