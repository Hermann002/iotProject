from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort
from psycopg2.extras import DictCursor
from .auth import login_required
from .db import get_db
import datetime

from .dbmongo import insertDB, findToken

bp = Blueprint('api', __name__)

@bp.route('/')
def index():
    # connect to sqlite database
    db = get_db()
    exc = db.cursor(cursor_factory=DictCursor)
    # check if user is login and if he is admin
    if g.user is None or g.user['is_admin'] == False:
        return render_template('blog/index.html')
    else:
        tokens = findToken()
         
        print(tokens)
        return render_template('blog/index.html', tokens=tokens, exc=exc)
        

@bp.route('/add_message/', methods=['GET', 'POST'])
def add_message():
    content = request.json

    #add field that content the date when data fetch
    content['created'] = datetime.datetime.now()
    print(content)

    # insert in the mongo database
    try:
        insertDB(content)
    except Exception as e:
        print("erreur d'envoie")

    return "ok"
    
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