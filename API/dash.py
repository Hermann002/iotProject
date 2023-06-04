# Create a function which creates your dashapp
from dash import Dash, html, dash_table, dcc, callback, Output, Input
from flask import g
import plotly.express as px
# from .db import findData
import pandas as pd
from dash.exceptions import PreventUpdate


app.config['suppress_callback_exceptions'] = True
app.title='Dash App'

# Incorporate data
token = g.user
df = pd.DataFrame(1)

# App layout
app.layout = html.Div([
    html.Div([
        html.H2('My First App with Data, Graph, and Controls', className="text")
    ]),

    html.Header(
    [
        html.Nav([
            html.Div(
                className = "nav-items",
                children = [
                    dcc.Link("Home", href="api/home.html", className='nav-item')],
            )
        ],className = "nav-bar"),
    
        html.Span('Dashboard', className='title-header')
    ],className="app-header"),

    html.Button('refresh', id='refresh'),

    html.Div([
        html.Div([
            dash_table.DataTable(data = df.to_dict('records'), page_size=15, style_table={'overflowX': 'auto'},  id='table')
        ], className='tab'),

        html.Div([
            dcc.Graph(figure=px.line(df, x='created', y=['temperature','humidity']), className='my-first-graph-final',  id='graph')
        ], className='grh'),
    ],className = "analytics"),

],className="new-page")

# create callbacks to refresh data in table and graph

@callback(
    Output(component_id = 'table', component_property = 'data'),
    Input(component_id = 'refresh', component_property = 'n_clicks')
)

def update_output(n_clicks):
    if n_clicks is None:
        raise PreventUpdate
    else:
        df = pd.DataFrame(1)
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
        df = pd.DataFrame(1)
        figure = px.line(df, x='created', y=['temperature','humidity'])
    return figure

return app