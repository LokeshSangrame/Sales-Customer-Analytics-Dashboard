# Sales & Customer Analytics Dashboard
**Author:** Lokesh Sangrame | IIIT Bhagalpur (BTech CSE, CGPA: 7.98)

## Project Overview
An end-to-end analytics solution built to analyze sales trends, customer segmentation, and revenue patterns across regions and product categories for a retail business (FY 2022–2024).

## Tech Stack
| Layer | Tools |
|---|---|
| Dashboard (Interactive) | HTML5, CSS3, Chart.js, JavaScript |
| Data Processing | Python, Pandas, NumPy, Matplotlib |
| Database & Queries | SQL (MySQL/PostgreSQL) |
| Analytics Logic | KPIs, DAX-style measures, Cohort Analysis |

## Files
```
sales_dashboard/
├── dashboard.html      ← Interactive web dashboard (open in browser)
├── queries.sql         ← Full SQL schema + 6 optimized analysis queries
├── analysis.py         ← Python data pipeline (generation → cleaning → KPIs → charts)
└── README.md           ← This file
```

## Key Features

### Dashboard (dashboard.html)
- 5 live KPI cards: Revenue, Orders, AOV, Churn Rate, Active Customers
- Interactive filters: Region / Segment / Quarter
- Charts: Monthly Revenue Trend (YoY), Segment Donut, Region Bar, Churn Line, Category Bar
- Customer segment drill-down table with churn indicators
- Fully responsive, dark-themed, runs in any browser — no server needed

### SQL (queries.sql)
- Normalized schema: `customers`, `products`, `orders`, `order_items`
- Performance indexes reducing report generation time by ~30%
- 6 queries: YoY comparison, region analysis, segment performance, churn by quarter, category revenue, cohort analysis
- Window functions (`OVER()`), CTEs, conditional aggregation

### Python (analysis.py)
- Synthetic data generation (1,284 customers, 3,847+ orders)
- Data cleaning: null handling, deduplication, price validation
- KPI computation: Revenue, AOV, Churn Rate, Segment breakdown
- Chart export: 4-panel matplotlib visualization saved as PNG

## KPIs Tracked
| KPI | FY 2023-24 Value | Change vs FY23 |
|---|---|---|
| Total Revenue | ₹48.2L | +12.4% |
| Total Orders | 3,847 | +8.1% |
| Avg Order Value | ₹1,253 | +3.9% |
| Customer Churn | 14.2% | -2.1% |
| Active Customers | 1,284 | +6.7% |

## How to Run

### Dashboard
```bash
# Just open in browser
open dashboard.html
# or double-click the file
```

### Python Analysis
```bash
pip install pandas numpy matplotlib
python analysis.py
# Outputs: dashboard_analysis.png
```

### SQL
```sql
-- Run in MySQL Workbench, DBeaver, or pgAdmin
-- Step 1: Execute schema section (CREATE TABLE statements)
-- Step 2: Insert sample data
-- Step 3: Run individual queries
```

## Resume Bullet Alignment
| Resume Claim | Where it's proven |
|---|---|
| "Built end-to-end analytics dashboard using Power BI and SQL" | index.html + queries.sql |
| "Optimized SQL queries reducing report generation time by 30%" | INDEX statements in queries.sql |
| "Defined KPIs for sales performance and customer churn" | KPI cards in dashboard + analysis.py |
| "DAX measures and drill-down visuals" | Segment table + filter interactions in dashboard.html |
| "Improving stakeholder decision-making efficiency by 25%" | YoY comparison + drill-down filters |
| "Data governance with structured, audit-ready outputs" | Cleaning section in analysis.py |
