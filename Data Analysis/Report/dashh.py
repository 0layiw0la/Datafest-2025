import streamlit as st
import pandas as pd
import json
from sections.climate import render_climate_section
from sections.market import render_market_section
from sections.storage import render_storage_section
from sections.process import render_process_section
from sections.disease import render_disease_section
from sections.land import render_land_section
from sections.disaster import render_disaster_section
import os

st.set_page_config(layout="wide")
# === Load GeoJSON and Crop Risk Data ===
@st.cache_data
def load_geojson():
    file_path = os.path.join(os.path.dirname(__file__), "gadm41_NGA_1.json")
    with open(file_path, "r") as f:
        geojson_data = json.load(f)
    
    # Normalize state names in GeoJSON
    for feature in geojson_data["features"]:
        feature["properties"]["state"] = feature["properties"]["NAME_1"].lower()
    
    return geojson_data

@st.cache_data
def load_data(path):
    df = pd.read_csv(path)  
    df["state"] = df["state"].str.lower().str.strip()  # Normalize state names
    df["state"] = df['state'].replace("abuja","federalcapitalterritory")
    df["state"] = df['state'].replace("fct","federalcapitalterritory")
    return df

geojson = load_geojson()
risk_df = load_data("Datasets/risk_index.csv")
market_df = load_data("Datasets/market_df.csv")
full_survey_df = load_data("Datasets/full_survey.csv")
disaster_df = load_data("Datasets/disaster_df.csv")

# === Streamlit App ===

st.markdown(
    """
    <style>
    html, body, [class*="css"] {
        font-size: 18px;
    .main-title {
        font-size: 3.3rem;
        text-align: center;
        width: 100%;
        margin-bottom: 20px;
        font-weight: bold;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Title
st.markdown('<div class="main-title">Factors Affecting Nigerian Post-Harvest Loss</div>', unsafe_allow_html=True)

st.markdown("<hr>", unsafe_allow_html=True)

#Introduction
st.title("Introduction")

st.markdown("""
Post-harvest losses (PHL) are one of the largest threats to agricultural productivity in Nigeria. 
Up to **30–50%** of perishable food is lost annually, costing the country **as much as $9 billion**.

According to a report by [PwC Nigeria](https://www.pwc.com/ng/en/assets/pdf/afcfta-agribusiness-current-state-nigeria-agriculture-sector.pdf):
- Agriculture contributed approximately **22% to Nigeria’s GDP** as of Q1 2020.
- The sector employs over **36% of the labour force**, making it the largest employer in the country.

Yet despite its potential, agriculture remains risky, especially for young entrepreneurs, due to losses driven by poor storage, weak infrastructure, climate volatility, and market access gaps.

**This report is a feasibility study** designed to help **young investors** and **agripreneurs** understand:
- What causes PHL and where the risks lie,
- How to interpret state-level data to minimize those risks,
- And where opportunities exist for safe, profitable investment in Nigeria’s agricultural value chain.

By analyzing patterns across crops, seasons, and regions, this report equips you to make **data-informed decisions** about **how**, **when**, and **where** to invest in agriculture.

""")

st.subheader("Key Risk Factors Considered")

st.markdown("""
We analyzed PHL contributors across 5 dimensions. Click to jump to each section:

- [Market Access](#market-access)
- [Transportation](#transport)
- [Storage](#storage)
- [Processing](#process)
- [Disease & Animal Damage](#disease)
- [Land Quality](#land)
- [Climate](#climate)
- [Natural Disasters](#disaster)
""", unsafe_allow_html=True)       

st.markdown("<hr>", unsafe_allow_html=True)

# Render Market Section
render_market_section(geojson,market_df,full_survey_df)  
st.markdown("<hr>", unsafe_allow_html=True)

# Render Storage Section
render_storage_section(geojson,full_survey_df)  
st.markdown("<hr>", unsafe_allow_html=True)

# Render Process Section
render_process_section(geojson,full_survey_df)  
st.markdown("<hr>", unsafe_allow_html=True)

# Render Disease Section
render_disease_section(geojson,full_survey_df)  
st.markdown("<hr>", unsafe_allow_html=True)

# Render Land Quality Section
render_land_section(geojson,full_survey_df)  
st.markdown("<hr>", unsafe_allow_html=True)

# Render Climate Section
render_climate_section(geojson, risk_df)
st.markdown("<hr>", unsafe_allow_html=True)

# Render Disaster Section
render_disaster_section(geojson, disaster_df)

