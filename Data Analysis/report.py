from dash import dcc, Dash, html, Input, Output, callback
import pandas as pd   
import plotly.express as px

app = Dash(__name__)
app.title = "PHL Risk Dashboard - Nigeria"

app.layout = html.Div([
    html.H1("📊 Post-Harvest Loss Risk Explorer - Nigeria", style={'textAlign': 'center'}),
    
    # Navigation Links (scroll-to-section)
    html.Div([
        html.A("Climate", href="#climate", style={'marginRight': '20px'}),
        html.A("Loss by Stage", href="#loss_stage", style={'marginRight': '20px'}),
        html.A("Storage & Processing", href="#storage", style={'marginRight': '20px'}),
        html.A("Disease & Animal", href="#disease", style={'marginRight': '20px'}),
        html.A("Land Quality", href="#land", style={'marginRight': '20px'}),
        html.A("Market Access", href="#market", style={'marginRight': '20px'}),
        html.A("Disasters", href="#disaster", style={'marginRight': '20px'}),
    ], style={'textAlign': 'center', 'padding': '20px', 'backgroundColor': '#f5f5f5'}),
    
    html.Hr(),

    # Section: Climate
    html.Div([
        html.H2("🌦️ Climate Risk", id="climate"),
        dcc.Markdown("Analysis of climate-related risk factors like seasonal shifts, floods, and droughts."),
        dcc.Dropdown(id="climate_crop_dropdown", options=[...], placeholder="Select Crop"),
        dcc.Dropdown(id="climate_month_dropdown", options=[...], placeholder="Select Month"),
        dcc.Graph(id="climate_choropleth")
    ], style={'padding': '40px'}),

    # Section: Loss by Stage
    html.Div([
        html.H2("📉 Food Loss by Stage", id="loss_stage"),
        dcc.Markdown("Explore where in the value chain most food loss occurs."),
        dcc.Graph(id="loss_by_stage_bar"),
        dcc.Graph(id="crop_stage_loss_stacked")
    ], style={'padding': '40px'}),

    # Section: Storage & Processing
    html.Div([
        html.H2("🏭 Storage & Processing", id="storage"),
        dcc.Markdown("Infrastructure gaps in cold storage and agro-processing."),
        dcc.Graph(id="storage_choropleth"),
        dcc.Graph(id="processing_choropleth"),
        dcc.Dropdown(id="storage_state_dropdown", options=[...], placeholder="Select State"),
        dcc.Graph(id="facility_bar")
    ], style={'padding': '40px'}),

    # Section: Disease & Animal Damage
    html.Div([
        html.H2("🦠 Disease & Animal Damage", id="disease"),
        dcc.Markdown("Biological threats to crops after harvest."),
        dcc.Graph(id="disease_choropleth"),
        dcc.Graph(id="animal_damage_choropleth")
    ], style={'padding': '40px'}),

    # Section: Land Quality
    html.Div([
        html.H2("🌱 Land Quality", id="land"),
        dcc.Markdown("Effects of degraded land and abandoned farms."),
        dcc.Graph(id="land_quality_choropleth"),
        dcc.Graph(id="abandoned_farms_choropleth")
    ], style={'padding': '40px'}),

    # Section: Market Access
    html.Div([
        html.H2("🛣️ Market Access & Transportation", id="market"),
        dcc.Markdown("How distance, poor roads, and logistics lead to loss."),
        dcc.Graph(id="market_distance_choropleth"),
        dcc.Graph(id="market_score_bar"),
        dcc.Graph(id="market_type_location_stacked")
    ], style={'padding': '40px'}),

    # Section: Disasters
    html.Div([
        html.H2("🌪️ Disaster Impact", id="disaster"),
        dcc.Markdown("Natural disasters and their disruption to agriculture."),
        dcc.Graph(id="abandoned_due_to_disaster_bar"),
        dcc.Graph(id="production_disruption_bar"),
        dcc.Graph(id="disaster_severity_grouped"),
        dcc.Graph(id="economic_severity_treemap"),
        dcc.Graph(id="crop_loss_choropleth")
    ], style={'padding': '40px'}),
])

if __name__ == '__main__':
    app.run(debug=True)


