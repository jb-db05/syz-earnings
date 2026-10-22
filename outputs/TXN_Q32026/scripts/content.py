"""content.py: all text for the TXN Q3 2026 Earnings update (HTML entities; fill.json is derived from this)."""
DATE = "22 October 2026"
TICKER, Q = "TXN", "Q32026"
W1, W2 = 80, 94            # PDF chart widths, % of text width
W1_PPTX, W2_PPTX = 72, 90

TITLE = "Texas Instruments Q3 2026: upcycle broadens, earnings must do the work"
THEME = "Semiconductors"
QUOTE, QUOTE_WHO = "", ""   # no verbatim executive quote available (see reply); block omitted

TAKEAWAYS = [
    ("pos", "Beat", "Revenue USD 6.06bn (+28% year on year) and EPS USD 2.62 beat consensus by 2% and 9%."),
    ("pos", "Raised", "Q4 guide midpoints of USD 6.05bn revenue and USD 2.62 EPS sit 6% and 14% above consensus."),
    ("neg", "Watch", "Nearly 45% of analysts stay neutral or negative after the print, citing valuation and capital intensity."),
    ("neu", "Valuation", "32.4x forward earnings, 48% above the 2010 to 2026 average: upgrades, not the multiple, must drive returns."),
]
KPIS = [
    ("Revenue", "USD 6.06bn", "+2.4% vs. consensus", "pos"),
    ("EPS", "USD 2.62", "+8.7% vs. consensus", "pos"),
    ("Operating margin", "47.5%", "+290bp vs. consensus", "pos"),
    ("Q4 revenue guide", "USD 6.05bn", "+5.6% vs. consensus", "pos"),
]

H_P1 = "The cycle is now showing up in margins"
P1 = ("For investors, the quality of the beat matters more than its size. Revenue rose 11% from the second quarter, "
      "ahead of the 8% the company had guided, and operating margin reached 47.5%, 13.4 percentage points higher than a "
      "year ago. Texas Instruments&rsquo; heavy investment in its own 300mm factories is now paying back: rising volumes "
      "absorb fixed costs, so most of each extra dollar of sales drops to profit. We read this as the early part of an "
      "earnings upswing, not a peak.")

C1_TITLE = "TXN: Q3 2026 results and Q4 guidance vs. consensus"
C1_SUB = "Reported Q3 2026 and Q4 2026 guidance midpoints vs. Bloomberg consensus &middot; Revenue, EPS and guidance in %, margins in percentage points"
C1_COMMENT = ("Every line beat, and the forward lines beat by more. The Q4 earnings per share guide "
              "of USD 2.62 at the midpoint is 14% above consensus and flat on Q3, in a quarter that is usually seasonally "
              "softer. Annualised, that run-rate is USD 10.5 a share, 19% above the USD 8.8 consensus for the next twelve "
              "months: we expect estimates to rise.")

BASE_CASE = ("We stay positive on Texas Instruments but would not chase the stock at USD 286; we would add on pullbacks "
             "towards the 40-week moving average, now close to USD 260. We underwrite consensus 12m-forward earnings per "
             "share moving from USD 8.8 towards USD 10 over the next two quarters, as the Q4 run-rate, analog price "
             "increases and customer restocking feed through. The debate has moved from whether the cycle has turned to how "
             "much of it the multiple already pays for. At 32.4 times forward earnings, the catalyst is upgrades, not a "
             "re-rating. The next test is the Q4 print and the 2027 capital spending plan in late January.")
UPSIDE = ("Consensus 12m-forward EPS passing the 2022 peak of USD 9.5 by the Q4 print; confirmation in January that analog "
          "price increases extend into 2027 contracts; distributor and customer inventories starting to rebuild, which "
          "management says has not yet begun.")
DOWNSIDE = ("A Q1 2027 revenue guide weaker than the usual seasonal decline, which would point to Q4 pull-ins; a 2027 capital "
            "spending plan that keeps free cash flow below the trailing USD 8.4bn; the P/E holding above 30x while "
            "earnings upgrades stall.")

P2_TITLE = "Beyond the key takeaways"
H_A1 = "Results: volume and mix now, pricing later"
A1 = [
    ("Q3 revenue of USD 6.06bn rose 28% year on year and 11% sequentially, beating the guidance midpoint of "
     "USD 5.90bn and consensus of USD 5.92bn. Analog, about 81% of sales, grew 32% to USD 4.91bn; Embedded Processing "
     "rose 21% to USD 858m. By end market, Industrial grew more than 40% to an all-time high and Data Center nearly "
     "doubled (+95%), driven by power management chips for AI servers. Automotive also set a "
     "record. Management sees demand as broad across regions and most end markets, and says customers are not yet "
     "building inventory: this is end demand, not restocking."),
    ("The margin read is the stronger signal. Gross margin reached 64.2%, 2.4 percentage points above consensus and 6.8 "
     "points above Q3 2025, as higher utilisation of the 300mm fabs spread fixed costs over more wafers. Operating margin "
     "of 47.5% was 13.4 points higher year on year, and EPS of USD 2.62 rose 77% despite a one-cent charge outside the "
     "original guidance. Operating cash flow was USD 3.42bn in the quarter and trailing free cash flow USD 8.4bn, helped "
     "by CHIPS Act incentives. Pricing played only a small part: increases started in the second half of 2026."),
]
H_A2 = "Outlook: Q4 holds flat, 2027 adds pricing"
A2 = ("Q4 guidance of USD 5.8 to 6.3bn revenue and USD 2.45 to 2.79 EPS sits 6% and 14% above consensus at the midpoints. "
      "The more important message concerns 2027. Management expects price increases across analog, power and "
      "microcontrollers to contribute more once current negotiations close, while some competitors quote lead times of up "
      "to 52 weeks on specialised parts against about six months at Texas Instruments. That gap should let the company "
      "gain share as supply tightens. Restocking has not started, which leaves a second leg of demand ahead. The quarterly "
      "dividend rises 7% to USD 1.52, and USD 5.8bn was returned to shareholders over twelve months.")

H_C2 = "Valuation: the multiple is already full"
C2_TITLE = "TXN: share price vs. consensus earnings and valuation"
C2_SUB = ("Weekly, January 2010 to 22 October 2026 &middot; Bloomberg consensus 12m-forward EPS &middot; 40-week simple MA "
          "&middot; Log scale &middot; Last price USD 285.71 on 22 October, the first session after the release")
C2_COMMENT = ("The share price has risen 67% over twelve months, ahead of a 54% increase in consensus 12m-forward EPS, so "
              "part of the rally came from the multiple. Since the July results the pattern has reversed: estimates are up "
              "13% while the price is 2% lower, taking the P/E from 37.5x to 32.4x. That is still 48% above the 21.9x "
              "average since 2010, though below the 43.1x peak of November 2024. The price sits 10% above its 40-week "
              "average. If consensus reaches the USD 10.5 Q4 run-rate, the multiple falls to 27.3x at today&rsquo;s price.")

SOURCE_LINE = ("Source: Syz Research, Bloomberg, company filings, Texas Instruments Q3 2026 earnings release of "
               "21 October 2026, analyst research notes of 22 October 2026")
