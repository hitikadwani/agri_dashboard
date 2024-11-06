import dash
from dash import dcc, html, Input, Output
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
from dash.exceptions import PreventUpdate
from utils.helpers import REGION_MAPPING, CROP_OPTIONS, FEATURE_OPTIONS, load_and_preprocess_data, filter_dataframe, get_feature_column

# Load and preprocess the data
df = load_and_preprocess_data()

# Layout definition
layout = html.Div([
    html.Div([
        dbc.Row([
            dbc.Col([html.Label('Select Region'),
                     dcc.Dropdown(id='region-dropdown', options=[{'label': region, 'value': region} for region in REGION_MAPPING.keys()], value='North')],
                    width=4),
            dbc.Col([html.Label('Select State 1'),
                     dcc.Dropdown(id='state1-dropdown', options=[], value='Andhra Pradesh')],
                    width=4),
            dbc.Col([html.Label('Select State 2'),
                     dcc.Dropdown(id='state2-dropdown', options=[], value='Uttar Pradesh')],
                    width=4),
        ]),
        dbc.Row([
            dbc.Col([html.Label('Select Crop'),
                     dcc.Dropdown(id='crop-dropdown', options=CROP_OPTIONS, value='Rice')],
                    width=4),
            dbc.Col([html.Label('Select Feature 1'),
                     dcc.Dropdown(id='feature1-dropdown', options=FEATURE_OPTIONS, value='Yield')],
                    width=4),
            dbc.Col([html.Label('Select Feature 2'),
                     dcc.Dropdown(id='feature2-dropdown', options=FEATURE_OPTIONS, value='Production')],
                    width=4),
        ])
    ], className="mb-4"),

    dbc.Row([
        dbc.Col([dbc.Card([dbc.CardHeader(html.H4(id='chart1-title')), dbc.CardBody(dcc.Graph(id='chart1'))])], width=6),
        dbc.Col([dbc.Card([dbc.CardHeader(html.H4(id='chart2-title')), dbc.CardBody(dcc.Graph(id='chart2'))])], width=6)
    ])
])

# Callback to update the state dropdowns based on the region selected
@dash.callback(
    [Output('state1-dropdown', 'options'), Output('state1-dropdown', 'value'),
     Output('state2-dropdown', 'options'), Output('state2-dropdown', 'value')],
    [Input('region-dropdown', 'value')]
)
def update_state_dropdowns(selected_region):
    if selected_region:
        states = REGION_MAPPING[selected_region]
        state_options = [{'label': state, 'value': state} for state in states]
        return state_options, states[0], state_options, states[1]
    else:
        raise PreventUpdate

# Callback to update the charts based on the selected features, crop, and states
@dash.callback(
    [Output('chart1', 'figure'),
     Output('chart1-title', 'children'),
     Output('chart2', 'figure'),
     Output('chart2-title', 'children')],
    [Input('state1-dropdown', 'value'),
     Input('state2-dropdown', 'value'),
     Input('crop-dropdown', 'value'),
     Input('feature1-dropdown', 'value'),
     Input('feature2-dropdown', 'value')]
)
def update_charts(state1, state2, selected_crop, feature1, feature2):
    # Filter data for the selected crop
    filtered_df = filter_dataframe(df, None, None, None, selected_crop)
    
    # Get the feature columns for each feature
    feature_column1 = get_feature_column(selected_crop, feature1)
    feature_column2 = get_feature_column(selected_crop, feature2)
    
    # Generate the first chart for State 1 (using feature1)
    chart1 = px.line(filtered_df[filtered_df['State Name'] == state1], x='Year', y=feature_column1)
    chart1_title = f"{feature1} for {selected_crop} in {state1}"
    
    # Generate the second chart for State 2 (using feature2)
    chart2 = px.line(filtered_df[filtered_df['State Name'] == state2], x='Year', y=feature_column2)
    chart2_title = f"{feature2} for {selected_crop} in {state2}"
    
    # Return all outputs, including chart figures and titles
    return chart1, chart1_title, chart2, chart2_title

# To run the app, the following code would be used (e.g., in app.py or a separate file)
# app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
# app.layout = layout
# app.run_server(debug=True)
