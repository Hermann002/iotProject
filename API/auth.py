import functools
from psycopg2 import IntegrityError
from psycopg2.extras import DictCursor
from flask import(
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

from werkzeug.security import check_password_hash, generate_password_hash
import uuid
from .db import get_db
from .model import User

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = request.form['username']
        useremail = request.form['useremail']
        password = request.form['password']
        # token = str(uuid.uuid1())
        db = get_db()
        error = None

        if not username:
            error = 'Username is required.'
        elif not useremail:
            error = 'Useremail is required.'
        elif not password:
            error = 'Password is required.'
        
        if error is None:
            user = User(username, useremail, password)
            try:
                user.insertUser()
            except IntegrityError :
                error  = f'User{username} is already registered'
            else:
                flash(f'mettre ce token dans le microcontroleur {user.token}')
                return redirect(url_for("auth.login"))
            
        flash(error)
    return render_template('auth/register.html')

@bp.route('/login', methods = ('GET', 'POST'))
def login():
    if request.method == 'POST':
        useremail = request.form['useremail']
        password = request.form['password']
        db = get_db()
        error = None
        exc = db.cursor(cursor_factory=DictCursor)
        exc.execute('SELECT * FROM "user" WHERE useremail = %s', (useremail,))
        user = exc.fetchone()
        if user is None:
            error = 'Incorrect useremail'
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect password'
        # set cookies
        if error is None:
            session.clear()
            session['user_token'] = user['token']
            return redirect(url_for('index'))
        flash(error)
    return render_template('auth/login.html')

@bp.before_app_request
def load_logged_in_user():
    user_token = session.get('user_token')
    db = get_db()
    exc = db.cursor(cursor_factory=DictCursor)

    if user_token is None:
        g.user = None
    else:
        exc.execute('SELECT * FROM "user" WHERE token = %s', (user_token,))
        g.user = exc.fetchone()

@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view

# vue du coté administrateur pour plus tard 

# @bp.route('/db_access/')
# @login_required
# def access():
#     if g.user['useremail'] == 'hermannnzeudeu@gmail.com':
#         try:
#             db = get_db()
#             count = db.execute('SELECT * FROM user').fetchall()
#             result = []
#             for coun in count:
#                 result.append(dict(coun))
#         except Exception as e:
#             print(e)
#         return result
#     else:
#         return "vous n'avez pas les accès à cette page :("