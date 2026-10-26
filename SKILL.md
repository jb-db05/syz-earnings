---
name: "syz-earnings"
description: "Produce Syz post-earnings investment updates (Earnings update as PDF and portrait A4 PowerPoint with the same visual: page 1 executive investment summary for all clients with a company introduction under the quote, page 2 'Beyond the key takeaways' in-depth analysis with the share price vs. consensus EPS and P/E chart, page 3 disclaimer) from a Bloomberg weekly export. Use for any 'Syz Earnings' request or post-results company update; keep using syz-visual for 'Syz Visual' macro Research Comments."
---

# Syz Earnings: post-earnings investment update

Produce a concise, institutional-quality **Earnings update** on a single company after its results: **page 1 tells investors what they need to know (including our positioning), page 2 "Beyond the key takeaways" helps them understand why**, page 3 carries the source line and the fixed disclaimer. Same page geometry, chart kit and voice as the Syz Research Comment format (`syz-visual`), adapted to a post-results use case, with a four-size type scale (see Typography).

Where this skill and `syz-house-style` or `syz-visual` differ, **this skill wins**. Apply silently; do not describe the style back to the user.

## Deliverables (every time)
1. `Earnings_Update_<Ticker>_<QxYYYY>.pdf`: 3-page A4 (page 1 executive investment summary, page 2 in-depth analysis, page 3 source + disclaimer).
2. `Earnings_Update_<Ticker>_<QxYYYY>.pptx`: the same three pages as a **portrait A4 PowerPoint** (21 x 29.7 cm), same margins, type sizes, colours and charts, with native editable text and shapes.
3. The standalone chart PNGs **with** their header/footnote (for decks and LinkedIn): at least the price vs. consensus EPS and P/E chart.
4. The build scripts (data → charts → PDF, and `fill.json` → PPTX), parameterised for the next quarter: keep all text in one `content.py` (HTML entities), a `build_charts.py` with a `PARAMS` dict, and a `build_pdf.py` that fills the template, renders, rasterises and writes `fill.json`.

## Inputs
- **Bloomberg weekly export (.xlsx)**, one sheet, newest row first, header row 1, columns matched by keyword (order does not matter):
  `Date | <Ticker> - Last Price (R1) | <Ticker> - BEst EPS (L1) | Moving Average(Simple,40,0) (<Ticker>) | <Ticker> - BEst P/E Ratio`.
  Reference files: `ASML.xlsx` (877 weekly rows, Jan 2010 to 14 Oct 2026), `VAT.xlsx` (549 rows, Apr 2016 to 15 Oct 2026; consensus EPS only from May 2016). `load_bloomberg_sheet()` below reads it. Trailing empty rows are dropped. **Start the chart window at the first row with consensus EPS** (`df = df[df["eps"].notna()]`), otherwise the log ticks fail on NaN. Check whether the last row is the pre-results close (export taken on results day): if so, say so in the Chart 2 sub-line.
- **Publication-day share price reaction (mandatory):** the close-to-close move on the release day in % (previous close to release-day close), and the same-day move of the local index or sector where available, so the reaction can be read relative to the market. The weekly export does not contain it: take it from the user's material or Bloomberg; if neither is available, take it from a dated web source, date it in the text and flag it in the reply for a Bloomberg check. If the results were published after the close, the reaction day is the next trading day; say which day was used in the text. Store it in `PARAMS` (`reaction_pct`, `reaction_date`, `market_pct`).
- **Company description material:** the annual report, the IR "at a glance" page or the user's files, for the 25 to 36 word introduction (what the company makes, for whom, where it earns its money, scale). Facts only, no adjectives; no figure that is not sourced.
- **Results material** the user supplies or points to: press release, presentation, transcript, consensus table, broker first takes. Web-sourced facts (consensus, guidance, quotes) are dated in the text and flagged for a Bloomberg check in the reply. Cross-check the headline figures against the company's own release (EQS/ad hoc feed or the IR site) when the user's material is secondary.
- **A management quote**, sourced in this order, never invented or paraphrased into quotation marks:
  1. The transcript or press release the user provided.
  2. If the user provided no quote, check **www.stockanalysis.com**: open the stock's page (`https://stockanalysis.com/quote/<exchange>/<ticker>/`, e.g. `swx/VACN`, or `/stocks/<ticker>/` for US names) and its **Transcripts** tab for the latest earnings or trading-update call; take a verbatim sentence from the CEO or CFO, with name, role, event and date. If the fetch needs a URL permission, ask the user to paste the stockanalysis.com link.
  3. If no executive is quoted anywhere, a **verbatim company statement from the release** is acceptable, attributed as "<Company>, <Qx YYYY> trading update, ad hoc release of <date> (company statement; no executive is quoted in the release)".
  4. If none of these yields 20 to 35 usable words that carry the investment message, drop the quote block (`QUOTE` = empty string).

## Workflow
1. **Data first, silently.** Load the Bloomberg sheet; note the window, the last date, the last price, 12m-forward EPS, 40-week MA and P/E; compute the P/E average since the start of the window and the premium/discount to it, the one-year average P/E, the peak P/E and its date, price and EPS change over 12 months and since the previous results; check whether the price sits above its 40-week MA. From the results material, build the KPI table (reported vs. consensus, guidance vs. consensus). Record the publication-day reaction and **classify surprise vs. reaction**: aligned (beat and up, miss and down) or divergent (beat and down, miss and up, or a move out of proportion to the surprise); a divergence is always explained in the text (see Text format). Compute every number you will quote. Never invent or extrapolate. Sanity-check the user's consensus tables: a BQL pull with `fpt=A` returns the last fiscal year, not the last half-year.
2. **Pick the charts.** Chart 2 (page 2) is fixed: `price_eps_pe_chart`. Chart 1 (page 1) is one impactful results chart: by default `bar_chart` of surprises vs. consensus (reported lines + guidance); for a **trading update with only one or two consensus-comparable lines** (orders and sales), use `bar_chart` of the decisive line in absolute terms instead (prior year, previous record, consensus, reported; reported bar in Tiger Orange). Another archetype is allowed only if it carries the page-1 message better.
3. **Setup** (fonts, logo, WeasyPrint), write `syz_charts.py` (below) verbatim and build the charts. Extract the three code blocks (chart kit, HTML template, PPTX builder) from this file with a script rather than retyping them: `re.findall(r"```(\w+)\n(.*?)```", skill_md, re.S)`.
4. **Crop** each chart for the PDF (`crop_for_pdf`): the PDF typesets titles in HTML, so the chart's own header/footnote is removed.
5. **Write the text** following the Text format rules: page 1 first (the company introduction, then the 80% message, including our positioning), then page 2 (the why, including the surprise vs. reaction read), with no repetition between them. Count words against the budgets with a script before rendering.
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

