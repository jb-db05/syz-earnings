"""content.py: all text for the Galderma Q3 2026 Earnings update (HTML entities; build_pdf.py derives fill.json)."""

TICKER, PERIOD = "GALD", "Q32026"
W1, W2 = 74, 94            # PDF chart widths, % of text width
W1_PPTX, W2_PPTX = 68, 90  # PPTX chart widths

DOC_TYPE = "Earnings update"
THEME = "Dermatology"
DATE = "22 October 2026"
TITLE = ('Galderma Q3 2026: a beat, a raise and a rally')

QUOTE = ("With a stronger-than-anticipated trajectory in the first nine months, especially in Therapeutic Dermatology, "
         "across both Nemluvio and the mature portfolio, as well as in Dermatological Skincare and Neuromodulators, "
         "Galderma is raising its full-year 2026 net sales growth guidance")
QUOTE_WHO = "Galderma, Q3 2026 trading update, release of 22 October 2026 (company statement)"

TAKEAWAYS = [
    ("pos", "Beat", "Q3 sales USD 1,632m, up 26% at constant currency and 5.1% above consensus, with every category contributing."),
    ("pos", "Raised", "2026 sales growth guide raised to 22.5&ndash;23.5% from 19&ndash;21%; core operating margin (EBITDA) held at about 26%."),
    ("neg", "Watch", "Fillers grew only 4.8%, mature brands face generics, and the US Relfydess refiling waits until early 2027."),
    ("neu", "Valuation", "46.7x this year&rsquo;s consensus earnings with the shares just below their record: upgrades must now do the work."),
]

KPIS = [
    ("Q3 net sales", "USD 1,632m", "+5.1% vs. consensus", "pos"),
    ("Q3 growth, constant FX", "+26.0%", "Nine months: +25.1%", "neu"),
    ("Nemluvio Q3 sales", "USD 302m", "About +7% vs. consensus", "pos"),
    ("FY26 sales growth guide", "+22.5&ndash;23.5%", "Raised from +19&ndash;21%", "pos"),
]

H_P1 = "What the quarter means for the investment case"
P1 = ('This is the second beat and raise in a row, and the key message is breadth. Therapeutic dermatology grew 58.9%, but neuromodulators (+24.1%) and dermatological skincare (+15.6%) also ran well ahead of their markets: the quarter does not rest on Nemluvio alone. With the sales guide raised by more than three points and the margin target held, analysts expect 2026 sales and core EBITDA about 1.5% above prior consensus.')

C1_TITLE = ('GALD: contribution to Q3 2026 group growth (bridge)')
C1_SUB = ('Contribution to group growth at constant currency, pp &middot; weighted by Q3 2025 sales mix (USD 1,289m) &middot; sum 26.2pp vs. 26.0% reported (rounding)')
C1_COMMENT = ('Therapeutic dermatology added 14.4 points of the 26.0% growth, but neuromodulators (6.5), dermatological skincare (4.2) and fillers (1.1) delivered close to 12 points. Neuromodulators were helped by US shipments shifted from Q2, which flatters the quarter. Fillers and biostimulators, up only 4.8%, remain the soft spot after last year&rsquo;s Sculptra launch in China.')

BASE_CASE = ('We stay positive on Galderma. Our base case is 2026 sales growth of about 23% at constant currency, a core EBITDA margin near 26% and consensus earnings per share of USD 4.80 edging higher after the raise. The debate has moved from whether Galderma can grow to whether it can hold the pace through generic erosion, the Relfydess delay and the ZO Skin Health integration. With the shares up 6% on the day and just below their June record, the easy re-rating is done. The next test is the full-year release in early 2027.')

UPSIDE = ('Consensus 2026 earnings per share above USD 4.90; Nemluvio above USD 300m again in Q4, taking the year beyond USD 1bn; fillers growth back towards double digits in 2027; the US Relfydess refiling on time in Q1 2027.')
DOWNSIDE = ('Mature therapeutic brands falling faster than expected as generics arrive; a 2026 core EBITDA margin below 26% or a weak 2027 margin outlook once ZO Skin Health is consolidated; a further Relfydess delay; the shares breaking below CHF 162.')

P2_TITLE = "Beyond the key takeaways"
H_A1 = "Results: the beat came from every category"
A1 = ['Injectable aesthetics, the largest category, delivered USD 736m (+15.4% at constant currency). Neuromodulators reached USD 433m (+24.1%) as unfavourable US shipment phasing from Q2 unwound on top of continued Dysport share gains and the international Relfydess launch; part of the 24.1% is therefore timing, not demand. Fillers and biostimulators grew 4.8% to USD 303m against a soft market and the prior-year Sculptra launch in China, but nine-month growth of 8.5% and double-digit Sculptra growth in the US and abroad point to continued share gains. Dermatological skincare added USD 396m (+15.6%), led by Cetaphil in Asia and by Alastin, with e-commerce the fastest-growing channel.', 'Therapeutic dermatology was the standout at USD 499m (+58.9%), about 8% above consensus. Nemluvio contributed USD 302m, some 7% ahead of expectations, taking nine-month sales to USD 735m and the USD 1bn full-year mark within reach. The mature portfolio, at USD 197m, benefited from generic entries arriving later than expected, a support the company expects to turn into negative growth pressure in the second half. The United States grew 39.3% to USD 755m, flattered by neuromodulator phasing, and international markets 17.1% to USD 876m. Volume led growth, helped by mix.']
H_A2 = "Outlook: the new guide still looks prudent"
A2 = ('The full-year guide of 22.5 to 23.5% at constant currency compares with nine-month growth of 25.1%. By our arithmetic it implies Q4 growth of roughly 16 to 19%, well below the 26% of Q3, absorbing generic erosion, the fillers comparison and some consumer caution: we read it as prudent. The core EBITDA margin of about 26% compares with 25.6% in the first half. Post-release analyst estimates put 2026 sales near USD 6.5bn and core EBITDA near USD 1.69bn, about 1.5% above prior consensus. The new US Section 232 tariffs do not touch Nemluvio in 2026. ZO Skin Health (USD 1.5bn) is excluded: earnings-neutral in year one, slightly margin-dilutive in 2027.')

H_C2 = "Valuation: earnings must do the work"
C2_TITLE = "GALD: share price vs. consensus earnings and valuation"
C2_SUB = ('GALD SW Equity, daily &middot; consensus current-year EPS (USD), rolls each January &middot; 200-day MA &middot; log scale &middot; last price: 21 October close +6%')
C2_COMMENT = ('The shares trade at 46.7x consensus 2026 earnings, 3% below the 48.2x average since May 2024 and close to the 44.0x average of 2026; the long-run figure is inflated by late-2025 readings on an ageing 2025 base. Consensus 2026 earnings per share has risen 6.4% since January and 4.3% since the H1 results, while the price was flat between the releases until today&rsquo;s 6% gain: the stock de-rated from 46.4x to 44.0x before the print. The price sits 14% above its 200-day average. At about 33x 2027 analyst estimates, upgrades, not the multiple, drive the next leg.')

SOURCE_LINE = ("Source: Syz Research, Bloomberg, company filings, Galderma Q3 2026 trading update of 22 October 2026, "
               "analyst research notes of October 2026")
