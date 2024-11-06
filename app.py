import dash
from dash import dcc, html, Input, Output
import pandas as pd
import plotly.express as px

# Load the dataset
df = pd.read_csv("data/state.csv")

# Define region mapping
region_mapping = {
    'North': ['Delhi', 'Haryana', 'Himachal Pradesh', 'Jammu and Kashmir', 'Punjab', 'Rajasthan', 'Uttarakhand', 'Uttar Pradesh'],
    'South': ['Andhra Pradesh', 'Karnataka', 'Kerala', 'Tamil Nadu', 'Telangana'],
    'East': ['Bihar', 'Jharkhand', 'Odisha', 'West Bengal'],
    'West': ['Gujarat', 'Maharashtra', 'Goa', 'Madhya Pradesh', 'Chhattisgarh'],
    'Northeast': ['Arunachal Pradesh', 'Assam', 'Manipur', 'Meghalaya', 'Mizoram', 'Nagaland', 'Sikkim', 'Tripura']
}

# Add region column to the dataframe
df['Region'] = df['State Name'].map({state: region for region, states in region_mapping.items() for state in states})

# Get min and max years from the data
min_year = df['Year'].min()
max_year = df['Year'].max()

# Get min and max production values
min_production = df['Avg Rice Production (1000 tons)'].min()
max_production = df['Avg Rice Production (1000 tons)'].max()

# Get min and max annual rainfall values
min_rainfall = df['Annual_Rainfall'].min()
max_rainfall = df['Annual_Rainfall'].max()

# Crop options
crop_options = [
    {"label": "Rice", "value": "Rice"},
    {"label": "Wheat", "value": "Wheat"},
    {"label": "Maize", "value": "Maize"},
    {"label": "Chickpea", "value": "Chickpea"},
    {"label": "Groundnut", "value": "Groundnut"}
]

# Feature options
feature_options = [
    {"label": "Yield (Kg/ha)", "value": "Yield"},
    {"label": "Production (tons)", "value": "Production"},
    {"label": "Area (1000 ha)", "value": "Area"},
    {"label": "Irrigated Area (1000 ha)", "value": "Irrigated_Area"},
    {"label": "Fertilizer Consumption (tons)", "value": "Fertilizer"},
    {"label": "Annual Rainfall (mm)", "value": "Annual_Rainfall"}
]

# Initialize the Dash app
app = dash.Dash(__name__, external_stylesheets=[
    "https://cdn.jsdelivr.net/npm/tailwindcss@2.2.19/dist/tailwind.min.css"
])
app.title = "India State-wise Crop Analysis Dashboard"
server = app.server

