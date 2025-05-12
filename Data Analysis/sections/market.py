import pandas as pd
import plotly.express as px
import streamlit as st
def add_space():
    st.markdown("<br><br>", unsafe_allow_html=True)

def render_market_section(geojson, market_df,full_survey_df):
    st.header("Market Access")
    st.markdown('<div id="market-access"></div>', unsafe_allow_html=True)
    st.markdown("""
        Market access is a critical factor in determining the profitability and sustainability of agricultural practices. In Nigeria, the lack of efficient market access can lead to significant post-harvest losses.
        We analyse the responses of farmers from a nationwide survey by the [NBS](https://microdata.nigerianstat.gov.ng/index.php/catalog/80/get-microdata), to get insights on what states are lacking access and where a young entreprenur may profer solutions like mobile markets or delivery 
        services to help farmers get their produce to customers (markets or end-users directly).
             """)
    
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
        
        fig.update_layout(margin={"r": 0, "t": 30, "l": 0, "b": 0})
        st.plotly_chart(fig, use_container_width=True)
    st.markdown("""
                From the map we can see that:
    - In **FCT (Abuja)**, about **12.24%** of respondents said their closest market is **outside the state**, highlighting strong demand for localized aggregation or transport services.
    - States like **Jigawa (20%), Bayelsa (15%), and Rivers (13.7%)** have the most respondents with the closest market **in another LGA**. 
                """)
    add_space()

    with col3:
        st.empty()
    
    st.write("Select your state of interest for a more comprehensive overview of market access within it.")
    col1,col2,col3 =  st.columns([1,4,1])


    def format_state(state_name):
            if state_name.lower() == "federalcapitalterritory":
                return "FCT"
            return state_name.capitalize()
    with col1:
        state = st.selectbox(
            "Select State",
            sorted(market_df["state"].apply(format_state).unique()),
            key="state_selectbox_1"
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
       
    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown('<div id="transport"></div>', unsafe_allow_html=True)
    st.header("Transportation")
    st.markdown("""
    Even with a market within reasonable distance the farmers still need a realiable method to move their crops especially crops which need cold storage or gentle handling.
    We analyzed farmer responses across Nigeria on their **primary method of transporting produce**:
   
    * **53%** use **tricycles or motorcycles**
    * **21.5%** use **cars or vans**
    * **19.8%** move produce **on foot**

                
    This indicates a **lack of access to efficient, scalable logistics**, especially in rural and semi-urban areas.
    For entrepreneurs, this gap suggests an opportunity to build affordable **transport cooperatives**, **last-mile delivery platforms** and provide **rentable cold storage units or mobile cooling vans**
    """)
    st.markdown("<br>",unsafe_allow_html=True)

    col1,col2,col3 = st.columns([1,4,1])
    state_list = sorted(market_df["state"].apply(format_state).unique())
    state_list.insert(0,'Nigeria')

    with col1:
        state = st.selectbox(
            "Select State",
            state_list,
            key="state_selectbox_2",
            index=0
        )
    if state == "FCT":
        state = "federalcapitalterritory"

    if state == 'Nigeria':
        counts = full_survey_df['produce_transport_method'].value_counts().sort_values(ascending=False).reset_index()
        counts['count'] = (counts['count'] / counts['count'].sum())*100
        counts = counts[counts['produce_transport_method'] != "Other (specify)"]
    else:
        counts = full_survey_df[full_survey_df['state']==state.lower()]['produce_transport_method'].value_counts().sort_values(ascending=False).reset_index()
        counts['count'] = (counts['count'] / counts['count'].sum())*100
        counts = counts[counts['produce_transport_method'] != "Other (specify)"]
    
    with col2:
        fig = px.bar(
        counts,
        y='produce_transport_method',
        x='count',
        orientation='h',
        title=f"Transport Methods Used by Nigerian Farmers in {state.capitalize()}",
        labels={'produce_transport_method': 'Transport Method  ', 'count': 'Percentage who use it  '},
        color='produce_transport_method',
        color_discrete_sequence=px.colors.sequential.YlOrRd,
        range_x=(0,100),
        )

        st.plotly_chart(fig, use_container_width=True)
        add_space()


    st.markdown("""
        It's also important to consider that in some cases people opt for other methods not by choice, **but due to a lack of motorable roads**.
        The map below shows the **percentage of farmers in each state who reported poor roads affected their livelihood**. This higlights areas where **lack
        of infrastructure could limit transport solutions**, and helps make decisions on **logistics solutions targeted for a specific region**. 
""")
    
    st.markdown("<br>",unsafe_allow_html=True)
    col1,col2,col3 = st.columns([1,4,1])
    counts = full_survey_df.groupby(['state', 'poor_transport']).size().unstack(fill_value=0)
    counts['total'] = counts.sum(axis=1)
    counts['yes_pct'] = (counts['Yes'] / counts['total']) * 100
    counts['no_pct'] = (counts['No'] / counts['total']) * 100
    counts = counts.reset_index()

    with col2:
        fig = px.choropleth_mapbox(
        counts,
        geojson=geojson,
        locations='state',
        featureidkey='properties.state',
        color='yes_pct',
        color_continuous_scale='YlOrRd',
        title='Percentage of Farmers with Complaints About Poor Transport by State',
        labels={'yes_pct': 'Percentage of Complaints'},
        mapbox_style='carto-positron',
        zoom=4.9,
        center={"lat": 9.1, "lon": 8.7},
        opacity=0.7
    )

        fig.update_layout(margin={"r": 0, "t": 30, "l": 0, "b": 0})
        st.plotly_chart(fig, use_container_width=True)
    
    st.markdown("""
    Access to good roads is a general issue nationwide. As, **Imo the state with the least complaints, has about 32.8%** of respondents identifying poor roads as a problem.
    
    From the map above we see the **most affected states are**:     
    - **Akwa Ibom (79.5%)**.
    - **Ebonyi (74.8%)**.
    - **Cross River (74.3%)**.
    - **Ondo (74.26%)**.
    - **Kwara (72.3%)**. 
         
    These high complaint rates could be red flags for entrepreneurs offering logistics solutions by road, but could also be a chance for smore targeted solutions.
""")
    
    