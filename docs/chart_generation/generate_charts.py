"""
Generate charts from Gold layer models in DuckDB warehouse.
Output: charts/*.png
"""

import os
import duckdb
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import numpy as np

# ---- Config ----
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../.."))
DUCKDB_PATH = os.getenv(
    "DUCKDB_PATH", os.path.join(BASE_DIR, "duckdb_warehouse", "warehouse.duckdb")
)
CHARTS_DIR = os.path.join(os.path.dirname(__file__), "charts")
os.makedirs(CHARTS_DIR, exist_ok=True)

conn = duckdb.connect(DUCKDB_PATH, read_only=True)

# ---- Style ----
plt.rcParams.update(
    {
        "figure.facecolor": "#1a1a2e",
        "axes.facecolor": "#16213e",
        "axes.edgecolor": "#e94560",
        "axes.labelcolor": "#eaeaea",
        "text.color": "#eaeaea",
        "xtick.color": "#aaaaaa",
        "ytick.color": "#aaaaaa",
        "grid.color": "#2a2a4a",
        "grid.alpha": 0.5,
        "font.family": "sans-serif",
        "font.size": 12,
    }
)

PALETTE = [
    "#e94560",
    "#0f3460",
    "#533483",
    "#16c79a",
    "#f5a623",
    "#48dbfb",
    "#ff6b6b",
    "#feca57",
    "#54a0ff",
    "#5f27cd",
]


def save(fig, name):
    path = os.path.join(CHARTS_DIR, f"{name}.png")
    fig.savefig(path, dpi=150, bbox_inches="tight", facecolor=fig.get_facecolor())
    plt.close(fig)
    print(f"  ✅ {path}")


# ================================================================
# 1. Total Revenue & Profit  (KPI Cards style)
# ================================================================
print("[1/10] Total Revenue & Profit")
df = conn.execute("SELECT total_revenue, total_profit FROM total_revenue_profit").df()
rev, prof = df.iloc[0]
fig, ax = plt.subplots(figsize=(8, 3))
ax.axis("off")
ax.text(0.25, 0.7, "Total Revenue", ha="center", va="center", fontsize=16, color="#aaa")
ax.text(
    0.25,
    0.25,
    f"${rev:,.0f}",
    ha="center",
    va="center",
    fontsize=32,
    fontweight="bold",
    color="#16c79a",
)
ax.text(0.75, 0.7, "Total Profit", ha="center", va="center", fontsize=16, color="#aaa")
ax.text(
    0.75,
    0.25,
    f"${prof:,.0f}",
    ha="center",
    va="center",
    fontsize=32,
    fontweight="bold",
    color="#e94560",
)
ax.axvline(0.5, 0.1, 0.9, color="#333", lw=2)
fig.suptitle("Overall Business KPIs", fontsize=18, fontweight="bold", y=0.98)
save(fig, "01_total_revenue_profit")


# ================================================================
# 2. Revenue by Segment  (Horizontal Bar)
# ================================================================
print("[2/10] Revenue by Segment")
df = conn.execute(
    "SELECT segment, revenue, profit FROM revenue_by_segment WHERE segment IS NOT NULL ORDER BY revenue DESC"
).df()
df["segment"] = df["segment"].astype(str)
fig, ax = plt.subplots(figsize=(9, 4))
y = range(len(df))
bars = ax.barh(
    list(y), df["revenue"], color=PALETTE[: len(df)], height=0.5, edgecolor="none"
)
for i, (r, p) in enumerate(zip(df["revenue"], df["profit"])):
    ax.text(
        r + 30000,
        i,
        f"${r:,.0f}  (Profit: ${p:,.0f})",
        va="center",
        fontsize=11,
        color="#eee",
    )
ax.set_yticks(list(y))
ax.set_yticklabels(df["segment"], fontsize=13)
ax.set_xlabel("Revenue ($)")
ax.set_title(
    "Revenue & Profit by Customer Segment", fontsize=16, fontweight="bold", pad=12
)
ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"${x/1e6:.1f}M"))
ax.invert_yaxis()
ax.grid(axis="x")
save(fig, "02_revenue_by_segment")


# ================================================================
# 3. Profit Margin by Market  (Bar chart)
# ================================================================
print("[3/10] Profit Margin by Market")
df = conn.execute(
    "SELECT market, profit_margin FROM profit_margin_by_market WHERE market IS NOT NULL ORDER BY profit_margin DESC"
).df()
df["market"] = df["market"].astype(str)
fig, ax = plt.subplots(figsize=(9, 5))
bars = ax.bar(
    df["market"],
    df["profit_margin"] * 100,
    color=PALETTE[: len(df)],
    width=0.55,
    edgecolor="none",
)
for bar, v in zip(bars, df["profit_margin"] * 100):
    ax.text(
        bar.get_x() + bar.get_width() / 2,
        bar.get_height() + 0.5,
        f"{v:.1f}%",
        ha="center",
        va="bottom",
        fontsize=12,
        fontweight="bold",
        color="#eee",
    )