# Define the layout with improved UI and Tailwind CSS classes
app.layout = html.Div(className="bg-gray-100 min-h-screen", children=[
    html.Div(className="container mx-auto px-4 py-8", children=[
        html.H1("State-wise Crop Analysis in India", className="text-4xl font-bold mb-8 text-center text-gray-800 border-b-2 border-green-500 pb-4"),
        
        # Filters Section
        html.Div(className="bg-white rounded-lg shadow-lg p-6 mb-8", children=[
            html.H2("Filters", className="text-2xl font-semibold mb-4 text-gray-800"),
            
            # Grid for filters
            html.Div(className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4", children=[
                # Region Filter
                html.Div(children=[
                    html.Label("Select Region:", className="block mb-2 text-sm font-medium text-gray-700"),
                    dcc.Dropdown(
                        id="region-dropdown",
                        options=[{"label": region, "value": region} for region in region_mapping.keys()],
                        value="North",
                        clearable=False,
                        className="w-full"
                    ),
                ]),
                
                # Crop Selection
                html.Div(children=[
                    html.Label("Select Crop:", className="block mb-2 text-sm font-medium text-gray-700"),
                    dcc.Dropdown(
                        id="crop-dropdown",
                        options=crop_options,
                        value="Rice",
                        clearable=False,
                        className="w-full"
                    ),
                ]),
                
                # State Selection based on Region
                html.Div(children=[
                    html.Label("Select State:", className="block mb-2 text-sm font-medium text-gray-700"),
                    dcc.Dropdown(
                        id="state-dropdown",
                        className="w-full"
                    ),
                ]),
                
                # Year Range Slider
                html.Div(className="col-span-full", children=[
                    html.Label("Select Year Range:", className="block mb-2 text-sm font-medium text-gray-700"),
                    dcc.RangeSlider(
                        id="year-range-slider",
                        min=min_year,
                        max=max_year,
                        value=[min_year, max_year],
                        marks={str(year): str(year) for year in range(min_year, max_year + 1, 2)},
                        className="mt-2"
                    ),
                ]),
                
                # Production Range Slider
                html.Div(className="col-span-full", children=[
                    html.Label("Production Scale (1000 tons):", className="block mb-2 text-sm font-medium text-gray-700"),
                    dcc.RangeSlider(
                        id="production-range-slider",
                        min=min_production,
                        max=max_production,
                        value=[min_production, max_production],
                        marks={
                            str(int(min_production)): str(int(min_production)),
                            str(int(max_production/2)): str(int(max_production/2)),
                            str(int(max_production)): str(int(max_production))
                        },
                        className="mt-2"
                    ),
                ]),
                
                # Rainfall Range Slider
                html.Div(className="col-span-full", children=[
                    html.Label("Annual Rainfall Scale (mm):", className="block mb-2 text-sm font-medium text-gray-700"),
                    dcc.RangeSlider(
                        id="rainfall-range-slider",
                        min=min_rainfall,
                        max=max_rainfall,
                        value=[min_rainfall, max_rainfall],
                        marks={
                            str(int(min_rainfall)): str(int(min_rainfall)),
                            str(int(max_rainfall/2)): str(int(max_rainfall/2)),
                            str(int(max_rainfall)): str(int(max_rainfall))
                        },
                        className="mt-2"
                    ),
                ]),
            ]),
        ]),
        
        # Visualization Section with Feature Selection
        html.Div(className="grid grid-cols-1 lg:grid-cols-2 gap-8", children=[
            # First Card with Feature Selection
            html.Div(className="bg-white rounded-lg shadow-lg p-6", children=[
                html.Div(className="flex justify-between items-center mb-4", children=[
                    html.H2("Feature Analysis 1", className="text-2xl font-semibold text-gray-800"),
                    dcc.Dropdown(
                        id="feature-dropdown-1",
                        options=feature_options,
                        value="Yield",
                        clearable=False,
                        className="w-48"
                    ),
                ]),
                dcc.Graph(id="feature-chart-1", className="h-96")
            ]),
            
            # Second Card with Feature Selection
            html.Div(className="bg-white rounded-lg shadow-lg p-6", children=[
                html.Div(className="flex justify-between items-center mb-4", children=[
                    html.H2("Feature Analysis 2", className="text-2xl font-semibold text-gray-800"),
                    dcc.Dropdown(
                        id="feature-dropdown-2",
                        options=feature_options,
                        value="Production",
                        clearable=False,
                        className="w-48"
                    ),
                ]),
                dcc.Graph(id="feature-chart-2", className="h-96")
            ]),
        ]),
        
        # Map for state analysis
        html.Div(className="bg-white rounded-lg shadow-lg p-6 mt-8", children=[
            html.H2("State Analysis Map", className="text-2xl font-semibold mb-4 text-gray-800"),
            dcc.Graph(id="state-analysis-map", className="h-[600px]")
        ]),
        
        html.Footer(className="mt-8 text-center text-gray-600", children=[
           
            html.P("India State-wise Crop Analysis Dashboard")
        ])
    ])
])

# Callback to update state dropdown based on region selection
@app.callback(
    Output("state-dropdown", "options"),
    Output("state-dropdown", "value"),
    Input("region-dropdown", "value")
)
def update_state_dropdown(selected_region):
    if not selected_region:
        raise dash.exceptions.PreventUpdate
    states = region_mapping[selected_region]
    options = [{"label": state, "value": state} for state in states]
    return options, states[0]

# Function to filter dataframe
def filter_dataframe(df, region, year_range, production_range, rainfall_range, selected_crop):
    filtered_df = df.copy()
    
    if region:
        filtered_df = filtered_df[filtered_df['Region'] == region]
    
    filtered_df = filtered_df[
        (filtered_df['Year'] >= year_range[0]) & 
        (filtered_df['Year'] <= year_range[1])
    ]
    
    production_column = f'Avg {selected_crop} Production (1000 tons)'
    if production_column in filtered_df.columns:
        filtered_df = filtered_df[
            (filtered_df[production_column] >= production_range[0]) & 
            (filtered_df[production_column] <= production_range[1])
        ]
    
    filtered_df = filtered_df[
        (filtered_df['Annual_Rainfall'] >= rainfall_range[0]) &
        (filtered_df['Annual_Rainfall'] <= rainfall_range[1])
    ]
    
    return filtered_df

