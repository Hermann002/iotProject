import dash
from dash import html, dcc, callback
from flask import Flask, redirect, url_for

server = Flask(__name__)
app = dash.Dash(__name__, server=server)

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])

@callback(dash.dependencies.Output('page-content', 'children'),
              [dash.dependencies.Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/':
        return html.Div([
            html.H3('Home Page'),
            dcc.Link('Go to Page 1', href='/page-1'),
            html.Br(),
            dcc.Link('Go to Page 2', href='/page-2'),
        ])
    elif pathname == '/page-1':
        return html.Div([
            html.H3('Page 1'),
            html.Br(),
            dcc.Link('Go back to Home', href='/'),
        ])
    elif pathname == '/page-2':
        return html.Div([
            html.H3('Page 2'),
            html.Br(),
            dcc.Link('Go back to Home', href='/'),
        ])
    else:
        # If the user tries to reach a different page, return a 404 message
        return '404'

@server.route('/redirect')
def redirect_to_home():
    return redirect(url_for('/'))

if __name__ == '__main__':
    app.run_server(host = '127.0.0.1', port=5000 ,debug=True)