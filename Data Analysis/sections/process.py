import streamlit as st
import plotly.express as px
import pandas as pd

def add_space(space=2):
    br = "<br>"*space
    st.markdown(br, unsafe_allow_html=True)


def render_process_section(geojson, full_survey_df):
    st.header("Processing")
    st.markdown('<div id="process"></div>', unsafe_allow_html=True)
    st.markdown("""

    """)
