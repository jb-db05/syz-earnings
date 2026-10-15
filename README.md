# syz-earnings

Claude skill that produces a Syz **Earnings update**: a concise post-earnings investment update on a single company, delivered as a **PDF and a portrait A4 PowerPoint with the same visual**.

- **Page 1, executive investment summary**: for every reader, including private clients. Management quote, key takeaways, one key-numbers strip, what the quarter means for the investment case, one chart, base case and implications (including our positioning), what would strengthen or change the view.
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

Sentence case, no em dashes, Nunito Bold and ExtraBold only, one Space Blue bordered box (square corners, no fill), Tiger Orange for negative indicators, sources without a full stop. Brokers and sell-side houses are never named in the deliverables: consensus and "analyst estimates" only.

## Changelog

- **15 Oct 2026**: page-2 title "Beyond the key takeaways"; positioning merged into the page-1 base case (no page-2 positioning section); no broker names; quote sourcing order with stockanalysis.com; logo taken from the project file and validated; Chart 1 trading-update variant (order-intake levels); Chart 2 end-label offsets; chart window starts at the first consensus EPS; updated word budgets and W1/W2 ranges; VAT Group Q3 2026 reference instance.
- **14 Oct 2026**: portrait A4 PowerPoint output with the same visual as the PDF.
