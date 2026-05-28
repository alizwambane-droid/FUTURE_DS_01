# ============================================================
# FUTURE INTERNS – Task 1: Business Sales Performance Analytics
# Tool: Python (Google Colab ready)
# Repository: FUTURE_DS_01
# ============================================================

# STEP 1: Install & Import Libraries
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import seaborn as sns
import warnings
warnings.filterwarnings("ignore")

sns.set_theme(style="whitegrid")
plt.rcParams["figure.figsize"] = (12, 5)

# ============================================================
# STEP 2: Load the Dataset
# Upload sales_data.csv to Colab first, then run this cell
# ============================================================
df = pd.read_csv("sales_data.csv", parse_dates=["Date"])
print("Dataset Shape:", df.shape)
print("\nFirst 5 rows:")
df.head()

# ============================================================
# STEP 3: Data Cleaning & Overview
# ============================================================
print("Missing values:\n", df.isnull().sum())
print("\nData types:\n", df.dtypes)
print("\nBasic Stats:\n", df.describe())

# Add Month and Year columns
df["Month"] = df["Date"].dt.month_name()
df["Month_Num"] = df["Date"].dt.month
df["Year"] = df["Date"].dt.year

# ============================================================
# STEP 4: KPI Summary
# ============================================================
total_revenue = df["Revenue"].sum()
total_orders = df["Order_ID"].nunique()
avg_order_value = df["Revenue"].mean()
top_region = df.groupby("Region")["Revenue"].sum().idxmax()

print("\n========== KEY PERFORMANCE INDICATORS ==========")
print(f"  Total Revenue     : ${total_revenue:,.2f}")
print(f"  Total Orders      : {total_orders:,}")
print(f"  Avg Order Value   : ${avg_order_value:,.2f}")
print(f"  Top Region        : {top_region}")
print("=================================================")

# ============================================================
# STEP 5: Revenue by Region (Bar Chart)
# ============================================================
region_rev = df.groupby("Region")["Revenue"].sum().sort_values(ascending=False)

fig, ax = plt.subplots()
bars = ax.bar(region_rev.index, region_rev.values, color=sns.color_palette("Blues_d", len(region_rev)))
ax.set_title("Total Revenue by Region", fontsize=16, fontweight="bold")
ax.set_xlabel("Region")
ax.set_ylabel("Revenue (USD)")
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"${x:,.0f}"))
for bar in bars:
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 500,
            f"${bar.get_height():,.0f}", ha="center", va="bottom", fontsize=9)
plt.tight_layout()
plt.savefig("revenue_by_region.png", dpi=150)
plt.show()

# ============================================================
# STEP 6: Revenue by Category (Pie Chart)
# ============================================================
cat_rev = df.groupby("Category")["Revenue"].sum()

fig, ax = plt.subplots(figsize=(8, 8))
ax.pie(cat_rev, labels=cat_rev.index, autopct="%1.1f%%",
       colors=sns.color_palette("Set2", len(cat_rev)), startangle=140)
ax.set_title("Revenue Share by Category", fontsize=16, fontweight="bold")
plt.tight_layout()
plt.savefig("revenue_by_category.png", dpi=150)
plt.show()

# ============================================================
# STEP 7: Top 10 Best-Selling Products (Horizontal Bar)
# ============================================================
top_products = df.groupby("Product")["Revenue"].sum().sort_values(ascending=False).head(10)

fig, ax = plt.subplots(figsize=(12, 6))
bars = ax.barh(top_products.index[::-1], top_products.values[::-1],
               color=sns.color_palette("viridis", 10))
ax.set_title("Top 10 Products by Revenue", fontsize=16, fontweight="bold")
ax.set_xlabel("Revenue (USD)")
ax.xaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"${x:,.0f}"))
plt.tight_layout()
plt.savefig("top_products.png", dpi=150)
plt.show()

# ============================================================
# STEP 8: Monthly Revenue Trend (Line Chart)
# ============================================================
monthly_rev = df.groupby("Month_Num")["Revenue"].sum().reset_index()
month_names = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
monthly_rev["Month_Name"] = monthly_rev["Month_Num"].apply(lambda x: month_names[x-1])

fig, ax = plt.subplots()
ax.plot(monthly_rev["Month_Name"], monthly_rev["Revenue"],
        marker="o", color="#4C72B0", linewidth=2.5, markersize=8)
ax.fill_between(monthly_rev["Month_Name"], monthly_rev["Revenue"], alpha=0.15, color="#4C72B0")
ax.set_title("Monthly Revenue Trend (2024)", fontsize=16, fontweight="bold")
ax.set_xlabel("Month")
ax.set_ylabel("Revenue (USD)")
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"${x:,.0f}"))
plt.tight_layout()
plt.savefig("monthly_trend.png", dpi=150)
plt.show()

# ============================================================
# STEP 9: Region × Category Heatmap
# ============================================================
heatmap_data = df.pivot_table(index="Region", columns="Category", values="Revenue", aggfunc="sum")

fig, ax = plt.subplots(figsize=(12, 5))
sns.heatmap(heatmap_data, annot=True, fmt=".0f", cmap="YlGnBu", linewidths=0.5, ax=ax)
ax.set_title("Revenue Heatmap: Region × Category", fontsize=16, fontweight="bold")
plt.tight_layout()
plt.savefig("heatmap_region_category.png", dpi=150)
plt.show()

# ============================================================
# STEP 10: Insights & Recommendations (Print Report)
# ============================================================
best_category = df.groupby("Category")["Revenue"].sum().idxmax()
worst_category = df.groupby("Category")["Revenue"].sum().idxmin()
best_month_num = monthly_rev.loc[monthly_rev["Revenue"].idxmax(), "Month_Name"]
top_product = top_products.index[0]

print("""
╔══════════════════════════════════════════════════════════╗
║         BUSINESS SALES PERFORMANCE – INSIGHTS REPORT    ║
╚══════════════════════════════════════════════════════════╝
""")
print(f"1. REVENUE LEADER: '{top_region}' region generated the highest revenue.")
print(f"2. TOP CATEGORY : '{best_category}' drives the most sales value.")
print(f"3. LOWEST CATEGORY: '{worst_category}' underperforms – review pricing or marketing.")
print(f"4. PEAK MONTH   : '{best_month_num}' had the highest monthly revenue – leverage seasonality.")
print(f"5. STAR PRODUCT : '{top_product}' is the single highest-revenue product.")
print("""
RECOMMENDATIONS:
  → Increase inventory and promotions in the top-performing region.
  → Run targeted campaigns to boost the lowest-performing category.
  → Plan flash sales around the peak month to maximize revenue.
  → Bundle the top product with low-selling items to lift average order value.
  → Apply data-driven discounting – avoid deep discounts on already high-revenue products.
""")
print("All charts saved as PNG files. Upload to your FUTURE_DS_01 GitHub repo.")
