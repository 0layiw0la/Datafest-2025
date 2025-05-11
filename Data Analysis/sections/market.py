import pandas as pd
import plotly.express as px
import streamlit as st

def render_market_section(geojson, market_df,full_survey_df):
    st.header("Market Access")
    st.write("Market access is a critical factor in determining the profitability and sustainability of agricultural practices. In Nigeria, the lack of efficient market access can lead to significant post-harvest losses.")
    
    col1, col2, col3 = st.columns([1,4,1])
    

    # Calculate percentage of market issues by LGA
    market_issues_lga = market_df[market_df['market_location'].isin(['In another LGA'])]
    state_market_issue_pct_lga = (
        (market_issues_lga.groupby('state').size() / market_df.groupby('state').size()) * 100
    ).reset_index(name='pct_outside_market')

    # Calculate percentage of market issues by state
    market_issues_state = market_df[market_df['market_location'].isin(['In another state'])]
    state_market_issue_pct_state = (
        (market_issues_state.groupby('state').size() / market_df.groupby('state').size()) * 100
    ).reset_index(name='pct_outside_market')


    feature_id_key = "properties.state"  

    # Add a dropdown to select the view (LGA or State)
    with col1:
        st.subheader("Filters")
        view_option = st.selectbox(
            "Select Market Access View",
            options=["LGA", "State"],
            index=0
        )


    with col2:
        st.subheader("Nigerian States Market Access Map")
        # Determine which data to use based on the selected view
        if view_option == "LGA":
            st.write("The map below shows the percentage of respondents with markets outside their LGA.")
            data = state_market_issue_pct_lga
            label = '% Market Outside LGA'
        else:
            st.write("The map below shows the percentage of respondents with markets outside their state.")
            data = state_market_issue_pct_state
            label = '% Market Outside State'

        # Create a choropleth map
        fig = px.choropleth_mapbox(
            data,
            geojson=geojson,
            locations='state',
            featureidkey=feature_id_key,
            color='pct_outside_market',
            color_continuous_scale="YlOrRd",
            mapbox_style='carto-positron',
            zoom=4.9,
            center={"lat": 9.1, "lon": 8.7},
            opacity=0.7,
            labels={'pct_outside_market': label},
        )
        
        # Display the map in Streamlit
        fig.update_layout(margin={"r": 0, "t": 30, "l": 0, "b": 0})
        st.plotly_chart(fig, use_container_width=True)

    with col3:
        st.empty()

    col1,col2,col3 =  st.columns([1.5,3.5,1])

    with col1:
        def format_state(state_name):
            if state_name.lower() == "federalcapitalterritory":
                return "FCT"
            return state_name.capitalize()

        state = st.selectbox(
            "Select State",
            sorted(market_df["state"].apply(format_state).unique())
        )
        st.subheader(f"Market Access in {state}")
        
    
    if state == "FCT":
        state = "federalcapitalterritory"

    counts = market_df[market_df['state']==state.lower()]['market_location'].value_counts().sort_values(ascending=False).reset_index()
    counts['count'] = (counts['count'] / counts['count'].sum()) * 100

    with col2:
        fig = px.bar(
            counts,
            x='market_location',
            y='count',
            orientation='v',
            labels={'market_location': 'Market Location', 'count': 'Percentage of markets located within this range'},
            color='market_location',
            color_discrete_sequence=px.colors.sequential.YlOrRd,
            range_y=(0,100)
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    st.header("Transportation")
    st.write("")

    counts = new_df['produce_transport_method'].value_counts().sort_values(ascending=False).reset_index()
    counts['count'] = (counts['count'] / counts['count'].sum())*100
    counts = counts.drop(index=6)
    full_survey_df