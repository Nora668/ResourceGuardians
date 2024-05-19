import dash
import dash_bootstrap_components as dbc
from dash import dcc, html, Input, Output, State
import pandas as pd
import base64
import io

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = dbc.Container([
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

if __name__ == "__main__":
    app.run_server(debug=True)
