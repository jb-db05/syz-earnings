"""content.py: all text for the Sandoz Q3 2026 earnings update (HTML entities; fill.json is derived from it)."""

DOC_TYPE = "Earnings update"
DATE = "28 October 2026"
TITLE = "Sandoz Q3 2026: margins up, sales miss at a full valuation"

# No verbatim executive quote in the material provided and no transcript reachable: quote block omitted.
QUOTE = ""
QUOTE_WHO = ""

COMPANY_INTRO = ("Sandoz, spun off from Novartis in October 2023, sells generic medicines and biosimilars, copies of "
                 "biologic drugs. Biosimilars are 34% of sales and Europe 53%. Nine-month 2026 sales USD 8.7bn; "
                 "SIX-listed, market value around CHF 34bn.")

TAKEAWAYS = [
    ("neg", "Miss", "Q3 sales of USD 2.94bn grew 5% at constant currencies, 1.8% below consensus."),
    ("neg", "Reaction", "Shares fell 4.0% on 28 October from a record close, after a 42% gain this year."),
    ("pos", "Raised", "Core EBITDA margin guide raised to 23.0&ndash;23.5% from about 22.7%; sales growth narrowed to 5&ndash;6%."),
    ("neu", "Valuation", "23.3x forward earnings, 38% above the average since the 2023 listing, after a 23% rise since August."),
]

KPIS = [
    ("Net sales", "USD 2.94bn", "&minus;1.8% vs. consensus", "neg"),
    ("Biosimilars", "USD 998m", "&minus;2% vs. consensus", "neg"),
    ("2026 sales growth guide", "5&ndash;6% CC", "Narrowed, lower end", "neg"),
    ("2026 core EBITDA margin", "23.0&ndash;23.5%", "+55bp vs. prior guide", "pos"),
]

H_P1 = "A margin upgrade meets a full valuation"
P1_PARAGRAPH = ("Q3 sales missed consensus by 1.8%, Sandoz narrowed its 2026 growth guide to the low end of its "
                "range, and the shares fell 4.0% on 28 October. The fall is large for the size of the miss, "
                "since the higher margin guide points to earnings estimates 1% to 3% higher. The stock entered the "
                "release at a record 24.3x forward earnings.")

C1_TITLE = "SDZ: Q3 2026 sales growth by business and region"
C1_SUB = ("Net sales growth at constant currencies, % &middot; group ex B2B excludes the anti-infective active "
          "ingredient headwind &middot; company figures")
C1_COMMENT = ("Biosimilars grew 17% and now make up 34% of sales, carried by Wyost and Jubbonti in North America, "
              "where sales rose 20%. Generics were flat, held back by lower penicillin ingredient prices; excluding "
              "that B2B headwind, group growth was 7%. Europe grew 1%, slowed by biosimilar supply tightness and a "
              "difficult German market.")

BASE_CASE = ("We stay positive on Sandoz and keep the position. We underwrite consensus forward EPS of USD 4.08, 27% "
             "above a year ago, carried by the biosimilar mix and the higher margin guide. The debate has moved from "
             "growth to supply: biosimilar capacity stays tight until 2027 and the German market is unsettled. At "
             "23.3x, the valuation leaves little room for further sales misses, and we expect the shares to follow "
             "earnings upgrades from here. The next test is the full-year results in March 2027, with the first "
             "2027 guidance.")

UPSIDE = ("Biosimilar supply restored ahead of the 2027 target, with European growth back above 5%; the "
          "anti-infective headwind gone in Q4 as guided; a 2027 core EBITDA margin guide above 24%, helped by "
          "generic semaglutide launches.")
DOWNSIDE = ("Q4 sales growth below 4% at constant currencies, leaving 2026 under the new 5% floor; supply "
            "limits lasting into the second half of 2027; further German price cuts or tender losses that keep "
            "European growth near zero.")

P2_TITLE = "Beyond the key takeaways"
H_A1 = "Results: biosimilars grew, generics stalled"
A1_PARAGRAPHS = [
    ("Net sales rose 4% in dollars and 5% at constant currencies to USD 2.94bn. Biosimilars grew 17% at constant "
     "currencies to USD 998m, supported by Wyost and Jubbonti in the US, with shares of 56% and 49% of their "
     "biosimilar markets, and by the European launch of Afqlir, at 73% share across 22 markets. Generics were flat at "
     "USD 1.94bn: lower prices for penicillin active ingredients, after Chinese suppliers cut prices following US "
     "tariffs, weighed on the anti-infective B2B business. Excluding that effect, generics grew 2% and the group 7%. "
     "Over nine months, sales rose 5% to USD 8.70bn, with volumes up 10% and prices down 5%."),
    ("Sales were 1.8% below consensus, with biosimilars 2% short and generics 1.8% short, and the shares fell 4.0% "
     "on 28 October. The move is large for a sales miss of this size combined with a higher margin guide, so "
     "surprise and reaction diverge in degree. The confirmed drivers are the narrowed sales guide, now at the lower "
     "end of the earlier range, and the shortfall in European biosimilar supply. We think positioning explains the "
     "rest: the shares closed at a record CHF 82.36 two days before the release, up 23% since the H1 results, on "
     "24.5x forward earnings."),
]
H_A2 = "Outlook: margin guide up, sales range narrowed"
A2_PARAGRAPHS = [
    ("Sandoz now expects 2026 sales growth of 5% to 6% at constant currencies, against mid-to-high single digits "
     "before, and a core EBITDA margin of 23.0% to 23.5%, against an earlier target of about 22.7% and 21.7% in "
     "2025. With a first-half margin of 20.9%, the new range implies a second-half margin of about 25% on our "
     "estimates. Management expects the anti-infective headwind to become immaterial from Q4 and the biosimilar "
     "supply constraints to ease by 2027 as partners add capacity. Generic semaglutide shipped to Brazil and won "
     "approval in Canada; it adds nothing material in 2026 and becomes a growth driver in 2027."),
]
H_C2 = "Valuation: the multiple ran ahead of earnings"
C2_TITLE = "SDZ: share price vs. consensus earnings and valuation"
C2_SUB = ("SDZ SW Equity, daily data resampled to weekly, from October 2023 &middot; BEst 12m-forward consensus, EPS "
          "converted to CHF as price divided by P/E &middot; 40-week simple MA &middot; log scale &middot; P/E shaded "
          "above (orange) / below (blue) its average since October 2023 &middot; last price as of 28 October, the "
          "release day")
C2_COMMENT = ("Over 12 months the share price rose 58% while consensus forward EPS rose 27% in dollars, so most of "
              "the gain came from the multiple. Since the H1 results on 5 August the price is up 23% and EPS in "
              "francs 4%, taking the forward P/E from 19.8x to a record 24.5x on 26 October. It now "
              "stands at 23.3x, 38% above the 16.9x average since the 2023 listing and above the 21.0x "
              "one-year average. The price is 17% above its 40-week average of CHF 67.5. A 10% upgrade at "
              "today&rsquo;s price would bring the multiple to 21.2x.")

SOURCE_LINE = ("Source: Syz Research, Bloomberg, company filings, Sandoz results release of 28 October 2026, "
               "Finanz und Wirtschaft and AWP of 28 October 2026, analyst research notes of 16 and 28 October 2026")

W1, W2 = 78, 94            # PDF chart widths, % of text width
W1_PPTX, W2_PPTX = 70, 88  # PPTX chart widths
