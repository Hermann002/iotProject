from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for, jsonify, current_app, session
)
from werkzeug.exceptions import abort
from .db import insertDB, findToken, Stats
import datetime

bp = Blueprint('api', __name__)

@bp.before_app_request
def fonction_a_executer():
    user_token = session.get('user_token')
    global results
    if not current_app.config.get('fonction_executée') and user_token:
        results = Stats(user_token)
        print("La fonction s'exécute une seule fois.")
        current_app.config['fonction_executée'] = True

@bp.route('/')
def index():
    # check if user is login and if he is admin
    if g.user is None:
        print('guser')
    elif not g.user['is_admin']:
        """moyennes"""
    else:
        try:
            tokens = findToken()
            return render_template('blog/index.html', tokens=tokens)
        except: 
            flash('Veillez vérifier votre connexion et rafraichissez la page !')
    return render_template('blog/index.html')

@bp.route('/stats/')
def stats():
    medium = {}
    median = {}
    mode = {}
    ecart = {}
    variance = {}

    if g.user['temp_hum']:

        moy_temp = results['medium']['temperature']
        moy_hum = results['medium']['humidity']
        medium['temp'] = moy_temp
        medium['hum'] = moy_hum

        med_temp = results['median']['temperature']
        med_hum = results['median']['humidity']
        median['temp'] = med_temp
        median['hum'] = med_hum

    if g.user['volt_int']:
        moy_volt = results['medium']['temperature']
        medium['volt'] = moy_volt

        med_temp = results['median']['temperature']
        median['temp'] = med_temp
    if g.user['smoke']:
        moy_smoke = results['medium']['humidity']
        medium['smoke'] = moy_smoke

        med_smoke = results['median']['humidity']
        median['smoke'] = med_smoke
    return render_template('blog/stats.html', medium=medium, median=median)

@bp.route('/refresh/', methods=['GET', 'POST'])
def refresh():
    if request.method == 'POST':
        current_app.config['fonction_executée'] = False
    return redirect(url_for('api.stats'))

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