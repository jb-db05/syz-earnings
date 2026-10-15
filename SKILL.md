---
name: "syz-earnings"
description: "Produce Syz post-earnings investment updates (Earnings update as PDF and portrait A4 PowerPoint with the same visual: page 1 executive investment summary for all clients, page 2 in-depth analysis with the share price vs. consensus EPS and P/E chart, page 3 disclaimer) from a Bloomberg weekly export. Use for any 'Syz Earnings' request or post-results company update; keep using syz-visual for 'Syz Visual' macro Research Comments."
---

# Syz Earnings: post-earnings investment update

Produce a concise, institutional-quality **Earnings update** on a single company after its results: **page 1 tells investors what they need to know, page 2 helps them understand why**, page 3 carries the source line and the fixed disclaimer. Same page geometry, typography, chart kit and voice as the Syz Research Comment format (`syz-visual`), adapted to a post-results use case.

Where this skill and `syz-house-style` or `syz-visual` differ, **this skill wins**. Apply silently; do not describe the style back to the user.

## Deliverables (every time)
1. `Earnings_Update_<Ticker>_<QxYYYY>.pdf`: 3-page A4 (page 1 executive investment summary, page 2 in-depth analysis, page 3 source + disclaimer).
2. `Earnings_Update_<Ticker>_<QxYYYY>.pptx`: the same three pages as a **portrait A4 PowerPoint** (21 x 29.7 cm), same margins, type sizes, colours and charts, with native editable text and shapes.
3. The standalone chart PNGs **with** their header/footnote (for decks and LinkedIn): at least the price vs. consensus EPS and P/E chart.
4. The build scripts (data → charts → PDF, and `fill.json` → PPTX), parameterised for the next quarter.

## Inputs
- **Bloomberg weekly export (.xlsx)**, one sheet, newest row first, header row 1, columns matched by keyword (order does not matter):
  `Date | <Ticker> - Last Price (R1) | <Ticker> - BEst EPS (L1) | Moving Average(Simple,40,0) (<Ticker>) | <Ticker> - BEst P/E Ratio`.
  Reference file: `ASML.xlsx` (877 weekly rows, Jan 2010 to 14 Oct 2026). Trailing empty rows are dropped. `load_bloomberg_sheet()` below reads it.
- **Results material** the user supplies or points to: press release, presentation, transcript, consensus table. Web-sourced facts (consensus, guidance, quotes) are dated in the text and flagged for a Bloomberg check in the reply.
- **A management quote**: only from the transcript or press release the user provided or that was verifiably published. Never invent or paraphrase a quote into quotation marks; if no usable quote exists, drop the quote block (set `QUOTE_BLOCK` to an empty string).

## Workflow
1. **Data first, silently.** Load the Bloomberg sheet; note the window, the last date, the last price, 12m-forward EPS, 40-week MA and P/E; compute the P/E average since the start of the window and the premium/discount to it; check whether the price sits above its 40-week MA. From the results material, build the KPI table (reported vs. consensus, guidance vs. consensus). Compute every number you will quote. Never invent or extrapolate.
2. **Pick the charts.** Chart 2 (page 2) is fixed: `price_eps_pe_chart`. Chart 1 (page 1) is one impactful results chart, by default `bar_chart` of surprises vs. consensus (reported lines + guidance). Another archetype is allowed only if it carries the page-1 message better (see Chart archetypes).
3. **Setup** (fonts, logo, WeasyPrint), write `syz_charts.py` (below) verbatim and build the charts.
4. **Crop** each chart for the PDF (`crop_for_pdf`): the PDF typesets titles in HTML, so the chart's own header/footnote is removed.
5. **Write the text** following the Text format rules: page 1 first (the 80% message), then page 2 (the why), with no repetition between them.
6. **Fill the HTML template** (below), render with WeasyPrint, rasterise all pages and **look at them**.
7. **Fit to exactly 3 pages** (Fit & QA).
8. **Build the PowerPoint** from the same content: write `fill.json` (plain text, no HTML entities) and run `build_pptx.js` (below); validate, render with LibreOffice and look at the three slides. Then deliver PDF + PPTX + PNGs + scripts.

## Setup
```bash
pip install weasyprint pdf2image --break-system-packages -q
mkdir -p /home/claude/fonts && cd /home/claude/fonts
curl -sL -o Nunito.ttf "https://raw.githubusercontent.com/google/fonts/main/ofl/nunito/Nunito%5Bwght%5D.ttf"
python3 -c "
from fontTools.varLib.instancer import instantiateVariableFont
from fontTools.ttLib import TTFont
for w,n in [(300,'Light'),(400,'Regular'),(600,'SemiBold'),(700,'Bold'),(800,'ExtraBold')]:
    f=TTFont('Nunito.ttf'); instantiateVariableFont(f,{'wght':w},inplace=True); f.save(f'Nunito-{n}.ttf')
"
```
Also install the fonts for LibreOffice (used to render the PPTX for QA) and build the gradient rule image used on the slides:
```bash
mkdir -p ~/.local/share/fonts && cp /home/claude/fonts/Nunito-*.ttf ~/.local/share/fonts/ && fc-cache -f
python3 -c "
from PIL import Image; import numpy as np
w=1200; a=np.zeros((4,w,3),dtype=np.uint8); c0=np.array([255,108,14]); c1=np.array([255,197,69])
for i in range(w): a[:,i,:]=c0+(c1-c0)*i/(w-1)
Image.fromarray(a).save('/home/claude/syz_gradbar.png')"
```
Fallback for fonts if GitHub is blocked: `npm install @fontsource/nunito`, convert the woff files to ttf with fontTools (`f.flavor=None; f.save()`). Never ship without Nunito. The font is **Nunito** (rounded terminals), not Nunito Sans. Only **Bold (700)** and **ExtraBold (800)** are used in the document and the charts.

**Logo.** The Syz logo (206x186 RGBA, transparent background, orange gradient) is embedded here so it never has to be located. Write it to `/home/claude/syz_logo_hq.png` before rendering; never use a logo with a white box.
```python
import base64
LOGO_B64 = "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"
open("/home/claude/syz_logo_hq.png", "wb").write(base64.b64decode(LOGO_B64))
```

