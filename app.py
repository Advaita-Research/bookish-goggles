# app.py

import streamlit as st
import pandas as pd
from fuzzywuzzy import fuzz

# Load the CSV file
@st.cache_data
def load_data():
    return pd.read_csv("trademarks - Sheet1.csv")

df = load_data()

st.set_page_config(page_title="Trademark Search", layout="centered")
st.title("🔍 Simple Trademark Search Engine")

# Search input
query = st.text_input("Enter trademark name:")

# Search logic
def search_trademarks(query):
    df['similarity'] = df['name'].apply(lambda x: fuzz.partial_ratio(str(x).lower(), query.lower()))
    filtered = df[df['similarity'] > 60].sort_values(by='similarity', ascending=False)
    return filtered

# Show results
if query:
    results = search_trademarks(query)
    if not results.empty:
        st.success(f"Found {len(results)} matching trademark(s).")
        st.dataframe(results[['name', 'registration_number', 'owner', 'status', 'nice_class']], use_container_width=True)
    else:
        st.warning("No similar trademarks found.")
