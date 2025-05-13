import streamlit as st
import plotly.express as px

def add_space(space=2):
    br = "<br>"*space
    st.markdown(br, unsafe_allow_html=True)

def render_climate_section(geojson, risk_df):
    st.markdown('<div id="climate"></div>', unsafe_allow_html=True)
    st.header("Climate Risk Analysis")
    st.markdown("""
    This map shows crop-specific climate risk across Nigerian states based on key environmental factors, **precipitation, temperature, wind, evapotranspiration, humidity, and floods (weighted most heavily)**. Higher scores indicate greater risk of post-harvest spoilage.
    """)
    add_space(1)
    col1, col2, col3= st.columns([1, 3,1])  # Adjust the width ratio (e.g., 1:3)


    # Column 1: Dropdowns
    with col1:
        st.subheader("Filters")
        crop = st.selectbox("Select Crop", ['Maize','Rice','Sorghum','Beans','Millet'],index=0)
        month = st.selectbox("Select Month", ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'],index=0)

    # Filter data
    filtered = risk_df[risk_df["Month"] == month]

    feature_id_key = "properties.state"  # make sure your GeoJSON uses this; adjust if needed


    # Column 2: Map
    with col2:
        fig = px.choropleth_mapbox(
            filtered,
            geojson=geojson,
            locations="state",
            featureidkey=feature_id_key,
            color=crop,
            color_continuous_scale="YlOrRd",
            title = 'Climate Risk Index for Post Harvest Losses',
            mapbox_style="carto-positron",
            zoom=4.9,
            center={"lat": 9.1, "lon": 8.7},
            opacity=0.7,
            hover_name="state",
        )

        fig.update_layout(margin={"r": 0, "t": 30, "l": 0, "b": 0}, title=f"{crop.title()} Risk - {month}")
        st.plotly_chart(fig, use_container_width=True)
        add_space(1)
    
    with col3:
        st.empty()
    
    st.markdown("""
    From the map, **March shows the lowest climate-related risk for fresh maize in Kano**, with favorable storage conditions and minimal flood activity.
    """)