ax.set_ylabel("Profit Margin (%)")
ax.set_title("Profit Margin by Market Region", fontsize=16, fontweight="bold", pad=12)
ax.grid(axis="y")
save(fig, "03_profit_margin_by_market")


# ================================================================
# 4. Top 10 Products  (Horizontal Bar)
# ================================================================
print("[4/10] Top 10 Products")
df = conn.execute("SELECT product_name, order_count, revenue FROM top_10_products").df()
df["short_name"] = df["product_name"].astype(str).str[:30]
fig, ax = plt.subplots(figsize=(10, 6))
y = range(len(df))
bars = ax.barh(
    list(y), df["revenue"], color=PALETTE[: len(df)], height=0.6, edgecolor="none"
)
for i, (r, cnt) in enumerate(zip(df["revenue"], df["order_count"])):
    ax.text(
        r + 500, i, f"${r:,.0f}  ({cnt} orders)", va="center", fontsize=10, color="#ccc"
    )
ax.set_yticks(list(y))
ax.set_yticklabels(df["short_name"], fontsize=10)
ax.set_xlabel("Revenue ($)")
ax.set_title("Top 10 Best-Selling Products", fontsize=16, fontweight="bold", pad=12)
ax.invert_yaxis()
ax.grid(axis="x")
save(fig, "04_top_10_products")


# ================================================================
# 5. Top 15 Countries by Revenue  (Bar chart)
# ================================================================
print("[5/10] Top 15 Countries by Revenue")
df = conn.execute(
    "SELECT country, revenue FROM top_15_countries_by_revenue WHERE country IS NOT NULL ORDER BY revenue DESC"
).df()
df["country"] = df["country"].astype(str)
fig, ax = plt.subplots(figsize=(12, 5))
bars = ax.bar(
    range(len(df)),
    df["revenue"],
    color=[PALETTE[i % len(PALETTE)] for i in range(len(df))],
    width=0.65,
    edgecolor="none",
)
ax.set_xticks(range(len(df)))
ax.set_xticklabels(df["country"], rotation=40, ha="right", fontsize=10)
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"${x/1e3:.0f}K"))
ax.set_ylabel("Revenue ($)")
ax.set_title("Top 15 Countries by Revenue", fontsize=16, fontweight="bold", pad=12)
ax.grid(axis="y")
save(fig, "05_top_15_countries")


# ================================================================
# 6. Monthly Revenue + YoY Change  (Line + Area)
# ================================================================
print("[6/10] Monthly Revenue YoY")
df = conn.execute(
    "SELECT month_date, revenue, change_pct FROM monthly_revenue_yoy ORDER BY month_date"
).df()
df["month_date"] = df["month_date"].astype(str)
fig, ax1 = plt.subplots(figsize=(12, 5))
ax1.fill_between(df["month_date"], df["revenue"], alpha=0.3, color="#16c79a")
ax1.plot(
    df["month_date"],
    df["revenue"],
    color="#16c79a",
    linewidth=2,
    marker="o",
    markersize=3,
    label="Revenue",
)
ax1.set_ylabel("Revenue ($)", color="#16c79a")
ax1.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"${x/1e3:.0f}K"))
ax1.set_xticks(range(0, len(df), 3))
ax1.set_xticklabels(df["month_date"].iloc[::3], rotation=30, ha="right", fontsize=9)
ax2 = ax1.twinx()
ax2.bar(
    df["month_date"],
    df["change_pct"].fillna(0),
    width=0.4,
    alpha=0.4,
    color="#e94560",
    label="MoM Change %",
)
ax2.set_ylabel("MoM Change (%)", color="#e94560")
ax2.axhline(0, color="#555", lw=1, ls="--")
fig.suptitle("Monthly Revenue Trend & MoM Change %", fontsize=16, fontweight="bold")
ax1.grid(axis="y")
save(fig, "06_monthly_revenue_yoy")


# ================================================================
# 7. Average Discount by Category  (Bar chart)
# ================================================================
print("[7/10] Avg Discount by Category")
df = conn.execute(
    "SELECT category, avg_discount FROM avg_discount_by_category WHERE category IS NOT NULL ORDER BY avg_discount DESC"
).df()
df["category"] = df["category"].astype(str)
fig, ax = plt.subplots(figsize=(9, 5))
bars = ax.bar(
    df["category"],
    df["avg_discount"] * 100,
    color=PALETTE[: len(df)],
    width=0.5,
    edgecolor="none",
)
for bar, v in zip(bars, df["avg_discount"] * 100):
    ax.text(
        bar.get_x() + bar.get_width() / 2,
        bar.get_height() + 0.1,
        f"{v:.1f}%",
        ha="center",
        va="bottom",
        fontsize=11,
        color="#eee",
    )