## Chart kit: write to `/home/claude/syz_charts.py` verbatim
```python
"""syz_charts.py: Syz earnings chart kit (white-background report charts, Research Comment format)."""
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import matplotlib.dates as mdates
import matplotlib.ticker as mticker
from matplotlib.colors import LinearSegmentedColormap
from PIL import Image

FONT_DIR = "/home/claude/fonts"
ORANGE, AMBER, GOLD = "#FF6C0E", "#FFA400", "#FFC545"
NAVY, BLUEB = "#202945", "#4B5F80"
MINT, TEAL, SKY, PEACH, MULB = "#3BAF90", "#9DD9D2", "#79D6FF", "#E6A4AD", "#AC5D85"
GREY, AXIS_TXT, SPINE, GRID = "#8A8F98", "#5A5F68", "#D6D9DE", "#EDEFF2"
SYZ_GRAD = LinearSegmentedColormap.from_list("syz", [ORANGE, GOLD])
DASH = (0, (5, 4))


def setup_fonts():
    for w in ["Light", "Regular", "SemiBold", "Bold", "ExtraBold"]:
        fm.fontManager.addfont(f"{FONT_DIR}/Nunito-{w}.ttf")
    plt.rcParams["font.family"] = "Nunito"
    plt.rcParams["font.weight"] = "bold"          # Nunito Bold everywhere; ExtraBold for titles
    plt.rcParams["axes.titleweight"] = "bold"


def style_ax(ax, grid_axis="y"):
    ax.set_facecolor("white")
    ax.spines[["top", "right"]].set_visible(False)
    ax.spines[["left", "bottom"]].set_color(SPINE)
    ax.tick_params(colors=AXIS_TXT, labelsize=9.5, length=3)
    ax.grid(axis=grid_axis, color=GRID, linewidth=0.8, zorder=0)


def header(fig, title, subtitle, footnote, title_y=0.945, sub_y=0.906, bar_y=0.886, foot_y=0.032, rule=True):
    """Standalone-PNG header: navy title, optional grey subtitle + orange->gold rule, grey source footnote."""
    fig.patch.set_facecolor("white")
    fig.text(0.07, title_y, title, fontsize=16.5, fontweight="extra bold", color=NAVY, ha="left")
    if subtitle:
        fig.text(0.07, sub_y, subtitle, fontsize=10.5, color=AXIS_TXT, ha="left")
    if rule:
        bar = fig.add_axes([0.07, bar_y, 0.89, 0.006])
        bar.imshow(np.linspace(0, 1, 256).reshape(1, -1), aspect="auto", cmap=SYZ_GRAD)
        bar.set_axis_off()
    fig.text(0.07, foot_y, footnote, fontsize=8, color=GREY, ha="left", fontweight="normal")


def source_line(provider, asof, *notes):
    """No full stop at the end, ever."""
    return " · ".join([f"Source: Syz Research, {provider}", f"As of {asof}", *[n for n in notes if n]])


def legend(ax, loc="upper left", ncol=1):
    leg = ax.legend(loc=loc, frameon=False, fontsize=10.5, ncol=ncol, handlelength=2.2)
    for t in leg.get_texts():
        t.set_color(NAVY); t.set_fontweight("bold")
    return leg


def _fmt_thousands(v, _):
    return f"{v:,.0f}"


def _log_ticks(ax, lo, hi, subs=(1, 2, 5)):
    """1-2-5 ladder on a log axis, clipped to the data range (e.g. 1, 2, 5, 10, 20, 50)."""
    ticks = [m * 10 ** e for e in range(int(np.floor(np.log10(lo))) - 1, int(np.ceil(np.log10(hi))) + 2)
             for m in subs]
    ticks = [t for t in ticks if lo * 0.9 <= t <= hi * 1.35]
    ax.set_yticks(ticks); ax.set_yticks([], minor=True)
    ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda v, _: f"{v:,.0f}" if v >= 1 else f"{v:g}"))


# ---------------------------------------------------------------- data loader (Bloomberg weekly export)
def load_bloomberg_sheet(path, sheet=0):
    """Bloomberg export, one row per week, newest first, header row 1:
    Date | <Ticker> - Last Price (R1) | <Ticker> - BEst EPS (L1) | Moving Average(Simple,40,0) | <Ticker> - BEst P/E Ratio
    Column order is matched by keyword, not position. Returns a DataFrame sorted oldest -> newest."""
    df = pd.read_excel(path, sheet_name=sheet)
    df = df.dropna(how="all")
    cols = {c: c.lower() for c in df.columns}
    pick = lambda *keys: next(c for c, l in cols.items() if all(k in l for k in keys))
    out = pd.DataFrame({
        "date": pd.to_datetime(df[pick("date")]),
        "price": pd.to_numeric(df[pick("last price")], errors="coerce"),
        "eps": pd.to_numeric(df[pick("best eps")], errors="coerce"),
        "ma40": pd.to_numeric(df[pick("moving average")], errors="coerce"),
        "pe": pd.to_numeric(df[pick("best p/e")], errors="coerce"),
    }).dropna(subset=["date"]).sort_values("date").reset_index(drop=True)
    return out


# ---------------------------------------------------------------- archetype: price vs. consensus EPS + P/E panel
def price_eps_pe_chart(path, df, name, title, footnote, ccy="EUR", pe_avg_from=None,
                       p1_title=None, p2_title=None):
    """Reference earnings chart. Top: share price (Blueberry, rhs, log) + 40-week MA (dashed) + 12m-forward
    EPS (Orange, lhs, log). Bottom: 12m-forward P/E (Orange) vs. its long-run average (dashed navy), shaded
    orange above / blue-grey below. df from load_bloomberg_sheet(). Returns the numbers quoted in the labels."""
    x = mdates.date2num(df["date"])
    p1_title = p1_title or f"Share price and consensus 12m-forward EPS (log scale)"
    p2_title = p2_title or "12m-forward P/E"
    start_year, end_year = df["date"].iloc[0].year, df["date"].iloc[-1].year
    pe_series = df["pe"] if pe_avg_from is None else df.loc[df["date"] >= pe_avg_from, "pe"]
    pe_avg = float(pe_series.mean())

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12.5, 8.6), dpi=200, sharex=True,
                                   gridspec_kw={"height_ratios": [2.45, 1], "hspace": 0.16})
    fig.subplots_adjust(top=0.875, bottom=0.085, left=0.075, right=0.925)

    # --- top panel: EPS on the left axis, price + MA on a twin right axis, both log
    style_ax(ax1)
    ax1.set_yscale("log")
    ax1.plot(x, df["eps"], color=ORANGE, linewidth=2.1, zorder=3, label=f"12m-forward EPS, {ccy} (lhs)")
    ax1.set_ylabel(f"12m-forward EPS ({ccy}, log scale)", fontsize=10, color=ORANGE, fontweight="bold")
    ax1.tick_params(axis="y", colors=ORANGE)
    _log_ticks(ax1, float(df["eps"].min()), float(df["eps"].max()))
    ax1.set_title(p1_title, fontsize=12, fontweight="bold", color=NAVY, loc="left", pad=8)

    axr = ax1.twinx()
    axr.set_yscale("log")
    axr.spines[["top"]].set_visible(False)
    axr.spines[["right", "left", "bottom"]].set_color(SPINE)
    axr.plot(x, df["price"], color=BLUEB, linewidth=1.9, zorder=4, label=f"Share price, {ccy} (rhs)")
    axr.plot(x, df["ma40"], color=BLUEB, linewidth=1.3, linestyle=DASH, zorder=3, label="40-week moving average (rhs)")
    axr.set_ylabel(f"Share price ({ccy}, log scale)", fontsize=10, color=AXIS_TXT, fontweight="bold")
    axr.tick_params(axis="y", colors=AXIS_TXT, labelsize=9.5, length=3)
    _log_ticks(axr, float(df["price"].min()), float(df["price"].max()), subs=(1, 2.5, 5))
    ax1.set_zorder(axr.get_zorder() + 1); ax1.patch.set_visible(False)

    # end labels
    last_p, last_e = float(df["price"].iloc[-1]), float(df["eps"].iloc[-1])
    axr.plot(x[-1], last_p, "o", color=BLUEB, ms=5, zorder=5)
    axr.annotate(f"{last_p:,.0f}", (x[-1], last_p), xytext=(10, 6), textcoords="offset points",
                 color=BLUEB, fontsize=10.5, fontweight="bold")
    ax1.plot(x[-1], last_e, "o", color=ORANGE, ms=5, zorder=5)
    ax1.annotate(f"{last_e:,.1f}", (x[-1], last_e), xytext=(10, -14), textcoords="offset points",
                 color=ORANGE, fontsize=10.5, fontweight="bold")

    # one legend combining both axes
    h1, l1 = axr.get_legend_handles_labels(); h2, l2 = ax1.get_legend_handles_labels()
    leg = ax1.legend(h1 + h2, l1 + l2, loc="upper left", frameon=False, fontsize=10.5, handlelength=2.4)
    for t in leg.get_texts():
        t.set_color(NAVY); t.set_fontweight("bold")

    # --- bottom panel: P/E vs. average
    style_ax(ax2)
    pe = df["pe"].to_numpy(float)
    ax2.plot(x, pe, color=ORANGE, linewidth=1.9, zorder=3, label="12m-forward P/E")
    ax2.axhline(pe_avg, color=NAVY, linestyle=DASH, linewidth=1.3, zorder=2,
                label=f"Average since {pe_series.index.map(lambda i: df['date'][i]).min().year}: {pe_avg:.1f}x")
    ax2.fill_between(x, pe, pe_avg, where=pe >= pe_avg, interpolate=True, color=ORANGE, alpha=0.12, zorder=1)
    ax2.fill_between(x, pe, pe_avg, where=pe < pe_avg, interpolate=True, color=BLUEB, alpha=0.14, zorder=1)
    ax2.yaxis.set_major_formatter(mticker.FuncFormatter(lambda v, _: f"{v:.0f}x"))
    ax2.set_title(p2_title, fontsize=12, fontweight="bold", color=NAVY, loc="left", pad=8)
    ax2.plot(x[-1], pe[-1], "o", color=ORANGE, ms=5, zorder=4)
    ax2.annotate(f"{pe[-1]:.1f}x", (x[-1], pe[-1]), xytext=(10, -4), textcoords="offset points",
                 color=ORANGE, fontsize=10.5, fontweight="bold")
    legend(ax2, loc="upper left", ncol=2)

    ax2.xaxis.set_major_locator(mdates.YearLocator(1))
    ax2.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))
    ax2.set_xlim(x[0] - 30, x[-1] + 330)

    header(fig, title, None, footnote, title_y=0.955, foot_y=0.028, rule=False)
    fig.savefig(path, dpi=200, facecolor="white"); plt.close(fig)
    return {"price": last_p, "eps": last_e, "pe": float(pe[-1]), "pe_avg": pe_avg,
            "pe_premium_pct": (float(pe[-1]) / pe_avg - 1) * 100,
            "above_ma": last_p > float(df["ma40"].iloc[-1]), "ma40": float(df["ma40"].iloc[-1])}


# ---------------------------------------------------------------- generic single-series bar (KPI vs. consensus etc.)
def bar_chart(path, labels, values, title, subtitle, footnote, colors=None, fmt="{:+.1f}%", ylabel="",
              zero_line=True, highlight_negative=True):
    """Simple bar archetype for page 1 (e.g. beat/miss by line, revisions by segment). Positive = Blueberry,
    negative = Tiger Orange (bearish tag colour), unless colors is given."""
    vals = np.asarray(values, float)
    if colors is None:
        colors = [ORANGE if (highlight_negative and v < 0) else BLUEB for v in vals]
    fig, ax = plt.subplots(figsize=(12.5, 5.0), dpi=200)
    fig.subplots_adjust(top=0.80, bottom=0.16, left=0.07, right=0.96)
    style_ax(ax)
    ax.tick_params(labelsize=12)
    bars = ax.bar(range(len(vals)), vals, color=colors, width=0.62, linewidth=0, zorder=3)
    if zero_line:
        ax.axhline(0, color=NAVY, linewidth=1.0, zorder=2)
    for b, v in zip(bars, vals):
        ax.annotate(fmt.format(v), (b.get_x() + b.get_width() / 2, v),
                    xytext=(0, 5 if v >= 0 else -13), textcoords="offset points",
                    ha="center", fontsize=13, fontweight="bold", color=NAVY)
    ax.set_xticks(range(len(vals))); ax.set_xticklabels(labels, fontsize=12.5, color=NAVY, fontweight="bold")
    ax.set_ylabel(ylabel, fontsize=11.5, color=AXIS_TXT, fontweight="bold")
    header(fig, title, subtitle, footnote)
    fig.savefig(path, dpi=200, facecolor="white"); plt.close(fig)


# ---------------------------------------------------------------- PDF embedding
CROPS = {"price_eps_pe": (0.085, 0.045), "bar": (0.165, 0.055)}


def crop_for_pdf(src, dst, kind):
    """Strip the standalone header/footnote: in the PDF, titles are typeset in HTML."""
    top, bot = CROPS[kind]
    im = Image.open(src); w, h = im.size
    im.crop((0, int(h * top), w, int(h * (1 - bot)))).save(dst)
```

