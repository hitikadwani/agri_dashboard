import pandas as pd

# Constants
REGION_MAPPING = {
    'North': ['Delhi', 'Haryana', 'Himachal Pradesh', 'Jammu and Kashmir', 'Punjab', 'Rajasthan', 'Uttarakhand', 'Uttar Pradesh'],
    'South': ['Andhra Pradesh', 'Karnataka', 'Kerala', 'Tamil Nadu', 'Telangana'],
    'East': ['Bihar', 'Jharkhand', 'Odisha', 'West Bengal'],
    'West': ['Gujarat', 'Maharashtra', 'Goa', 'Madhya Pradesh', 'Chhattisgarh'],
    'Northeast': ['Arunachal Pradesh', 'Assam', 'Manipur', 'Meghalaya', 'Mizoram', 'Nagaland', 'Sikkim', 'Tripura']
}

CROP_OPTIONS = [
    {"label": "Rice", "value": "Rice"},
    {"label": "Wheat", "value": "Wheat"},
    {"label": "Maize", "value": "Maize"},
    {"label": "Chickpea", "value": "Chickpea"},
    {"label": "Groundnut", "value": "Groundnut"}
]

FEATURE_OPTIONS = [
    {"label": "Yield (Kg/ha)", "value": "Yield"},
    {"label": "Production (tons)", "value": "Production"},
    {"label": "Area (1000 ha)", "value": "Area"},
    {"label": "Irrigated Area (1000 ha)", "value": "Irrigated_Area"},
    {"label": "Fertilizer Consumption (tons)", "value": "Fertilizer"}
]

# Helper functions
def load_and_preprocess_data():
    """Load and preprocess the dataset"""
    df = pd.read_csv("data/state.csv")
    df['Region'] = df['State Name'].map(
        {state: region for region, states in REGION_MAPPING.items() for state in states}
    )
    return df

def filter_dataframe(df, region=None, year_range=None, production_range=None, selected_crop=None):
    """Filter dataframe based on selected criteria"""
    filtered_df = df.copy()
    
    if region:
        filtered_df = filtered_df[filtered_df['Region'] == region]
    
    if year_range:
        filtered_df = filtered_df[
            (filtered_df['Year'] >= year_range[0]) & 
            (filtered_df['Year'] <= year_range[1])
        ]
    
    if production_range and selected_crop:
        production_column = f'Avg {selected_crop} Production (1000 tons)'
        if production_column in filtered_df.columns:
            filtered_df = filtered_df[
                (filtered_df[production_column] >= production_range[0]) & 
                (filtered_df[production_column] <= production_range[1])
            ]
    
    return filtered_df

def get_feature_column(selected_crop, selected_feature):
    """Get the appropriate column name for a selected feature"""
    feature_map = {
        "Yield": f"Avg {selected_crop} Yield (Kg/ha)",
        "Production": f"Avg {selected_crop} Production (1000 tons)",
        "Area": f"Avg {selected_crop} Area (1000 ha)",
        "Irrigated_Area": f"{selected_crop.upper()}_IRRIGATED_AREA_(1000_ha)",
        "Fertilizer": "Total State Consumption (tons)"
    }
    return feature_map[selected_feature]