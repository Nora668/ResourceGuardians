from dash import Dash, html, dcc, callback, Output, Input
import pandas as pd
import plotly.express as px
import dash_bootstrap_components as dbc
import base64
import io
from dash.dependencies import State


# Incorporate data from a local CSV file
df = pd.read_csv("C:\\Users\\aikoz\\Documents\\resourceguardian\\ResourceGuardians\\inputPage\\data.csv")

# Initialize the app - incorporate a Dash Bootstrap theme
external_stylesheets = [dbc.themes.CERULEAN]
app = Dash(__name__, external_stylesheets=external_stylesheets)

# Define layout for the CSV sorter page
sorter_layout = dbc.Container([
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
], fluid=True)

# Define layout for the graph converter page
converter_layout = dbc.Container([
    dbc.Row([
        dbc.Col(html.H1("CSV Sorter"), className="text-center my-4")
    ]),
    dbc.Row([
        dbc.Col(dcc.Upload(
            id='upload-csv',
            children=html.Div([
                'Drag and Drop or ',
                html.A('Select a CSV File')
            ]),
            style={
                'width': '100%',
                'height': '60px',
                'lineHeight': '60px',
                'borderWidth': '1px',
                'borderStyle': 'dashed',
                'borderRadius': '5px',
                'textAlign': 'center',
                'margin': '10px'
            },
            multiple=False
        ), width=6)
    ]),
    dbc.Row([
        dbc.Col(html.Div(id='output-text', className="mt-4"), width=12)
    ])
])

def parse_contents(contents, filename):
    content_type, content_string = contents.split(',')
    decoded = base64.b64decode(content_string)
    try:
        if 'csv' in filename:
            df = pd.read_csv(io.StringIO(decoded.decode('utf-8')))
            return df
    except Exception as e:
        return html.Div([
            'There was an error processing this file.'
        ])

@app.callback(
    Output('output-text', 'children'),
    Input('upload-csv', 'contents'),
    State('upload-csv', 'filename')
)
def update_output(contents, filename):
    if contents is not None:
        df = parse_contents(contents, filename)
        if isinstance(df, pd.DataFrame):
            df['month'] = pd.to_datetime(df['month'], format='%B')
            sorted_by_location = df.sort_values(by=['location']).reset_index(drop=True)
            sorted_by_month = df.sort_values(by=['month']).reset_index(drop=True)
            sorted_by_water = df.sort_values(by=['water']).reset_index(drop=True)
            sorted_by_energy = df.sort_values(by=['energy']).reset_index(drop=True)

            return html.Div([
                html.H5("Sorted by Location:"),
                html.Pre(sorted_by_location.to_string(index=False)),
                html.H5("Sorted by Month:"),
                html.Pre(sorted_by_month.to_string(index=False)),
                html.H5("Sorted by Water:"),
                html.Pre(sorted_by_water.to_string(index=False)),
                html.H5("Sorted by Energy:"),
                html.Pre(sorted_by_energy.to_string(index=False)),
            ])
        else:
            return df
    return "No file uploaded yet."

# Define routes for different pages
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])

@app.callback(
    Output('page-content', 'children'),
    [Input('url', 'pathname')]
)
def display_page(pathname):
    if pathname == '/sorter':
        return sorter_layout
    elif pathname == '/converter':
        return converter_layout
    else:
        return html.Div([
            html.H1("Welcome to the Dashboard Home"),
            html.P("Please select an option:"),
            html.Ul([
                html.Li(html.A("Go to CSV Sorter", href="/sorter")),
                html.Li(html.A("Go to Graph Converter", href="/converter")),
            ])
        ])

# Add controls to build the interaction
@app.callback(
    [Output('water-graph', 'figure'),
     Output('energy-graph', 'figure')],
    [Input('location-selector', 'value')]
)
def update_graphs(selected_location):
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

    return water_fig, energy_fig

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
