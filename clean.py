import pandas as pd
import numpy as np
from sqlalchemy import create_engine

# ── Load Dataset ───────────────────────────────────────
df = pd.read_csv("darkstore_pnl.csv")

print("=" * 55)
print("   QUICKCOMMERCE — DATA CLEANING + P&L ANALYSIS")
print("=" * 55)

# ══════════════════════════════════════════════════════
# STEP 1 — Basic Data Check
# ══════════════════════════════════════════════════════
print(f"\n📋 Shape: {df.shape}")
print(f"Missing values:\n{df.isnull().sum().sum()} total missing values")
print(f"\nData types:\n{df.dtypes}")

# ══════════════════════════════════════════════════════
# STEP 2 — Add Contribution Margin %
# CM% = (CM / Revenue) × 100
# Tells us what % of revenue becomes profit
# ══════════════════════════════════════════════════════
df["CM_Percentage"] = (df["Contribution_Margin"] / df["Revenue"] * 100).round(2)

print("\n✅ STEP 2 — CM% column added!")

# ══════════════════════════════════════════════════════
# STEP 3 — Break-Even Analysis
# Break-even orders = Fixed Costs / CM per order
# Fixed costs = Rent + Staff + Utilities
# ══════════════════════════════════════════════════════
df["Fixed_Costs"] = df["Rent"] + df["Staff_Cost"] + df["Utilities"]
df["Variable_Cost_Per_Order"] = (
    (df["Delivery_Cost"] + df["Inventory_Waste"] + df["Discounts"])
    / df["Monthly_Orders"]
).round(2)

# Revenue per order = AOV
# Variable cost per order already calculated
# Contribution per order = AOV - Variable cost per order
df["Contribution_Per_Unit"] = (
    df["Avg_Order_Value"] - df["Variable_Cost_Per_Order"]
    - (df["COGS"] / df["Monthly_Orders"])
).round(2)

df["Breakeven_Orders_Monthly"] = (
    df["Fixed_Costs"] / df["Contribution_Per_Unit"]
).round(0)

print("✅ STEP 3 — Break-even analysis done!")

# ══════════════════════════════════════════════════════
# STEP 4 — Store Annual P&L Summary
# Group by store — sum up 12 months
# ══════════════════════════════════════════════════════
store_annual = df.groupby(
    ["Store_ID", "Store_Name", "Company", "City"]
).agg(
    Annual_Revenue        = ("Revenue", "sum"),
    Annual_CM             = ("Contribution_Margin", "sum"),
    Annual_Orders         = ("Monthly_Orders", "sum"),
    Avg_CM_Pct            = ("CM_Percentage", "mean"),
    Avg_Daily_Orders      = ("Daily_Orders", "mean"),
    Profitable_Months     = ("Profitable", lambda x: (x=="Yes").sum()),
    Avg_Inventory_Waste   = ("Inventory_Waste", "mean"),
    Avg_Breakeven_Orders  = ("Breakeven_Orders_Monthly", "mean")
).reset_index()

store_annual["Avg_CM_Pct"] = store_annual["Avg_CM_Pct"].round(2)
store_annual["Avg_Daily_Orders"] = store_annual["Avg_Daily_Orders"].round(0)
store_annual["Profitable"] = store_annual["Profitable_Months"].apply(
    lambda x: "✅ Profitable" if x >= 10 else
              "⚠️ Mixed" if x >= 6 else "❌ Loss-Making"
)

print("\n✅ STEP 4 — Store Annual P&L Summary created!")

# ── Top 5 Stores ───────────────────────────────────────
print("\n🏆 TOP 5 MOST PROFITABLE STORES:")
top5 = store_annual.nlargest(5, "Annual_CM")[
    ["Store_Name","Company","City","Annual_Revenue",
     "Annual_CM","Avg_CM_Pct","Profitable_Months"]
]
print(top5.to_string(index=False))

# ── Bottom 5 Stores ────────────────────────────────────
print("\n🚨 BOTTOM 5 LOSS-MAKING STORES:")
bottom5 = store_annual.nsmallest(5, "Annual_CM")[
    ["Store_Name","Company","City","Annual_Revenue",
     "Annual_CM","Avg_CM_Pct","Profitable_Months"]
]
print(bottom5.to_string(index=False))

# ── Break-even Summary ─────────────────────────────────
print("\n📊 BREAK-EVEN ANALYSIS:")
print(f"Average break-even orders/month: {df['Breakeven_Orders_Monthly'].mean():.0f}")
print(f"Minimum orders needed daily: {df['Breakeven_Orders_Monthly'].mean()/30:.0f}")
avg_breakeven_daily = df["Breakeven_Orders_Monthly"].mean() / 30
stores_below_be = (store_annual["Avg_Daily_Orders"] < avg_breakeven_daily).sum()
print(f"Stores below break-even: {stores_below_be} out of 25")

# ══════════════════════════════════════════════════════
# STEP 5 — Save Clean CSV for Power BI
# ══════════════════════════════════════════════════════
df.to_csv("darkstore_clean.csv", index=False)
store_annual.to_csv("store_annual_pnl.csv", index=False)
print("\n✅ STEP 5 — Clean files saved!")
print("  → darkstore_clean.csv (monthly data)")
print("  → store_annual_pnl.csv (annual store summary)")
print("\n🎉 Cleaning Complete!")