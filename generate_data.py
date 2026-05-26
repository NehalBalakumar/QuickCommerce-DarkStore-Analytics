import pandas as pd
import numpy as np
import random

# ── Reproducibility ────────────────────────────────────
np.random.seed(42)
random.seed(42)

# ══════════════════════════════════════════════════════
# DARK STORE MASTER DATA
# 25 stores across 5 Indian cities
# ══════════════════════════════════════════════════════
stores = [
    # Bangalore — 8 stores
    {"store_id": "BLR-01", "store_name": "Koramangala Central",  "city": "Bangalore", "zone": "South", "size_sqft": 650, "rent_monthly": 185000, "company": "Blinkit"},
    {"store_id": "BLR-02", "store_name": "Indiranagar Hub",      "city": "Bangalore", "zone": "East",  "size_sqft": 580, "rent_monthly": 165000, "company": "Blinkit"},
    {"store_id": "BLR-03", "store_name": "HSR Layout Store",     "city": "Bangalore", "zone": "South", "size_sqft": 500, "rent_monthly": 145000, "company": "Zepto"},
    {"store_id": "BLR-04", "store_name": "Whitefield Express",   "city": "Bangalore", "zone": "East",  "size_sqft": 450, "rent_monthly": 120000, "company": "Zepto"},
    {"store_id": "BLR-05", "store_name": "Jayanagar Store",      "city": "Bangalore", "zone": "South", "size_sqft": 420, "rent_monthly": 130000, "company": "Blinkit"},
    {"store_id": "BLR-06", "store_name": "Hebbal North",         "city": "Bangalore", "zone": "North", "size_sqft": 380, "rent_monthly": 110000, "company": "Zepto"},
    {"store_id": "BLR-07", "store_name": "Electronic City",      "city": "Bangalore", "zone": "South", "size_sqft": 350, "rent_monthly": 95000,  "company": "Blinkit"},
    {"store_id": "BLR-08", "store_name": "Marathahalli Hub",     "city": "Bangalore", "zone": "East",  "size_sqft": 400, "rent_monthly": 115000, "company": "Zepto"},

    # Mumbai — 6 stores
    {"store_id": "MUM-01", "store_name": "Bandra West Express",  "city": "Mumbai",    "zone": "West",  "size_sqft": 600, "rent_monthly": 220000, "company": "Blinkit"},
    {"store_id": "MUM-02", "store_name": "Andheri Central",      "city": "Mumbai",    "zone": "West",  "size_sqft": 550, "rent_monthly": 195000, "company": "Zepto"},
    {"store_id": "MUM-03", "store_name": "Powai Tech Hub",       "city": "Mumbai",    "zone": "East",  "size_sqft": 480, "rent_monthly": 170000, "company": "Blinkit"},
    {"store_id": "MUM-04", "store_name": "Malad Store",          "city": "Mumbai",    "zone": "West",  "size_sqft": 420, "rent_monthly": 155000, "company": "Zepto"},
    {"store_id": "MUM-05", "store_name": "Thane Express",        "city": "Mumbai",    "zone": "East",  "size_sqft": 400, "rent_monthly": 135000, "company": "Blinkit"},
    {"store_id": "MUM-06", "store_name": "Dadar Hub",            "city": "Mumbai",    "zone": "Central","size_sqft":360, "rent_monthly": 175000, "company": "Zepto"},

    # Delhi NCR — 5 stores
    {"store_id": "DEL-01", "store_name": "Gurugram Cyber City",  "city": "Delhi NCR", "zone": "South", "size_sqft": 580, "rent_monthly": 175000, "company": "Blinkit"},
    {"store_id": "DEL-02", "store_name": "Noida Sector 18",      "city": "Delhi NCR", "zone": "East",  "size_sqft": 520, "rent_monthly": 155000, "company": "Zepto"},
    {"store_id": "DEL-03", "store_name": "South Delhi Store",    "city": "Delhi NCR", "zone": "South", "size_sqft": 480, "rent_monthly": 165000, "company": "Blinkit"},
    {"store_id": "DEL-04", "store_name": "Dwarka Express",       "city": "Delhi NCR", "zone": "West",  "size_sqft": 420, "rent_monthly": 130000, "company": "Zepto"},
    {"store_id": "DEL-05", "store_name": "Rohini North",         "city": "Delhi NCR", "zone": "North", "size_sqft": 380, "rent_monthly": 115000, "company": "Blinkit"},

    # Hyderabad — 3 stores
    {"store_id": "HYD-01", "store_name": "Hitec City Hub",       "city": "Hyderabad", "zone": "West",  "size_sqft": 520, "rent_monthly": 145000, "company": "Blinkit"},
    {"store_id": "HYD-02", "store_name": "Banjara Hills Store",  "city": "Hyderabad", "zone": "Central","size_sqft":460, "rent_monthly": 130000, "company": "Zepto"},
    {"store_id": "HYD-03", "store_name": "Gachibowli Express",   "city": "Hyderabad", "zone": "West",  "size_sqft": 400, "rent_monthly": 115000, "company": "Blinkit"},

    # Chennai — 3 stores
    {"store_id": "CHN-01", "store_name": "Sholinganallur Hub",   "city": "Chennai",   "zone": "South", "size_sqft": 480, "rent_monthly": 125000, "company": "Zepto"},
    {"store_id": "CHN-02", "store_name": "T Nagar Central",      "city": "Chennai",   "zone": "Central","size_sqft":440, "rent_monthly": 140000, "company": "Blinkit"},
    {"store_id": "CHN-03", "store_name": "Anna Nagar Store",     "city": "Chennai",   "zone": "North", "size_sqft": 380, "rent_monthly": 110000, "company": "Zepto"},
]

