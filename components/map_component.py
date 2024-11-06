import folium
from dash import html
from folium.plugins import MarkerCluster

def create_map(df, state_name):
    # Filter data for the selected state
    state_data = df[df["State Name"] == state_name]

    # Define the map center and initialize the map
    m = folium.Map(location=[20.5937, 78.9629], zoom_start=5)

    # Add MarkerCluster for each year
    marker_cluster = MarkerCluster().add_to(m)
    for _, row in state_data.iterrows():
        folium.Marker(
            location=[row['Latitude'], row['Longitude']], # Assuming latitude and longitude columns
            popup=f"Year: {row['Year']}<br>Rice Yield: {row['Avg Rice Yield (Kg/ha)']}"
        ).add_to(marker_cluster)

    return html.Iframe(srcDoc=m._repr_html_(), width="100%", height="500")