### Chart archetypes and rules
| Archetype | Use for | Fixed geometry |
|---|---|---|
| `price_eps_pe_chart` | **Chart 2, always**: share price (Blueberry, rhs, log) with 40-week MA (dashed) and 12m-forward consensus EPS (Orange, lhs, log); 12m-forward P/E vs. its average since the start of the window, shaded orange above / blue-grey below | 12.5x8.6 in, 200 dpi |
| `bar_chart` | **Chart 1, default**: surprise vs. consensus by line (revenue, gross margin, EBIT, EPS, next-quarter guide, FY outlook); or revisions by segment; positive bars Blueberry, negative bars Tiger Orange | 12.5x5.0 in |

- **Colour convention:** reference series Blueberry Blue `#4B5F80`; emphasis series Tiger Orange `#FF6C0E`. Dashed lines navy `(0,(5,4))`. **Negative or bearish = Tiger Orange**, never purple. P/E shading: above average orange α 0.12, below average Blueberry α 0.14.
- **Log axes** use the 1-2-5 ladder (1, 2, 5, 10, 20, 50 for EPS; 25, 50, 100, 250, 500, 1,000 for price), thousands separators, no minor ticks.
- **Standalone title** = `<Ticker>: <descriptor>` with a colon, sentence case, e.g. "ASML: share price vs. consensus earnings and valuation". No em dashes anywhere. **Footnote** = `source_line(provider, "<D Mon YYYY>", notes…)`, naming the series, the MA, the log scale and the shading rule; **no full stop at the end**.
- **Typography in charts:** Nunito Bold for everything, ExtraBold for the figure title (set by `setup_fonts` and `header`).
- **Other chart types** (a stacked contribution bar, a revisions line) are allowed only if built with `style_ax` + `header` + `source_line`, 12.5 in wide, 200 dpi, margins `left=0.07, right=0.96`; add a crop preset in `CROPS` and check the crop visually.