ax.set_ylabel("Average Discount (%)")
ax.set_title(
    "Average Discount Rate by Product Category", fontsize=16, fontweight="bold", pad=12
)
ax.grid(axis="y")
save(fig, "07_avg_discount_by_category")


# ================================================================
# 8. RFM Segment Distribution  (Pie chart)
# ================================================================
print("[8/10] Customer RFM Segments")
df = conn.execute(
    """
    SELECT 
        CASE 
            WHEN TRY_CAST(rfm_segment AS INT) >= 444 THEN 'Champions (444-555)'
            WHEN TRY_CAST(rfm_segment AS INT) >= 333 THEN 'Loyal (333-443)'
            WHEN TRY_CAST(rfm_segment AS INT) >= 222 THEN 'At Risk (222-332)'
            ELSE 'Lost (111-221)'
        END AS segment_label,
        COUNT(*) as cnt
    FROM customer_rfm_segments
    GROUP BY segment_label
    ORDER BY cnt DESC
"""
).df()
df["segment_label"] = df["segment_label"].astype(str)
fig, ax = plt.subplots(figsize=(8, 6))
wedges, texts, autotexts = ax.pie(
    df["cnt"],
    labels=df["segment_label"],
    autopct="%1.1f%%",
    colors=["#16c79a", "#f5a623", "#e94560", "#533483"],
    textprops={"fontsize": 12},
    pctdistance=0.75,
    startangle=140,
)
for t in autotexts:
    t.set_fontweight("bold")
ax.set_title(
    "Customer RFM Segment Distribution", fontsize=16, fontweight="bold", pad=12
)
save(fig, "08_rfm_segments")


# ================================================================
# 9. Loss Orders by Segment  (Donut chart)
# ================================================================
print("[9/10] Loss Orders by Segment")
df = conn.execute(
    "SELECT segment, loss_order_count FROM loss_orders_by_segment WHERE segment IS NOT NULL ORDER BY loss_order_count DESC"
).df()
df["segment"] = df["segment"].astype(str)
fig, ax = plt.subplots(figsize=(7, 6))
wedges, texts, autotexts = ax.pie(
    df["loss_order_count"],
    labels=df["segment"],
    autopct="%1.1f%%",
    colors=["#e94560", "#0f3460", "#533483"],
    textprops={"fontsize": 12},
    pctdistance=0.78,
    startangle=90,
    wedgeprops={"width": 0.5},
)
for t in autotexts:
    t.set_fontweight("bold")
centre = plt.Circle((0, 0), 0.35, fc="#1a1a2e")
ax.add_artist(centre)
total = df["loss_order_count"].sum()
ax.text(
    0,
    0,
    f"{total:,}\nLoss Orders",
    ha="center",
    va="center",
    fontsize=14,
    fontweight="bold",
    color="#e94560",
)
ax.set_title(
    "Loss Orders Distribution by Segment", fontsize=16, fontweight="bold", pad=12
)
save(fig, "09_loss_orders_by_segment")


# ================================================================
# 10. Customers by Gender & Occupation  (Grouped Bar)
# ================================================================
print("[10/10] Customers by Gender & Occupation")
df = conn.execute(
    "SELECT gender, occupation, customer_count FROM customers_by_gender_occupation WHERE occupation IS NOT NULL AND gender IS NOT NULL ORDER BY occupation, gender"
).df()
df["occupation"] = df["occupation"].astype(str)
df["gender"] = df["gender"].astype(str)
occupations = df["occupation"].unique()
genders = df["gender"].unique()
x = np.arange(len(occupations))
width = 0.35
fig, ax = plt.subplots(figsize=(10, 5))
for i, g in enumerate(genders):
    subset = df[df["gender"] == g]
    vals = [
        (
            subset[subset["occupation"] == o]["customer_count"].values[0]
            if len(subset[subset["occupation"] == o]) > 0
            else 0
        )
        for o in occupations
    ]
    offset = (i - 0.5) * width
    bars = ax.bar(
        x + offset,
        vals,
        width,
        label=f"Gender: {g}",
        color=PALETTE[i],
        edgecolor="none",
    )
    for bar, v in zip(bars, vals):
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height() + 30,
            str(v),
            ha="center",
            va="bottom",
            fontsize=9,
            color="#ccc",
        )
ax.set_xticks(x)
ax.set_xticklabels(occupations, rotation=20, ha="right", fontsize=10)
ax.set_ylabel("Customer Count")
ax.set_title(
    "Customer Distribution by Gender & Occupation",
    fontsize=16,
    fontweight="bold",
    pad=12,
)
ax.legend(loc="upper right")
ax.grid(axis="y")
save(fig, "10_customers_gender_occupation")


conn.close()
print(f"\n🎉 All 10 charts saved to {CHARTS_DIR}/")
