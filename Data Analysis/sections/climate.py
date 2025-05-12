import streamlit as st
import plotly.express as px

def render_climate_section(geojson, risk_df):
    st.header("Climate Risk Analysis")
    st.write("The map below shows monthly climate-related risk of post-harvest losses across Nigerian states, using a crop-specific index — for example, maize is more sensitive to flood and rainfall, while sorghum is more affected by temperature.")
  
    col1, col2, col3= st.columns([1, 3,1])  # Adjust the width ratio (e.g., 1:3)


    # Column 1: Dropdowns
    with col1:
        st.subheader("Filters")
        crop = st.selectbox("Select Crop", [col for col in risk_df.columns if col not in ["state", "Month"]])
        month = st.selectbox("Select Month", sorted(risk_df["Month"].unique()))

    # Filter data
    filtered = risk_df[risk_df["Month"] == month]

    feature_id_key = "properties.state"  # make sure your GeoJSON uses this; adjust if needed


    # Column 2: Map
    with col2:
        st.subheader("Nigerian States Climate Risk Map")
        fig = px.choropleth_mapbox(
            filtered,
            geojson=geojson,
            locations="state",
            featureidkey=feature_id_key,
            color=crop,
            color_continuous_scale="YlOrRd",
            mapbox_style="carto-positron",
            zoom=4.9,
            center={"lat": 9.1, "lon": 8.7},
            opacity=0.7,
            hover_name="state",
        )

        fig.update_layout(margin={"r": 0, "t": 30, "l": 0, "b": 0}, title=f"{crop.title()} Risk - {month}")
        st.plotly_chart(fig, use_container_width=True)
    
    with col3:
        st.empty()