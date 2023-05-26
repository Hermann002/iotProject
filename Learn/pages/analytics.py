# Import packages
import dash
from dash import Dash, html, dash_table, dcc, callback, Output, Input
import plotly.express as px
from models.database import findData
import pandas as pd
from dash.exceptions import PreventUpdate

dash.register_page(__name__)

# Incorporate data


# App layout
layout = html.Div([
    html.Div([
        html.H2('My First App with Data, Graph, and Controls', className="text")
    ]),

    html.Button('refresh', id='refresh'),

    html.Div([
        html.Div([
            dash_table.DataTable(data = [], page_size=10, style_table={'overflowX': 'auto'},  id='table')
        ], className='tab'),

        html.Div([
            dcc.Graph(figure={}, className='my-first-graph-final',  id='graph')
        ], className='grh'),
    ],className = "analytics"),

],className="new-page")

@callback(
    Output(component_id = 'table', component_property = 'data'),
    Input(component_id = 'refresh', component_property = 'n_clicks')
)

def update_output(n_clicks):
    if n_clicks is None:
        raise PreventUpdate
    else:
        df = pd.DataFrame(findData())
        data = df.to_dict('records')
    return data

@callback(
    Output(component_id = 'graph', component_property = 'figure'),
    Input(component_id = 'refresh', component_property = 'n_clicks')
)

def update_output(n_clicks):
    if n_clicks is None:
        raise PreventUpdate
    else:
        df = pd.DataFrame(findData())
        figure = px.line(df, x='created', y=['temperature','humidity'])
    return figure