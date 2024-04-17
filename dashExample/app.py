# Import packages
from dash import Dash, html, dcc, callback, Output, Input
import pandas as pd
import plotly.express as px
import dash_bootstrap_components as dbc

# Incorporate data from a local CSV file
df = pd.read_csv('data.csv')

# Initialize the app - incorporate a Dash Bootstrap theme
external_stylesheets = [dbc.themes.CERULEAN]
app = Dash(__name__, external_stylesheets=external_stylesheets)

# App layout
app.layout = dbc.Container([
    dbc.Row([
        html.Div('Water and Energy Usage by Location and Month', className="text-primary text-center fs-3")
    ]),

    dbc.Row([
        dbc.Col([
            dbc.RadioItems(
                options=[{"label": location, "value": location} for location in df['location'].unique()],
                value=df['location'].unique()[0],  # Default to the first location
                id='location-selector',
                inline=True,
                className="mt-3"
            )
        ], width={"size": 6, "offset": 3})  # Center the radio buttons
    ]),

    dbc.Row([
        dbc.Col([
            dcc.Graph(id='water-graph')
        ], width=12),  # Use full width for the water usage graph
    ]),

    dbc.Row([
        dbc.Col([
            dcc.Graph(id='energy-graph')
        ], width=12),  # Use full width for the energy usage graph
    ]),

    # New Row for additional radio buttons to select data type for comparison graph
    dbc.Row([
        dbc.Col([
            dbc.RadioItems(
                options=[
                    {"label": "Water", "value": "water"},
                    {"label": "Energy", "value": "energy"}
                ],
                value='water',  # Default to 'water'
                id='data-type-selector',
                inline=True,
                className="mt-3"
            )
        ], width={"size": 6, "offset": 3})  # Center the radio buttons
    ]),

    # New Row for the comparison graph
    dbc.Row([
        dbc.Col([
            dcc.Graph(id='comparison-graph')
        ], width=12),  # Use full width for the comparison graph
    ]),
], fluid=True)

# Add controls to build the interaction
@callback(
    [Output('water-graph', 'figure'),
     Output('energy-graph', 'figure'),
     Output('comparison-graph', 'figure')],
    [Input('location-selector', 'value'),
     Input('data-type-selector', 'value')]
)
def update_graphs(selected_location, data_type):
    filtered_df = df[df['location'] == selected_location]
    # Water usage bar graph
    water_fig = px.bar(filtered_df, x='month', y='water', title=f"Water Usage in {selected_location}",
                       category_orders={"month": ["January", "February", "March", "April", "May", "June",
                                                  "July", "August", "September", "October", "November", "December"]})
    water_fig.update_layout(xaxis_title="Month", yaxis_title="Water (Units)", barmode='group')
    
    # Energy usage line graph
    energy_fig = px.line(filtered_df, x='month', y='energy', title=f"Energy Usage in {selected_location}",
                         category_orders={"month": ["January", "February", "March", "April", "May", "June",
                                                    "July", "August", "September", "October", "November", "December"]},
                         markers=True)
    energy_fig.update_layout(xaxis_title="Month", yaxis_title="Energy (Units)")

    # Multiple bar graph for all locations
    comparison_fig = px.bar(df, x='month', y=data_type, color='location', barmode='group',
                            title=f'{data_type.capitalize()} Usage Comparison Across Locations')
    comparison_fig.update_layout(xaxis_title="Month", yaxis_title=f"{data_type.capitalize()} (Units)")

    return water_fig, energy_fig, comparison_fig

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
