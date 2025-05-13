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
    st.markdown("""
    Natural disasters are a key threat to agricultural productivity in Nigeria. **Between 2020 and 2022, farmers experienced an average of 3.3 disaster events**, with varying impacts depending on region and disaster type.

                

    ### Disaster Frequency
    The bar chart below highlights the most frequently reported disasters nationwide. **Heavy rainfall has been the most frequent in the last 3 years with an average of 3.61 events, followed closely by extreme cold or heat at 3.56. Drought, despite being less frequent. The next charts show its effects are far more damaging.
    """)
    add_space(1)
    col1,col2,col3 = st.columns([1,4,1])

    state_list = sorted(disaster_df["state"].apply(format_state).unique())
    state_list.insert(0,'Nigeria')

    with col1:
        state = st.selectbox(
            "Select State",
            state_list,
            key='select_state_5',
            index=0
        )

    if state == "FCT":
        state = "federalcapitalterritory"
    else:
        state = state.lower()

    subset = disaster_df
    if state != 'nigeria':
         subset = disaster_df[disaster_df['state'] == state]
        
    counts = subset.groupby(['disaster'])['disaster_frequency_3_years'].mean().sort_values().reset_index()
    counts = counts[counts['disaster'] != "Other (specify)"]
    with col2:
        fig = go.Figure()

        fig.add_trace(go.Bar(
            y=counts['disaster'],
            x=counts['disaster_frequency_3_years'],
            orientation='h',
            marker_color=px.colors.sequential.YlOrRd
            
        ))

        fig.update_layout(
            barmode='group',
            title=f"Disasters ranked by frequency (3 years) in {state.capitalize()}",
            xaxis_title='Average disaster frequency',
            yaxis_title='Disasters'
        )

        st.plotly_chart(fig, use_container_width=True)
        add_space(2)

    st.markdown("""
    ### States Most Affected by Disasters
    
    From our disaster incidence map, **Lagos** emerges as the most affected state, with an average of **9.58 disaster events per respondent over the 3-year period**. **Edo and Akwa Ibom** follow with **6.4 and 5.1** respectively. Such regions may need resilient infrastructure or risk mitigation support. But also present an opportunity for services like climate-resilient warehousing or weather-indexed insurance.
""")
    add_space(1)

    col1,col2,col3= st.columns([1,4,1])

    counts = disaster_df.groupby(['state'])['disaster_frequency_3_years'].mean().reset_index()
    with col2:
        fig = px.choropleth_mapbox(
        counts,
        geojson=geojson,
        locations='state',
        featureidkey='properties.state',
        color='disaster_frequency_3_years',
        color_continuous_scale='YlOrRd',
        title='Disaster Frequency by State (3 Years)',
        labels={'disaster_frequency_3_years': 'Avg no of events'},
        mapbox_style='carto-positron',
        zoom=4.9,
        center={"lat": 9.1, "lon": 8.7},
        opacity=0.7
    )
        fig.update_layout(margin={"r": 0, "t": 30, "l": 0, "b": 0})
        st.plotly_chart(fig, use_container_width=True)
        add_space()

    st.markdown("""
    ### Crop Loss & Disasters
                
     A major consequence of these disasters is crop loss. Here, drought has the most impact, 89% of affected farmers reported losing crops due to it, followed by flooding at 76%. These figures highlight the need for drought- and flood-tolerant seed varieties or protective infrastructure like raised-bed farming.
    """)

    col1,col2,col3 = st.columns([1,4,1])

    with col1:
        state = st.selectbox(
            "Select State",
            state_list,
            key='select_state_6',
            index=0
        )

    if state == "FCT":
        state = "federalcapitalterritory"
    else:
        state = state.lower()

    subset = disaster_df
    if state != 'nigeria':
         subset = disaster_df[disaster_df['state'] == state]
        
    crop_loss_disaster_pct = (
        subset.groupby('disaster')['Crop losses']
        .value_counts(normalize=True)
        .unstack()
        .get('Yes', pd.Series(dtype=float)) * 100
    ).sort_values().reset_index()
    crop_loss_disaster_pct = crop_loss_disaster_pct[crop_loss_disaster_pct['disaster'] != "Other (specify)"]
    with col2:
        fig = px.bar(
            crop_loss_disaster_pct,
            x = 'Yes',
            y='disaster',
            orientation='h',
            labels={'Yes': 'Farmers with loss %', 'disaster': 'Disaster'},
            title='Percentage of Farmers who lost crops',
            color_discrete_sequence=px.colors.sequential.Reds
        )
        st.plotly_chart(fig, use_container_width=True)
        add_space()

    st.markdown("""
    This map shows how risky these disasters are to harvest across the country. Asides **Abuja, Lagos, Edo, and Ondo**, **every other state has over 50% of farmers claiming crop loss.**
    This presents a challenge to be considered when investing, but opportunity for early warning systems to be profitable.    
""")
    
    crop_loss_pct = (
        disaster_df.groupby('state')['Crop losses']
        .value_counts(normalize=True)
        .unstack()
        .get('Yes', pd.Series(dtype=float)) * 100
    ).reset_index(name='pct_crop_loss')

    col1,col2,col3 = st.columns([1,4,1])
    with col2:
        fig = px.choropleth_mapbox(
        crop_loss_pct,
        geojson=geojson,
        locations='state',
        featureidkey='properties.state',
        color='pct_crop_loss',
        color_continuous_scale='YlOrRd',
        title='Percentage of Farmers who lost crops',
        labels={'pct_crop_loss': 'Farmers with loss (%) '},
        mapbox_style='carto-positron',
        zoom=4.9,
        center={"lat": 9.1, "lon": 8.7},
        opacity=0.7
    )
        fig.update_layout(margin={"r": 0, "t": 30, "l": 0, "b": 0})
        st.plotly_chart(fig, use_container_width=True)
        add_space()
    
    st.markdown("""
    ### Economic loss & Disaster
                
    While the previous charts give us an idea of how widesrpead loss due to disasters is, it doesnt say much about the severity.
                
    This chart explores how bad these losses get depending on the disaster and region. With **flood being the most severe**, about **83% of farmers report significant to total losses**
""")
    
    col1,col2,col3 = st.columns([1,4,1])

    with col1:
        state = st.selectbox(
            "Select State",
            state_list,
            key='select_state_7',
            index=0
        )

    if state == "FCT":
        state = "federalcapitalterritory"
    else:
        state = state.lower()

    subset = disaster_df
    if state != 'nigeria':
         subset = disaster_df[disaster_df['state'] == state]

    severity_counts = (
        subset
        .dropna(subset=['loss_severity_economic'])
        .groupby(['disaster', 'loss_severity_economic'])
        .size()
        .reset_index(name='count')
    )

    total_per_disaster = (
        severity_counts.groupby('disaster')['count']
        .sum()
        .reset_index(name='total')
    )

    severity_pct = severity_counts.merge(total_per_disaster, on='disaster')
    severity_pct['percentage'] = (severity_pct['count'] / severity_pct['total']) * 100
    severity_pct = severity_pct[severity_pct['disaster'] != 'Other (specify)']
    severity_pct['disaster'] = severity_pct['disaster'].replace('Extreme temperatures (cold or heat)','	Extreme temperatures')
    
    color_map = {
        'Small losses': 'yellow',
        'Significant losses': 'orange',
        'Almost total or total losses': 'red'
    }

    with col2:
        fig = px.bar(
        severity_pct,
        x='disaster',
        y='percentage',
        color='loss_severity_economic',
        barmode='group',
        title='Disasters by Economic Loss Severity (%)',
        labels={'percentage': 'Percentage'},
        color_discrete_map=color_map
    )
        st.plotly_chart(fig, use_container_width=True)
        add_space() 

    st.markdown("""
    ### Disasters & Migration
                
    Another Effect of disasters is the displacement of people. This next chart visualizes what percentage of farmers have had to migrate due to each disaster. With migrations like these, even if the farmers were to later return would undoubtedly lead to losses.
    """)

    col1,col2,col3 = st.columns([1,4,1])

    with col1:
        state = st.selectbox(
            "Select State",
            state_list,
            key='select_state_8',
            index=0
        )

    if state == "FCT":
        state = "federalcapitalterritory"
    else:
        state = state.lower()

    subset = disaster_df
    if state != 'nigeria':
         subset = disaster_df[disaster_df['state'] == state]

    abandon_pct = (
        subset.groupby('disaster')['abandoned_area']
        .value_counts(normalize=True)
        .unstack()
        .get('Yes', pd.Series(dtype=float)) * 100
    ).sort_values()
    abandon_pct = abandon_pct[abandon_pct.index != 'Other (specify)']
    with col2:
        fig = px.bar(
        abandon_pct,
        orientation='h',
        labels={'value': '% Fled', 'index': 'Disaster'},
        title='Disasters Ranked by % of Respondents Who Fled',
        color_discrete_sequence=px.colors.sequential.YlOrRd
    )
        st.plotly_chart(fig, use_container_width=True)


    
    