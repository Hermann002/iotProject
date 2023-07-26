# Import packages
import dash
from dash import html, dash_table, dcc
import plotly.express as px
from ..db import findData, findPermission
from flask import g
import pandas as pd
from ..auth import login_required
# from dash.exceptions import PreventUpdate

dash.register_page(__name__, path_template="/<token>")

# Incorporate data
@login_required
def layout(token=None):
    if g.user['token'] != token and g.user['is_admin'] == False:
        return "vous n'avez pas accès à cette page !"
    # find data in MongoDB
    df = pd.DataFrame(findData(token))

    permission = findPermission(token)
    try:
    # App layout
        lay = html.Div([
            html.Header(
                [
                    html.Span('Dashboard', className='title-header'),
                    html.Nav([
                        html.A("Acceuil", href="http://127.0.0.1:5000", className='nav-item'),
                        html.P(g.user['username'], className='username nav-item'),
                        html.A("Sortir", href=" http://127.0.0.1:5000/logout/", className='nav-item'),
                        html.A("Graph", href="#", className='nav-item'),
                        html.A("Stats", href=" http://127.0.0.1:5000/stats/", className='nav-item')], className="nav-bar")
                ],className="app-header"),


            html.Div([
                html.H2('My First App with Data, Graph, and Controls', className="text")
            ]),

            # html.Button('refresh', id='refresh'),

            html.Div(className="blocks",
                    children=[
                            html.Div(
                                        [
                                            dash_table.DataTable(data = df.to_dict('records'), page_size=13, style_table={'overflowX': 'auto'},  id='table')
                                        ], className='tab'
                                    ),

                            html.Div(
                                    className = "analytics",
                                    children = [
                                                    html.Div([
                                                        dcc.Graph(figure=px.line(df, x='created', y=['humidity', 'temperature']), className='my-first-graph-final',  id='graph')
                                                            ], className='grh'),
                                                ]
                                    ) if permission['temp_hum'] == True else None,


            # module voltage et current
                            html.Div(
                                    className = "analytics",
                                    children = [
                                                    html.Div([
                                                        dcc.Graph(figure=px.line(df, x='created', y=['voltage', 'intensity']), className='my-first-graph-final',  id='graph')
                                                            ], className='grh'),
                                                ]
                                    ) if permission['volt_int'] == True else None,

            # module smoke

                            html.Div(
                                    className = "analytics",
                                    children = [
                                                    html.Div([
                                                        dcc.Graph(figure=px.line(df, x='created', y='smoke'), className='my-first-graph-final',  id='graph')
                                                            ], className='grh'),
                                                ]
                                    ) if permission['smoke'] == True else None
                                    ]),
            # accès à la température et l'humidité
            

        ],className="new-page")

        return lay

    except:
        lay = html.Div([
        html.Header(
                [
                    html.Span('Dashboard', className='title-header'),
                    html.Nav([
                        html.A("Acceuil", href="http://127.0.0.1:5000", className='nav-item'),
                        html.P(g.user['username'], className='username nav-item'),
                        html.A("Sortir", href=" http://127.0.0.1:5000/logout/", className='nav-item'),
                        html.A("Graph", href="#", className='nav-item'),
                        html.A("Stats", href=" http://192.168.100.27:5000/stats/", className='nav-item')], className="nav-bar")
                ],className="app-header"),
        html.H2('Rien à Afficher pour l\'instant !', className="text")
                ])
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