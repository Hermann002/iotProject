from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, jsonify, current_app, session
)
from werkzeug.exceptions import abort
from .db import insertDB, findToken, Stats, get_db
import datetime
from markupsafe import escape

from psycopg2.extras import DictCursor
import pdb
from dateutil import parser
import requests

bp = Blueprint('api', __name__)


@bp.route('/add_message/', methods=['GET', 'POST'])
def add_message():
    if request.method == 'POST':
        content = request.json

        #add field that content the date when data fetch
        content['created'] = datetime.datetime.now()
        print(content)

        # insert in the mongo database
        try:
            insertDB(content)
        except Exception as e:
            pass

        return jsonify({'response': 200})
    
    else:
        return 'POST request is required'