import pandas as pd
import numpy as np
from sqlalchemy import create_engine

engine = create_engine("sqlite:///darkstore_analytics.db")
df = pd.read_csv("darkstore_clean.csv")
store_annual = pd.read_csv("store_annual_pnl.csv")

print("=" * 55)
print("   QUICKCOMMERCE — DEEP BUSINESS ANALYSIS")
print("=" * 55)

# ══════════════════════════════════════════════════════
# ANALYSIS 1 — Close vs Fix vs Expand Decision
# ══════════════════════════════════════════════════════
print("\n📊 ANALYSIS 1 — Store Action Recommendations:")

def recommend_action(row):
    if row["Annual_CM"] < 0:
        return "🔴 CLOSE — Negative CM"
    elif row["Avg_CM_Pct"] < 3:
        return "🟠 FIX URGENTLY — CM% < 3%"
    elif row["Avg_CM_Pct"] < 8:
        return "🟡 IMPROVE — Below Average"
    elif row["Avg_CM_Pct"] >= 14:
        return "🟢 EXPAND — Star Store"
    else:
        return "🔵 MAINTAIN — Healthy"

store_annual["Recommendation"] = store_annual.apply(recommend_action, axis=1)
action_summary = store_annual[["Store_Name","Company","City",
                                "Avg_CM_Pct","Annual_CM","Recommendation"]]
print(action_summary.sort_values("Annual_CM", ascending=False).to_string(index=False))

# ══════════════════════════════════════════════════════
# ANALYSIS 2 — Revenue Impact of Closing Bad Stores
# ══════════════════════════════════════════════════════
print("\n📊 ANALYSIS 2 — Financial Impact of Recommendations:")

close_stores = store_annual[store_annual["Annual_CM"] < 0]
fix_stores = store_annual[store_annual["Avg_CM_Pct"].between(0, 3)]
expand_stores = store_annual[store_annual["Avg_CM_Pct"] >= 14]

print(f"\n🔴 Stores to CLOSE: {len(close_stores)}")
print(f"   Annual losses saved: ₹{abs(close_stores['Annual_CM'].sum()):,.0f}")

print(f"\n🟠 Stores to FIX URGENTLY: {len(fix_stores)}")
print(f"   Potential CM if improved to 8%: ₹{(fix_stores['Annual_Revenue'].sum()*0.08):,.0f}")
print(f"   Current CM: ₹{fix_stores['Annual_CM'].sum():,.0f}")
print(f"   Improvement potential: ₹{(fix_stores['Annual_Revenue'].sum()*0.08 - fix_stores['Annual_CM'].sum()):,.0f}")

print(f"\n🟢 Star Stores to EXPAND: {len(expand_stores)}")
for _, row in expand_stores.iterrows():
    print(f"   {row['Store_Name']} ({row['City']}) — {row['Avg_CM_Pct']}% CM")

# ══════════════════════════════════════════════════════
# ANALYSIS 3 — Which City to Expand Next?
# ══════════════════════════════════════════════════════
print("\n📊 ANALYSIS 3 — City Expansion Opportunity:")

city_metrics = df.groupby("City").agg(
    Avg_CM_Pct       = ("CM_Percentage", "mean"),
    Avg_Daily_Orders = ("Daily_Orders", "mean"),
    Avg_Revenue      = ("Revenue", "mean"),
    Stores           = ("Store_ID", "nunique")
).round(2).reset_index()

city_metrics["Revenue_Per_Store"] = (
    city_metrics["Avg_Revenue"] / 100000
).round(2)

city_metrics["Expansion_Score"] = (
    city_metrics["Avg_CM_Pct"] * 0.5 +
    city_metrics["Avg_Daily_Orders"] / 10 * 0.3 +
    city_metrics["Revenue_Per_Store"] * 0.2
).round(2)

city_metrics = city_metrics.sort_values("Expansion_Score", ascending=False)
print(city_metrics[["City","Stores","Avg_CM_Pct",
                     "Avg_Daily_Orders","Expansion_Score"]].to_string(index=False))

print(f"\n✅ Best city for next dark store: {city_metrics.iloc[0]['City']}")
print(f"   Reason: Highest expansion score based on CM%, orders, and revenue")

# ══════════════════════════════════════════════════════
# ANALYSIS 4 — Inventory Waste Deep Dive
# ══════════════════════════════════════════════════════
print("\n📊 ANALYSIS 4 — Inventory Waste Impact:")
total_waste = df["Inventory_Waste"].sum()
avg_waste_pct = (df["Inventory_Waste"].sum() / df["Revenue"].sum() * 100)
print(f"Total annual inventory waste: ₹{total_waste:,.0f}")
print(f"As % of total revenue: {avg_waste_pct:.2f}%")
print(f"If waste reduced by 50%: ₹{total_waste*0.5:,.0f} saved annually")

waste_by_city = df.groupby("City").agg(
    Total_Waste = ("Inventory_Waste", "sum"),
    Waste_Pct   = ("Inventory_Waste", lambda x: (x.sum()/df.loc[x.index,"Revenue"].sum()*100))
).round(2)
print(f"\nWaste by City:\n{waste_by_city.to_string()}")

# ══════════════════════════════════════════════════════
# ANALYSIS 5 — Diwali vs Off-Season Comparison
# ══════════════════════════════════════════════════════
print("\n📊 ANALYSIS 5 — Peak vs Off-Season Performance:")
diwali = df[df["Month_Num"].isin([10, 11])]
offseason = df[df["Month_Num"].isin([7, 8])]

print(f"DIWALI Season (Oct-Nov):")
print(f"  Avg Daily Orders: {diwali['Daily_Orders'].mean():.0f}")
print(f"  Avg CM%: {diwali['CM_Percentage'].mean():.2f}%")
print(f"  Avg Revenue/store: ₹{diwali['Revenue'].mean():,.0f}")

print(f"\nOFF-SEASON (Jul-Aug):")
print(f"  Avg Daily Orders: {offseason['Daily_Orders'].mean():.0f}")
print(f"  Avg CM%: {offseason['CM_Percentage'].mean():.2f}%")
print(f"  Avg Revenue/store: ₹{offseason['Revenue'].mean():,.0f}")

orders_diff = ((diwali['Daily_Orders'].mean() - offseason['Daily_Orders'].mean())
               / offseason['Daily_Orders'].mean() * 100)
print(f"\nDiwali vs Off-Season: {orders_diff:.1f}% more orders during Diwali!")

print("\n🎉 Deep Analysis Complete!")