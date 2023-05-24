# Import packages
import dash
from dash import Dash, html, dash_table, dcc, callback, Output, Input
import plotly.express as px
from models.database import connect
import pandas as pd

dash.register_page(__name__)

# Incorporate data
df = pd.DataFrame(connect())

# App layout
layout = html.Div([
    html.Div([
        html.H2('My First App with Data, Graph, and Controls', className="text")
    ]),

    html.Div([
        html.Div([
            dash_table.DataTable(data=df.to_dict('records'), page_size=10, style_table={'overflowX': 'auto'})
        ], className='table'),

        html.Div([
            dcc.Graph(figure=px.line(df, x='created', y=['temperature','humidity']), id='my-first-graph-final')
        ], className='graph'),
    ],className = "analytics"),

],className="new-page")