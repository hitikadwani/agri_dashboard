import dash
from dash import html, dcc, Input, Output
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px
from dash.exceptions import PreventUpdate
from utils.helpers import REGION_MAPPING, CROP_OPTIONS, FEATURE_OPTIONS, load_and_preprocess_data, filter_dataframe, get_feature_column

# Load and preprocess the data
df = load_and_preprocess_data()

# Define layout
layout = html.Div([

    # Row for region, state dropdowns, and crop/feature selection
    html.Div([
        dbc.Row([

            # Region Dropdown
            dbc.Col([
                html.Label('Select Region'),
                dcc.Dropdown(
                    id='region-dropdown',
                    options=[{'label': region, 'value': region} for region in REGION_MAPPING.keys()],
                    value='North'  # default region
                )
            ], width=4),

            # State 1 Dropdown
            dbc.Col([
                html.Label('Select State 1'),
                dcc.Dropdown(
                    id='state1-dropdown',
                    options=[],  # options will be updated dynamically
                    value=None  # Initially empty, will get updated
                )
            ], width=4),

            # State 2 Dropdown
            dbc.Col([
                html.Label('Select State 2'),
                dcc.Dropdown(
                    id='state2-dropdown',
                    options=[],  # options will be updated dynamically
                    value=None  # Initially empty, will get updated
                )
            ], width=4)
        ]),

        dbc.Row([

            # Crop Dropdown
            dbc.Col([
                html.Label('Select Crop'),
                dcc.Dropdown(
                    id='crop-dropdown',
                    options=CROP_OPTIONS,  # predefined list of crops
                    value='Rice'  # default crop
                )
            ], width=4),

            # Feature Dropdown
            dbc.Col([
                html.Label('Select Feature'),
                dcc.Dropdown(
                    id='feature-dropdown',
                    options=FEATURE_OPTIONS,  # predefined list of features
                    value='Yield'  # default feature
                )
            ], width=4)

        ])
    ], className="mb-4"),

    # Row for displaying charts
    dbc.Row([

        # Chart 1 for State 1
        dbc.Col([
            dbc.Card([
                dbc.CardHeader(html.H4(id='chart1-title')),  # Chart Title
                dbc.CardBody(
                    dcc.Graph(id='chart1')  # Graph for State 1
                )
            ])
        ], width=6),

        # Chart 2 for State 2
        dbc.Col([
            dbc.Card([
                dbc.CardHeader(html.H4(id='chart2-title')),  # Chart Title
                dbc.CardBody(
                    dcc.Graph(id='chart2')  # Graph for State 2
                )
            ])
        ], width=6)

    ])

])


# Callback to update State Dropdowns based on Region Selection
@dash.callback(
    [Output('state1-dropdown', 'options'),
     Output('state1-dropdown', 'value'),
     Output('state2-dropdown', 'options'),
     Output('state2-dropdown', 'value')],
    [Input('region-dropdown', 'value')]
)
def update_state_dropdowns(selected_region):
    if selected_region:
        # Get the states for the selected region
        states = REGION_MAPPING[selected_region]
        state_options = [{'label': state, 'value': state} for state in states]
        return state_options, states[0], state_options, states[1]  # Default two states to be selected
    else:
        raise PreventUpdate


# Callback to update charts based on state, crop, and feature selection
@dash.callback(
    [Output('chart1', 'figure'),
     Output('chart1-title', 'children'),
     Output('chart2', 'figure'),
     Output('chart2-title', 'children')],
    [Input('state1-dropdown', 'value'),
     Input('state2-dropdown', 'value'),
     Input('crop-dropdown', 'value'),
     Input('feature-dropdown', 'value')]
)
def update_charts(state1, state2, selected_crop, selected_feature):
    # Prevent update if no states are selected
    if not state1 or not state2:
        raise PreventUpdate

    # Filter dataframe based on selected crop
    filtered_df = filter_dataframe(df, None, None, None, selected_crop)

    # Get the feature column for the selected feature
    feature_column = get_feature_column(selected_crop, selected_feature)

    # Create chart for State 1
    chart1 = px.line(filtered_df[filtered_df['State Name'] == state1], x='Year', y=feature_column)
    chart1.update_layout(
        title=f"{selected_feature} for {selected_crop} in {state1}",
        xaxis_title="Year",
        yaxis_title=selected_feature
    )

    # Create chart for State 2
    chart2 = px.line(filtered_df[filtered_df['State Name'] == state2], x='Year', y=feature_column)
    chart2.update_layout(
        title=f"{selected_feature} for {selected_crop} in {state2}",
        xaxis_title="Year",
        yaxis_title=selected_feature
    )

    # Return updated charts and titles
    return chart1, f"{selected_feature} for {selected_crop} in {state1}", chart2, f"{selected_feature} for {selected_crop} in {state2}"

