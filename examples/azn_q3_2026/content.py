"""AstraZeneca Q3 2026 Earnings update: all text (HTML entities), shared by the PDF and the PPTX."""
DOC_TYPE = "Earnings update"
DATE = "30 October 2026"
TITLE = "AstraZeneca Q3 2026: a sales beat, flattered by cost timing"
QUOTE, QUOTE_WHO = "", ""   # no verbatim executive quote reachable: release blocked, no Q3 transcript indexed yet

COMPANY_INTRO = ("AstraZeneca discovers, develops and sells prescription medicines in oncology, rare disease, "
                 "cardiovascular, renal and metabolism, respiratory and vaccines. Oncology was 44% of 2025 revenue "
                 "of USD 58.7bn. Listed in London, market value about USD 270bn.")

TAKEAWAYS = [
    ("pos", "Beat", "Revenue USD 16.2bn (+2% vs. consensus), core earnings per share USD 2.79 (+8%); shares up 3.1% this morning."),
    ("neg", "Watch", "Lower research and overhead spending lifted the 9% core operating profit beat; full-year guidance unchanged."),
    ("neg", "Pipeline", "AVANZAR lung cancer readout moves to Q1 2027 from end-2026; SERENA-4 failed in breast cancer."),
    ("neu", "Valuation", "26.1x forward earnings before the release, in line with the 26.3x average since 2018."),
]

KPIS = [
    ("Revenue", "USD 16.2bn", "+1.7% vs. consensus", "pos"),
    ("Core EPS", "USD 2.79", "+7.7% vs. consensus", "pos"),
    ("Gross margin", "81.9%", "&minus;10bp vs. consensus", "neg"),
    ("FY 2026 guidance", "Unchanged", "Low double-digit core EPS", "neu"),
]

H_P1 = "Sales did the work, costs added the rest"
P1_PARAGRAPH = ("<p>Revenue beat consensus by 1.7% and core EPS by 7.7%, and the shares rose 3.1% in morning trading on "
                "30 October: surprise and reaction point the same way. Oncology and rare disease delivered the sales beat. "
                "The earnings beat goes further than sales because research and overhead spending came in below "
                "expectations, a timing effect we expect to reverse in Q4. Full-year guidance is unchanged.</p>")

C1_TITLE = "AZN: Q3 2026 surprise vs. consensus by line"
C1_SUB = ("Reported vs. pre-results consensus, % &middot; Segments rounded to the nearest percent &middot; "
          "Revenue, core operating profit and core EPS computed from USD figures")
C1_COMMENT = ("<p>Chart 1 shows sales 2% ahead of consensus and core operating profit 9% ahead. Gross margin of 81.9% "
              "was in line with consensus, so the gap sits in operating expenses. Cardiovascular, renal and metabolism "
              "(CVRM) missed by 1% on Farxiga generics and a 22% shortfall for Wainua; vaccines beat by 18% on FluMist.</p>")

BASE_CASE = ("The investment case remains constructive and the risk/reward balanced, with upside tied to the pipeline. "
             "We underwrite low double-digit core EPS growth for 2026, in line with guidance, and modest consensus "
             "upgrades after Q3. The restructuring programme targets USD 1.5bn of annual savings by 2029, all reinvested "
             "in research. At 26.1x, close to its 26.3x average since 2018, the stock needs no re-rating. The next tests are the 2027 "
             "readouts, AVANZAR first, which must cover the 2031 to 2033 patent expiries.")
UPSIDE = ("A positive AVANZAR result in first-line lung cancer in Q1 2027; laroprovstat and Farxiga combination data "
          "in 2027 backing over USD 10bn of peak sales; EPS upgrades after the February results.")
DOWNSIDE = ("A negative or mixed AVANZAR result in Q1 2027, after the SERENA-4 failure; full-year core EPS growth below the low "
            "double-digit guide once Q4 spending catches up; Soliris and Farxiga erosion outpacing new launches.")

P2_TITLE = "Beyond the key takeaways"
H_A1 = "Results: oncology and rare disease led"
A1_PARAGRAPHS = [
    ("<p>Total revenue of USD 16,209m grew 7% at constant exchange rates and came in 1.7% above the USD 15,942m "
     "consensus. Oncology reached USD 7,070m, 1% ahead, with Tagrisso at USD 2,087m beating by 4%; Lynparza, at "
     "USD 811m, missed by 5%. Among the growth assets, Enhertu rose 54% year on year and Imfinzi 24%, with Imfinzi and "
     "Imjudo still gaining. Rare disease, at USD 2,633m, beat by 2%: Ultomiris at USD 1,432m (+4% vs. consensus) and "
     "Strensiq at USD 588m (+8%) more than offset a 14% miss on Soliris, as patients move to newer therapies. "
     "Oncology now accounts for 44% of group revenue.</p>"),
    ("<p>Core operating profit of USD 5,855m beat consensus by 9.2%, a core operating margin of 36.1% against 33.6% "
     "expected, and core EPS of USD 2.79 beat by 7.7%; the shares rose 3.1% in morning trading on 30 October. "
     "Surprise and reaction are aligned. The confirmed drivers are in the reported numbers: research and overhead "
     "spending below expectations, and a gross margin of 81.9% against 82.0% expected. Higher financial expenses and "
     "tax absorbed part of the operating beat. We read most of the profit gap as phasing, because full-year guidance "
     "is unchanged; in our view the measured share price move already reflects that.</p>"),
]
H_A2 = "Outlook: guidance kept, savings go to research"
A2_PARAGRAPHS = (
    "<p>AstraZeneca reiterated its 2026 guidance: total revenue growth in the mid-to-high single digits and core EPS "
    "growth in the low double digits, both at constant exchange rates. Nine-month core EPS grew 14%, so the guide "
    "implies a slower fourth quarter, consistent with costs catching up. Analysts see the unchanged guidance as support "
    "for consensus and expect only modest upward revisions for the year. A new restructuring programme, "
    "Reshaping for Sustainable Growth, targets USD 1.5bn of annual pre-tax savings by the end of 2029, fully "
    "reinvested in research and development to accelerate new programmes. The year to date counts 12 positive Phase "
    "III readouts and first approvals for four new medicines.</p>")

H_C2 = "Valuation: priced at its long-run average"
C2_TITLE = "AZN: share price vs. consensus earnings and valuation"
C2_SUB = ("Weekly, November 2018 (first consensus EPS) to 29 October 2026 &middot; Share price in GBp with 40-week moving "
          "average &middot; Bloomberg BEst 12m-forward EPS &middot; Log scale &middot; Last price is the 29 October close, "
          "before the release")
C2_COMMENT = (
    "<p>Over 12 months the share price rose 4.7% and consensus 12m-forward EPS 8.8%, so earnings ran ahead of the "
    "price. The shares closed at 13,052p on 29 October, 16% below the February 2026 peak of 15,542p and 2.8% under the "
    "40-week moving average of 13,428p; the 3.1% gain this morning takes the price just above that average. The "
    "12m-forward P/E of 26.1x sits 0.9% below its 26.3x average since 2018, against a peak of 31.0x in January 2021."
    " At about 26.9x after this morning&rsquo;s move, EPS upgrades of 2% would bring "
    "the multiple back to the average.</p>")

SOURCE_LINE = ("Source: Syz Research, Bloomberg, company filings, AstraZeneca 9M and Q3 2026 results of 30 October 2026, "
               "analyst research notes of 30 October 2026")
W1, W2 = 74, 94
