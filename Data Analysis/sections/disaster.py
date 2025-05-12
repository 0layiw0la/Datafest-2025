import streamlit as st
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go

def add_space(space=2):
    br = "<br>"*space
    st.markdown(br, unsafe_allow_html=True)

def format_state(state_name):
            if state_name.lower() == "federalcapitalterritory":
                return "FCT"
            return state_name.capitalize()
def render_disaster_section(geojson,disaster_df):
       st.header("Natural Disasters")
       st.markdown('<div id="disaster"></div>', unsafe_allow_html=True)
       
