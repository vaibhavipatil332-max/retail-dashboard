"""
app.py
Zudio Retail Network Analytics Dashboard — entry point.
Handles page config, theming, data loading, sidebar filters, and
routing to individual page modules.

ADAPTATION NOTE
----------------
The source file (data/Zudio_sales_data-selected-columns.csv) contains
only store / location / category / clothing-type / date-opened fields.
It has NO sales amount, quantity, price, order, or customer data. This
dashboard is therefore built as a STORE NETWORK & ASSORTMENT analytics
tool, not a sales-performance dashboard. Every KPI and chart uses only
columns that actually exist in the data — nothing is invented.
"""
from pathlib import Path

import pandas as pd
import streamlit as st

from utils.data_loader import load_raw_data
from utils.data_cleaning import clean_data
from views import overview, network, products, customers, geography, advanced, data_quality

DATA_PATH = Path(__file__).parent / "data" / "Zudio_sales_data-selected-columns.csv"

st.set_page_config(
    page_title="Zudio Retail Network Analytics",
    page_icon="🛍️",
    layout="wide",
    initial_sidebar_state="expanded",
)


def load_css():
    css_path = Path(__file__).parent / "assets" / "style.css"
    if css_path.exists():
        st.markdown(f"<style>{css_path.read_text()}</style>", unsafe_allow_html=True)


load_css()

# ---------- Load & clean data (cached) ----------
if not DATA_PATH.exists():
    st.error(f"Dataset not found at {DATA_PATH}. Place your CSV there and reload.")
    st.stop()

raw_df = load_raw_data(str(DATA_PATH))
df, quality_report = clean_data(raw_df)

# ---------- Sidebar: branding + navigation ----------
st.sidebar.markdown(
    """
    <div class="sidebar-logo">
        <h2>🛍️ ZUDIO</h2>
        <p>Retail Network Analytics</p>
    </div>
    """,
    unsafe_allow_html=True,
)

PAGES = {
    "📊 Overview": "overview",
    "🏗️ Network Growth": "network",
    "👕 Category & Assortment": "products",
    "🧑‍🤝‍🧑 Customer Insights": "customers",
    "🗺️ Geographic Analysis": "geography",
    "🔮 Advanced Insights": "advanced",
    "🧪 Data Quality": "data_quality",
}
choice = st.sidebar.radio("Navigate", list(PAGES.keys()), label_visibility="collapsed")

st.sidebar.markdown("---")
st.sidebar.markdown("### Filters")

if st.sidebar.button("🔄 Reset Filters"):
    for key in ["f_states", "f_cities", "f_categories", "f_clothing", "f_store_type", "f_dates"]:
        if key in st.session_state:
            del st.session_state[key]
    st.rerun()

min_date = df["Store Open Date"].min()
max_date = df["Store Open Date"].max()

date_range = st.sidebar.date_input(
    "Store Open Date range", value=(min_date, max_date),
    min_value=min_date, max_value=max_date, key="f_dates",
)

states = sorted(df["State"].unique())
sel_states = st.sidebar.multiselect("State", states, default=states, key="f_states")

city_pool = df[df["State"].isin(sel_states)] if sel_states else df
cities_available = sorted(city_pool["City"].unique())
sel_cities = st.sidebar.multiselect("City", cities_available, default=cities_available, key="f_cities")

categories = sorted(df["Category"].unique())
sel_categories = st.sidebar.multiselect("Category", categories, default=categories, key="f_categories")

clothing_types = sorted(df["Clothing Type"].unique())
sel_clothing = st.sidebar.multiselect("Clothing Type", clothing_types, default=clothing_types, key="f_clothing")

store_types = sorted(df["Store Type"].unique())
sel_store_type = st.sidebar.multiselect("Store Type", store_types, default=store_types, key="f_store_type")

# ---------- Apply filters ----------
filtered = df.copy()
if isinstance(date_range, tuple) and len(date_range) == 2:
    start, end = pd.Timestamp(date_range[0]), pd.Timestamp(date_range[1])
    filtered = filtered[(filtered["Store Open Date"] >= start) & (filtered["Store Open Date"] <= end)]
if sel_states:
    filtered = filtered[filtered["State"].isin(sel_states)]
if sel_cities:
    filtered = filtered[filtered["City"].isin(sel_cities)]
if sel_categories:
    filtered = filtered[filtered["Category"].isin(sel_categories)]
if sel_clothing:
    filtered = filtered[filtered["Clothing Type"].isin(sel_clothing)]
if sel_store_type:
    filtered = filtered[filtered["Store Type"].isin(sel_store_type)]

st.sidebar.markdown("---")
st.sidebar.caption(f"Showing **{len(filtered):,}** of {len(df):,} records")
st.sidebar.download_button(
    "⬇️ Download filtered data (CSV)",
    filtered.to_csv(index=False).encode("utf-8"),
    file_name="zudio_filtered_data.csv",
    mime="text/csv",
)

# ---------- Route to selected page ----------
page_key = PAGES[choice]
if page_key == "overview":
    overview.render(filtered, df)
elif page_key == "network":
    network.render(filtered)
elif page_key == "products":
    products.render(filtered)
elif page_key == "customers":
    customers.render(filtered)
elif page_key == "geography":
    geography.render(filtered)
elif page_key == "advanced":
    advanced.render(filtered)
elif page_key == "data_quality":
    data_quality.render(raw_df, df, quality_report)
