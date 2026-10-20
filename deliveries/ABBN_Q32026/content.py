"""content.py: all text for the ABB Q3 2026 Earnings update (HTML entities). Edit here only."""

DOC_TYPE = "Earnings update"
THEME = "Industrials"
DATE = "20 October 2026"
TICKER, PERIOD = "ABBN", "Q32026"

TITLE = "ABB Q3 2026: record orders, but the premium needs broader growth"

# No verbatim executive quote available from the user's files; ABB release and transcript not reachable
QUOTE, QUOTE_WHO = "", ""

TAKEAWAYS = [
    ("pos", "Beat", "Orders rose 40% to a record USD 12.1bn, 8% above consensus, led by data centres."),
    ("neg", "Miss", "Basic EPS of USD 0.65 missed consensus by about 17%, partly on a USD 115m non-cash hedge charge."),
    ("neg", "Watch", "Growth is narrow: Automation orders were flat at USD 2.1bn, 9% below consensus."),
    ("neu", "Valuation", "At 25.6x consensus earnings, 36% above the 2006 to 2026 average, the shares need upgrades."),
]

KPIS = [
    ("Orders", "USD 12.1bn", "+8% vs. consensus", "pos"),
    ("Operational EBITA", "USD 2.0bn", "+2% vs. consensus", "pos"),
    ("Basic EPS", "USD 0.65", "&minus;17% vs. consensus", "neg"),
    ("Free cash flow", "USD 1.58bn", "+29% vs. consensus", "pos"),
]

H_P1 = "The case now rests on electrification"

P1_PARAGRAPH = (
    "ABB is becoming an electrification company with an industrial tail. Electrification orders rose 70% "
    "on a comparable basis to USD 7.7bn and its order book reached a record USD 16bn, up 83% on the year, "
    "which secures growth into 2027 and 2028. Elsewhere momentum is thinner: Motion grew orders 12% "
    "but lost one percentage point of margin, and Automation orders were flat. The shares fell 5.5% on the "
    "day because investors had already paid for the strong part."
)

C1_TITLE = "ABBN: Q3 2026 results vs. consensus"
C1_SUB = ("Reported vs. pre-results consensus, % &middot; EPS vs. the midpoint of USD 0.77 to 0.79 "
          "&middot; operational EBITA and segment surprises approximate")

C1_COMMENT = (
    "The lines that point to future earnings beat; the line that prices the stock today missed. Orders and "
    "free cash flow, 29% above consensus, show strong demand and cash conversion. The USD 115m revaluation "
    "of a currency hedge linked to the Rotork acquisition is non-cash and explains about half of the EPS "
    "shortfall. The rest, and the 9% gap in Automation orders, are real."
)

BASE_CASE = (
    "We stay constructive on ABB and hold, but would not add at current levels. We "
    "underwrite full-year revenue growth in the low teens and an operational EBITA margin up at least 270 "
    "basis points, knowing that about CHF 240m of Q4 property gains flatter it. Demand "
    "is not the debate any more; breadth and conversion are: can the USD 16bn Electrification backlog lift "
    "2027 earnings while Automation and Motion lag? The catalyst would be 2027 upgrades, and "
    "consensus 2026 EPS has risen only 1% since the July results. With the shares 7% below their 40-week "
    "average, sentiment has reset. The next test is the Q4 release in early 2027."
)

UPSIDE = (
    "Q4 orders hold above USD 11bn with Electrification orders still well ahead of revenues; Automation "
    "orders return to growth as delayed large projects are booked; consensus 2027 EPS rises 5% or more "
    "before the Q4 results."
)

DOWNSIDE = (
    "Data centre customers push out deliveries despite their deposits; the Electrification margin slips "
    "below 24% as large projects ramp up; the Q4 margin is flat only thanks to property gains; weakness in "
    "the Middle East spreads to other regions."
)

P2_TITLE = "Beyond the key takeaways"

H_A1 = "Results: the beat was in orders, not earnings"

A1_PARAGRAPHS = [
    "Electrification carried the quarter. Orders rose 70% organically to USD 7.7bn, about 16% above "
    "consensus, with triple-digit growth in data centres and a 117% jump in the Americas; utilities, "
    "semiconductors and grid infrastructure also contributed. Revenues increased 21% to USD 5.4bn and "
    "operational EBITA 27% to USD 1.4bn, a 25.6% margin. On the call, management addressed the "
    "durability question directly: data centre orders are secured by large down payments and clear "
    "cancellation clauses, and each contract is tied to a specific site with permits and grid "
    "connections, which limits the risk of withdrawal. The 800-volt direct current Infinitus portfolio, "
    "with a solid-state transformer due in the second half of 2027, should support mix.",
    "The rest of the group was weaker. Motion orders grew 12% organically, but its margin fell 100 basis "
    "points to 19.1%, partly due to the newly acquired Gamesa Electric. Automation orders were flat at "
    "USD 2.1bn, with the margin up 90 basis points to 14.8%; management attributes the sequential slowdown "
    "to the timing of large projects, but the Middle East has been subdued since Q1. At group level, gross "
    "margin fell 60 basis points to 40.6% on unrealised FX and commodity derivative effects, and pricing "
    "of just over 2% only offset cost inflation. Free cash flow of USD 1.58bn cut net debt to 0.2x EBITDA.",
]

H_A2 = "Outlook: a softer Q4 and a new Japan platform"

A2_PARAGRAPH = (
    "Guidance rose less than orders. ABB expects full-year revenue growth in the "
    "low teens and an operational EBITA margin up at least 270 basis points, including about CHF 240m of "
    "Q4 property gains, so the underlying upgrade is modest. For Q4, "
    "management guides to low to mid single-digit revenue growth and a broadly stable margin. "
    "Robotics should be sold by late 2026 and Rotork closes by mid-2027. ABB will pay USD 495m for 51% of a joint venture with Mitsubishi Electric&rsquo;s "
    "low-voltage business, valued at about EUR 890m on EUR 640m of revenue: a Japanese market leader "
    "targeting a margin of at least 20% within five years."
)

H_C2 = "Valuation: the premium waits for 2027 upgrades"
C2_TITLE = "ABBN: share price vs. consensus earnings and valuation"
C2_SUB = ("Weekly, Jan 2006 to 20 Oct 2026, resampled from daily &middot; Bloomberg BEst EPS for the current "
          "fiscal year in USD (steps each January) vs. price in CHF and its 40-week MA &middot; log scales "
          "&middot; P/E vs. its 2006 to 2026 average &middot; last price is the 20 October close, after the release")

C2_COMMENT = (
    "The price has run with earnings, not ahead of them, but the multiple is still rich. The shares are up "
    "21% over 12 months and 20% this year, while consensus 2026 EPS has risen 15% since January. Since the "
    "July results, however, the price has fallen 10% and EPS has risen only 1%. The P/E of 25.6x is 36% "
    "above its 18.8x average since 2006, down from a 33.2x peak on 3 July 2026 and a one-year average of "
    "28.9x. A 10% upgrade at an unchanged price would take the "
    "multiple to 23.3x, still 24% above the average."
)

SOURCE_LINE = ("Source: Syz Research, Bloomberg, company filings, "
               "analyst research notes of 20 October 2026")