## HTML template: fill every `{{…}}`, change nothing else
```html
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
@font-face { font-family: 'Nunito'; src: url('file:///home/claude/fonts/Nunito-Bold.ttf'); font-weight: 700; }
@font-face { font-family: 'Nunito'; src: url('file:///home/claude/fonts/Nunito-ExtraBold.ttf'); font-weight: 800; }

@page {
  size: A4;
  margin: 18mm 15mm 12.5mm 15mm;
  @top-right { content: url('file:///home/claude/syz_logo_hq.png'); image-resolution: 370dpi; vertical-align: bottom; padding-top: 9mm; }
  @bottom-left {
    content: "Syz Research \0000b7\0000a0{{DOC_TYPE}} \0000b7\0000a0{{DATE}}";
    font-family: 'Nunito'; font-weight: 700; font-size: 7pt; color: #9AA0A8;
  }
  @bottom-right {
    content: counter(page) " / " counter(pages);
    font-family: 'Nunito'; font-weight: 700; font-size: 7pt; color: #9AA0A8;
  }
}

* { margin: 0; padding: 0; box-sizing: border-box; }
body { font-family: 'Nunito'; font-weight: 700; color: #202945; font-size: 8.7pt; line-height: 1.42; }

.gradbar { height: 3.5px; background: linear-gradient(90deg, #FF6C0E 0%, #FFC545 100%); margin-bottom: 4mm; }

.kicker { font-size: 8pt; font-weight: 800; letter-spacing: 1.2px; color: #FF6C0E; margin-bottom: 1.5mm; }
h1 { font-size: 17pt; font-weight: 800; color: #202945; line-height: 1.22; margin-bottom: 1.5mm; }
.dateline { font-size: 8.5pt; color: #6B7280; margin-bottom: 3.2mm; }

/* Management quote: orange left rule, no fill */
.quote { border-left: 1.2mm solid #FF6C0E; padding: 1mm 0 1mm 4mm; margin: 0 0 3.2mm 0; }
.quote p { font-size: 9.8pt; font-weight: 800; color: #202945; line-height: 1.35; text-align: left; margin-bottom: 1mm; }
.quote .who { font-size: 7.6pt; color: #6B7280; font-weight: 700; }

/* Section heading */
.sec { break-inside: avoid; break-after: avoid; margin-top: 3.2mm; }
.sec.first { margin-top: 0; }
h2 { font-size: 11pt; font-weight: 800; color: #202945; line-height: 1.2; margin-bottom: 1.4mm; }

p { margin-bottom: 2.2mm; text-align: justify; }

/* Key numbers: the only boxed element on page 1. One Space Blue border, straight corners, no fill,
   four columns separated by hairlines */
table.kpi { width: 100%; border-collapse: collapse; border: 0.45mm solid #202945; margin: 0 0 3.2mm 0; break-inside: avoid; }
table.kpi td { width: 25%; padding: 2.2mm 3mm; vertical-align: top; border-left: 0.2mm solid #D6D9DE; }
table.kpi td:first-child { border-left: none; }
.kpi .lbl { font-size: 7.2pt; color: #6B7280; margin-bottom: 0.6mm; }
.kpi .val { font-size: 13pt; font-weight: 800; color: #202945; line-height: 1.1; }
.kpi .sub { font-size: 7.2pt; margin-top: 0.8mm; color: #4B5F80; }
.kpi .sub.pos { color: #3BAF90; }
.kpi .sub.neg { color: #FF6C0E; }

/* Key takeaways: tagged lines, no box */
ul.takeaways { list-style: none; margin-bottom: 1.2mm; }
ul.takeaways li { display: flex; align-items: baseline; margin-bottom: 1.3mm; }
.tag { flex: 0 0 auto; width: 16mm; font-size: 7pt; font-weight: 800; letter-spacing: 0.8px; }
.tag.pos { color: #3BAF90; }
.tag.neg { color: #FF6C0E; }
.tag.neu { color: #4B5F80; }
ul.takeaways li span.t { flex: 1 1 auto; text-align: left; }

/* Strengthen / change: two text columns with a hairline divider, no boxes */
table.duo { break-inside: avoid; width: 100%; border-collapse: collapse; margin-top: 1mm; }
table.duo td { width: 50%; padding: 0 5mm 0 0; vertical-align: top; }
table.duo td + td { border-left: 0.2mm solid #D6D9DE; padding: 0 0 0 5mm; }
table.duo .head { font-size: 7.8pt; font-weight: 800; letter-spacing: 1px; color: #FF6C0E; margin-bottom: 1.2mm; }
table.duo p { margin-bottom: 0; text-align: left; }

.chart-title { font-size: 9.5pt; font-weight: 800; color: #202945; margin: 1.5mm 0 1.5mm 0; }
.chart-sub { font-size: 7.2pt; color: #6B7280; margin: -1mm 0 1.2mm 0; }
.chart-title .num { color: #FF6C0E; }
img.chart { width: {{W1}}%; display: block; margin: 0 auto 1.2mm auto; }
img.c2 { width: {{W2}}%; }

/* Page 3: source + disclaimer, pinned to the bottom of the page */
.legal { font-size: 6.8pt; color: #9AA0A8; line-height: 1.4; position: absolute; bottom: 0; left: 0; right: 0; }
.legal .syz { color: #FF6C0E; font-weight: 800; }
.legal .src-line { margin-bottom: 4mm; }
.legal .disc-head { color: #FF6C0E; font-weight: 800; letter-spacing: 1.2px; margin-bottom: 1.5mm; }
.legal p { font-size: 6.8pt; margin-bottom: 1.6mm; text-align: justify; }

.pagebreak { page-break-before: always; }
</style>
</head>
<body>

<!-- PAGE 1: executive investment summary -->
<div class="gradbar"></div>
<div class="kicker">{{DOC_TYPE}} &middot; {{THEME}}</div>
<h1>{{TITLE}}</h1>
<div class="dateline">{{DATE}} &middot; Syz Research</div>

{{QUOTE_BLOCK}}

<div class="sec first"><h2>Key takeaways</h2></div>
<ul class="takeaways">
{{TAKEAWAYS}}
</ul>

<table class="kpi"><tr>
{{KPI_TILES}}
</tr></table>

<div class="sec"><h2>{{H_P1}}</h2></div>
{{P1_PARAGRAPH}}

<div class="chart-title"><span class="num">Chart 1</span> &middot; {{C1_TITLE}}</div>
<div class="chart-sub">{{C1_SUB}}</div>
<img class="chart" src="file://{{C1_IMG}}">
{{C1_COMMENT}}

<div class="sec"><h2>Base case and implications</h2></div>
<p>{{BASE_CASE}}</p>

<table class="duo"><tr>
  <td><div class="head">What would strengthen our view</div><p>{{UPSIDE}}</p></td>
  <td><div class="head">What would change our view</div><p>{{DOWNSIDE}}</p></td>
</tr></table>

<!-- PAGE 2: in-depth analysis -->
<div class="pagebreak"></div>
<div class="gradbar"></div>

<div class="sec first"><h2>{{H_A1}}</h2></div>
{{A1_PARAGRAPHS}}

<div class="sec"><h2>{{H_A2}}</h2></div>
{{A2_PARAGRAPHS}}

<div class="sec"><h2>{{H_C2}}</h2></div>
<div class="chart-title"><span class="num">Chart 2</span> &middot; {{C2_TITLE}}</div>
<div class="chart-sub">{{C2_SUB}}</div>
<img class="chart c2" src="file://{{C2_IMG}}">
{{C2_COMMENT}}

<div class="sec"><h2>{{H_A3}}</h2></div>
{{A3_PARAGRAPHS}}

<!-- PAGE 3: source + disclaimer only, pinned to the bottom -->
<div class="pagebreak"></div>
<div class="gradbar"></div>
<div class="legal">
  <div class="src-line"><span class="syz">SYZ</span> {{SOURCE_LINE}}</div>
  <div class="disc-head">Disclaimer</div>
  <p>This communication has been issued and made available to recipients for the purpose of advertising investment services and/or financial instruments. It has been sent for information purposes and cannot be considered as an offer or a personalised recommendation to buy or sell a financial instrument or any other investment or currency. This communication does not constitute investment research within the meaning of regulatory rules applicable in the European Economic Area, or research under the rules of the U.S. Self-Regulatory Organizations.</p>
  <p>This information is made solely for professional and institutional clients as defined by the Swiss Financial Services Act, as well as qualified investors according to the Swiss Collective Investment Schemes Act. It is not intended for retail clients or non-qualified investors and consequently cannot be transmitted to any third party.</p>
  <p>This communication is not directed to any person in any jurisdiction where, by reason of that person&rsquo;s nationality, residence or otherwise, its dissemination or use is prohibited. It cannot be quoted, reproduced, disclosed, distributed or otherwise referred to, in whole or in part, to any third party without the Bank&rsquo;s prior written consent.</p>
  <p>This communication may contain information on past performances of a financial product, all kinds of economic and financial valuations and analyses, as well as opinions of the Bank or of third parties. Any market valuations, terms and calculation methods, yields and opinions expressed are subject to change without notice. The information and opinions contained herein have been compiled and provided in good faith, based on information obtained from sources believed to be trustworthy. However, such information has not been independently verified. No guarantee, representation, or warranty of any kind, whether express or implied, is provided by the Bank or by relevant data vendors and other sources with respect to the accuracy, reliability, currentness or exhaustiveness of the information communicated, the methodology employed or the prices contained herein.</p>
  <p>Past performance is not a reliable indicator of current or future results. Any reference to the past performance of an investment does not guarantee its future performance. Fluctuations in exchange rates may adversely affect the value, price or income of any investment.</p>
  <p>Nothing in the present communication constitutes investment, legal, accounting or tax advice. This information is purely objective since it does not take into consideration the personal situation (including financial knowledge and experience), the investment objectives and risk profile of any recipient. Moreover, certain financial instruments mentioned (in particular, but not exclusively, derivatives, options and futures) involve a high risk of loss and may not be suitable. Accordingly, recipients should consult their own advisors on such matters, including but not limited to the possible tax consequences of investing in any financial product mentioned herein, and make their own assessment of the suitability of such investment product.</p>
  <p>Should a recipient make an investment on the basis of the present communication, the recipient alone shall bear the consequences thereof. In no event shall the Bank, its directors, employees, affiliates or agents be held responsible for damages of any kind arising out of the use of all or part of the information provided herein.</p>
</div>

</body>
</html>
```
**Default values:** `DOC_TYPE` = "Earnings update"; `THEME` = the sector in sentence case ("Semiconductors"); `DATE` = publication date, e.g. "14 October 2026" (dateline and footer); `W1` = 74 (minimum 66), `W2` = 84 (minimum 76); `SOURCE_LINE` = "Source: Syz Research, Bloomberg, company filings" (no full stop). Paragraph placeholders take complete `<p>…</p>` blocks. `TAKEAWAYS` takes `<li>` rows, `KPI_TILES` takes four `<td>` cells, as in the examples below. The image paths are absolute (`/home/claude/c1_crop.png`). The disclaimer text is fixed: never edit, shorten or paraphrase it.

