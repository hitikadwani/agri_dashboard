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

# Get all states for dropdowns
all_states = sorted([state for states in region_mapping.values() for state in states])

# Get min and max years from the data
min_year = df['Year'].min()
max_year = df['Year'].max()

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

# Define the layout
app.layout = html.Div(className="bg-gradient-to-r from-green-50 to-blue-50 min-h-screen p-4 sm:p-6", children=[
    html.Div(className="max-w-7xl mx-auto space-y-6", children=[
        html.H1("State-wise Crop Analysis in India", className="text-3xl sm:text-4xl font-bold mb-8 text-center text-gray-800 border-b-2 border-green-500 pb-4"),
        
        # Filters Section with improved spacing
        html.Div(className="bg-white rounded-lg shadow-lg p-4 sm:p-6", children=[
            html.H2("Filters", className="text-xl sm:text-2xl font-semibold mb-6 text-gray-800"),
            
            # Grid for filters with even spacing
            html.Div(className="grid grid-cols-1 sm:grid-cols-3 gap-6", children=[
                # State 1 Selection
                html.Div(className="flex flex-col", children=[
                    html.Label("Select State 1:", className="block mb-2 text-sm font-medium text-gray-700"),
                    dcc.Dropdown(
                        id="state-dropdown-1",
                        options=[{"label": state, "value": state} for state in all_states],
                        value=all_states[0],
                        clearable=False,
                        className="w-full"
                    ),
                ]),
                
                # State 2 Selection
                html.Div(className="flex flex-col", children=[
                    html.Label("Select State 2:", className="block mb-2 text-sm font-medium text-gray-700"),
                    dcc.Dropdown(
                        id="state-dropdown-2",
                        options=[{"label": state, "value": state} for state in all_states],
                        value=all_states[1],
                        clearable=False,
                        className="w-full"
                    ),
                ]),
                
                # Crop Selection
                html.Div(className="flex flex-col", children=[
                    html.Label("Select Crop:", className="block mb-2 text-sm font-medium text-gray-700"),
                    dcc.Dropdown(
                        id="crop-dropdown",
                        options=crop_options,
                        value="Rice",
                        clearable=False,
                        className="w-full"
                    ),
                ]),
            ]),
            
            # Year Range Slider with better spacing
            html.Div(className="mt-6", children=[
                html.Label("Select Year Range:", className="block mb-4 text-sm font-medium text-gray-700"),
                dcc.RangeSlider(
                    id="year-range-slider",
                    min=min_year,
                    max=max_year,
                    value=[min_year, max_year],
                    marks={str(year): {"label": str(year), "style": {"transform": "rotate(-45deg)", "margin-top": "10px"}} 
                           for year in range(min_year, max_year + 1, 2)},
                    className="mt-2"
                ),
            ]),
        ]),
        
        # Visualization Section with improved styling
        html.Div(className="grid grid-cols-1 lg:grid-cols-2 gap-6 mt-6", children=[
            # First Card - Feature Comparison
            html.Div(className="bg-white rounded-lg shadow-lg p-4 sm:p-6", children=[
                html.Div(className="flex flex-col sm:flex-row justify-between items-center mb-6", children=[
                    html.H2("Feature Comparison", className="text-xl sm:text-2xl font-semibold text-gray-800 mb-4 sm:mb-0"),
                    dcc.Dropdown(
                        id="feature-dropdown-1",
                        options=feature_options,
                        value="Yield",
                        clearable=False,
                        className="w-full sm:w-64"
                    ),
                ]),
                dcc.Graph(id="feature-chart-1")
            ]),
            
            # Second Card - Another Feature Comparison
            html.Div(className="bg-white rounded-lg shadow-lg p-4 sm:p-6", children=[
                html.Div(className="flex flex-col sm:flex-row justify-between items-center mb-6", children=[
                    html.H2("Additional Comparison", className="text-xl sm:text-2xl font-semibold text-gray-800 mb-4 sm:mb-0"),
                    dcc.Dropdown(
                        id="feature-dropdown-2",
                        options=feature_options,
                        value="Production",
                        clearable=False,
                        className="w-full sm:w-64"
                    ),
                ]),
                dcc.Graph(id="feature-chart-2")
            ]),
        ]),
        
        # Map Section
        html.Div(className="bg-white rounded-lg shadow-lg p-4 sm:p-6 mt-6", children=[
            html.H2("State Analysis Map", className="text-xl sm:text-2xl font-semibold mb-4 text-gray-800"),
            dcc.Graph(id="state-analysis-map")
        ]),
        
        html.Footer(className="mt-8 text-center text-gray-600", children=[
            
            html.P("© 2024 India State-wise Crop Analysis Dashboard")
        ])
    ])
])