# ══════════════════════════════════════════════════════
# GENERATE 12 MONTHS OF P&L DATA PER STORE
# ══════════════════════════════════════════════════════
months = [f"2024-{str(m).zfill(2)}" for m in range(1, 13)]
records = []

for store in stores:
    # Base orders depends on store size and city
    city_multiplier = {
        "Bangalore": 1.20, "Mumbai": 1.15,
        "Delhi NCR": 1.10, "Hyderabad": 1.0, "Chennai": 0.95
    }
    size_multiplier = store["size_sqft"] / 500

    base_orders = int(
        random.randint(180, 520) *
        city_multiplier[store["city"]] *
        size_multiplier
    )

    for month in months:
        # Monthly variation — festive season boost
        month_num = int(month.split("-")[1])
        seasonal = 1.0
        if month_num in [10, 11]:  # Diwali season
            seasonal = 1.25
        elif month_num in [7, 8]:  # Monsoon — slight dip
            seasonal = 0.92
        elif month_num in [1, 2]:  # New Year boost
            seasonal = 1.10

        daily_orders = int(base_orders * seasonal * random.uniform(0.88, 1.12))
        monthly_orders = daily_orders * 30

        # Average Order Value — ₹280 to ₹380
        aov = random.randint(280, 380)

        # Revenue
        revenue = monthly_orders * aov

        # COGS — 58% to 64% of revenue
        cogs_pct = random.uniform(0.58, 0.64)
        cogs = revenue * cogs_pct

        # Gross Profit
        gross_profit = revenue - cogs

        # Staff cost — based on store size
        staff_cost = random.randint(160000, 300000)

        # Delivery cost — ₹14 to ₹22 per order
        delivery_cost_per_order = random.uniform(14, 22)
        delivery_cost = monthly_orders * delivery_cost_per_order

        # Inventory waste — 6% to 18% of COGS
        waste_pct = random.uniform(0.06, 0.18)
        inventory_waste = cogs * waste_pct

        # Discounts & marketing — 2% to 5% of revenue
        discount_pct = random.uniform(0.02, 0.05)
        discounts = revenue * discount_pct

        # Utilities
        utilities = random.randint(25000, 55000)

        # Total costs
        total_costs = (
            store["rent_monthly"] +
            staff_cost +
            delivery_cost +
            inventory_waste +
            discounts +
            utilities
        )

        # Contribution Margin
        contribution_margin = gross_profit - total_costs

        # CM per order
        cm_per_order = contribution_margin / monthly_orders if monthly_orders > 0 else 0

        # Profitable?
        profitable = "Yes" if contribution_margin > 0 else "No"

        records.append({
            "Store_ID":              store["store_id"],
            "Store_Name":            store["store_name"],
            "Company":               store["company"],
            "City":                  store["city"],
            "Zone":                  store["zone"],
            "Size_SqFt":             store["size_sqft"],
            "Month":                 month,
            "Month_Num":             month_num,
            "Daily_Orders":          daily_orders,
            "Monthly_Orders":        monthly_orders,
            "Avg_Order_Value":       aov,
            "Revenue":               round(revenue, 0),
            "COGS":                  round(cogs, 0),
            "Gross_Profit":          round(gross_profit, 0),
            "Rent":                  store["rent_monthly"],
            "Staff_Cost":            staff_cost,
            "Delivery_Cost":         round(delivery_cost, 0),
            "Inventory_Waste":       round(inventory_waste, 0),
            "Discounts":             round(discounts, 0),
            "Utilities":             utilities,
            "Total_Operating_Cost":  round(total_costs, 0),
            "Contribution_Margin":   round(contribution_margin, 0),
            "CM_Per_Order":          round(cm_per_order, 2),
            "Profitable":            profitable,
        })

# ── Build DataFrame ────────────────────────────────────
df = pd.DataFrame(records)

# ── Save ───────────────────────────────────────────────
df.to_csv("darkstore_pnl.csv", index=False)

# ── Summary ────────────────────────────────────────────
print("=" * 55)
print("   QUICKCOMMERCE DARK STORE DATASET GENERATED!")
print("=" * 55)
print(f"\nTotal Records:  {len(df)} (25 stores × 12 months)")
print(f"Total Columns:  {len(df.columns)}")
print(f"\nCities covered: {df['City'].unique().tolist()}")
print(f"Companies:      {df['Company'].unique().tolist()}")
print(f"\nProfitable months:     {(df['Profitable']=='Yes').sum()}")
print(f"Loss-making months:    {(df['Profitable']=='No').sum()}")
print(f"\nAvg Monthly Revenue:   ₹{df['Revenue'].mean():,.0f}")
print(f"Avg Contribution Margin: ₹{df['Contribution_Margin'].mean():,.0f}")
print(f"\nTop 5 rows:")
print(df[['Store_Name','City','Month','Revenue',
          'Contribution_Margin','Profitable']].head())
print(f"\n✅ Saved as darkstore_pnl.csv")