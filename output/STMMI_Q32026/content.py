"""content.py: all text for the STMicroelectronics Q3 2026 Earnings update (HTML entities)."""
P = lambda s: f"<p>{s}</p>"

DOC_TYPE = "Earnings update"
DATE = "29 October 2026"
TITLE = "STMicroelectronics Q3 2026: orders surge, margins follow"

QUOTE = ("To conclude, we continue to see a very strong demand for our AI datacenters and Low Earth Orbit satellite "
         "communications products and technologies, alongside an ongoing cyclical recovery in Automotive and Industrial.")
QUOTE_WHO = "Jean-Marc Chery, President and CEO, Q3 2026 earnings call, 29 October 2026"

COMPANY_INTRO = ("STMicroelectronics makes microcontrollers, analog, power, sensor and optical chips. Automotive is "
                 "about 35% of revenue, industrial about 23%; 2026 revenue about USD 14.5bn. Listed in Paris, Milan "
                 "and New York.")

TAKEAWAYS = [
    ("pos", "Orders", "Book-to-bill well above 2 lifts the backlog above USD 20bn, about five quarters of revenue."),
    ("pos", "Photonics", "Datacenter sales more than double in 2027 as silicon photonics capacity rises more than fourfold."),
    ("pos", "Reaction", "Shares closed 1.9% higher on 29 October, after opening 1.3% lower before the call."),
    ("neu", "Valuation", "19.9x forward earnings, close to the 19.2x average since 2014 and half the June peak."),
]

KPIS = [
    ("Revenue", "USD 3.76bn", "+0.7% vs. consensus", "pos"),
    ("Gross margin", "37.3%", "+30bp vs. consensus", "pos"),
    ("Adj. EPS", "USD 0.37", "&minus;9.8% vs. consensus", "neg"),
    ("Q4 gross margin guide", "39.0%", "+90bp vs. consensus", "pos"),
]

H_P1 = "The order book outweighs the EPS miss"
P1_PARAGRAPH = P(
    "Revenue beat consensus by 0.7% and gross margin by 30bp, but adjusted EPS missed by 10%; the shares opened "
    "1.3% lower on 29 October, then closed 1.9% higher. The call carried the day: book-to-bill well "
    "above 2, a Q4 margin guide 90bp above consensus and a Q1 held at consensus despite fewer days. The recovery "
    "now has visibility.")

C1_TITLE = "STMMI: Q3 2026 results and Q4 guide vs. consensus"
C1_SUB = ("Reported vs. pre-results consensus, % &middot; Q4 guide at the midpoint &middot; 2026 revenue implied by "
          "the Q4 guide &middot; adj.: non-GAAP")
C1_COMMENT = P(
    "Adjusted operating income beat by 7%, so the EPS miss sits below the operating line; neither the release "
    "nor the call explained it. Every forward line is above consensus: the Q4 revenue guide by 0.7% and the 2026 "
    "revenue it implies, about USD 14.5bn, by 0.6%, with the second half about 20% above the first.")

BASE_CASE = (
    "We are constructive on STMicroelectronics. We underwrite a recovery led by AI datacenters, about USD 1.3bn of "
    "revenue this year and more than double in 2027 as silicon photonics ramps, satellites and industrial, with gross margin rising from 39% "
    "toward the 44% to 46% model once four legacy fabs close in late 2027 or early 2028. Forward EPS of USD 2.48 "
    "is still 43% below the 2023 peak. At 19.9x, upgrades do the work. Next test: the January update with 2027 "
    "datacenter targets.")
UPSIDE = ("Q4 gross margin at or above 39% and Q1 at consensus despite 86 days; a 2027 datacenter target above "
          "USD 2.6bn in January with a first photonics revenue figure; fab closures on schedule.")
DOWNSIDE = ("Book-to-bill falling back toward 1 as lead times ease; Q4 gross margin below 38%; fab closures slipping "
            "beyond early 2028, or price cuts in the 2027 contract negotiations with European automotive Tier 1 suppliers.")

P2_TITLE = "Beyond the key takeaways"
H_A1 = "Results: AI and industrial did the work"
A1_PARAGRAPHS = [
    P("Revenue rose 17.9% to USD 3.76bn, 1.5% above the guide midpoint. Communication equipment and computer "
      "peripherals grew 64% on AI datacenter and low Earth orbit satellite chips, and industrial 40% on "
      "general-purpose microcontrollers, analog and power; automotive grew only 5% and personal electronics fell 4%. "
      "By segment, RF and optical communication rose 46% at a 26.2% operating margin and embedded processing 24% at "
      "23.1%, while power and discrete ran at a loss of 17.1% of sales. Gross margin of 37.3% rose 410bp on lower "
      "unused-capacity charges and mix, still carrying about 100bp of transition costs. Free cash flow was USD 351m."),
    P("The reaction diverged from the EPS miss: the shares opened 1.3% lower on 29 October and closed 1.9% higher "
      "after the call. Confirmed drivers: adjusted operating income of USD 429m beat the estimate by 7%; "
      "book-to-bill was well above 2, and above 3 in communications and industrial; and management said it was "
      "comfortable delivering Q1 revenue and gross margin at least at consensus despite an 86-day quarter. We think "
      "positioning did the rest: the shares had fallen 42% from the June peak to EUR 39.45 a week earlier, taking "
      "the multiple to 18.1x."),
]
H_A2 = "Outlook: Q4 at 39%, Q1 held at consensus"
A2_PARAGRAPHS = P(
    "ST guides Q4 revenue of USD 4.15bn, up 10.5% sequentially and 0.7% above consensus, and gross margin of 39.0%, "
    "90bp above, still absorbing about 70bp of unused-capacity and reshaping costs. That implies 2026 revenue of about "
    "USD 14.5bn, up 22.8%. Datacenter revenue should reach about USD 1.3bn this year, mostly microcontrollers, "
    "silicon photonics and BiCMOS chips, and more than double in 2027, when photonics becomes tens of percent of it: "
    "management sees ST as probably the only 12-inch photonics producer at scale and will lift capacity more "
    "than fourfold. Satellite revenue should at least match 2026, limited by capacity. The 400bp fab gain lands in "
    "late 2027 or early 2028.")

H_C2 = "Valuation: the June premium is gone"
C2_TITLE = "STMMI: share price vs. consensus earnings and valuation"
C2_SUB = ("STMMI IM Equity, weekly, January 2014 to October 2026 (window starts after the 2009 loss and the 2012 to "
          "2013 earnings trough) &middot; BEst 12m-forward EPS in USD, price in EUR &middot; 40-week simple MA "
          "&middot; log scale &middot; last price EUR 44.21 is the 29 October close, after the release")
C2_COMMENT = P(
    "The multiple has round-tripped: the forward P/E peaked at 42.2x in June 2026, when the shares reached EUR 68.0, "
    "and is back to 19.9x, 4% above its 19.2x average since 2014 and well below the one-year average of 27.3x. Over "
    "12 months consensus EPS rose 141% to USD 2.48 and the price 107%, so earnings now lead. Since the July results "
    "the price fell 6% while EPS rose 19%. The shares sit on their 40-week average of EUR 44.2. A 10% EPS upgrade at "
    "an unchanged price would take the multiple to 18.1x.")

SOURCE_LINE = ("Source: Syz Research, Bloomberg, company filings, STMicroelectronics Q3 2026 earnings release and "
               "call of 29 October 2026, analyst research notes of 27 and 28 October 2026")
W1, W2 = 76, 94            # PDF chart widths, % of text width
W1_PPTX, W2_PPTX = 66, 88