**Logo.** Use the Syz logo from the project files, `SYZ logo.png` (206x186 RGBA, transparent background, orange gradient): copy it to `/home/claude/syz_logo_hq.png` and validate it before rendering (`Image.open(path).load()`; alpha at the corners must be 0). Never use a logo with a white box, and never ship a page without the logo top-right: WeasyPrint silently drops a broken PNG from the margin box, so check the rasterised pages.
```python
from PIL import Image; import numpy as np, glob
src = [p for p in glob.glob("/root/.claude/uploads/**/*SYZ*logo*.png", recursive=True)][0]
im = Image.open(src); im.load(); a = np.array(im); assert im.size == (206, 186) and a[0, 0, 3] == 0
im.save("/home/claude/syz_logo_hq.png")
```
If the file is not in the project, ask the user for it rather than substituting another logo.

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
    axr.annotate(f"{last_p:,.0f}", (x[-1], last_p), xytext=(10, 10), textcoords="offset points",
                 color=BLUEB, fontsize=10.5, fontweight="bold")
    ax1.plot(x[-1], last_e, "o", color=ORANGE, ms=5, zorder=5)
    ax1.annotate(f"{last_e:,.1f}", (x[-1], last_e), xytext=(10, -22), textcoords="offset points",
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
    negative = Tiger Orange (bearish tag colour), unless colors is given. One label size (12) for ticks,
    category labels and value annotations; the y label takes the legend size (10.5)."""
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
                    ha="center", fontsize=12, fontweight="bold", color=NAVY)
    ax.set_xticks(range(len(vals))); ax.set_xticklabels(labels, fontsize=12, color=NAVY, fontweight="bold")
    ax.set_ylabel(ylabel, fontsize=10.5, color=AXIS_TXT, fontweight="bold")
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
| `bar_chart` | **Chart 1, default**: surprise vs. consensus by line (revenue, gross margin, EBIT, EPS, next-quarter guide, FY outlook); or revisions by segment; positive bars Blueberry, negative bars Tiger Orange. **Trading-update variant**: the decisive line in absolute terms (prior year, previous record, consensus, reported) with `colors=[BLUEB, BLUEB, BLUEB, ORANGE]`, `fmt="{:,.0f}"`, `zero_line=False`, two-line x labels | 12.5x5.0 in |

- **Colour convention:** reference series Blueberry Blue `#4B5F80`; emphasis series Tiger Orange `#FF6C0E`. Dashed lines navy `(0,(5,4))`. **Negative or bearish = Tiger Orange**, never purple. P/E shading: above average orange α 0.12, below average Blueberry α 0.14.
- **Log axes** use the 1-2-5 ladder (1, 2, 5, 10, 20, 50 for EPS; 25, 50, 100, 250, 500, 1,000 for price), thousands separators, no minor ticks.
- **End labels** on Chart 2 sit at offsets (10, 10) for the price and (10, -22) for the EPS so they do not collide when both series end at the same height; zoom into the top-right corner of the PNG to check.
- **Standalone title** = `<Ticker>: <descriptor>` with a colon, sentence case, e.g. "ASML: share price vs. consensus earnings and valuation". No em dashes anywhere. **Footnote** = `source_line(provider, "<D Mon YYYY>", notes…)`, naming the series, the MA, the log scale and the shading rule; **no full stop at the end**. Consensus provenance is described neutrally ("Consensus: Bloomberg pre-results (analyst first takes)"), never by broker name.
- **Typography in charts:** Nunito Bold for everything, ExtraBold for the figure title (set by `setup_fonts` and `header`). Chart text sizes are the kit's own (the PNG is scaled to 66 to 94% of the text width, so every chart label renders below the document's footnote tier): use only the sizes already in the kit (16.5 standalone title, 12 panel titles and bar labels, 10.5 legends and end labels, 9.5 ticks, 8 footnote) and never introduce another.
- **Other chart types** (a stacked contribution bar, a revisions line) are allowed only if built with `style_ax` + `header` + `source_line`, 12.5 in wide, 200 dpi, margins `left=0.07, right=0.96`; add a crop preset in `CROPS` and check the crop visually.

## Typography: four sizes, one hierarchy
The whole typeset document (PDF and PPTX) uses **exactly four font sizes**, each with one role. Never add a fifth, never nudge a size to fit:

| Tier | Size | Weight | Used for |
|---|---|---|---|
| Title | 17pt | ExtraBold | page-1 title (h1), page-2 title "Beyond the key takeaways" |
| Heading | 11pt | ExtraBold | section headings (h2), KPI values |
| Body | 8.7pt | Bold (ExtraBold for emphasis roles) | body text, company introduction, dateline, takeaway text, management quote (ExtraBold), chart titles (ExtraBold), base case, strengthen/change text |
| Label | 7pt | Bold (ExtraBold for coloured labels) | kicker, tags, KPI labels and sub lines, quote attribution, chart sub-lines, column heads, footer, source line, disclaimer |

Emphasis within a tier comes from weight (Bold vs. ExtraBold), colour (Space Blue, Tiger Orange, grey) and letter-spacing, never from size. Fit problems are solved with the chart widths and the word budgets, never with type size.

## HTML template: fill every `{{…}}`, change nothing else
```html
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
@font-face { font-family: 'Nunito'; src: url('file:///home/claude/fonts/Nunito-Bold.ttf'); font-weight: 700; }
@font-face { font-family: 'Nunito'; src: url('file:///home/claude/fonts/Nunito-ExtraBold.ttf'); font-weight: 800; }

/* Type scale: exactly four sizes. 17pt titles, 11pt headings, 8.7pt body, 7pt labels/footnotes. */
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

.kicker { font-size: 7pt; font-weight: 800; letter-spacing: 1.2px; color: #FF6C0E; margin-bottom: 1.5mm; }
.page-title { font-size: 17pt; font-weight: 800; color: #202945; line-height: 1.22; margin-bottom: 3.2mm; }
h1 { font-size: 17pt; font-weight: 800; color: #202945; line-height: 1.22; margin-bottom: 1.5mm; }
.dateline { font-size: 8.7pt; color: #6B7280; margin-bottom: 3.2mm; }

/* Management quote: orange left rule, no fill */
.quote { border-left: 1.2mm solid #FF6C0E; padding: 1mm 0 1mm 4mm; margin: 0 0 3.2mm 0; }
.quote p { font-size: 8.7pt; font-weight: 800; color: #202945; line-height: 1.35; text-align: left; margin-bottom: 1mm; }
.quote .who { font-size: 7pt; color: #6B7280; font-weight: 700; }

/* Company introduction: one short paragraph directly below the quote, body size, no box */
p.intro { margin-bottom: 3.2mm; }

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
.kpi .lbl { font-size: 7pt; color: #6B7280; margin-bottom: 0.6mm; }
.kpi .val { font-size: 11pt; font-weight: 800; color: #202945; line-height: 1.1; }
.kpi .sub { font-size: 7pt; margin-top: 0.8mm; color: #4B5F80; }
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
table.duo .head { font-size: 7pt; font-weight: 800; letter-spacing: 1px; color: #FF6C0E; margin-bottom: 1.2mm; }
table.duo p { margin-bottom: 0; text-align: left; }

.chart-title { font-size: 8.7pt; font-weight: 800; color: #202945; margin: 1.5mm 0 1.5mm 0; }
.chart-sub { font-size: 7pt; color: #6B7280; margin: -1mm 0 1.2mm 0; }
.chart-title .num { color: #FF6C0E; }
img.chart { width: {{W1}}%; display: block; margin: 0 auto 1.2mm auto; }
img.c2 { width: {{W2}}%; }

/* Page 3: source + disclaimer, pinned to the bottom of the page */
.legal { font-size: 7pt; color: #9AA0A8; line-height: 1.4; position: absolute; bottom: 0; left: 0; right: 0; }
.legal .syz { color: #FF6C0E; font-weight: 800; }
.legal .src-line { margin-bottom: 4mm; }
.legal .disc-head { color: #FF6C0E; font-weight: 800; letter-spacing: 1.2px; margin-bottom: 1.5mm; }
.legal p { font-size: 7pt; margin-bottom: 1.6mm; text-align: justify; }

.pagebreak { page-break-before: always; }
</style>
</head>
<body>

<!-- PAGE 1: executive investment summary -->
<div class="gradbar"></div>
<div class="kicker">{{DOC_TYPE}}</div>
<h1>{{TITLE}}</h1>
<div class="dateline">{{DATE}} &middot; Syz Research</div>

{{QUOTE_BLOCK}}

<p class="intro">{{COMPANY_INTRO}}</p>

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
<div class="page-title">{{P2_TITLE}}</div>

<div class="sec first"><h2>{{H_A1}}</h2></div>
{{A1_PARAGRAPHS}}

<div class="sec"><h2>{{H_A2}}</h2></div>
{{A2_PARAGRAPHS}}

<div class="sec"><h2>{{H_C2}}</h2></div>
<div class="chart-title"><span class="num">Chart 2</span> &middot; {{C2_TITLE}}</div>
<div class="chart-sub">{{C2_SUB}}</div>
<img class="chart c2" src="file://{{C2_IMG}}">
{{C2_COMMENT}}


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
**Default values:** `DOC_TYPE` = "Earnings update" (the kicker carries this and nothing else: **no sector, theme or ticker after it**); `DATE` = publication date, e.g. "15 October 2026" (dateline and footer); `COMPANY_INTRO` = the 25 to 36 word company introduction, always present; `P2_TITLE` = "Beyond the key takeaways" (fixed page-2 title, sentence case); `W1` = 74 (range 66 to 80), `W2` = 92 (range 76 to 94); `SOURCE_LINE` = "Source: Syz Research, Bloomberg, company filings" (no full stop), extended with the release ("<Company> ad hoc release of <date>") and "analyst research notes of <date>" when first takes were used, never with broker names. Paragraph placeholders take complete `<p>…</p>` blocks. `TAKEAWAYS` takes `<li>` rows, `KPI_TILES` takes four `<td>` cells, as in the examples below. The image paths are absolute (`/home/claude/c1_crop.png`). The disclaimer text is fixed: never edit, shorten or paraphrase it.

**Takeaway rows and KPI tiles:**
```html
<li><span class="tag pos">Beat</span><span class="t">Revenue EUR 9.2bn (+4% vs. consensus) and EPS EUR 7.85 (+6%), driven by EUV mix and services.</span></li>
<li><span class="tag neg">Reaction</span><span class="t">Shares fell 5.1% on the day (sector +0.3%): the Q4 guide, 2% below consensus, outweighed the beat.</span></li>
<li><span class="tag neg">Watch</span><span class="t">China fell to 22% of system sales from 29%; export-licence timing remains the main swing factor.</span></li>
<li><span class="tag neu">Valuation</span><span class="t">30.6x forward earnings, 18% above the 2010 to 2026 average: the upcycle is priced, not the next leg.</span></li>

<td><div class="lbl">Revenue</div><div class="val">EUR 9.2bn</div><div class="sub pos">+4.1% vs. consensus</div></td>
<td><div class="lbl">Q4 revenue guide</div><div class="val">EUR 9.6bn</div><div class="sub neg">-2.3% vs. consensus</div></td>
```
Tag classes: `pos` Mint Green (beat, raised, upgrade), `neg` Tiger Orange (miss, cut, watch, risk, a negative reaction), `neu` Blueberry (valuation, neutral, an aligned reaction). Tags are coloured words, not pills: one word in sentence case ("Beat", "Raised", "Reaction", "Watch", "Valuation"), ≤ 9 characters so it fits the 16mm column. KPI `sub` classes follow the sign of the surprise; keep the `sub` line short enough to stay on one line in the PowerPoint tile ("In line, top of guide", not "In line, top of CHF 355–385m guide").

**Fill and render:**
```python
html = open("template.html").read()
for k, v in fill.items():
    html = html.replace("{{" + k + "}}", str(v))
assert "{{" not in html, "unfilled placeholder"
assert "—" not in html, "em dash"
open("doc.html", "w").write(html)
from weasyprint import HTML; HTML("doc.html").write_pdf(OUT_PDF)
from pdf2image import convert_from_path
pages = convert_from_path(OUT_PDF, dpi=100)
for i, p in enumerate(pages): p.save(f"page{i+1}.png")
print("pages:", len(pages))   # must be 3, then Read page1.png, page2.png and page3.png
```

## PowerPoint build: write to `/home/claude/build_pptx.js` verbatim
The PPTX is generated with `pptxgenjs` (preinstalled) from a `fill.json` that carries the same content as the HTML fill, as **plain text** (real quotes and apostrophes, `·` for separators, no `&middot;`/`&ndash;` entities). It reproduces the PDF page by page: same A4 portrait margins (18/15/12.5/15 mm), the same four type sizes (17 / 11 / 8.7 / 7), Nunito Bold with ExtraBold-weight titles, logo top-right, gradient rule, footer, the company introduction under the quote, the single key-numbers box, the two-column strengthen/change block, the page-2 title and the same cropped chart PNGs. Elements flow top to bottom from calibrated text metrics; the script prints each page's bottom edge against the guard line.

```javascript
// build_pptx.js: Syz Earnings update, portrait A4 PowerPoint with the same visual as the PDF.
// Usage: node build_pptx.js fill.json out.pptx
// fill.json carries the same keys as the HTML template (plain text, no HTML entities).
// Type scale: exactly four sizes, T_TITLE 17, T_HEAD 11, T_BODY 8.7, T_LABEL 7. Never add a fifth.
const pptxgen = require("pptxgenjs");
const fs = require("fs");

const [fillPath, outPath] = process.argv.slice(2);
const F = JSON.parse(fs.readFileSync(fillPath, "utf8"));

const NAVY = "202945", BLUEB = "4B5F80", ORANGE = "FF6C0E", AMBER = "FFA400", MINT = "3BAF90";
const GREY = "6B7280", LIGHT = "9AA0A8", HAIR = "D6D9DE", WHITE = "FFFFFF";
const FONT = "Nunito";
const T_TITLE = 17, T_HEAD = 11, T_BODY = 8.7, T_LABEL = 7;
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
  const cpl = Math.max(10, Math.floor((width * 72) / (pt * 0.49)));
  return text.split("\n").reduce((n, p) => n + Math.max(1, Math.ceil(p.length / cpl)), 0);
}
function hOf(text, pt, width, lh = LH) { return (lines(text, pt, width) * pt * lh) / 72; }

// ---- page chrome
function chrome(slide, pageNo) {
  slide.background = { color: WHITE };
  slide.addImage({ path: F.LOGO, x: W - MR - 0.55, y: 0.18, w: 0.55, h: 0.55 * 186 / 206 });
  slide.addImage({ path: F.GRADBAR, x: ML, y: MT, w: CW, h: 0.045 });
  slide.addText(`Syz Research · ${F.DOC_TYPE} · ${F.DATE}`, {
    x: ML, y: H - MB - 0.02, w: CW / 2, h: 0.2, fontFace: FONT, fontSize: T_LABEL, color: LIGHT, bold: true, margin: 0, isTextBox: true, valign: "bottom" });
  slide.addText(`${pageNo} / 3`, {
    x: W - MR - CW / 2, y: H - MB - 0.02, w: CW / 2, h: 0.2, fontFace: FONT, fontSize: T_LABEL, color: LIGHT, bold: true, margin: 0, align: "right", isTextBox: true, valign: "bottom" });
  return MT + 0.045 + 0.16;   // y after the gradient rule
}

// ---- flow helpers (all return the new y)
function para(slide, y, text, opts = {}) {
  const pt = opts.pt || T_BODY, w = opts.w || CW, x = opts.x || ML;
  const h = hOf(text, pt, w) + 0.02;
  slide.addText(text, { x, y, w, h, fontFace: FONT, fontSize: pt, color: opts.color || NAVY, bold: true,
    align: opts.align || "justify", valign: "top", margin: 0, isTextBox: true, lineSpacingMultiple: mult(LH), paraSpaceAfter: 0 });
  return y + h + (opts.gap === undefined ? 0.087 : opts.gap);
}
function h2(slide, y, text) {
  slide.addText(text, { x: ML, y, w: CW, h: 0.24, fontFace: FONT, fontSize: T_HEAD, color: NAVY, bold: true, margin: 0, isTextBox: true, valign: "top" });
  return y + 0.24 + 0.03;
}
function chartTitle(slide, y, num, title, sub) {
  slide.addText([{ text: `Chart ${num}`, options: { color: ORANGE } }, { text: ` · ${title}`, options: { color: NAVY } }],
    { x: ML, y, w: CW, h: 0.19, fontFace: FONT, fontSize: T_BODY, bold: true, margin: 0, isTextBox: true, valign: "top" });
  y += 0.19;
  const hs = hOf(sub, T_LABEL, CW, 1.3);
  slide.addText(sub, { x: ML, y, w: CW, h: hs, fontFace: FONT, fontSize: T_LABEL, color: GREY, bold: true, margin: 0, isTextBox: true, valign: "top", lineSpacingMultiple: mult(1.3) });
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
s.addText(F.DOC_TYPE, { x: ML, y, w: CW, h: 0.17, fontFace: FONT, fontSize: T_LABEL, color: ORANGE, bold: true, charSpacing: 1.2, margin: 0, isTextBox: true, valign: "top" });
y += 0.2;
const th = hOf(F.TITLE, T_TITLE, CW, 1.22);
s.addText(F.TITLE, { x: ML, y, w: CW, h: th, fontFace: FONT, fontSize: T_TITLE, color: NAVY, bold: true, margin: 0, isTextBox: true, valign: "top", lineSpacingMultiple: mult(1.22) });
y += th + 0.04;
s.addText(`${F.DATE} · Syz Research`, { x: ML, y, w: CW, h: 0.18, fontFace: FONT, fontSize: T_BODY, color: GREY, bold: true, margin: 0, isTextBox: true, valign: "top" });
y += 0.18 + 0.13;

if (F.QUOTE) {
  const qw = CW - 0.2, qh = hOf(F.QUOTE, T_BODY, qw, 1.35);
  s.addShape(pres.ShapeType.rect, { x: ML, y, w: 0.047, h: qh + 0.26, fill: { color: ORANGE }, line: { color: ORANGE, width: 0 } });
  s.addText(`“${F.QUOTE}”`, { x: ML + 0.2, y: y + 0.02, w: qw, h: qh, fontFace: FONT, fontSize: T_BODY, color: NAVY, bold: true, margin: 0, isTextBox: true, valign: "top", lineSpacingMultiple: mult(1.35) });
  s.addText(F.QUOTE_WHO, { x: ML + 0.2, y: y + qh + 0.06, w: qw, h: 0.17, fontFace: FONT, fontSize: T_LABEL, color: GREY, bold: true, margin: 0, isTextBox: true, valign: "top" });
  y += qh + 0.26 + 0.13;
}

// company introduction: one body paragraph directly below the quote, no box
y = para(s, y, F.COMPANY_INTRO, { gap: 0.13 });

y = h2(s, y, "Key takeaways");
for (const t of F.TAKEAWAYS) {
  const col = t.tag === "pos" ? MINT : t.tag === "neg" ? ORANGE : BLUEB;
  const tw = CW - 0.65, hh = hOf(t.text, T_BODY, tw);
  s.addText(t.label, { x: ML, y: y + 0.015, w: 0.63, h: hh, fontFace: FONT, fontSize: T_LABEL, color: col, bold: true, charSpacing: 0.8, margin: 0, isTextBox: true, valign: "top" });
  s.addText(t.text, { x: ML + 0.65, y: y - 0.01, w: tw, h: hh, fontFace: FONT, fontSize: T_BODY, color: NAVY, bold: true, margin: 0, isTextBox: true, valign: "top", lineSpacingMultiple: mult(LH) });
  y += hh + 0.05;
}
y += 0.08;

// key numbers strip: the only box on the page
const kh = 0.70;
s.addShape(pres.ShapeType.rect, { x: ML, y, w: CW, h: kh, fill: { color: WHITE }, line: { color: NAVY, width: 1.3 } });
F.KPIS.forEach((k, i) => {
  const cx = ML + (CW / 4) * i, cw = CW / 4;
  if (i > 0) s.addShape(pres.ShapeType.line, { x: cx, y: y, w: 0, h: kh, line: { color: HAIR, width: 0.6 } });
  s.addText(k.label, { x: cx + 0.12, y: y + 0.08, w: cw - 0.2, h: 0.15, fontFace: FONT, fontSize: T_LABEL, color: GREY, bold: true, margin: 0, isTextBox: true, valign: "top" });
  s.addText(k.value, { x: cx + 0.12, y: y + 0.23, w: cw - 0.2, h: 0.22, fontFace: FONT, fontSize: T_HEAD, color: NAVY, bold: true, margin: 0, isTextBox: true, valign: "top" });
  s.addText(k.sub, { x: cx + 0.12, y: y + 0.46, w: cw - 0.2, h: 0.15, fontFace: FONT, fontSize: T_LABEL, color: k.sign === "pos" ? MINT : k.sign === "neg" ? ORANGE : BLUEB, bold: true, margin: 0, isTextBox: true, valign: "top" });
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
const uh = hOf(F.UPSIDE, T_BODY, colW), dh = hOf(F.DOWNSIDE, T_BODY, colW), ch = Math.max(uh, dh) + 0.22;
s.addShape(pres.ShapeType.line, { x: ML + CW / 2, y, w: 0, h: ch, line: { color: HAIR, width: 0.6 } });
s.addText("What would strengthen our view", { x: ML, y, w: colW, h: 0.17, fontFace: FONT, fontSize: T_LABEL, color: ORANGE, bold: true, charSpacing: 1, margin: 0, isTextBox: true, valign: "top" });
s.addText(F.UPSIDE, { x: ML, y: y + 0.21, w: colW, h: uh, fontFace: FONT, fontSize: T_BODY, color: NAVY, bold: true, margin: 0, isTextBox: true, valign: "top", lineSpacingMultiple: mult(LH) });
s.addText("What would change our view", { x: ML + CW / 2 + 0.2, y, w: colW, h: 0.17, fontFace: FONT, fontSize: T_LABEL, color: ORANGE, bold: true, charSpacing: 1, margin: 0, isTextBox: true, valign: "top" });
s.addText(F.DOWNSIDE, { x: ML + CW / 2 + 0.2, y: y + 0.21, w: colW, h: dh, fontFace: FONT, fontSize: T_BODY, color: NAVY, bold: true, margin: 0, isTextBox: true, valign: "top", lineSpacingMultiple: mult(LH) });
y += ch;
console.log("page 1 bottom:", y.toFixed(2), "limit:", (H - MB - 0.25).toFixed(2));

// ================= PAGE 2
s = pres.addSlide();
y = chrome(s, 2);
if (F.P2_TITLE) {
  s.addText(F.P2_TITLE, { x: ML, y, w: CW, h: 0.36, fontFace: FONT, fontSize: T_TITLE, color: NAVY, bold: true, margin: 0, isTextBox: true, valign: "top" });
  y += 0.36 + 0.08;
}
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
console.log("page 2 bottom:", y.toFixed(2), "limit:", (H - MB - 0.25).toFixed(2));

// ================= PAGE 3: source + disclaimer pinned to the bottom
s = pres.addSlide();
chrome(s, 3);
const legal = F.DISCLAIMER;
let lh = 0;
const parts = legal.map(p => { const h = hOf(p, T_LABEL, CW, 1.4) + 0.06; lh += h; return h; });
const srcH = 0.2, headH = 0.2;
let ly = H - MB - 0.35 - lh - srcH - headH - 0.16;
s.addText([{ text: "SYZ", options: { color: ORANGE } }, { text: ` ${F.SOURCE_LINE}`, options: { color: LIGHT } }],
  { x: ML, y: ly, w: CW, h: srcH, fontFace: FONT, fontSize: T_LABEL, bold: true, margin: 0, isTextBox: true, valign: "top" });
ly += srcH + 0.16;
s.addText("Disclaimer", { x: ML, y: ly, w: CW, h: headH, fontFace: FONT, fontSize: T_LABEL, color: ORANGE, bold: true, charSpacing: 1.2, margin: 0, isTextBox: true, valign: "top" });
ly += headH;
legal.forEach((p, i) => {
  s.addText(p, { x: ML, y: ly, w: CW, h: parts[i], fontFace: FONT, fontSize: T_LABEL, color: LIGHT, bold: true, align: "justify", margin: 0, isTextBox: true, valign: "top", lineSpacingMultiple: mult(1.4) });
  ly += parts[i];
});

pres.writeFile({ fileName: outPath }).then(() => console.log("written", outPath));
```

**`fill.json` keys** (all strings unless noted): `LOGO`, `GRADBAR` (absolute paths), `DOC_TYPE`, `DATE`, `TITLE`, `QUOTE` (text without quotation marks; empty string to omit the block), `QUOTE_WHO`, `COMPANY_INTRO`, `TAKEAWAYS` (list of `{tag: pos|neg|neu, label, text}`), `KPIS` (four `{label, value, sub, sign: pos|neg|neu}`), `H_P1`, `P1_PARAGRAPH`, `C1_TITLE`, `C1_SUB`, `C1_IMG`, `C1_ASPECT` (image height/width), `W1` (number, % of text width), `C1_COMMENT`, `BASE_CASE`, `UPSIDE`, `DOWNSIDE`, `P2_TITLE`, `H_A1`, `A1_PARAGRAPHS` (list of two), `H_A2`, `A2_PARAGRAPH`, `H_C2`, `C2_TITLE`, `C2_SUB`, `C2_IMG`, `C2_ASPECT`, `W2`, `C2_COMMENT`, `SOURCE_LINE`, `DISCLAIMER` (list of the seven fixed paragraphs, taken verbatim from the HTML template with `&rsquo;` turned into a real apostrophe). There is no `THEME` key any more. Generate `fill.json` from the same `content.py` as the PDF (`html.unescape` on every string, `−` turned into `-`) so the two deliverables cannot drift.

**Defaults for the PPTX:** `W1` = 66 (range 66 to 70), `W2` = 88 (range 80 to 90): the PowerPoint runs the charts a few points narrower than the PDF to keep both pages inside the guard line with the same word budgets. The font face is Nunito; on a machine without Nunito, PowerPoint substitutes and line breaks may shift slightly.

**Build, validate, render:**
```bash
node /home/claude/build_pptx.js fill.json Earnings_Update_<Ticker>_<QxYYYY>.pptx     # prints "page N bottom: x limit: y"
python3 /mnt/skills/public/pptx/scripts/office/validate.py Earnings_Update_<Ticker>_<QxYYYY>.pptx
python3 /mnt/skills/public/pptx/scripts/office/soffice.py --headless --convert-to pdf Earnings_Update_<Ticker>_<QxYYYY>.pptx
pdftoppm -jpeg -r 100 Earnings_Update_<Ticker>_<QxYYYY>.pdf slide    # then Read slide-1.jpg, slide-2.jpg, slide-3.jpg
```
If a page bottom exceeds the limit, lower `W1`/`W2` by 2 to 4 points (minimum 66 / 80), then tighten prose to the lower end of the budgets; never change type sizes or margins. The metric is conservative (LibreOffice usually renders with a little more room), but the printed bottoms must be below the limit before delivery.

## Text format
**Page plan (fixed):**
- **Page 1, executive investment summary** (for every reader, including private clients; carries ~80% of the message): kicker ("Earnings update", nothing else) → title → dateline → management quote (optional, orange left rule) → **company introduction** (one short paragraph, always present, directly below the quote or, without a quote, below the dateline) → **Key takeaways** heading + 3 to 4 tagged lines → the **key numbers strip** (the only box on the page: one Space Blue border, four columns separated by hairlines) → heading + 1 paragraph on what the quarter means for the investment case, opening with the surprise and the publication-day reaction → Chart 1 + 1 comment paragraph → **Base case and implications** heading + 1 paragraph that carries **our stance and positioning in plain words, never a rating label** (the regime for the stock, the earnings path we underwrite, the catalyst, the tactical qualifier, the next test) → two text columns with a hairline divider, **What would strengthen our view** / **What would change our view**. One box on page 1, never more: structure comes from headings, tags and the column divider.
- **Page 2, "Beyond the key takeaways"** (fixed page title, 17pt ExtraBold, for readers who want the why): heading + 2 paragraphs on the results and their drivers, the second of which carries the surprise vs. reaction read → heading + 1 paragraph on outlook and guidance → heading + Chart 2 + 1 comment paragraph on valuation. **No positioning or implications section on page 2**: positioning lives in the page-1 base case. Page 2 builds on page 1 without repeating it: page 1 states the conclusion, page 2 shows the evidence.
- **Page 3:** gradient rule, source line and the fixed disclaimer pinned to the bottom. Nothing else.

**Word budgets (calibrated to fit, do not exceed):**
| Element | Words |
|---|---|
| Management quote | 20 to 35, plus a one-line attribution (name, role, event, date; or company statement wording) |
| Company introduction | 25 to 36, one paragraph |
| Key takeaways | 3 to 4 lines, ≤ 18 words each, one number in each |
| KPI tiles | 4 tiles: label, value, surprise vs. consensus (or vs. guide), sub line short enough for one line |
| Investment-case paragraph (H_P1) | 55 to 65 |
| Chart 1 comment | 50 to 55 |
| Base case and implications paragraph (with positioning) | 80 to 90 |
| Strengthen / change columns | 34 to 38 each |
| Results paragraphs (H_A1) | 100 to 115 and 90 to 105 (the second carries the reaction read) |
| Outlook paragraph (H_A2) | 95 to 110 |
| Chart 2 comment | 85 to 100 |

With the quote block and the company introduction both present, page 1 is full at these budgets: keep the investment-case paragraph and the two columns at the lower end, and lower `W1` before cutting anything else. Never recover space with a smaller type size. Calibration (26 Oct 2026, text metric at 0.49 em per character): introduction 36 words, investment case 60, Chart 1 comment 55, base case 85, columns 36 each, quote 25, four takeaways, gives a PPTX page-1 bottom of 10.77 vs. the 10.95 guard at `W1` 66, and fits the PDF at `W1` 74 with room to spare.

**Element rules:**
- **Title:** `<Company> <Qx YYYY>: <conviction message in sentence case>`, ≤ ~70 characters, e.g. "ASML Q3 2026: orders confirm the upcycle, valuation leaves little slack", "VAT Group Q3 2026: record orders rewrite 2027, upgrades carry the stock". It states the verdict, not the topic. The kicker above it reads "Earnings update" only: no sector, theme, ticker or date appended.
- **Management quote:** lead with it only when it carries the investment message (tone on demand, a guidance commitment, a change of stance). Verbatim from the transcript, the release or stockanalysis.com (see Inputs), in `&ldquo;…&rdquo;`, attributed with name, role, event and date, or as a company statement. Omit rather than invent.
- **Company introduction:** 25 to 36 words, body size, directly below the quote. Two or three sentences a private client can read cold: what the company makes or does and for whom, where it earns its money (segments, geographies or end markets with one share figure), and its scale (revenue or market capitalisation with currency, listing). Facts from the annual report or IR material only; no adjectives, no verdict, no repetition of the takeaways. Example: "ASML is the sole supplier of extreme ultraviolet lithography systems, the machines that print the most advanced chips. Systems are three quarters of sales; 2025 revenue EUR 32bn. Listed in Amsterdam, market value around EUR 600bn."
- **Key takeaways:** each line = tag + one fact with a number + its implication. Together they must give a client the whole story in 30 seconds: result, guidance, the main risk, the valuation verdict. When surprise and reaction diverge, one line (tag "Reaction") states the move and the confirmed reason in ≤ 18 words.
- **KPI tiles:** the four lines that decided the quarter (typically revenue, EPS, a margin, next-period guidance; for a trading update: orders, sales, backlog, next-quarter sales guide). Surprise in % or bp, sign-coloured.
- **Section headings (h2):** four variable ones per document (H_P1, H_A1, H_A2, H_C2), plus the two fixed page-1 headings "Key takeaways" and "Base case and implications" and the fixed page-2 title. Each is a takeaway in sentence case, ≤ ~45 characters, no full stop, e.g. "Results: the beat was mix, not volume", "Outlook: Q4 is capacity-bound, 2027 is reset", "Valuation: the work is done by earnings". Don't repeat the H1's verdict. Plain 11pt ExtraBold Space Blue, no rule or accent.
- **Chart titles in the PDF:** `<span class="num">Chart N</span> &middot; <Ticker>: <descriptor>`. **Chart sub-line:** one line of methodology (series, window, consensus source, MA, log scale, shading), joined by `&middot;`; disclose stale or partial data here (e.g. "Last price is the 14 October close, before the release"; "Q3 2025 and Q2 2026 derived from reported growth rates").
- **Surprise vs. market reaction (mandatory, every document):** every mention of a beat or a miss is read **together with the share price move on the publication day**, with both numbers in the same sentence ("Revenue beat consensus by 4% and EPS by 6%, yet the shares fell 5.1% on 15 October, against a sector up 0.3%"). The investment-case paragraph on page 1 opens with this pairing; the second results paragraph on page 2 develops it. When the two **diverge** (beat and down, miss and up, or a move out of proportion to the surprise), the text must name the divergence and explain it, testing in turn: guidance or outlook below expectations; margin or mix deterioration behind the headline; elevated expectations and positioning into the print (the run-up into results, the pre-results multiple vs. its averages, the "whisper" vs. the published consensus); valuation; the quality of the beat (one-offs, FX, tax, pull-forward); disappointing underlying trends (orders, backlog, pricing, cash conversion, a segment); and sector or market moves on the same day. **Separate confirmed drivers from plausible interpretations** with explicit wording: a confirmed driver is a reported number or a management statement ("the Q4 guide of EUR 9.6bn, 2% below consensus", "management said the China mix will fall further"); a plausible interpretation is our reading of positioning, expectations or valuation and is marked as such ("we think", "the most likely reading is", "this is consistent with, but not confirmed by"). Never present an interpretation as a fact and never report a beat or a miss without the reaction. When surprise and reaction are aligned, one sentence pairs them and the paragraph moves on to the drivers.
- **Base case and implications paragraph:** 4 to 6 sentences: the regime for the stock and what we would do, expressed as a view and an action in plain words ("We stay positive on VAT and would add on ramp-related weakness", "We keep the position and see the risk/reward as balanced at this multiple", "We would wait for the Q4 guide before adding"), the earnings path we underwrite with numbers, where the debate has moved, the catalyst (upgrade cycle, multiple vs. its averages), the tactical qualifier (positioning, expectations into the print), and the next test with its date. **Never use rating labels anywhere in the document**: no "Buy", "Hold", "Sell", "Overweight", "Underweight", "Accumulate", "Reduce", "Outperform", "Neutral" as a rating, and no target price. Stance is conveyed by the verb (stay positive, remain constructive, keep, add, trim, wait, prefer), the earnings path and the risk/reward. No list of triggers inside it; those go in the columns.
- **Strengthen / change columns:** 2 to 3 concrete, observable triggers each (a number, a date, a decision), not generic risk language.
- **Page 2 valuation comment:** read Chart 2 explicitly: price vs. EPS trend (is price running ahead of earnings? give both 12-month changes), P/E vs. its average and the premium in %, where it came from (previous print, peak), price vs. 40-week MA, and what multiple the base case implies (e.g. "a 10% upgrade at an unchanged price takes the multiple to 36.5x, the long-run average").

**Style rules (mandatory):**
- **Sentence case throughout**: titles, headings, page-2 title, box heads, tags, chart titles, legends. Uppercase only where grammatically required (tickers, index names, acronyms such as EUV, EPS, P/E).
- **Never name brokers or sell-side houses** anywhere in the document, the charts or the source line: no "UBS", "BNP Paribas", "Deutsche Bank", no bank price targets, no peer preferences attributed to a bank. Use neutral wording: "analyst expectations", "analyst estimates published after the release range from X to Y", "several analysts expect EPS upgrades of 10% or more", "analyst first takes", "analyst research notes of <date>". Consensus is "consensus" or "Bloomberg consensus". Broker names may appear in the reply to the user (for the Bloomberg check), not in the deliverables.
- **No rating labels or target prices** anywhere in the deliverables (see the base case rule): the words Buy, Hold, Sell, Overweight, Underweight, Accumulate, Reduce and Outperform do not appear as recommendations; a grep in QA must come back clean or every hit must be a non-recommendation use ("sell-through", "holds 40% of the market") and is then rewritten anyway if it could be read as a rating.
- **No em dashes** anywhere (text, charts, headings). Use a comma, a colon or `&ndash;` only for numeric ranges (2022&ndash;25). Prefer "2010 to 2026" in prose.
- **Typography**: exactly four sizes, 17 / 11 / 8.7 / 7 pt, with the roles set in the Typography section; Nunito Bold (700) for body and ExtraBold (800) for headings, titles, box heads, KPI values, chart titles and quote text. No Light, Regular or SemiBold anywhere, and no size outside the four.
- **Boxes**: only the key numbers strip is boxed: Space Blue `#202945` border 0.45mm, straight corners, no fill. No other box on either page, no blue-filled backgrounds, no rounded corners.
- **Negative indicators**: Tiger Orange `#FF6C0E` for bearish or negative tags, bars and KPI deltas, never purple.
- **Sources**: `Source: Syz Research, Bloomberg…` with no full stop at the end, on page 3 and in every chart footnote.
- Typography uses HTML entities: `&ndash;` for ranges, `&rsquo;` for apostrophes, `&ldquo;…&rdquo;` for quotes, `&amp;`, `&middot;` for separators, `&minus;` for a minus sign in KPI tiles.

**Voice:**
- Institutional, quantified and decisive; first person plural ("We read this as…", "We stay…"). Page 1 is readable by a private client: plain words, every acronym used once in full, no jargon that needs a footnote. Page 2 can be more technical (mix, incremental margins, revisions, multiples).
- Every claim carries a number: reported vs. consensus in % or bp, guidance in ranges, EPS to one decimal, P/E to one decimal and its premium to the average in %, the publication-day move in % with its date, "highest since <Qx YYYY>" computed from the data.
- Separate signal from noise: a one-off (FX, tax rate, a pulled-forward order) is named and stripped from the read. For an orders-driven print, say what the company states about double bookings or ordering windows.
- No bullet lists outside the Key takeaways block, no exclamation marks, no marketing adjectives. British spelling (stabilised, programme, licence).
- Never invent numbers, consensus figures or quotes. Anything taken from the web is dated in the text and flagged in the reply for a Bloomberg check.

## Fit & QA (mandatory)
1. The PDF must be **exactly 3 pages**. Page 1 ends with the two strengthen/change columns; page 2 starts with the page title "Beyond the key takeaways" and the results heading and ends with the Chart 2 valuation comment; page 3 holds only the source line and the disclaimer.
2. **If a page overflows,** apply these levers in order: reduce `W1` (minimum 66) or `W2` (minimum 76 in the PDF, 80 in the PPTX) by 2 to 4 points; tighten the prose to the lower end of the budgets. Never change font sizes, margins, colours, headings or the page plan. Never let a heading or the key numbers strip sit alone at the bottom of a page. If page 2 has spare room, widen `W2` (up to 94 in the PDF, 90 in the PPTX) rather than adding text.
3. **Rasterise all three pages at 100 dpi and look at them.** Check for:
   - logo top-right and gradient rule on every page (a missing logo means a broken PNG, see Setup);
   - kicker reads "Earnings update" only, with nothing after it; the company introduction sits directly below the quote (or below the dateline when there is no quote) and above "Key takeaways";
   - exactly one box on page 1 (the key numbers strip): Space Blue border, square corners, no fill, four columns in one row, every `sub` line on one line;
   - tags: negative ones in Tiger Orange; no purple anywhere;
   - no em dash in any text or chart; sentence case everywhere; no broker name anywhere (`pdftotext … | grep -i "UBS\|BNP\|Deutsche\|Goldman\|Morgan\|Barclays\|Jefferies"` returns nothing);
   - no rating label anywhere (`pdftotext … | grep -iw "buy\|hold\|sell\|overweight\|underweight\|accumulate\|outperform"` returns nothing, apart from the fixed disclaimer's "buy or sell"; the same grep on `fill.json`);
   - the publication-day reaction appears with a number and a date, paired with the surprise, in the page-1 investment-case paragraph and in the page-2 results paragraphs; if surprise and reaction diverge, the divergence is named and the explanation separates confirmed drivers from interpretations with explicit wording;
   - four section headings and the page-2 title on one line each;
   - footer reads "Syz Research · Earnings update · <date>" with a space after each dot;
   - Chart 2 legible: legend, end labels (price, EPS, P/E) and the P/E average line visible, no label collisions;
   - page 3: source line (no full stop) followed by the full disclaimer, pinned above the footer.
4. Run `pdffonts` on the output: only Nunito Bold and Nunito ExtraBold (shown as Nunito-Ultra-Bold) may be embedded. Check the type scale: `grep -o "font-size: [0-9.]*pt" template.html | sort -u` returns exactly 17pt, 11pt, 8.7pt and 7pt, and `grep -o "fontSize: [A-Z_0-9.]*" build_pptx.js | sort -u` returns only `T_TITLE`, `T_HEAD`, `T_BODY`, `T_LABEL` (or `pt` inside `para`). Any other value is a defect to fix before delivery.
5. **PowerPoint:** `validate.py` passes; `build_pptx.js` reports both page bottoms below the limit; the three LibreOffice-rendered slides show the same layout as the PDF pages (one box on page 1, the introduction under the quote, no text touching the next heading, footer and logo on every slide, disclaimer pinned to the bottom of slide 3); `markitdown` shows three slides with no leftover placeholder text, no broker name and no rating label.
6. In the reply, report: the data window and last date (and whether the last price is pre-results); the 3 to 5 numbers the document turns on (surprise, publication-day reaction, guidance, P/E and premium); whether surprise and reaction were aligned or divergent and the confirmed driver; the quote source and the source of the company introduction; any figure or quote taken from outside the user's files that needs verifying, including the reaction figure if web-sourced and the broker first takes the neutral wording summarises.

## Reference instances
**ASML Q3 2026 (14 October 2026)**
- **Data:** `ASML.xlsx`, weekly, 1 Jan 2010 to 14 Oct 2026; last price EUR 1,541.8, 12m-forward EPS EUR 50.3, 40-week MA EUR 1,386, 12m-forward P/E 30.6x vs. a 26.0x average since 2010 (an 18% premium).
- **Chart 1:** `bar_chart` of surprises vs. consensus (revenue, gross margin, EBIT, EPS, Q4 guide, FY27 outlook).
- **Chart 2:** `price_eps_pe_chart`, title "ASML: share price vs. consensus earnings and valuation", footnote `source_line("Bloomberg", "14 Oct 2026", "ASML NA Equity, weekly", "BEst 12m-forward consensus", "40-week simple MA", "Log scale", "P/E shaded above (orange) / below (blue) its 2010-26 average")`.
- **Headings pattern:** "What the quarter means for the investment case" · "Results: the beat was mix, not volume" · "Outlook: guidance leans on EUV and services" · "Valuation: the upcycle is priced, the next leg is not".
- Built before the company introduction, the reaction rule and the four-size scale were added: when reusing it as a model, add the introduction, pair every beat with the day-1 move and apply the current type scale.

**VAT Group Q3 2026 trading update (15 October 2026)**
- **Data:** `VAT.xlsx`, weekly, window from 27 May 2016 (first consensus EPS) to 15 Oct 2026; last price CHF 635 (the 14 October close, before the release), 12m-forward EPS CHF 15.8, 40-week MA CHF 594, 12m-forward P/E 40.3x vs. a 36.1x average since 2016 (an 11.5% premium), one-year average 47x.
- **Inputs:** Bloomberg export, a Finanz und Wirtschaft first assessment, a Bloomberg-sourced summary of analyst first takes; figures cross-checked against the EQS ad hoc release. No executive quoted in the release and no transcript yet, so the quote block carried a verbatim company statement from the release.
- **Chart 1:** `bar_chart` of quarterly order intake in CHF m (Q3 2025 reported, Q2 2026 previous record, Q3 2026 consensus, Q3 2026 reported in orange), title "VACN: Q3 2026 order intake vs. consensus and history".
- **Title:** "VAT Group Q3 2026: record orders rewrite 2027, upgrades carry the stock". **Headings:** "The debate shifts from demand to delivery" · "Results: orders tripled, sales inflected" · "Outlook: Q4 is capacity-bound, 2027 is reset" · "Valuation: the work is done by earnings".
- **Fit (pre-introduction layout):** PDF `W1` 72 / `W2` 94; PPTX `W1` 66 / `W2` 90; page bottoms 10.85 and 10.43 vs. the 10.95 guard. With the introduction added, run the PPTX at `W1` 66 and keep page-1 prose at the lower end of the budgets.
