# syz-earnings

Claude skill that produces a Syz **Earnings update**: a concise post-earnings investment update on a single company, delivered as a **PDF and a portrait A4 PowerPoint with the same visual**.

- **Page 1, executive investment summary**: for every reader, including private clients. Management quote, key takeaways, one key-numbers strip, what the quarter means for the investment case, one chart, base case, what would strengthen or change the view.
- **Page 2, in-depth analysis**: results and drivers, outlook and guidance, the share price vs. consensus 12m-forward EPS and P/E chart, investment implications and positioning.
- **Page 3**: source line and the fixed Syz disclaimer.

## Files

| File | Role |
|---|---|
| `SKILL.md` | The skill itself (self-contained: workflow, chart kit, HTML template, text rules, QA, embedded logo) |
| `syz_charts.py` | Chart kit as a standalone module (identical to the block in `SKILL.md`) |
| `template.html` | WeasyPrint template (identical to the block in `SKILL.md`) |
| `render_test.py` | Layout calibration script: renders the PDF template with filler text at given word budgets |
| `build_pptx.js` | PowerPoint build (pptxgenjs): `node build_pptx.js fill.json out.pptx`, portrait A4, same layout as the PDF |
| `syz_gradbar.png` | Orange-to-gold gradient rule used on the slides |
| `assets/syz_logo.png` | Syz logo, 206x186 RGBA |
| `examples/` | Calibration renders in PDF and PPTX (filler text, illustrative numbers), the `fill.json` that produced them, and a sample page-2 chart |

## Input

A Bloomberg weekly export (.xlsx) with `Date`, `Last Price`, `BEst EPS`, `Moving Average (Simple, 40)` and `BEst P/E Ratio` columns, plus the results material (release, presentation, transcript). The data file is not part of this repository.

## Style rules

Sentence case, no em dashes, Nunito Bold and ExtraBold only, one Space Blue bordered box (square corners, no fill), Tiger Orange for negative indicators, sources without a full stop.
