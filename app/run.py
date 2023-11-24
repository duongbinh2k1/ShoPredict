import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd

from process_data.mongo_db import MongoDBClient

app = dash.Dash(__name__)

# Create an instance of MongoDBClient
database_url = "mongodb://localhost:27017/"
database_name = "shopredict"
collection_name = "classified_products"
mongo_client = MongoDBClient(database_url, database_name)

data = pd.DataFrame(mongo_client.get_page(
    collection_name, limit=100)) 

app.layout = html.Div([
    dcc.Graph(id='my-graph'),
])


@app.callback(
    Output('my-graph', 'figure'),
    [Input('some-input', 'value')] 
)
def update_graph(some_input_value):
    updated_data = pd.DataFrame(mongo_client.get_page(
        collection_name, query={'some_field': some_input_value}, limit=100))
    figure = px.scatter(updated_data, x='some_column',
                        y='some_other_column', color='category', title='MongoDB Data')

    return figure


if __name__ == '__main__':
    app.run_server(debug=True)
