import sys; sys.path.insert(0, "/home/user/syz-earnings")
from syz_charts import *
setup_fonts()
XLSX = "/root/.claude/uploads/3d6ac444-4b93-557a-8d99-6ca7dfb751b9/58ddc5b9-McKesson.xlsx"
PARAMS = dict(ccy="USD", asof="5 Nov 2026", out="/home/claude")
df = load_bloomberg_sheet(XLSX)
df = df[df["eps"].notna() & df["price"].notna() & df["pe"].notna()].reset_index(drop=True)   # drops holidays and the 6 Nov row (no price)
fn2 = source_line("Bloomberg", PARAMS["asof"], "MCK US Equity, daily", "BEst 12m-forward consensus", "40-day simple MA", "Log scale",
                  "P/E shaded above (orange) / below (blue) its 2005-26 average", "Last price is the 5 Nov close")
nums = price_eps_pe_chart(f"{PARAMS['out']}/c2.png", df, "MCK", "MCK: share price vs. consensus earnings and valuation", fn2,
                          ccy="USD", ma_label="40-day moving average", price_lbl=(10, 8), eps_lbl=(10, -20))
crop_for_pdf(f"{PARAMS['out']}/c2.png", f"{PARAMS['out']}/c2_crop.png", "price_eps_pe")
print(nums)
labels = ["Revenue", "Operating profit", "N. Am. Pharma", "Oncology", "Rx Technology", "Med-Surg", "Adj. EPS"]
vals = [0.9, 7.4, 14.8, 3.6, 5.5, -14.8, 9.0]
fn1 = source_line("Bloomberg consensus, company results", PARAMS["asof"], "Segment lines are adjusted operating profit")
bar_chart(f"{PARAMS['out']}/c1.png", labels, vals, "MCK: Q2 2027 results vs. Bloomberg consensus", "Surprise vs. Bloomberg consensus, %", fn1, ylabel="Surprise vs. consensus (%)")
crop_for_pdf(f"{PARAMS['out']}/c1.png", f"{PARAMS['out']}/c1_crop.png", "bar")
from PIL import Image
for n in ("c1", "c2"):
    im = Image.open(f"{PARAMS['out']}/{n}_crop.png"); print(n, im.size, im.size[1]/im.size[0])
