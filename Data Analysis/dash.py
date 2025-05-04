import streamlit as st
import pandas as pd
import geopandas as gpd
import json
import plotly.express as px

# === Load GeoJSON and Crop Risk Data ===
@st.cache_data
def load_geojson():
    with open("gadm41_NGA_1.json", "r") as f:
        geojson_data = json.load(f)
    return geojson_data

@st.cache_data
def load_risk_data():
    df = pd.read_csv("Datasets/risk_index_by_state_month.csv")  # columns: state, month, maize, rice, etc.
    df["state"] = df["state"].str.strip()
    return df

geojson = load_geojson()
risk_df = load_risk_data()

# === Streamlit App ===
st.title("Nigeria Post-Harvest Risk Map")

# Dropdowns
crop = st.selectbox("Select Crop", [col for col in risk_df.columns if col not in ["state", "month"]])
month = st.selectbox("Select Month", sorted(risk_df["Month"].unique()))

# Filter data
filtered = risk_df[risk_df["Month"] == month]

# Match state names
feature_id_key = "properties.state"  # make sure your GeoJSON uses this; adjust if needed
for feature in geojson["features"]:
    feature["properties"]["state"] = feature["properties"]["NAME_1"]

# Plot
fig = px.choropleth_mapbox(
    filtered,
    geojson=geojson,
    locations="state",
    featureidkey=feature_id_key,
    color=crop,
    color_continuous_scale="YlOrRd",
    mapbox_style="carto-positron",
    zoom=5.3,
    center={"lat": 9.1, "lon": 8.7},
    opacity=0.7,
    hover_name="state",
)

fig.update_layout(margin={"r":0,"t":30,"l":0,"b":0}, title=f"{crop.title()} Risk - {month}")
st.plotly_chart(fig, use_container_width=True)
