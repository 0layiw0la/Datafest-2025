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

def render_land_section(geojson, full_survey_df):
    st.header("Land Quality (Fertility)")
    st.markdown('<div id="land"></div>', unsafe_allow_html=True)
    st.markdown("""
    Soil fertility also has a significant effect on post harvest losses as it affects the quality and shelf life of crops. Poor quality crops often spoil faster making them more vunerable to PHL.
    
    The map below shows an aggregated degradation score for each state (0–4 scale), based on farmer responses from the survey. 
    """)
    add_space(1)

    land_feats = ['state','land_degradation_pct','abandoned_farm_pct','produce_transport_method']
    land_df = full_survey_df[land_feats]
    degradation_order = ['None (0%)', '1%-25%', '26%-50%', '51%-75%', '76%-100%']
    category_to_score = {cat: i for i, cat in enumerate(degradation_order)}

    land_df["land_degradation_score"] = land_df["land_degradation_pct"].map(category_to_score).astype(int)
    land_df["abandoned_farm_score"] = land_df["abandoned_farm_pct"].map(category_to_score).astype(int)

    state_scores = land_df.groupby("state")[["land_degradation_score", "abandoned_farm_score"]].mean().reset_index()
    col1,col2,col3 = st.columns([1,4,1])

    with col2:
        fig = px.choropleth_mapbox(
        state_scores,
        geojson=geojson,
        locations='state',
        featureidkey='properties.state',
        color='land_degradation_score',
        color_continuous_scale='YlOrRd',
        title='Land Degradation Score by State ',
        labels={'land_degradation_score': 'Degradation Score'},
        mapbox_style='carto-positron',
        zoom=4.9,
        center={"lat": 9.1, "lon": 8.7},
        opacity=0.7
    )
        fig.update_layout(margin={"r": 0, "t": 30, "l": 0, "b": 0})
        st.plotly_chart(fig, use_container_width=True)
        add_space(1)

    st.markdown("""
    We found that **Taraba, Bayelsa, and Akwa Ibom, have the highest degradation rates at bettween 26-28% for each of the 3 states**.
    For entrepreneurs, these insights signal **areas to avoid for new farming ventures**, or **target zones for soil-improvement services** — from composting and organic amendments to precision input delivery.
    """)
    
    add_space()

    st.markdown("""
                This bar chart breaks down **how much land** farmers believe is affected by degradation, both nationally and by state.
    """)
    col1,col2,col3 = st.columns([1,4,1])

    state_list = sorted(land_df["state"].apply(format_state).unique())
    state_list.insert(0,'Nigeria')

    with col1:
        state = st.selectbox(
            "Select State",
            state_list,
            key='select_state_3',
            index=0
        )

    if state == "FCT":
        state = "federalcapitalterritory"
    else:
        state = state.lower()

    subset = land_df
    
    if state != 'nigeria':
         subset = land_df[land_df['state'] == state]

    subset['land_degradation_pct'] = subset['land_degradation_pct'].replace('None (0%)','0%')

    # Count land degradation categories
    deg_counts = ((subset['land_degradation_pct'].value_counts()/subset['land_degradation_pct'].shape[0])*100)

    # Convert to DataFrame for plotting
    deg_df = deg_counts.reset_index()
    deg_df.columns = ['land_degradation_pct', 'count']

    with col2:
        fig = go.Figure()

        fig.add_trace(go.Bar(
            x=deg_df['land_degradation_pct'],
            y=deg_df['count'],
            marker_color=px.colors.sequential.YlOrRd
            
        ))

        fig.update_layout(
            barmode='group',
            title=f'Land Degradation in {state.capitalize()}',
            xaxis_title='Degradation',
            yaxis_title='Percentage of responses'
        )

        st.plotly_chart(fig, use_container_width=True)
        add_space(2)

    st.markdown("""
    Finally, farmers were asked about **whether land quality is improving, stagnant, or declining**. On a **national level,** **50% say it’s worsening**, while only **28% believe it’s improving**. **20% feel conditions are stagnant**.
    """)

    col1,col2,col3 = st.columns([1,4,1])

    with col1:
        state = st.selectbox(
            "Select State",
            state_list,
            key='select_state_4',
            index=0
        )

    if state == "FCT":
        state = "federalcapitalterritory"
    else:
        state = state.lower()

    count = full_survey_df["increase_land_degradation"].value_counts().sort_values(ascending=False).reset_index()
    if state != 'nigeria':
         count = full_survey_df[full_survey_df['state'] == state]["increase_land_degradation"].value_counts().sort_values(ascending=False).reset_index()
    
    count['count'] = (count['count'] / count['count'].sum()) * 100

    with col2:
        fig = px.bar(
            count,
            y = "increase_land_degradation",
            x = 'count',
            title=f"Land Degradation Increase in {state.capitalize()}",
            labels={'increase_land_degradation': ' ', 'count': 'Percentage of response'},
            color='increase_land_degradation',
            color_discrete_sequence=px.colors.sequential.YlOrRd
        )
        st.plotly_chart(fig, use_container_width=True)
        