**Takeaway rows and KPI tiles:**
```html
<li><span class="tag pos">Beat</span><span class="t">Revenue EUR 9.2bn (+4% vs. consensus) and EPS EUR 7.85 (+6%), driven by EUV mix and services.</span></li>
<li><span class="tag neg">Watch</span><span class="t">China fell to 22% of system sales from 29%; export-licence timing remains the main swing factor.</span></li>
<li><span class="tag neu">Valuation</span><span class="t">30.6x forward earnings, 18% above the 2010 to 2026 average: the upcycle is priced, not the next leg.</span></li>

<td><div class="lbl">Revenue</div><div class="val">EUR 9.2bn</div><div class="sub pos">+4.1% vs. consensus</div></td>
<td><div class="lbl">Q4 revenue guide</div><div class="val">EUR 9.6bn</div><div class="sub neg">-2.3% vs. consensus</div></td>
```
Tag classes: `pos` Mint Green (beat, raised, upgrade), `neg` Tiger Orange (miss, cut, watch, risk), `neu` Blueberry (valuation, neutral). Tags are coloured words, not pills: one word in sentence case ("Beat", "Raised", "Watch", "Valuation"), ≤ 9 characters so it fits the 16mm column. KPI `sub` classes follow the sign of the surprise.

**Fill and render:**
```python
html = open("template.html").read()
for k, v in fill.items():
    html = html.replace("{{" + k + "}}", str(v))
assert "{{" not in html, "unfilled placeholder"
open("doc.html", "w").write(html)
from weasyprint import HTML; HTML("doc.html").write_pdf(OUT_PDF)
from pdf2image import convert_from_path
pages = convert_from_path(OUT_PDF, dpi=100)
for i, p in enumerate(pages): p.save(f"page{i+1}.png")
print("pages:", len(pages))   # must be 3, then Read page1.png, page2.png and page3.png
```

## PowerPoint build: write to `/home/claude/build_pptx.js` verbatim
The PPTX is generated with `pptxgenjs` (preinstalled) from a `fill.json` that carries the same content as the HTML fill, as **plain text** (real quotes and apostrophes, `·` for separators, no `&middot;`/`&ndash;` entities). It reproduces the PDF page by page: same A4 portrait margins (18/15/12.5/15 mm), same type sizes, Nunito Bold with ExtraBold-weight titles, logo top-right, gradient rule, footer, the single key-numbers box, the two-column strengthen/change block, and the same cropped chart PNGs. Elements flow top to bottom from calibrated text metrics; the script prints each page's bottom edge against the guard line.