# Function to filter dataframe for two states
def filter_dataframe(df, state1, state2, year_range, selected_crop):
    filtered_df = df.copy()
    
    filtered_df = filtered_df[
        (filtered_df['State Name'].isin([state1, state2])) &
        (filtered_df['Year'] >= year_range[0]) & 
        (filtered_df['Year'] <= year_range[1])
    ]
    
    return filtered_df

# Callback for feature comparison chart
# Update the line graph callback with improved styling
@app.callback(
    Output("feature-chart-1", "figure"),
    [Input("state-dropdown-1", "value"),
     Input("state-dropdown-2", "value"),
     Input("crop-dropdown", "value"),
     Input("feature-dropdown-1", "value"),
     Input("year-range-slider", "value")]
)
def update_feature_comparison(state1, state2, selected_crop, selected_feature, year_range):
    filtered_df = filter_dataframe(df, state1, state2, year_range, selected_crop)
    
    feature_map = {
        "Yield": f"Avg {selected_crop} Yield (Kg/ha)",
        "Production": f"Avg {selected_crop} Production (1000 tons)",
        "Area": f"Avg {selected_crop} Area (1000 ha)",
        "Irrigated_Area": f"{selected_crop.upper()}_IRRIGATED_AREA_(1000_ha)",
        "Fertilizer": "Total State Consumption (tons)",
        "Annual_Rainfall": "Annual_Rainfall"
    }
    
    fig = px.line(
        filtered_df,
        x="Year",
        y=feature_map[selected_feature],
        color="State Name",
        title=f"{selected_crop} {selected_feature} Comparison",
        labels={feature_map[selected_feature]: selected_feature}
    )
    
    # Enhanced line graph styling
    fig.update_traces(
        line=dict(width=3),
        marker=dict(size=8)
    )
    
    fig.update_layout(
        title=dict(
            text=f"{selected_crop} {selected_feature} Comparison",
            font=dict(size=20, color='#2D3748', family="Arial, sans-serif"),
            x=0.5,
            y=0.95
        ),
        xaxis=dict(
            title="Year",
            title_font=dict(size=14, family="Arial, sans-serif"),
            tickfont=dict(size=12),
            showgrid=True,
            gridwidth=1,
            gridcolor='rgba(211, 211, 211, 0.5)'
        ),
        yaxis=dict(
            title=selected_feature,
            title_font=dict(size=14, family="Arial, sans-serif"),
            tickfont=dict(size=12),
            showgrid=True,
            gridwidth=1,
            gridcolor='rgba(211, 211, 211, 0.5)'
        ),
        plot_bgcolor='white',
        paper_bgcolor='white',
        margin=dict(t=80, r=30, b=50, l=50),
        legend=dict(
            yanchor="top",
            y=0.99,
            xanchor="right",
            x=0.99,
            bgcolor='rgba(255, 255, 255, 0.8)',
            bordercolor='rgba(211, 211, 211, 0.8)',
            borderwidth=1
        ),
        hovermode='x unified'
    )
    
    return fig

