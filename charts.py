import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import seaborn as sns
import numpy as np

# ── Setup ──────────────────────────────────────────────
df = pd.read_csv("darkstore_clean.csv")
store_annual = pd.read_csv("store_annual_pnl.csv")
sns.set_theme(style="darkgrid")
plt.rcParams["figure.figsize"] = (12, 6)

# ══════════════════════════════════════════════════════
# CHART 1 — Store Profitability Ranking (Horizontal Bar)
# Top vs Bottom stores at a glance
# ══════════════════════════════════════════════════════
fig, ax = plt.subplots(figsize=(12, 8))
sorted_stores = store_annual.sort_values("Annual_CM")
colors = ["#e74c3c" if x < 0 else "#f39c12" if x < 500000
          else "#27ae60" for x in sorted_stores["Annual_CM"]]
bars = ax.barh(sorted_stores["Store_Name"],
               sorted_stores["Annual_CM"] / 100000,
               color=colors, edgecolor="none")
ax.axvline(x=0, color="white", linewidth=1.5, linestyle="--")
ax.set_title("Dark Store Annual Contribution Margin — All 25 Stores\n(Red=Close | Orange=Fix | Green=Healthy)",
             fontsize=13, fontweight="bold", pad=15)
ax.set_xlabel("Annual Contribution Margin (₹ Lakhs)")
ax.set_ylabel("")
red_p = mpatches.Patch(color="#e74c3c", label="Close (Negative CM)")
orange_p = mpatches.Patch(color="#f39c12", label="Fix Urgently (CM < ₹5L)")
green_p = mpatches.Patch(color="#27ae60", label="Healthy / Expand")
ax.legend(handles=[red_p, orange_p, green_p], loc="lower right")
plt.tight_layout()
plt.savefig("chart1_store_profitability.png", dpi=150, bbox_inches="tight")
plt.close()
print("✅ Chart 1 saved — Store Profitability Ranking")

# ══════════════════════════════════════════════════════
# CHART 2 — Cost Driver Breakdown by City
# Which cost is eating profits most?
# ══════════════════════════════════════════════════════
city_costs = df.groupby("City").agg(
    Rent         = ("Rent", "mean"),
    Staff        = ("Staff_Cost", "mean"),
    Delivery     = ("Delivery_Cost", "mean"),
    Waste        = ("Inventory_Waste", "mean"),
    Discounts    = ("Discounts", "mean")
).reset_index()

fig, ax = plt.subplots(figsize=(12, 6))
x = np.arange(len(city_costs["City"]))
width = 0.15
costs = ["Rent","Staff","Delivery","Waste","Discounts"]
colors_costs = ["#3498db","#e74c3c","#f39c12","#9b59b6","#1abc9c"]
for i, (cost, color) in enumerate(zip(costs, colors_costs)):
    ax.bar(x + i*width, city_costs[cost]/1000,
           width, label=cost, color=color, alpha=0.85)
ax.set_title("Cost Driver Breakdown by City\n(Which cost eats most profits?)",
             fontsize=13, fontweight="bold")
ax.set_xticks(x + width*2)
ax.set_xticklabels(city_costs["City"])
ax.set_ylabel("Average Monthly Cost (₹ Thousands)")
ax.legend()
plt.tight_layout()
plt.savefig("chart2_cost_drivers.png", dpi=150, bbox_inches="tight")
plt.close()
print("✅ Chart 2 saved — Cost Driver Breakdown")

# ══════════════════════════════════════════════════════
# CHART 3 — Monthly Seasonal Trend
# When do dark stores perform best?
# ══════════════════════════════════════════════════════
monthly = df.groupby("Month_Num").agg(
    Avg_Orders = ("Daily_Orders", "mean"),
    Avg_CM_Pct = ("CM_Percentage", "mean"),
    Avg_Revenue = ("Revenue", "mean")
).reset_index()
month_names = ["Jan","Feb","Mar","Apr","May","Jun",
               "Jul","Aug","Sep","Oct","Nov","Dec"]
monthly["Month_Name"] = [month_names[i-1] for i in monthly["Month_Num"]]

fig, ax1 = plt.subplots(figsize=(12, 6))
ax2 = ax1.twinx()
bars = ax1.bar(monthly["Month_Name"], monthly["Avg_Revenue"]/100000,
               alpha=0.6, color="#3498db", label="Avg Revenue (₹L)")
line = ax2.plot(monthly["Month_Name"], monthly["Avg_CM_Pct"],
                color="#e74c3c", linewidth=2.5, marker="o",
                markersize=8, label="CM%")
ax1.set_title("Monthly Seasonal Trend — Revenue vs Contribution Margin %",
              fontsize=13, fontweight="bold")
ax1.set_ylabel("Avg Monthly Revenue (₹ Lakhs)", color="#3498db")
ax2.set_ylabel("Contribution Margin %", color="#e74c3c")
ax1.annotate("🎆 Diwali Peak!", xy=(9, monthly["Avg_Revenue"].iloc[9]/100000),
             xytext=(7, monthly["Avg_Revenue"].max()/100000 * 0.95),
             arrowprops=dict(arrowstyle="->", color="white"),
             color="white", fontsize=10)
lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax1.legend(lines1+lines2, labels1+labels2, loc="upper left")
plt.tight_layout()
plt.savefig("chart3_seasonal_trend.png", dpi=150, bbox_inches="tight")
plt.close()
print("✅ Chart 3 saved — Seasonal Trend")

# ══════════════════════════════════════════════════════
# CHART 4 — CM% Heatmap (Store × Month)
# Which store struggles in which month?
# ══════════════════════════════════════════════════════
pivot = df.pivot_table(
    index="Store_Name",
    columns="Month_Num",
    values="CM_Percentage",
    aggfunc="mean"
)
pivot.columns = month_names

fig, ax = plt.subplots(figsize=(14, 10))
sns.heatmap(pivot, annot=True, fmt=".1f", cmap="RdYlGn",
            center=0, linewidths=0.3, ax=ax,
            cbar_kws={"label": "CM%"})
ax.set_title("Contribution Margin % Heatmap — Store × Month\n(Red=Loss | Yellow=Break-even | Green=Profitable)",
             fontsize=13, fontweight="bold")
ax.set_xlabel("Month")
ax.set_ylabel("")
plt.tight_layout()
plt.savefig("chart4_cm_heatmap.png", dpi=150, bbox_inches="tight")
plt.close()
print("✅ Chart 4 saved — CM% Heatmap")

# ══════════════════════════════════════════════════════
# CHART 5 — Blinkit vs Zepto Performance Comparison
# ══════════════════════════════════════════════════════
company_monthly = df.groupby(["Company","Month_Num"]).agg(
    Avg_CM_Pct = ("CM_Percentage","mean"),
    Avg_Orders = ("Daily_Orders","mean")
).reset_index()

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
for company, color in [("Blinkit","#f39c12"),("Zepto","#9b59b6")]:
    data = company_monthly[company_monthly["Company"]==company]
    ax1.plot([month_names[m-1] for m in data["Month_Num"]],
             data["Avg_CM_Pct"], marker="o", linewidth=2.5,
             color=color, label=company, markersize=7)
    ax2.plot([month_names[m-1] for m in data["Month_Num"]],
             data["Avg_Orders"], marker="s", linewidth=2.5,
             color=color, label=company, markersize=7)

ax1.set_title("Blinkit vs Zepto — CM% Monthly Trend",
              fontsize=12, fontweight="bold")
ax1.set_ylabel("Contribution Margin %")
ax1.legend()
ax1.tick_params(axis="x", rotation=45)

ax2.set_title("Blinkit vs Zepto — Daily Orders Monthly Trend",
              fontsize=12, fontweight="bold")
ax2.set_ylabel("Avg Daily Orders per Store")
ax2.legend()
ax2.tick_params(axis="x", rotation=45)

plt.suptitle("Blinkit vs Zepto — Head to Head Performance",
             fontsize=14, fontweight="bold", y=1.02)
plt.tight_layout()
plt.savefig("chart5_blinkit_vs_zepto.png", dpi=150, bbox_inches="tight")
plt.close()
print("✅ Chart 5 saved — Blinkit vs Zepto")

# ══════════════════════════════════════════════════════
# CHART 6 — City Expansion Opportunity
# ══════════════════════════════════════════════════════
city_data = df.groupby("City").agg(
    CM_Pct = ("CM_Percentage","mean"),
    Daily_Orders = ("Daily_Orders","mean"),
    Revenue = ("Revenue","mean")
).reset_index()

fig, ax = plt.subplots(figsize=(10, 7))
scatter = ax.scatter(
    city_data["Daily_Orders"],
    city_data["CM_Pct"],
    s=city_data["Revenue"]/5000,
    c=["#27ae60","#3498db","#e74c3c","#f39c12","#9b59b6"],
    alpha=0.8, edgecolors="white", linewidth=2
)
for _, row in city_data.iterrows():
    ax.annotate(row["City"],
                (row["Daily_Orders"], row["CM_Pct"]),
                textcoords="offset points", xytext=(10, 5),
                fontsize=11, color="white", fontweight="bold")

ax.axhline(y=city_data["CM_Pct"].mean(), color="white",
           linestyle="--", alpha=0.5, label="Avg CM%")
ax.set_title("City Expansion Opportunity Matrix\n(Bubble size = Average Revenue | X = Orders | Y = CM%)",
             fontsize=13, fontweight="bold")
ax.set_xlabel("Average Daily Orders per Store")
ax.set_ylabel("Average Contribution Margin %")
ax.legend()
plt.tight_layout()
plt.savefig("chart6_city_expansion.png", dpi=150, bbox_inches="tight")
plt.close()
print("✅ Chart 6 saved — City Expansion Matrix")

print("\n🎉 All 6 charts saved successfully!")