```javascript
// build_pptx.js: Syz Earnings update, portrait A4 PowerPoint with the same visual as the PDF.
// Usage: node build_pptx.js fill.json out.pptx
// fill.json carries the same keys as the HTML template (plain text, no HTML entities).
const pptxgen = require("pptxgenjs");
const fs = require("fs");

const [fillPath, outPath] = process.argv.slice(2);
const F = JSON.parse(fs.readFileSync(fillPath, "utf8"));

const NAVY = "202945", BLUEB = "4B5F80", ORANGE = "FF6C0E", AMBER = "FFA400", MINT = "3BAF90";
const GREY = "6B7280", LIGHT = "9AA0A8", HAIR = "D6D9DE", WHITE = "FFFFFF";
const FONT = "Nunito";
const W = 8.27, H = 11.69, ML = 0.59, MR = 0.59, MT = 0.71, MB = 0.49;   // A4 portrait, PDF margins
const CW = W - ML - MR;

const pres = new pptxgen();
pres.defineLayout({ name: "A4P", width: W, height: H });
pres.layout = "A4P";
pres.theme = { headFontFace: FONT, bodyFontFace: FONT };
pres.author = "Syz Research"; pres.title = F.TITLE;

// ---- text metrics (Nunito Bold, calibrated against the WeasyPrint render)
// CSS line-height values from the PDF template; PowerPoint's multiple is relative to ~1.2 x font size
const LH = 1.42, NAT = 1.2;
const mult = lh => lh / NAT;
function lines(text, pt, width) {
  const cpl = Math.max(10, Math.floor((width * 72) / (pt * 0.475)));
  return text.split("\n").reduce((n, p) => n + Math.max(1, Math.ceil(p.length / cpl)), 0);
}
function hOf(text, pt, width, lh = LH) { return (lines(text, pt, width) * pt * lh) / 72; }

// ---- page chrome
function chrome(slide, pageNo) {
  slide.background = { color: WHITE };
  slide.addImage({ path: F.LOGO, x: W - MR - 0.55, y: 0.18, w: 0.55, h: 0.55 * 186 / 206 });
  slide.addImage({ path: F.GRADBAR, x: ML, y: MT, w: CW, h: 0.045 });
  slide.addText(`Syz Research · ${F.DOC_TYPE} · ${F.DATE}`, {
    x: ML, y: H - MB - 0.02, w: CW / 2, h: 0.2, fontFace: FONT, fontSize: 7, color: LIGHT, bold: true, margin: 0, isTextBox: true, valign: "bottom" });
  slide.addText(`${pageNo} / 3`, {
    x: W - MR - CW / 2, y: H - MB - 0.02, w: CW / 2, h: 0.2, fontFace: FONT, fontSize: 7, color: LIGHT, bold: true, margin: 0, align: "right", isTextBox: true, valign: "bottom" });
  return MT + 0.045 + 0.16;   // y after the gradient rule
}

// ---- flow helpers (all return the new y)
function para(slide, y, text, opts = {}) {
  const pt = opts.pt || 8.7, w = opts.w || CW, x = opts.x || ML;
  const h = hOf(text, pt, w) + 0.02;
  slide.addText(text, { x, y, w, h, fontFace: FONT, fontSize: pt, color: opts.color || NAVY, bold: true,
    align: opts.align || "justify", valign: "top", margin: 0, isTextBox: true, lineSpacingMultiple: mult(LH), paraSpaceAfter: 0 });
  return y + h + (opts.gap === undefined ? 0.087 : opts.gap);
}
function h2(slide, y, text) {
  slide.addText(text, { x: ML, y, w: CW, h: 0.24, fontFace: FONT, fontSize: 11, color: NAVY, bold: true, margin: 0, isTextBox: true, valign: "top" });
  return y + 0.24 + 0.03;
}
function chartTitle(slide, y, num, title, sub) {
  slide.addText([{ text: `Chart ${num}`, options: { color: ORANGE } }, { text: ` · ${title}`, options: { color: NAVY } }],
    { x: ML, y, w: CW, h: 0.2, fontFace: FONT, fontSize: 9.5, bold: true, margin: 0, isTextBox: true, valign: "top" });
  y += 0.2;
  const hs = hOf(sub, 7.2, CW, 1.3);
  slide.addText(sub, { x: ML, y, w: CW, h: hs, fontFace: FONT, fontSize: 7.2, color: GREY, bold: true, margin: 0, isTextBox: true, valign: "top", lineSpacingMultiple: mult(1.3) });
  return y + hs + 0.05;
}
function chart(slide, y, path, widthPct, aspect) {
  const w = CW * widthPct / 100, h = w * aspect;
  slide.addImage({ path, x: ML + (CW - w) / 2, y, w, h });
  return y + h + 0.06;
}

// ================= PAGE 1
let s = pres.addSlide();
let y = chrome(s, 1);
s.addText(`${F.DOC_TYPE} · ${F.THEME}`, { x: ML, y, w: CW, h: 0.18, fontFace: FONT, fontSize: 8, color: ORANGE, bold: true, charSpacing: 1.2, margin: 0, isTextBox: true, valign: "top" });
y += 0.21;
const th = hOf(F.TITLE, 17, CW, 1.22);
s.addText(F.TITLE, { x: ML, y, w: CW, h: th, fontFace: FONT, fontSize: 17, color: NAVY, bold: true, margin: 0, isTextBox: true, valign: "top", lineSpacingMultiple: mult(1.22) });
y += th + 0.04;
s.addText(`${F.DATE} · Syz Research`, { x: ML, y, w: CW, h: 0.18, fontFace: FONT, fontSize: 8.5, color: GREY, bold: true, margin: 0, isTextBox: true, valign: "top" });
y += 0.18 + 0.13;

if (F.QUOTE) {
  const qw = CW - 0.2, qh = hOf(F.QUOTE, 9.8, qw, 1.35);
  s.addShape(pres.ShapeType.rect, { x: ML, y, w: 0.047, h: qh + 0.26, fill: { color: ORANGE }, line: { color: ORANGE, width: 0 } });
  s.addText(`“${F.QUOTE}”`, { x: ML + 0.2, y: y + 0.02, w: qw, h: qh, fontFace: FONT, fontSize: 9.8, color: NAVY, bold: true, margin: 0, isTextBox: true, valign: "top", lineSpacingMultiple: mult(1.35) });
  s.addText(F.QUOTE_WHO, { x: ML + 0.2, y: y + qh + 0.06, w: qw, h: 0.17, fontFace: FONT, fontSize: 7.6, color: GREY, bold: true, margin: 0, isTextBox: true, valign: "top" });
  y += qh + 0.26 + 0.13;
}

y = h2(s, y, "Key takeaways");
for (const t of F.TAKEAWAYS) {
  const col = t.tag === "pos" ? MINT : t.tag === "neg" ? ORANGE : BLUEB;
  const tw = CW - 0.65, hh = hOf(t.text, 8.7, tw);
  s.addText(t.label, { x: ML, y: y + 0.015, w: 0.63, h: hh, fontFace: FONT, fontSize: 7, color: col, bold: true, charSpacing: 0.8, margin: 0, isTextBox: true, valign: "top" });
  s.addText(t.text, { x: ML + 0.65, y: y - 0.01, w: tw, h: hh, fontFace: FONT, fontSize: 8.7, color: NAVY, bold: true, margin: 0, isTextBox: true, valign: "top", lineSpacingMultiple: mult(LH) });
  y += hh + 0.05;
}
y += 0.08;

// key numbers strip: the only box on the page
const kh = 0.74;
s.addShape(pres.ShapeType.rect, { x: ML, y, w: CW, h: kh, fill: { color: WHITE }, line: { color: NAVY, width: 1.3 } });
F.KPIS.forEach((k, i) => {
  const cx = ML + (CW / 4) * i, cw = CW / 4;
  if (i > 0) s.addShape(pres.ShapeType.line, { x: cx, y: y, w: 0, h: kh, line: { color: HAIR, width: 0.6 } });
  s.addText(k.label, { x: cx + 0.12, y: y + 0.09, w: cw - 0.2, h: 0.16, fontFace: FONT, fontSize: 7.2, color: GREY, bold: true, margin: 0, isTextBox: true, valign: "top" });
  s.addText(k.value, { x: cx + 0.12, y: y + 0.25, w: cw - 0.2, h: 0.26, fontFace: FONT, fontSize: 13, color: NAVY, bold: true, margin: 0, isTextBox: true, valign: "top" });
  s.addText(k.sub, { x: cx + 0.12, y: y + 0.51, w: cw - 0.2, h: 0.16, fontFace: FONT, fontSize: 7.2, color: k.sign === "pos" ? MINT : k.sign === "neg" ? ORANGE : BLUEB, bold: true, margin: 0, isTextBox: true, valign: "top" });
});
y += kh + 0.13;

y = h2(s, y, F.H_P1);
y = para(s, y, F.P1_PARAGRAPH);
y = chartTitle(s, y, 1, F.C1_TITLE, F.C1_SUB);
y = chart(s, y, F.C1_IMG, F.W1, F.C1_ASPECT);
y = para(s, y, F.C1_COMMENT);
y += 0.04;
y = h2(s, y, "Base case and implications");
y = para(s, y, F.BASE_CASE);
y += 0.04;
const colW = CW / 2 - 0.2;
const uh = hOf(F.UPSIDE, 8.7, colW), dh = hOf(F.DOWNSIDE, 8.7, colW), ch = Math.max(uh, dh) + 0.22;
s.addShape(pres.ShapeType.line, { x: ML + CW / 2, y, w: 0, h: ch, line: { color: HAIR, width: 0.6 } });
s.addText("What would strengthen our view", { x: ML, y, w: colW, h: 0.17, fontFace: FONT, fontSize: 7.8, color: ORANGE, bold: true, charSpacing: 1, margin: 0, isTextBox: true, valign: "top" });
s.addText(F.UPSIDE, { x: ML, y: y + 0.21, w: colW, h: uh, fontFace: FONT, fontSize: 8.7, color: NAVY, bold: true, margin: 0, isTextBox: true, valign: "top", lineSpacingMultiple: mult(LH) });
s.addText("What would change our view", { x: ML + CW / 2 + 0.2, y, w: colW, h: 0.17, fontFace: FONT, fontSize: 7.8, color: ORANGE, bold: true, charSpacing: 1, margin: 0, isTextBox: true, valign: "top" });
s.addText(F.DOWNSIDE, { x: ML + CW / 2 + 0.2, y: y + 0.21, w: colW, h: dh, fontFace: FONT, fontSize: 8.7, color: NAVY, bold: true, margin: 0, isTextBox: true, valign: "top", lineSpacingMultiple: mult(LH) });
y += ch;
console.log("page 1 bottom:", y.toFixed(2), "limit:", (H - MB - 0.25).toFixed(2));

// ================= PAGE 2
s = pres.addSlide();
y = chrome(s, 2);
y = h2(s, y, F.H_A1);
for (const p of F.A1_PARAGRAPHS) y = para(s, y, p);
y += 0.04;
y = h2(s, y, F.H_A2);
y = para(s, y, F.A2_PARAGRAPH);
y += 0.04;
y = h2(s, y, F.H_C2);
y = chartTitle(s, y, 2, F.C2_TITLE, F.C2_SUB);
y = chart(s, y, F.C2_IMG, F.W2, F.C2_ASPECT);
y = para(s, y, F.C2_COMMENT);
y += 0.04;
y = h2(s, y, F.H_A3);
y = para(s, y, F.A3_PARAGRAPH);
console.log("page 2 bottom:", y.toFixed(2), "limit:", (H - MB - 0.25).toFixed(2));

// ================= PAGE 3: source + disclaimer pinned to the bottom
s = pres.addSlide();
chrome(s, 3);
const legal = F.DISCLAIMER;
let lh = 0;
const parts = legal.map(p => { const h = hOf(p, 6.8, CW, 1.4) + 0.06; lh += h; return h; });
const srcH = 0.2, headH = 0.2;
let ly = H - MB - 0.35 - lh - srcH - headH - 0.16;
s.addText([{ text: "SYZ", options: { color: ORANGE } }, { text: ` ${F.SOURCE_LINE}`, options: { color: LIGHT } }],
  { x: ML, y: ly, w: CW, h: srcH, fontFace: FONT, fontSize: 6.8, bold: true, margin: 0, isTextBox: true, valign: "top" });
ly += srcH + 0.16;
s.addText("Disclaimer", { x: ML, y: ly, w: CW, h: headH, fontFace: FONT, fontSize: 6.8, color: ORANGE, bold: true, charSpacing: 1.2, margin: 0, isTextBox: true, valign: "top" });
ly += headH;
legal.forEach((p, i) => {
  s.addText(p, { x: ML, y: ly, w: CW, h: parts[i], fontFace: FONT, fontSize: 6.8, color: LIGHT, bold: true, align: "justify", margin: 0, isTextBox: true, valign: "top", lineSpacingMultiple: mult(1.4) });
  ly += parts[i];
});

pres.writeFile({ fileName: outPath }).then(() => console.log("written", outPath));
```

