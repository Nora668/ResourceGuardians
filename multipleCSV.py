import dash
from dash import html, dcc, callback, Output, Input
import pandas as pd
import io
import base64

app = dash.Dash(__name__)
app.layout = html.Div([
    dcc.Upload(
        id='upload-data',
        children=html.Button('Upload CSV File'),
        multiple=True
    ),
    html.Div(id='output-data')
])

@app.callback(
    Output('output-data', 'children'),
    [Input('upload-data', 'contents')]
)
def update_data(contents):
    if contents is not None:
        data_output = []
        for content in contents:
            content_type, content_string = content.split(',')
            decoded_content = base64.b64decode(content_string)            
            df = pd.read_csv(io.StringIO(decoded_content.decode('utf-8')))
            
            # Extract file name
            file_name = content_type.split(';')[1].split('=')[1]
            
            # Update historical data
            key = update_historical_data(df, file_name, content_string)
            
            # Append hash and data summary to data_output
            data_output.append(html.Div([
                html.H5(f'Uploaded CSV File (Hash: {key})'),
                html.H5(f'File Name: {file_name}'),
                html.Pre(df.to_string()),
                html.Hr()
            ]))
       
        return data_output
    
# Utilize a dictionary to keep track of data
historical_data = {}

def update_historical_data(df, file_name, content_string):
    key = hash(content_string)
    if key not in historical_data:
        historical_data[key] = {'file_name': file_name, 'data': df}
    else:
        historical_data[key] = {'file_name': file_name, 'data': df}
    return key

# def update_graph_content():

if __name__ == '__main__':
    app.run_server(debug=True)