# Callback for second feature comparison chart
@app.callback(
    Output("feature-chart-2", "figure"),
    [Input("state-dropdown-1", "value"),
     Input("state-dropdown-2", "value"),
     Input("crop-dropdown", "value"),
     Input("feature-dropdown-2", "value"),
     Input("year-range-slider", "value")]
)
def update_additional_comparison(state1, state2, selected_crop, selected_feature, year_range):
    filtered_df = filter_dataframe(df, state1, state2, year_range, selected_crop)
    
    feature_map = {
        "Yield": f"Avg {selected_crop} Yield (Kg/ha)",
        "Production": f"Avg {selected_crop} Production (1000 tons)",
        "Area": f"Avg {selected_crop} Area (1000 ha)",
        "Irrigated_Area": f"{selected_crop.upper()}_IRRIGATED_AREA_(1000_ha)",
        "Fertilizer": "Total State Consumption (tons)",
        "Annual_Rainfall": "Annual_Rainfall"
    }
    
    fig = px.bar(
        filtered_df,
        x="Year",
        y=feature_map[selected_feature],
        color="State Name",
        barmode="group",
        title=f"{selected_crop} {selected_feature} Comparison",
        labels={feature_map[selected_feature]: selected_feature}
    )
    
    # Enhanced bar graph styling
    fig.update_layout(
        title=dict(
            text=f"{selected_crop} {selected_feature} Comparison",
            font=dict(size=20, color='#2D3748', family="Arial, sans-serif"),
            x=0.5,
            y=0.95
        ),
        xaxis=dict(
            title="Year",
            title_font=dict(size=14, family="Arial, sans-serif"),
            tickfont=dict(size=12),
            showgrid=True,
            gridwidth=1,
            gridcolor='rgba(211, 211, 211, 0.5)'
        ),
        yaxis=dict(
            title=selected_feature,
            title_font=dict(size=14, family="Arial, sans-serif"),
            tickfont=dict(size=12),
            showgrid=True,
            gridwidth=1,
            gridcolor='rgba(211, 211, 211, 0.5)'
        ),
        plot_bgcolor='white',
        paper_bgcolor='white',
        margin=dict(t=80, r=30, b=50, l=50),
        legend=dict(
            yanchor="top",
            y=0.99,
            xanchor="right",
            x=0.99,
            bgcolor='rgba(255, 255, 255, 0.8)',
            bordercolor='rgba(211, 211, 211, 0.8)',
            borderwidth=1
        ),
        hovermode='x unified',
        bargap=0.15,
        bargroupgap=0.1
    )
    
    return fig

# Map callback - showing both selected states highlighted
@app.callback(
    Output("state-analysis-map", "figure"),
    [Input("state-dropdown-1", "value"),
     Input("state-dropdown-2", "value"),
     Input("crop-dropdown", "value"),
     Input("feature-dropdown-1", "value"),
     Input("year-range-slider", "value")]
)
def update_map(state1, state2, selected_crop, selected_feature, year_range):
    filtered_df = df.copy()
    filtered_df = filtered_df[filtered_df['Year'] == year_range[1]]  # Use the latest year
    
    feature_map = {
        "Yield": f"Avg {selected_crop} Yield (Kg/ha)",
        "Production": f"Avg {selected_crop} Production (1000 tons)",
        "Area": f"Avg {selected_crop} Area (1000 ha)",
        "Irrigated_Area": f"{selected_crop.upper()}_IRRIGATED_AREA_(1000_ha)",
        "Fertilizer": "Total State Consumption (tons)",
        "Annual_Rainfall": "Annual_Rainfall"
    }
    
    # Highlight selected states
    filtered_df['Selected'] = filtered_df['State Name'].isin([state1, state2])
    
    fig = px.choropleth_mapbox(
        filtered_df,
        locations='State Name',
        geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
        featureidkey='properties.ST_NM',
        color=feature_map[selected_feature],
        hover_data=['State Name', feature_map[selected_feature]],
        title=f"{selected_crop} {selected_feature} Across Indian States (Year: {year_range[1]})",
        mapbox_style="carto-positron",
        center={"lat": 20.5937, "lon": 78.9629},
        zoom=3,
        opacity=0.7,
        color_continuous_scale="Viridis"
    )
    
    # Add different styling for selected states
    for state in [state1, state2]:
        state_data = filtered_df[filtered_df['State Name'] == state]
        if not state_data.empty:
            fig.add_traces(px.choropleth_mapbox(
                state_data,
                locations='State Name',
                geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                featureidkey='properties.ST_NM',
                color_discrete_sequence=['rgba(255,0,0,0.3)']
                ).data[0])
    
    fig.update_layout(
        title=dict(
            text=f"{selected_crop} {selected_feature} Across Indian States (Year: {year_range[1]})",
            font=dict(size=20, color='#2D3748'),
            x=0.5
        ),
        mapbox=dict(
            center=dict(lat=20.5937, lon=78.9629),
            zoom=3,
            style="carto-positron"
        ),
        margin=dict(t=80, r=30, b=50, l=50),
        paper_bgcolor='white'
    )
    
    return fig

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True, port=8050)