**`fill.json` keys** (all strings unless noted): `LOGO`, `GRADBAR` (absolute paths), `DOC_TYPE`, `THEME`, `DATE`, `TITLE`, `QUOTE` (text without quotation marks; empty string to omit the block), `QUOTE_WHO`, `TAKEAWAYS` (list of `{tag: pos|neg|neu, label, text}`), `KPIS` (four `{label, value, sub, sign: pos|neg|neu}`), `H_P1`, `P1_PARAGRAPH`, `C1_TITLE`, `C1_SUB`, `C1_IMG`, `C1_ASPECT` (image height/width), `W1` (number, % of text width), `C1_COMMENT`, `BASE_CASE`, `UPSIDE`, `DOWNSIDE`, `H_A1`, `A1_PARAGRAPHS` (list of two), `H_A2`, `A2_PARAGRAPH`, `H_C2`, `C2_TITLE`, `C2_SUB`, `C2_IMG`, `C2_ASPECT`, `W2`, `C2_COMMENT`, `H_A3`, `A3_PARAGRAPH`, `SOURCE_LINE`, `DISCLAIMER` (list of the seven fixed paragraphs, taken verbatim from the HTML template with `&rsquo;` turned into a real apostrophe).

**Defaults for the PPTX:** `W1` = 74, `W2` = 80 (the PowerPoint runs Chart 2 four points narrower than the PDF to keep page 2 inside the guard line with the same word budgets). The font face is Nunito; on a machine without Nunito, PowerPoint substitutes and line breaks may shift slightly.

**Build, validate, render:**
```bash
node /home/claude/build_pptx.js fill.json Earnings_Update_<Ticker>_<QxYYYY>.pptx     # prints "page N bottom: x limit: y"
python3 /mnt/skills/public/pptx/scripts/office/validate.py Earnings_Update_<Ticker>_<QxYYYY>.pptx
python3 /mnt/skills/public/pptx/scripts/office/soffice.py --headless --convert-to pdf Earnings_Update_<Ticker>_<QxYYYY>.pptx
pdftoppm -jpeg -r 100 Earnings_Update_<Ticker>_<QxYYYY>.pdf slide    # then Read slide-1.jpg, slide-2.jpg, slide-3.jpg
```
If a page bottom exceeds the limit, lower `W1`/`W2` by 2 to 4 points (minimum 66 / 74), then tighten prose; never change type sizes or margins.

## Text format
**Page plan (fixed):**
- **Page 1, executive investment summary** (for every reader, including private clients; carries ~80% of the message): kicker → title → dateline → management quote (optional, orange left rule) → **Key takeaways** heading + 3 to 4 tagged lines → the **key numbers strip** (the only box on the page: one Space Blue border, four columns separated by hairlines) → heading + 1 paragraph on what the quarter means for the investment case → Chart 1 + 1 comment paragraph → **Base case and implications** heading + paragraph → two text columns with a hairline divider, **What would strengthen our view** / **What would change our view**. One box on page 1, never more: structure comes from headings, tags and the column divider.
- **Page 2, in-depth analysis** (for readers who want the why): heading + 2 paragraphs on the results and their drivers → heading + 1 paragraph on outlook and guidance → heading + Chart 2 + 1 comment paragraph on valuation → heading + 1 paragraph on investment implications and positioning. Builds on page 1 without repeating it: page 1 states the conclusion, page 2 shows the evidence.
- **Page 3:** gradient rule, source line and the fixed disclaimer pinned to the bottom. Nothing else.

