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

def render_process_section(geojson, full_survey_df):
    st.header("Processing")
    st.markdown('<div id="process"></div>', unsafe_allow_html=True)
    st.markdown("""
    Agro-processing remains critically underdeveloped across Nigeria. The **map below** shows the percentage of respondents in each state reporting **no access** to any agro-processing facilities.
    """)

    df_proc = full_survey_df[["state",'comid',"electricity_available", "agro_processing","milling_facility","feed_mill","corn_husker","cocoa_mill","palm_oil_mill",
     "rice_husker"]]
    
    counts = df_proc.groupby(['state', 'agro_processing']).size().unstack(fill_value=0)
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
        color='no_pct',
        color_continuous_scale='YlOrRd',
        title='Percentage of Farmers with No Acess to Agro-Processing by State',
        labels={'no_pct': 'Percentage of Complaints'},
        mapbox_style='carto-positron',
        zoom=4.9,
        center={"lat": 9.1, "lon": 8.7},
        opacity=0.7
    )
        fig.update_layout(margin={"r": 0, "t": 30, "l": 0, "b": 0})
        st.plotly_chart(fig, use_container_width=True)
        add_space(1)

    st.markdown("""
    Interestingly, **Lagos records the highest inaccessibility at 89%**, which may be linked to its high land costs and concentration of smaller-scale farming. **Oyo (50%)** follows closely.
    Overall, **21 of Nigeria’s 36 states** report that **over 30%** of respondents lack access to any form of processing — pointing to a widespread opportunity for investors to support decentralized, small-to-medium-scale agro-processing units.
    """)

    add_space(2)

    st.markdown("""
    The **bar chart below** highlights the **top five states** with the highest reported lack of agro-processing access. These locations represent **prime zones for infrastructure investment**, especially in equipment leasing models, cooperatives, or shared processing hubs that could serve multiple LGAs.
""")

    col1,col2,col3 = st.columns([1,4,1])
    top_no = counts.sort_values('no_pct', ascending=False).head(5)
    
    with col2:
        fig = go.Figure()

        fig.add_trace(go.Bar(
            x=top_no['state'],
            y=top_no['no_pct'],
            name='No Acess',
            marker_color='red'
        ))

        fig.update_layout(
            barmode='group',
            title='Top 5 States without Access to Agro-Processing facilities',
            xaxis_title='State',
            yaxis_title='Percentage without access'
        )

        st.plotly_chart(fig, use_container_width=True)
        add_space(2)
    
    st.markdown("""
    To better understand the gaps, farmers were also asked about access to **specific processing facilities**, such as cocoa mills, corn huskers, feed mills, and more.
    The chart below shows the **percentage of respondents lacking access** to each type
""")
    
    col1,col2,col3 = st.columns([1,4,1])

    state_list = sorted(df_proc["state"].apply(format_state).unique())
    state_list.insert(0,'Nigeria')

    with col1:
        state = st.selectbox(
            "Select State",
            state_list,
            index=0
        )

    if state == "FCT":
        state = "federalcapitalterritory"
    else:
        state = state.lower()

    # Melt the DataFrame for plotting
    facilities = ['milling_facility', 'feed_mill', 'corn_husker', 'cocoa_mill', 'palm_oil_mill', 'rice_husker']
    df_long = df_proc.melt(id_vars='state', value_vars=facilities, var_name='facility', value_name='response')

    # Filter by state
    if state != 'nigeria':
        df_long = df_long[df_long['state'] == state]

    # Count 'No' responses and calculate percentage
    no_pct = (
        df_long.groupby(['facility', 'response'])
        .size()
        .unstack(fill_value=0)
    )
    no_pct['no_pct'] = (no_pct['No'] / (no_pct['No'] + no_pct['Yes'])) * 100
    no_pct = no_pct.reset_index()

    with col2:
        fig = px.bar(
            no_pct,
            x='facility',
            y='no_pct',
            title=f'Percentage of Farmers without Access to Processing Facilities in {state.capitalize() if state != "nigeria" else "Nigeria"}',
            labels={'no_pct': 'Lack of Access (%)', 'facility': 'Facility'},
            color_discrete_sequence=['red']
        )
        fig.update_layout(xaxis_tickangle=-45)
        st.plotly_chart(fig, use_container_width=True)
        add_space(1)
    
    st.markdown("""
**Cocoa mills** are the most inaccessible: **95%** of respondents report no access. Even the most available (**milling factories**) still show **62%** inaccessibility. 
This underscores a **clear opportunity for targeted investments** based on crop value chains, especially in states known for specific crops.
""")
    