# Function to create feature chart
def create_feature_chart(filtered_df, selected_state, selected_crop, selected_feature):
    feature_map = {
        "Yield": f"Avg {selected_crop} Yield (Kg/ha)",
        "Production": f"Avg {selected_crop} Production (1000 tons)",
        "Area": f"Avg {selected_crop} Area (1000 ha)",
        "Irrigated_Area": f"{selected_crop.upper()}_IRRIGATED_AREA_(1000_ha)",
        "Fertilizer": "Total State Consumption (tons)",
        "Annual_Rainfall": "Annual_Rainfall"
    }
    
    state_data = filtered_df[filtered_df["State Name"] == selected_state]
    
    fig = px.line(
        state_data,
        x="Year",
        y=feature_map[selected_feature],
        title=f"{selected_crop} {selected_feature} in {selected_state}",
        labels={feature_map[selected_feature]: selected_feature}
    )
    
    fig.update_layout(
        xaxis_title="Year",
        yaxis_title=selected_feature,
        plot_bgcolor="white",
        paper_bgcolor="white"
    )
    
    return fig

# Callbacks for feature charts
@app.callback(
    Output("feature-chart-1", "figure"),
    [Input("state-dropdown", "value"),
     Input("crop-dropdown", "value"),
     Input("feature-dropdown-1", "value"),
     Input("region-dropdown", "value"),
     Input("year-range-slider", "value"),
     Input("production-range-slider", "value"),
     Input("rainfall-range-slider", "value")]
)
def update_feature_chart_1(selected_state, selected_crop, selected_feature, 
                         selected_region, year_range, production_range, rainfall_range):
    filtered_df = filter_dataframe(df, selected_region, year_range, production_range, rainfall_range, selected_crop)
    return create_feature_chart(filtered_df, selected_state, selected_crop, selected_feature)

@app.callback(
    Output("feature-chart-2", "figure"),
    [Input("state-dropdown", "value"),
     Input("crop-dropdown", "value"),
     Input("feature-dropdown-2", "value"),
     Input("region-dropdown", "value"),
     Input("year-range-slider", "value"),
     Input("production-range-slider", "value"),
     Input("rainfall-range-slider", "value")]
)
def update_feature_chart_2(selected_state, selected_crop, selected_feature, 
                         selected_region, year_range, production_range, rainfall_range):
    filtered_df = filter_dataframe(df, selected_region, year_range, production_range, rainfall_range, selected_crop)
    return create_feature_chart(filtered_df, selected_state, selected_crop, selected_feature)

# Map callback
@app.callback(
    Output("state-analysis-map", "figure"),
    [Input("crop-dropdown", "value"),
     Input("feature-dropdown-1", "value"),
     Input("region-dropdown", "value"),
     Input("year-range-slider", "value"),
     Input("production-range-slider", "value"),
     Input("rainfall-range-slider", "value")]
)
def update_map(selected_crop, selected_feature, 
               selected_region, year_range, production_range, rainfall_range):
    filtered_df = filter_dataframe(df, selected_region, year_range, production_range, rainfall_range, selected_crop)
    feature_map = {
        "Yield": f"Avg {selected_crop} Yield (Kg/ha)",
        "Production": f"Avg {selected_crop} Production (1000 tons)",
        "Area": f"Avg {selected_crop} Area (1000 ha)",
        "Irrigated_Area": f"{selected_crop.upper()}_IRRIGATED_AREA_(1000_ha)",
        "Fertilizer": "Total State Consumption (tons)",
        "Annual_Rainfall": "Annual_Rainfall"
    }
    
    latest_year = filtered_df['Year'].max()
    latest_data = filtered_df[filtered_df['Year'] == latest_year]
    
    fig = px.choropleth_mapbox(
        latest_data,
        locations='State Name',
        geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
        featureidkey='properties.ST_NM',
        color=feature_map[selected_feature],
        hover_data=['State Name', feature_map[selected_feature]],
        title=f"{selected_crop} {selected_feature} Across Indian States (Year: {latest_year})",
        mapbox_style="carto-positron",
        center={"lat": 20.5937, "lon": 78.9629},
        zoom=3,
        opacity=0.7,
        color_continuous_scale="Viridis"
    )
    
    fig.update_layout(
        margin={"r":0,"t":30,"l":0,"b":0},
        mapbox_style="carto-positron",
        height=600,
        paper_bgcolor="white"
    )
    
    return fig

if __name__ == "__main__":
    app.run_server(debug=True)
    port = int(os.environ.get("PORT", 8050))
    app.run_server(host="0.0.0.0", port=port)