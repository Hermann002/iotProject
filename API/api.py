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

@bp.before_app_request
def fonction_a_executer():
    user_token = session.get('user_token')
    global results
    global maximum
    if not current_app.config.get('fonction_execute') and user_token:
        try:
            db = get_db()
            exc = db.cursor(cursor_factory=DictCursor)
            exc.execute(
                'SELECT * FROM max_values WHERE token = %s', (user_token,)
                        )
            maximum = exc.fetchone()
            results = Stats(user_token, maximum['date_main'])
        except Exception as e:
            print(e)
            results = {}
        current_app.config['fonction_execute'] = True
        print(current_app.config['fonction_execute'])
        print("La fonction s'exécute une seule fois.")

    elif not user_token: 
        results = {}
        current_app.config['fonction_execute'] = False
        print(current_app.config['fonction_execute'])

        

@bp.route('/')
def index():
    # check if user is login and if he is admin
    # pdb.set_trace()
    if g.user and g.user['is_admin'] == False:
        try:
            danger = {}
            imminent = {}
            if g.user['temp_hum']:
                permit =  maximum['temp_max'] - maximum['temp_max']*2/100
                if maximum['temp_max'] <= results['recent']['temperature'] or maximum['temp_max'] <= results['medium']['temperature']:
                    danger['temp'] = True
                    imminent['temp'] = True
                    requests.get('https://blynk.cloud/external/api/update?token=ffujYGgbf805tgsf&v1=100')
                    requests.get('https://blynk.cloud/external/api/update?token=ffujYGgbf805tgsf&v1=100')
                elif permit >= results['recent']['temperature'] or permit >= results['medium']['temperature']:
                    danger['temp'] = False
                    imminent['temp'] = True
                else:
                    danger['temp'] = False
                    imminent['temp'] = False
            if g.user['volt_int']:
                permit =  maximum['volt_max'] - maximum['volt_max']*2/100
                if maximum['volt_max'] <= results['recent']['voltage'] or maximum['volt_max'] <= results['medium']['voltage']:
                    danger['volt'] = True
                    imminent['volt'] = True
                    requests.get('https://blynk.cloud/external/api/update?token=ffujYGgbf805tgsf&v1=100')
                    requests.get('https://blynk.cloud/external/api/update?token=ffujYGgbf805tgsf&v1=100')
                elif permit >= results['recent']['voltage'] or permit >= results['medium']['voltage'] :
                    danger['volt'] = False
                    imminent['volt'] = True
                else:
                    danger['volt'] = False
                    imminent['volt'] = False
                permit =  maximum['int_max'] - maximum['int_max']*2/100
                if maximum['int_max'] <= results['recent']['intensity'] or maximum['int_max'] <= results['medium']['intensity']:
                    danger['int'] = True
                    imminent['int'] = True
                    requests.get('https://blynk.cloud/external/api/update?token=ffujYGgbf805tgsf&v1=100')
                    requests.get('https://blynk.cloud/external/api/update?token=ffujYGgbf805tgsf&v1=100')
                elif permit >= results['recent']['intensity'] or permit >= results['medium']['intensity'] :
                    danger['int'] = False
                    imminent['int'] = True
                else:
                    danger['int'] = False
                    imminent['int'] = False
            if g.user['smoke']:
                permit =  maximum['smoke_max'] - maximum['smoke_max']*2/100
                if maximum['smoke_max'] <= results['recent']['humidity'] or maximum['smoke_max'] <= results['medium']['humidity']:
                    danger['smoke'] = True
                    imminent['smoke'] = True
                elif permit >= results['recent']['humidity'] or permit >= results['medium']['humidity'] :
                    danger['smoke'] = False
                    imminent['smoke'] = True
                else:
                    danger['smoke'] = False
                    imminent['smoke'] = False
            return render_template('blog/index.html', danger = danger, imminent = imminent, results = results)
        except Exception as e:
            print('erreur ici')
            print(e)
    elif g.user and g.user['is_admin'] == True:
        try:
            tokens = findToken()
            return render_template('blog/index.html', tokens=tokens)
        except: 
            flash('Veillez vérifier votre connexion et rafraichissez la page !')
            return render_template('blog/index.html')
    else:
        pass
    return render_template('blog/index.html')

@bp.route('/stats/')
def stats():

    if results != {}:
        return render_template('blog/stats.html', results = results)
    return render_template('blog/stats.html')



@bp.route('/refresh/', methods=['GET', 'POST'])
def refresh():
    if request.method == 'POST':
        current_app.config['fonction_execute'] = False
    return redirect(url_for('api.stats'))

@bp.route('/settings/', methods = ['GET', 'POST'])
def settings():
    if request.method == 'POST':
        token = g.user['token']
        date = request.form['date']

        date_main = parser.isoparse(date)
        print(date_main)     
        try:
            db = get_db()
            exc = db.cursor(cursor_factory=DictCursor)
            exc.execute(
                'SELECT * FROM max_values WHERE token = %s', (token,)
            )
            user = exc.fetchone()

            temp_max = user['temp_max']
            hum_max = user['hum_max']
            volt_max = user['volt_max']
            int_max = user['int_max']
            smoke_max = user['smoke_max']
        except:
            temp_max = 0
            hum_max = 0
            volt_max = 0
            int_max = 0
            smoke_max = 0
        

        if g.user['temp_hum']:
            temp_max = escape(request.form['temp_max'])
        if g.user['volt_int']:
            volt_max = escape(request.form['volt_max'])
            int_max = escape(request.form['int_max'])
        if g.user['smoke']:
            smoke_max = escape(request.form['smoke_max'])
        error = None

        if user is None:
            try:
                db = get_db()
                exc = db.cursor()
                exc.execute(
                            'INSERT INTO max_values (temp_max, hum_max, volt_max, int_max, smoke_max, date_main, token) VALUES (%s, %s, %s, %s, %s, %s, %s)',
                            (temp_max, hum_max, volt_max, int_max, smoke_max, date_main, token,)
                            )
                db.commit()
                db.close()
                flash('inséré avec succès !')
                return redirect(url_for('api.index'))
            except Exception as e: 
                print(e)
                error = 'Quelque chose s\'est mal passé ici!'
        
        else:
            try:
                db = get_db()
                exc = db.cursor()
                exc.execute(
                            "UPDATE max_values u SET temp_max = %s, hum_max = %s, volt_max = %s, int_max = %s, smoke_max = %s, date_main = %s WHERE u.token = %s",
                            (temp_max, hum_max, volt_max, int_max, smoke_max, date_main, token,)
                            )
                db.commit()
                db.close()
                flash('modifié avec succès !')
                return redirect(url_for('api.index'))
            except Exception as e:
                print(e)
                error = 'Quelque chose s\'est mal passé !'
        flash(error)
    return render_template('blog/settings.html')       

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