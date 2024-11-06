import plotly.graph_objects as go


def create_crop_line_chart(df, state_name, crop, feature):
    # Filter data for the selected state
    state_data = df[df["State Name"] == state_name]
    
    # Define the column name based on selected crop and feature
    if feature == "Yield":
        column_name = f"Avg {crop} Yield (Kg/ha)"
    elif feature == "Production":
        column_name = f"Avg {crop} Production (1000 tons)"
    else:
        raise ValueError("Invalid feature selected. Choose 'Yield' or 'Production'.")
    
    # Check if the column exists in the dataframe
    if column_name not in state_data.columns:
        raise KeyError(f"Column '{column_name}' not found in the dataset.")
    
    # Create a figure for the selected crop feature over years
    fig = go.Figure()
    
    # Add line for the selected crop feature (Yield or Production)
    fig.add_trace(go.Scatter(
        x=state_data["Year"],
        y=state_data[column_name],
        mode="lines+markers",
        name=f"{crop} {feature}"
    ))

    # Customize layout
    fig.update_layout(
        title=f"{crop} {feature} Over Years in {state_name}",
        xaxis_title="Year",
        yaxis_title=f"{feature} ({'Kg/ha' if feature == 'Yield' else '1000 tons'})"
    )
    return fig


def create_fertilizer_line_chart(df, state_name):
    # Filter data for the selected state
    state_data = df[df["State Name"] == state_name]
    
    # Create a line chart for Total State Consumption
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=state_data["Year"],
        y=state_data["Total State Consumption (tons)"],
        mode="lines+markers",
        name="Fertilizer Consumption"
    ))

    # Customize layout
    fig.update_layout(
        title=f"Fertilizer Consumption Over Years in {state_name}",
        xaxis_title="Year",
        yaxis_title="Consumption (tons)"
    )
    return fig
