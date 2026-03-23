"""
Sales & Customer Analytics Dashboard
Author  : Lokesh Sangrame | IIIT Bhagalpur
Purpose : Data generation, cleaning, KPI computation & visualization
Stack   : Python, Pandas, NumPy, Matplotlib
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

np.random.seed(42)

# ─────────────────────────────────────────────
# 1. GENERATE SYNTHETIC DATASET
# ─────────────────────────────────────────────

N_CUSTOMERS = 1284
N_PRODUCTS  = 80
START_DATE  = datetime(2022, 4, 1)
END_DATE    = datetime(2024, 3, 31)

REGIONS   = ['north', 'south', 'east', 'west']
SEGMENTS  = ['premium', 'standard', 'basic']
CATEGORIES = ['Electronics', 'Appliances', 'Furniture', 'FMCG', 'Automotive']

# Customers
customers = pd.DataFrame({
    'customer_id': range(1, N_CUSTOMERS + 1),
    'region':      np.random.choice(REGIONS,   N_CUSTOMERS, p=[0.29, 0.24, 0.20, 0.27]),
    'segment':     np.random.choice(SEGMENTS,  N_CUSTOMERS, p=[0.42, 0.40, 0.18]),
    'reg_date':    [START_DATE + timedelta(days=int(d))
                    for d in np.random.randint(0, 365, N_CUSTOMERS)]
})

# Churn: ~14% of customers
churn_mask = np.random.rand(N_CUSTOMERS) < 0.142
customers['churn_dt'] = None
customers.loc[churn_mask, 'churn_dt'] = [
    START_DATE + timedelta(days=int(d))
    for d in np.random.randint(180, 700, churn_mask.sum())
]
customers['is_active'] = customers['churn_dt'].isna()

# Products
products = pd.DataFrame({
    'product_id': range(1, N_PRODUCTS + 1),
    'category':   np.random.choice(CATEGORIES, N_PRODUCTS),
    'unit_price': np.round(np.random.uniform(200, 8000, N_PRODUCTS), 2),
    'cost_price': None
})
products['cost_price'] = np.round(products['unit_price'] * np.random.uniform(0.55, 0.75, N_PRODUCTS), 2)

# Orders (active customers only)
active_ids = customers[customers['is_active']]['customer_id'].values
orders_list = []
for cid in active_ids:
    n = np.random.choice([1,2,3,4,5,6,8,10], p=[0.20,0.22,0.18,0.16,0.10,0.07,0.04,0.03])
    for _ in range(n):
        odate = START_DATE + timedelta(days=int(np.random.randint(0, 730)))
        orders_list.append({'customer_id': cid, 'order_date': odate, 'status':'completed'})

orders = pd.DataFrame(orders_list).reset_index().rename(columns={'index':'order_id'})
orders['order_id'] += 1

# Order Items
items_list = []
for _, row in orders.iterrows():
    n_items = np.random.randint(1, 5)
    pids = np.random.choice(products['product_id'], n_items, replace=False)
    for pid in pids:
        price = float(products.loc[products['product_id']==pid, 'unit_price'].values[0])
        items_list.append({
            'order_id':    row['order_id'],
            'product_id':  pid,
            'quantity':    np.random.randint(1, 4),
            'unit_price':  price,
            'discount_pct': np.random.choice([0, 5, 10, 15], p=[0.55, 0.25, 0.15, 0.05])
        })

items = pd.DataFrame(items_list).reset_index().rename(columns={'index':'item_id'})
items['item_id'] += 1

print("✅ Data generated successfully")
print(f"   Customers : {len(customers):,}")
print(f"   Products  : {len(products):,}")
print(f"   Orders    : {len(orders):,}")
print(f"   Items     : {len(items):,}")


# ─────────────────────────────────────────────
# 2. DATA CLEANING & GOVERNANCE
# ─────────────────────────────────────────────

print("\n── Data Cleaning ──────────────────────────")

# Check nulls
print("Nulls before cleaning:")
print(customers.isnull().sum()[customers.isnull().sum() > 0])

# Remove duplicate orders
before = len(orders)
orders.drop_duplicates(subset=['customer_id', 'order_date'], inplace=True)
print(f"Duplicate orders removed : {before - len(orders)}")

# Validate price > 0
invalid_price = items[items['unit_price'] <= 0]
print(f"Invalid prices found     : {len(invalid_price)}")
items = items[items['unit_price'] > 0]

# Compute net revenue per item
items['net_revenue'] = (
    items['quantity'] * items['unit_price'] * (1 - items['discount_pct'] / 100)
).round(2)

print("✅ Data cleaning complete — audit-ready dataset")


# ─────────────────────────────────────────────
# 3. KPI COMPUTATION
# ─────────────────────────────────────────────

# Merge for full picture
full = (
    orders
    .merge(items,     on='order_id')
    .merge(products,  on='product_id')
    .merge(customers, on='customer_id')
)
full['year']    = pd.DatetimeIndex(full['order_date']).year
full['month']   = pd.DatetimeIndex(full['order_date']).month
full['quarter'] = pd.DatetimeIndex(full['order_date']).quarter

fy24 = full[full['year'] == 2024]
fy23 = full[full['year'] == 2023]

# KPI 1 — Total Revenue
rev24 = fy24['net_revenue'].sum()
rev23 = fy23['net_revenue'].sum()
print(f"\n── KPIs (FY 2023-24) ──────────────────────")
print(f"Total Revenue     : ₹{rev24/100000:.2f}L  (YoY: {(rev24-rev23)/rev23*100:+.1f}%)")

# KPI 2 — Total Orders
ord24 = fy24['order_id'].nunique()
ord23 = fy23['order_id'].nunique()
print(f"Total Orders      : {ord24:,}  (YoY: {(ord24-ord23)/ord23*100:+.1f}%)")

# KPI 3 — AOV
aov24 = fy24.groupby('order_id')['net_revenue'].sum().mean()
print(f"Avg Order Value   : ₹{aov24:,.0f}")

# KPI 4 — Churn Rate
churned  = customers['is_active'].value_counts()[False]
total    = len(customers)
churn_rt = churned / total * 100
print(f"Churn Rate        : {churn_rt:.1f}%")

# KPI 5 — Active Customers
print(f"Active Customers  : {customers['is_active'].sum():,}")


# ─────────────────────────────────────────────
# 4. SEGMENT ANALYSIS
# ─────────────────────────────────────────────

seg_kpis = (
    fy24.groupby('segment')
    .agg(
        revenue   = ('net_revenue',  'sum'),
        orders    = ('order_id',     'nunique'),
        customers = ('customer_id',  'nunique')
    )
    .assign(aov = lambda x: x['revenue'] / x['orders'])
    .assign(rev_share = lambda x: x['revenue'] / x['revenue'].sum() * 100)
    .round(2)
)
print(f"\n── Segment Performance ────────────────────")
print(seg_kpis.to_string())


# ─────────────────────────────────────────────
# 5. VISUALIZATION
# ─────────────────────────────────────────────

fig, axes = plt.subplots(2, 2, figsize=(14, 9))
fig.patch.set_facecolor('#0f1117')
for ax in axes.flat:
    ax.set_facecolor('#1a1d27')
    ax.tick_params(colors='#6b7094', labelsize=9)
    ax.spines[:].set_color('#2e3350')
    ax.title.set_color('#e8eaf6')

# ── Chart 1: Monthly Revenue Trend
ax1 = axes[0, 0]
monthly = (
    full[full['year'].isin([2023,2024])]
    .groupby(['year','month'])['net_revenue']
    .sum().reset_index()
)
for yr, color, ls in [(2024,'#4f8ef7','-'),(2023,'#6b7094','--')]:
    d = monthly[monthly['year']==yr].sort_values('month')
    ax1.plot(d['month'], d['net_revenue']/1000, color=color, ls=ls,
             lw=2, marker='o', ms=4, label=f'FY {yr}')
ax1.set_title('Monthly Revenue Trend (₹K)')
ax1.legend(fontsize=8, facecolor='#22263a', labelcolor='#e8eaf6')
ax1.xaxis.set_major_locator(mticker.MultipleLocator(1))
ax1.set_xlabel('Month', color='#6b7094')

# ── Chart 2: Revenue by Segment (bar)
ax2 = axes[0, 1]
seg_rev = seg_kpis['revenue'].sort_values(ascending=True)
bars = ax2.barh(seg_rev.index, seg_rev.values/100000,
                color=['#4f8ef7','#7c5cfc','#6b7094'], height=0.5)
for b in bars:
    ax2.text(b.get_width()+0.1, b.get_y()+b.get_height()/2,
             f'₹{b.get_width():.1f}L', va='center', color='#e8eaf6', fontsize=9)
ax2.set_title('Revenue by Customer Segment (₹L)')
ax2.set_xlabel('₹ Lakhs', color='#6b7094')

# ── Chart 3: Quarterly Churn Rate
ax3 = axes[1, 0]
churn_q = (
    customers[customers['churn_dt'].notna()]
    .assign(q=pd.to_datetime(customers['churn_dt']).dt.quarter)
    .groupby('q').size()
    / len(customers) * 100
)
ax3.bar(churn_q.index, churn_q.values, color='#f75a5a', alpha=0.8, width=0.5)
ax3.plot(churn_q.index, churn_q.values, 'o-', color='#f75a5a', lw=1.5, ms=5)
ax3.set_title('Churn Rate by Quarter (%)')
ax3.set_xlabel('Quarter', color='#6b7094')
ax3.set_xticks([1,2,3,4]); ax3.set_xticklabels(['Q1','Q2','Q3','Q4'])

# ── Chart 4: Category Revenue
ax4 = axes[1, 1]
cat_rev = (
    fy24.groupby('category')['net_revenue'].sum()
    .sort_values(ascending=False).head(5)
)
ax4.bar(cat_rev.index, cat_rev.values/100000,
        color='#4f8ef7', alpha=0.75)
ax4.set_title('Top 5 Categories by Revenue (₹L)')
ax4.set_xlabel('Category', color='#6b7094')
plt.xticks(rotation=15)

plt.suptitle('Sales & Customer Analytics Dashboard — FY 2023-24',
             color='#e8eaf6', fontsize=13, fontweight='bold', y=1.01)
plt.tight_layout()
plt.savefig('dashboard_analysis.png', dpi=150, bbox_inches='tight',
            facecolor='#0f1117')
print("\n✅ Chart saved → dashboard_analysis.png")
print("✅ Analysis complete.")
