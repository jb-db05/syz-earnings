# TSMC Q3 2026 Earnings update (15 October 2026)

| File | Content |
|---|---|
| `Earnings_Update_TSM_Q32026.pdf` / `.pptx` | The 3-page update (PDF and portrait A4 PowerPoint) |
| `TSM_price_eps_pe.png`, `TSM_Q3_2026_revenue.png` | Standalone charts with header and footnote |
| `content.py` | All text (HTML entities) |
| `build_charts.py` | Charts from the Bloomberg export (`PARAMS` dict) |
| `build_pdf.py` | Word-budget check, PDF render, `fill.json` for the PPTX |

Rebuild (after the repo Setup steps in `SKILL.md`):
```bash
python3 build_charts.py TSM.xlsx          # Bloomberg weekly export, not in the repo
python3 build_pdf.py 70 90                # args: PPTX W1 / W2
NODE_PATH=/home/claude/node_modules node /home/claude/build_pptx.js fill.json Earnings_Update_TSM_Q32026.pptx
```
Chart 2 note: the ADR trades in USD while Bloomberg carries the EPS in TWD per ADR, so `build_charts.py` relabels the EPS axis and swaps the end-label offsets (the EPS line ends above the price).
