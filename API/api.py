from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, jsonify, current_app, session
)
from werkzeug.exceptions import abort
from .db import insertDB, findToken, Stats, get_db
import datetime
from markupsafe import escape

from psycopg2.extras import DictCursor
import pdb

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
            print(results)
            current_app.config['fonction_execute'] = True
            print("La fonction s'exécute une seule fois.")
        except Exception as e:
            print(e)
        

@bp.route('/')
def index():
    # check if user is login and if he is admin
    if g.user is None:
        pass
    elif not g.user['is_admin']:
        pass
    else:
        try:
            tokens = findToken()
            return render_template('blog/index.html', tokens=tokens)
        except: 
            flash('Veillez vérifier votre connexion et rafraichissez la page !')
            return render_template('blog/index.html')
    return render_template('blog/index.html')

@bp.route('/stats/')
def stats():
    
    return render_template('blog/stats.html', results = results)



@bp.route('/refresh/', methods=['GET', 'POST'])
def refresh():
    if request.method == 'POST':
        current_app.config['fonction_execute'] = False
    return redirect(url_for('api.stats'))

@bp.route('/settings/', methods = ['GET', 'POST'])
def settings():
    if request.method == 'POST':
        token_int = g.user['token']
        token = str(token_int)
        date_main = request.form['date']
        if date_main >= datetime.datetime.now():
            error = 'veillez entrer une date inférieure à la date actuelle !'
            flash(error)
            return render_template('blog/settings.html')
        
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
        except Exception as e:
            temp_max = 0
            hum_max = 0
            volt_max = 0
            int_max = 0
            smoke_max = 0
            print(e)
        

        if g.user['temp_hum']:
            temp_max = escape(request.form['temp_max'])
        if g.user['volt_int']:
            volt_max = escape(request.form['volt_max'])
        if g.user['smoke']:
            smoke_max = escape(request.form['smoke_max'])
        error = None

        if user is None:
            try:
                db = get_db()
                exc = db.cursor()
                exc.execute(
                            'INSERT INTO max_values (temp_max, hum_max, volt_max, int_max, smoke_max, date_main, token) VALUES (%s, %s, %s, %s, %s, %s)',
                            (temp_max, hum_max, volt_max, int_max, smoke_max, date_main, token,)
                            )
                db.commit()
                db.close()
                flash('insert success !')
                return redirect(url_for('api.index'))
            except: 
                print(e)
                error = 'Something went wrong !'
        
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
                flash('update success !')
                return redirect(url_for('api.index'))
            except Exception as e:
                print(e)
                error = 'Something went wrong !'
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
    
# @bp.route('/create', methods=('GET', 'POST'))
# @login_required
# def create():
#     if request.method == 'POST':
#         title = request.form['title']
#         body = request.form['body']
#         error = None

#         if not title:
#             error = 'Title is required.'

#         if error is not None:
#             flash(error)
#         else:
#             db = get_db()
#             db.execute(
#                 'INSERT INTO post (title, body, author_id)'
#                 ' VALUES (?, ?, ?)',
#                 (title, body, g.user['id'])
#             )
#             db.commit()
#             return redirect(url_for('blog.index'))

#     return render_template('blog/create.html')
    
# def get_post(id, check_author=True):
#     post = get_db().execute(
#         'SELECT p.id, title, body, created, author_id, username'
#         ' FROM post as p JOIN user as u ON p.author_id = u.id'
#         ' WHERE p.id = ?',
#         (id,)
#     ).fetchone()

#     if post is None:
#         abort(404, f"Post id{id} doesn't exist")
    
#     if check_author and post['author_id'] != g.user['id']:
#         abort(403)
    
#     return post

# @bp.route('/<int:id>/update', methods=('GET','POST'))
# @login_required
# def update(id):
#     post = get_post(id)

#     if request.method == 'POST':
#         title = request.form['title']
#         body = request.form['body']
#         error = None

#         if not title:
#             error = 'Title is required.'

#         if error is not None:
#             flash(error)
#         else:
#             db = get_db()
#             db.execute(
#                 'UPDATE post SET title = ?, body = ?'
#                 ' WHERE id = ?',
#                 (title, body, id)
#             )
#             db.commit()
#             return redirect(url_for('blog.index'))
#     return render_template('blog/update.html', post=post)

# @bp.route('/<int:id>/delete', methods=('POST',))
# @login_required
# def delete(id):
#     get_post(id)
#     db = get_db()
#     db.execute('DELETE FROM post WHERE id = ?', (id,))
#     db.commit()
#     return redirect(url_for('blog.index'))