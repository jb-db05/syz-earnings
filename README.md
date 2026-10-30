# syz-earnings

Claude skill that produces a Syz **Earnings update**: a concise post-earnings investment update on a single company, delivered as a **PDF and a portrait A4 PowerPoint with the same visual**.

- **Page 1, executive investment summary**: for every reader, including private clients. Management quote, company introduction, key takeaways, the key-numbers strip (rounded box), what the quarter means for the investment case, one chart, and a second rounded box holding the base case and implications (our view, with positioning only for Focus List names) and what would strengthen or change the view.
- **Page 2, "Beyond the key takeaways"**: results and drivers, outlook and guidance, the share price vs. consensus 12m-forward EPS and P/E chart with the valuation read.
- **Page 3**: source line and the fixed Syz disclaimer.

## Files

| File | Role |
|---|---|
| `SKILL.md` | The skill itself (self-contained: workflow, chart kit, HTML template, PPTX builder, text rules, QA) |
| `syz_charts.py` | Chart kit as a standalone module (identical to the block in `SKILL.md`) |
| `template.html` | WeasyPrint template (identical to the block in `SKILL.md`) |
| `render_test.py` | Layout calibration script: renders the PDF template with filler text at given word budgets (`python3 render_test.py P1 C1 BASE UPDOWN A1 A2 C2 W1 W2`) |
| `build_pptx.js` | PowerPoint build (pptxgenjs): `node build_pptx.js fill.json out.pptx`, portrait A4, same layout as the PDF |
| `syz_gradbar.png` | Orange-to-gold gradient rule used on the slides |
| `assets/syz_logo.png` | Syz logo, 206x186 RGBA, transparent background (copy to `/home/claude/syz_logo_hq.png` before rendering) |
| `examples/` | Calibration renders in PDF and PPTX (filler text, illustrative numbers), the `fill.json` that produced them, and a sample page-2 chart |

## Input

A Bloomberg weekly export (.xlsx) with `Date`, `Last Price`, `BEst EPS`, `Moving Average (Simple, 40)` and `BEst P/E Ratio` columns, plus the results material (release, presentation, transcript). The data file is not part of this repository.

The management quote comes, in this order, from the transcript or release the user provided, from the company's transcript on www.stockanalysis.com, or from a verbatim company statement in the release; otherwise the quote block is omitted. Quotes are never invented.

## Style rules

Sentence case, no em dashes, Nunito Bold and ExtraBold only, exactly two Space Blue bordered boxes on page 1 (key numbers, base case with the strengthen/change columns; 2.5 mm rounded corners, no fill), Tiger Orange for negative indicators, sources without a full stop. Brokers and sell-side houses are never named in the deliverables: consensus and "analyst estimates" only. No rating labels (Buy, Hold, Sell and the like) or target prices: the stance is a verb and a risk/reward, and positioning verbs (keep, add, trim) are used only for names on the Syz Equity Focus List; other names get a general view ("the case remains very constructive, risk/reward skewed to the upside"). Exactly four font sizes (17 / 11 / 8.7 / 7 pt). Every beat or miss is read together with the publication-day share price move, and any divergence is explained with confirmed drivers separated from interpretations.

## Changelog

- **30 Oct 2026**: factual mode for names we do not own (no Syz view in the base case, columns headed "What would support the case" / "What would weaken the case" through the new `UP_HEAD`/`DOWN_HEAD` template keys and optional `UPSIDE_HEAD`/`DOWNSIDE_HEAD` in `fill.json`); column cap of about 200 characters in the two-box layout; after-hours reaction rule for after-close releases; ING Group and Intel Q3 2026 reference instances.
- **28 Oct 2026 (b)**: hairline between the base case paragraph and the strengthen/change columns inside the second box (PDF template and PPTX builder); chart kit takes `eps_ccy` (EPS axis labelled in the reporting currency when it differs from the price currency) and `price_lbl` / `eps_lbl` end-label offsets; window-start guidance for names with a loss history; UBS Group Q3 2026 reference instance.
- **28 Oct 2026**: two rounded boxes on page 1: the key-numbers strip now has 2.5 mm rounded corners, and the base case and implications paragraph sits with the strengthen/change columns inside a second rounded box of the same Space Blue stroke (PDF template and PPTX builder, `roundRect` with `rectRadius` 0.1 in and 0.13 x 0.07 in padding); base case capped at about 85 words to keep the slide inside the guard line; positioning verbs reserved for Focus List names; SK hynix Q3 2026 reference instance with the cyclical adaptation of Chart 2 (loss-making weeks blanked on the log EPS axis, P/E above 40x excluded from the average); calibration examples regenerated.
- **26 Oct 2026**: company introduction (25 to 36 words) directly below the quote; mandatory surprise vs. publication-day reaction read, divergence explained with confirmed drivers separated from interpretations; no rating labels or target prices; four-size type scale (17 / 11 / 8.7 / 7 pt) in the PDF template and the PPTX builder; kicker reads "Earnings update" only (no sector, `THEME` removed); page-1 word budgets recalibrated and the PPTX text metric corrected to 0.49 em per character; calibration examples regenerated.

- **15 Oct 2026**: page-2 title "Beyond the key takeaways"; positioning merged into the page-1 base case (no page-2 positioning section); no broker names; quote sourcing order with stockanalysis.com; logo taken from the project file and validated; Chart 1 trading-update variant (order-intake levels); Chart 2 end-label offsets; chart window starts at the first consensus EPS; updated word budgets and W1/W2 ranges; VAT Group Q3 2026 reference instance.
- **14 Oct 2026**: portrait A4 PowerPoint output with the same visual as the PDF.
