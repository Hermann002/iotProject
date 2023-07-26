import os

from flask import Flask, redirect, g
from dash import Dash
import dash

from dash import Dash, html, dcc

"""debut de l'Application dash"""

def create_app(test_config = None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)

    def create_dashapp(server):

        external_stylesheets = ['https://fonts.googleapis.com/css?family=Audiowide', 'https://fonts.googleapis.com/css2?family=Hind+Madurai']

        app = Dash(
            server=server,
            use_pages= True,
            external_stylesheets=external_stylesheets,
            url_base_pathname='/analytics/'
        )
        app.config['suppress_callback_exceptions'] = True
        app.title='Analytics'

        # Set the layout
        app.layout = html.Div([
            # html.Link(rel='icon', type='image/x-icon', href='https://cdn-icons-png.flaticon.com/512/6080/6080697.png'),
            dash.page_container
        ],className="main")

    """ Fin de l'application DASH"""

        # Register callbacks here if you want...

    create_dashapp(app)

    from . import db
    db.init_app(app)

    from . import auth
    app.register_blueprint(auth.bp)

    from . import logs
    app.register_blueprint(logs.bp)
    app.add_url_rule('/logs', endpoint='index')

    from . import api
    app.register_blueprint(api.bp)
    app.add_url_rule('/', endpoint='add_message')



    # app.config.from_mapping(
    #     SECRET_KEY = 'dev',
    #     DATABASE=os.path.join(app.instance_path, 'API.sqlite'),
    # )
    app.config.from_mapping(
        SECRET_KEY = 'dev',
        DATABASE = os.path.join(app.instance_path, 'API.bd'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed
        app.config.from_mapping(test_config)
    
    # ensure the instance folder exists 
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
        
    return app