import dash
from dash import html, dcc

dash.register_page(__name__)

layout = html.Div(className= "new-page", children=[
    html.H1(children='This is our Archive page'),

    html.Div(children='''
        This is our Archive page content.
    '''),

])