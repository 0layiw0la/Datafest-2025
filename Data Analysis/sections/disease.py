import streamlit as st
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go

def add_space(space=2):
    br = "<br>"*space
    st.markdown(br, unsafe_allow_html=True)


def render_disease_section(geojson, full_survey_df):
    st.header("Diseases & Animal Damage")
    st.markdown('<div id="disease"></div>', unsafe_allow_html=True)
    st.markdown("""
    ### Crop Diseases
    Biological threats such as crop diseases and animal damage can severely undermine post-harvest outcomes. The **map below** allows you to explore these risks by state.       
    **22 of 36 states** in Nigeria have over **50%** of farmers reporting disease related loss. **Akwa Ibom** tops the chart with **82.5%** of farmers reporting loss. **Cross River, Plateau, and Nasarawa** also report high rates, all **above 70%**.""")

    counts = full_survey_df.groupby(['state', 'challenge_crop_diseases']).size().unstack(fill_value=0)
    counts['total'] = counts.sum(axis=1)
    counts['yes_pct'] = (counts['Yes'] / counts['total']) * 100
    counts['no_pct'] = (counts['No'] / counts['total']) * 100
    counts = counts.reset_index()

    col1,col2,col3 = st.columns([1,4,1])

    with col2:
        fig = px.choropleth_mapbox(
        counts,
        geojson=geojson,
        locations='state',
        featureidkey='properties.state',
        color='yes_pct',
        color_continuous_scale='YlOrRd',
        title='Percentage of Farmers with Complaints on Crop Diseases by State',
        labels={'yes_pct': 'Percentage of Complaints'},
        mapbox_style='carto-positron',
        zoom=4.9,
        center={"lat": 9.1, "lon": 8.7},
        opacity=0.7
    )
        fig.update_layout(margin={"r": 0, "t": 30, "l": 0, "b": 0})
        st.plotly_chart(fig, use_container_width=True)
        add_space(1)
    
    st.markdown("""    
    These findings highlight the need for disease-resistant crop varieties, early detection and control solutions and improved storage and hygiene at collection points. Such challenges open doors for **agri-health innovations**, **input suppliers**, and **extension services** that can target these hotspots.
    """)

    add_space(2)
    st.markdown("""
    #### Animal Damage
    While still relevant, **animal damage appears less widespread** than disease. **Kwara** records the highest share, at **58%**, with a moderate spread across other states.
    For entrepreneurs, this suggests: **Physical crop protection** (e.g., fencing, off-ground storage) may be needed in select areas. There's space for **low-cost storage innovations** that shield crops from pests and animals post-harvest.
    
    Use the map below to explore each risk by state, and identify high-need zones for disease or damage interventions.
""")
    
    add_space(1)

    counts = full_survey_df.groupby(['state', 'challenge_animal_damage']).size().unstack(fill_value=0)
    counts['total'] = counts.sum(axis=1)
    counts['yes_pct'] = (counts['Yes'] / counts['total']) * 100
    counts['no_pct'] = (counts['No'] / counts['total']) * 100
    counts = counts.reset_index()

    col1,col2,col3 = st.columns([1,4,1])

    with col2:
        fig = px.choropleth_mapbox(
        counts,
        geojson=geojson,
        locations='state',
        featureidkey='properties.state',
        color='yes_pct',
        color_continuous_scale='YlOrRd',
        title='Percentage of Farmers with Complaints on Animal Damage by State',
        labels={'yes_pct': 'Percentage of Complaints'},
        mapbox_style='carto-positron',
        zoom=4.9,
        center={"lat": 9.1, "lon": 8.7},
        opacity=0.7
    )
        fig.update_layout(margin={"r": 0, "t": 30, "l": 0, "b": 0})
        st.plotly_chart(fig, use_container_width=True)
        add_space(1)

    st.markdown("From the map we can see that the **middle belt** is the hotspot for animal damage.")
    add_space(2)