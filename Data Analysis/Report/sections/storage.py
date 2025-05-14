import streamlit as st
import plotly.express as px
import pandas as pd

def add_space(space=2):
    br = "<br>"*space
    st.markdown(br, unsafe_allow_html=True)


def render_storage_section(geojson, full_survey_df):
    st.header("Storage")
    st.markdown('<div id="storage"></div>', unsafe_allow_html=True)
    st.markdown("""
    Access to storage is a critical problem in the post-harvest chain. The map below shows just how serious the problem is. 
    **21 out of 36 states** report that **over  90%** of respondents do **not** have access to storage facilities. And **Sokoto with the most access**
    having only **20.6% with storage**.
                
    This is not just a rural issue, seeing as **Lagos has the highest number** of respondents **without** access to storage.
                
    Whilst this lack of storage is a major problem, it presents a **major opportunity for entreprenuers** and investors to step in.
    The demand for storage solutions is widespread and largely unmet.
""")
    add_space(1)
    counts = full_survey_df.groupby(['state', 'storage_facility_available']).size().unstack(fill_value=0)


    counts['total'] = counts.sum(axis=1)
    counts['yes_pct'] = (counts['Yes'] / counts['total']) * 100
    counts['no_pct'] = (counts['No'] / counts['total']) * 100

    counts = counts.reset_index()

    col1,col2,col3 = st.columns([1,4.5,1])

    with col2:
        fig = px.choropleth_mapbox(
        counts,
        geojson=geojson,
        locations='state',
        featureidkey='properties.state',
        color='no_pct',
        color_continuous_scale='YlOrRd',
        title='Percentage of Farmers With No Acess to Storage',
        labels={'no_pct': 'Percentage Without Storage Access'},
        mapbox_style='carto-positron',
        zoom=4.9,
        center={"lat": 9.1, "lon": 8.7},
        opacity=0.7
    )

        fig.update_layout(margin={"r": 0, "t": 30, "l": 0, "b": 0})
        st.plotly_chart(fig, use_container_width=True)
    