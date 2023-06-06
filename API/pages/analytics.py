# Import packages
import dash
from dash import html, dash_table, dcc
import plotly.express as px
from ..dbmongo import findData, findToken
import pandas as pd
from ..auth import login_required
# from dash.exceptions import PreventUpdate

dash.register_page(__name__, path_template="/<token>")

# Incorporate data
@login_required
def layout(token=None):
    # find data in MongoDB
    df = pd.DataFrame(findData(token))

    # App layout
    lay = html.Div([
        html.Div([
            html.H2('My First App with Data, Graph, and Controls', className="text")
        ]),

        # html.Button('refresh', id='refresh'),

        html.Div([
            html.Div([
                dash_table.DataTable(data = df.to_dict('records'), page_size=13, style_table={'overflowX': 'auto'},  id='table')
            ], className='tab'),

            html.Div([
                dcc.Graph(figure=px.line(df, x='created', y=['temperature','humidity']), className='my-first-graph-final',  id='graph')
            ], className='grh'),
        ],className = "analytics"),

    ],className="new-page")
    
    return lay

# @callback(
#     Output(component_id = 'table', component_property = 'data'),
#     Input(component_id = 'refresh', component_property = 'n_clicks')
# )

# def update_output(n_clicks):
#     if n_clicks is None:
#         raise PreventUpdate
#     else:
#         df = pd.DataFrame(findData(token))
#         data = df.to_dict('records')
#     return data

# @callback(
#     Output(component_id = 'graph', component_property = 'figure'),
#     Input(component_id = 'refresh', component_property = 'n_clicks')
# )

# def update_output(n_clicks):
#     if n_clicks is None:
#         raise PreventUpdate
#     else:
#         df = pd.DataFrame(findData(token))
#         figure = px.line(df, x='created', y=['temperature','humidity'])
#     return figure