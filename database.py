import pandas as pd
from sqlalchemy import create_engine

# ── Load clean data ────────────────────────────────────
df = pd.read_csv("darkstore_clean.csv")
store_annual = pd.read_csv("store_annual_pnl.csv")

print("=" * 55)
print("   QUICKCOMMERCE — SQL DATABASE + QUERIES")
print("=" * 55)

# ══════════════════════════════════════════════════════
# STEP 1 — Create SQLite Database
# ══════════════════════════════════════════════════════
engine = create_engine("sqlite:///darkstore_analytics.db")
df.to_sql("monthly_pnl", engine, if_exists="replace", index=False)
store_annual.to_sql("store_summary", engine, if_exists="replace", index=False)
print("\n✅ Database created: darkstore_analytics.db")
print("   Tables: monthly_pnl, store_summary")

# ══════════════════════════════════════════════════════
# QUERY 1 — Store Profitability Ranking
# ══════════════════════════════════════════════════════
q1 = """
SELECT Store_Name, Company, City,
       ROUND(Annual_Revenue/10000000.0, 2) as Revenue_Cr,
       ROUND(Annual_CM/10000000.0, 2) as CM_Cr,
       ROUND(Avg_CM_Pct, 2) as CM_Pct,
       Profitable_Months,
       Profitable
FROM store_summary
ORDER BY Annual_CM DESC
"""
print("\n📊 QUERY 1 — All Stores Ranked by Profitability:")
print(pd.read_sql(q1, engine).to_string(index=False))

# ══════════════════════════════════════════════════════
# QUERY 2 — Blinkit vs Zepto Head to Head
# ══════════════════════════════════════════════════════
q2 = """
SELECT Company,
       COUNT(*) as Total_Stores,
       ROUND(SUM(Annual_Revenue)/10000000.0, 2) as Total_Revenue_Cr,
       ROUND(SUM(Annual_CM)/10000000.0, 2) as Total_CM_Cr,
       ROUND(AVG(Avg_CM_Pct), 2) as Avg_CM_Pct,
       SUM(Profitable_Months) as Total_Profitable_Months,
       SUM(CASE WHEN Profitable = '✅ Profitable' THEN 1 ELSE 0 END) as Fully_Profitable_Stores
FROM store_summary
GROUP BY Company
"""
print("\n📊 QUERY 2 — Blinkit vs Zepto Head to Head:")
print(pd.read_sql(q2, engine).to_string(index=False))

# ══════════════════════════════════════════════════════
# QUERY 3 — City Performance Ranking
# ══════════════════════════════════════════════════════
q3 = """
SELECT City,
       COUNT(*) as Stores,
       ROUND(SUM(Annual_Revenue)/10000000.0, 2) as Revenue_Cr,
       ROUND(SUM(Annual_CM)/10000000.0, 2) as CM_Cr,
       ROUND(AVG(Avg_CM_Pct), 2) as Avg_CM_Pct,
       SUM(CASE WHEN Profitable = '✅ Profitable' THEN 1 ELSE 0 END) as Profitable_Stores
FROM store_summary
GROUP BY City
ORDER BY CM_Cr DESC
"""
print("\n📊 QUERY 3 — City Performance Ranking:")
print(pd.read_sql(q3, engine).to_string(index=False))

# ══════════════════════════════════════════════════════
# QUERY 4 — Cost Driver Analysis
# What is eating profits most?
# ══════════════════════════════════════════════════════
q4 = """
SELECT City,
       ROUND(AVG(Rent)/AVG(Revenue)*100, 2) as Rent_Pct,
       ROUND(AVG(Staff_Cost)/AVG(Revenue)*100, 2) as Staff_Pct,
       ROUND(AVG(Delivery_Cost)/AVG(Revenue)*100, 2) as Delivery_Pct,
       ROUND(AVG(Inventory_Waste)/AVG(Revenue)*100, 2) as Waste_Pct,
       ROUND(AVG(Discounts)/AVG(Revenue)*100, 2) as Discount_Pct
FROM monthly_pnl
GROUP BY City
ORDER BY Waste_Pct DESC
"""
print("\n📊 QUERY 4 — Cost Driver Analysis (% of Revenue):")
print(pd.read_sql(q4, engine).to_string(index=False))

# ══════════════════════════════════════════════════════
# QUERY 5 — Seasonal Trend
# Which month has best performance?
# ══════════════════════════════════════════════════════
q5 = """
SELECT Month,
       ROUND(AVG(Daily_Orders), 0) as Avg_Daily_Orders,
       ROUND(AVG(Contribution_Margin)/10000, 2) as Avg_CM_Lakhs,
       ROUND(AVG(CM_Percentage), 2) as Avg_CM_Pct
FROM monthly_pnl
GROUP BY Month
ORDER BY Month
"""
print("\n📊 QUERY 5 — Monthly Seasonal Trend:")
print(pd.read_sql(q5, engine).to_string(index=False))

print("\n🎉 All SQL Queries Complete!")