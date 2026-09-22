"""
data_loader.py
Loads the raw Zudio dataset from CSV. No transformations happen here —
cleaning/validation lives in data_cleaning.py.
"""
import pandas as pd
import streamlit as st


@st.cache_data(show_spinner="Loading dataset...")
def load_raw_data(path: str) -> pd.DataFrame:
    """Load the raw CSV exactly as uploaded."""
    df = pd.read_csv(path)
    return df