**Word budgets (calibrated to fit, do not exceed):**
| Element | Words |
|---|---|
| Management quote | 20 to 35, plus a one-line attribution (name, role, event, date) |
| Key takeaways | 3 to 4 lines, ≤ 18 words each, one number in each |
| KPI tiles | 4 tiles: label, value, surprise vs. consensus (or vs. guide) |
| Investment-case paragraph (H_P1) | 70 to 85 |
| Chart 1 comment | 55 to 65 |
| Base case paragraph | 60 to 70 |
| Strengthen / change columns | 40 to 50 each |
| Results paragraphs (H_A1) | 100 to 115 and 90 to 105 |
| Outlook paragraph (H_A2) | 95 to 110 |
| Chart 2 comment | 85 to 100 |
| Implications paragraph (H_A3) | 90 to 110 |

**Element rules:**
- **Title:** `<Company> <Qx YYYY>: <conviction message in sentence case>`, ≤ ~70 characters, e.g. "ASML Q3 2026: orders confirm the upcycle, valuation leaves little slack". It states the verdict, not the topic.
- **Management quote:** lead with it only when it carries the investment message (tone on demand, a guidance commitment, a change of stance). Verbatim from the transcript or release, in `&ldquo;…&rdquo;`, attributed with name, role, event and date. Omit rather than invent.
- **Key takeaways:** each line = tag + one fact with a number + its implication. Together they must give a client the whole story in 30 seconds: result, guidance, the main risk, the valuation verdict.
- **KPI tiles:** the four lines that decided the quarter (typically revenue, EPS, a margin, next-period guidance). Surprise in % or bp, sign-coloured.
- **Section headings (h2):** five variable ones per document (H_P1, H_A1, H_A2, H_C2, H_A3), plus the two fixed page-1 headings "Key takeaways" and "Base case and implications". Each is a takeaway in sentence case, ≤ ~45 characters, no full stop, e.g. "Results: the beat was mix, not volume", "Valuation: the upcycle is priced, the next leg is not". Don't repeat the H1's verdict. Plain 11pt ExtraBold Space Blue, no rule or accent.
- **Chart titles in the PDF:** `<span class="num">Chart N</span> &middot; <Ticker>: <descriptor>`. **Chart sub-line:** one line of methodology (series, window, consensus source, MA, log scale, shading), joined by `&middot;`; disclose stale or partial data here.
- **Base case paragraph:** 2 to 3 sentences: the regime for the stock ("We stay overweight…", "We hold…"), the earnings path we underwrite, one qualifier. No list of triggers inside it.
- **Strengthen / change columns:** 2 to 3 concrete, observable triggers each (a number, a date, a decision), not generic risk language.
- **Page 2 valuation comment:** read Chart 2 explicitly: price vs. EPS trend (is price running ahead of earnings?), P/E vs. its average and the premium in %, price vs. 40-week MA, and what multiple the base case implies.

**Style rules (mandatory):**
- **Sentence case throughout**: titles, headings, box heads, tags, chart titles, legends. Uppercase only where grammatically required (tickers, index names, acronyms such as EUV, EPS, P/E).
- **No em dashes** anywhere (text, charts, headings). Use a comma, a colon or `&ndash;` only for numeric ranges (2022&ndash;25). Prefer "2010 to 2026" in prose.
- **Typography**: Nunito Bold (700) for body and ExtraBold (800) for headings, titles, box heads, KPI values and quote text. No Light, Regular or SemiBold anywhere.
- **Boxes**: only the key numbers strip is boxed: Space Blue `#202945` border 0.45mm, straight corners, no fill. No other box on either page, no blue-filled backgrounds, no rounded corners.
- **Negative indicators**: Tiger Orange `#FF6C0E` for bearish or negative tags, bars and KPI deltas, never purple.
- **Sources**: `Source: Syz Research, Bloomberg…` with no full stop at the end, on page 3 and in every chart footnote.
- Typography uses HTML entities: `&ndash;` for ranges, `&rsquo;` for apostrophes, `&ldquo;…&rdquo;` for quotes, `&amp;`, `&middot;` for separators.

**Voice:**
- Institutional, quantified and decisive; first person plural ("We read this as…", "We stay…"). Page 1 is readable by a private client: plain words, every acronym used once in full, no jargon that needs a footnote. Page 2 can be more technical (mix, incremental margins, revisions, multiples).
- Every claim carries a number: reported vs. consensus in % or bp, guidance in ranges, EPS to one decimal, P/E to one decimal and its premium to the average in %, "highest since <Qx YYYY>" computed from the data.
- Separate signal from noise: a one-off (FX, tax rate, a pulled-forward order) is named and stripped from the read.
- No bullet lists outside the Key takeaways block, no exclamation marks, no marketing adjectives. British spelling (stabilised, programme, licence).
- Never invent numbers, consensus figures or quotes. Anything taken from the web is dated in the text and flagged in the reply for a Bloomberg check.

## Fit & QA (mandatory)
1. The PDF must be **exactly 3 pages**. Page 1 ends with the two strengthen/change columns; page 2 starts with the results heading and ends with the implications paragraph; page 3 holds only the source line and the disclaimer.
2. **If a page overflows,** apply these levers in order: reduce `W1` (minimum 66) or `W2` (minimum 76) by 2 to 4 points; tighten the prose to the lower end of the budgets. Never change font sizes, margins, colours, headings or the page plan. Never let a heading or the key numbers strip sit alone at the bottom of a page.
3. **Rasterise all three pages at 100 dpi and look at them.** Check for:
   - logo top-right and gradient rule on every page;
   - exactly one box on page 1 (the key numbers strip): Space Blue border, square corners, no fill, four columns in one row;
   - tags: negative ones in Tiger Orange; no purple anywhere;
   - no em dash in any text or chart; sentence case everywhere;
   - five section headings on one line each;
   - footer reads "Syz Research · Earnings update · <date>" with a space after each dot;
   - Chart 2 legible: legend, end labels (price, EPS, P/E) and the P/E average line visible, no label collisions;
   - page 3: source line (no full stop) followed by the full disclaimer, pinned above the footer.
4. Run `pdffonts` on the output: only Nunito Bold and Nunito ExtraBold (shown as Nunito-Ultra-Bold) may be embedded.
5. **PowerPoint:** `validate.py` passes; `build_pptx.js` reports both page bottoms below the limit; the three LibreOffice-rendered slides show the same layout as the PDF pages (one box on page 1, no text touching the next heading, footer and logo on every slide, disclaimer pinned to the bottom of slide 3); `markitdown` shows three slides with no leftover placeholder text.
6. In the reply, report: the data window and last date; the 3 to 5 numbers the document turns on (surprise, guidance, P/E and premium); any figure or quote taken from outside the user's files that needs verifying.

## Reference instance: ASML Q3 2026 (14 October 2026)
- **Data:** `ASML.xlsx`, weekly, 1 Jan 2010 to 14 Oct 2026; last price EUR 1,541.8, 12m-forward EPS EUR 50.3, 40-week MA EUR 1,386, 12m-forward P/E 30.6x vs. a 26.0x average since 2010 (an 18% premium).
- **Chart 1:** `bar_chart` of surprises vs. consensus (revenue, gross margin, EBIT, EPS, Q4 guide, FY27 outlook).
- **Chart 2:** `price_eps_pe_chart`, title "ASML: share price vs. consensus earnings and valuation", footnote `source_line("Bloomberg", "14 Oct 2026", "ASML NA Equity, weekly", "BEst 12m-forward consensus", "40-week simple MA", "Log scale", "P/E shaded above (orange) / below (blue) its 2010-26 average")`.
- **Headings pattern:** "What the quarter means for the investment case" · "Results: the beat was mix, not volume" · "Outlook: guidance leans on EUV and services" · "Valuation: the upcycle is priced, the next leg is not" · "Investment implications and positioning".
