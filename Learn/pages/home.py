import dash
from dash import html, dcc

dash.register_page(__name__, path='/')

layout = html.Div(className = "new-page",children=[
    html.H3(children='This is our Home page', className = 'title-home'),

    html.Div(children='''
        This is our Home page content.
    '''),

])