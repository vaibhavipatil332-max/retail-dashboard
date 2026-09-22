# Zudio Retail Network Analytics Dashboard

An interactive Streamlit dashboard built from `Zudio_sales_data-selected-columns.csv`.

## ⚠️ Important: read this before you demo it

The uploaded CSV **does not contain any sales data**. It has 10 columns:

```
Store, Country, State, City, Category, Clothing Type,
Store Number, Postal Code, Store Type, Store Open Date
```

There is no Sales Amount, Quantity, Price, Order ID, or Customer ID anywhere
in the file. It is a **store network / assortment reference table**, not a
sales-transactions dataset.

So this dashboard is deliberately built as a **store network & assortment
analytics** tool rather than a sales-performance dashboard:

| Requested (sales-style) | What this dashboard actually shows |
|---|---|
| Total Sales / Revenue | Total assortment **records** |
| Sales trend over time | **Store-opening** trend over time (from `Store Open Date`) |
| Top products by revenue | Category / Clothing Type record-count mix |
| Top customers | **Not shown** — no customer data exists (page explains why) |
| Sales forecast | **Store-opening trend projection** (explicitly labeled, not a sales forecast) |
| Sales anomalies | Unusual **store-opening-count** months (z-score method) |

Also note: `Store Number` (1–100) looks like a store ID but is **not**
reliable — the same number appears against different states, cities and
open dates. It cannot be used to count unique physical stores. This is
flagged on the **Data Quality** page.

**If you get access to the full/original Kaggle dataset** (it may have more
columns than this exported subset), re-run the same pipeline — `Sales
Amount`, `Quantity`, `Customer ID`, etc. can be plugged into
`utils/calculations.py` to unlock real sales, product, and customer pages.

## Project structure

```text
retail_dashboard/
├── app.py                  # Entry point: theming, filters, page routing
├── requirements.txt
├── README.md
├── data/
│   └── Zudio_sales_data-selected-columns.csv
├── views/                  # (named "views", not "pages" — Streamlit
│   ├── overview.py         #  auto-turns a folder literally named
│   ├── network.py          #  "pages" into its own multipage nav,
│   ├── products.py         #  which would conflict with the custom
│   ├── customers.py        #  sidebar navigation used here)
│   ├── geography.py
│   ├── advanced.py
│   └── data_quality.py
├── utils/
│   ├── data_loader.py      # CSV loading (cached)
│   ├── data_cleaning.py    # Cleaning + data-quality audit (cached)
│   └── calculations.py     # All KPI / aggregation logic
└── assets/
    └── style.css           # Dark sidebar, light main, burgundy/gold theme
```

## How to run (VS Code / Cursor / terminal)

1. **Install Python 3.11+** if you don't already have it.
2. Open this folder in VS Code or Cursor.
3. Create and activate a virtual environment (recommended):
   ```bash
   python -m venv venv
   # Windows:
   venv\Scripts\activate
   # macOS / Linux:
   source venv/bin/activate
   ```
4. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
5. Run the app:
   ```bash
   streamlit run app.py
   ```
6. Your browser will open automatically at `http://localhost:8501`. If not,
   open that URL manually.

## Pages

- **Overview** — KPI cards + store-opening trend, category split, top cities/states
- **Network Growth** — monthly/yearly store-opening activity, cumulative growth, Owned vs Rented trend
- **Category & Assortment** — category/clothing-type distribution, treemap, matrix, search
- **Customer Insights** — honest "not available" notice (no customer data in source file)
- **Geographic Analysis** — state/city record distribution, approximate state-level bubble map
- **Advanced Insights** — store-opening trend projection, anomaly detection (z-score), data-supported observations
- **Data Quality** — full audit table, known limitations, CSV downloads

## Filters (sidebar)

Date range (Store Open Date), State, City, Category, Clothing Type, Store
Type — all cross-filtered, with a Reset Filters button and a filtered-data
CSV download.

## Extending with real sales data

If you later get a version of this dataset with `Sales Amount`, `Quantity`,
`Order ID`, `Customer ID`, or `Price`, the cleanest path is:

1. Add the new columns to `utils/data_cleaning.py`'s validation checks.
2. Add matching KPI functions to `utils/calculations.py` (e.g. `total_sales`,
   `average_order_value`, `top_products_by_sales`).
3. Update `views/overview.py`, `views/products.py`, and `views/customers.py`
   to call the new functions instead of the record-count proxies.
