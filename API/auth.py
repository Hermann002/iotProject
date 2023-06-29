import functools
from psycopg2 import IntegrityError
from psycopg2.extras import DictCursor
from flask import(
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)

from werkzeug.security import check_password_hash, generate_password_hash
import uuid
from .db import get_db
from markupsafe import escape

import pdb

"""define classes"""

class User:

    def __init__(self, username, useremail, password):
        self.username = username
        self.useremail = useremail
        self.password = password
        self.token = str(uuid.uuid1())
        self.__is_admin = False

    def get_is_admin(self):
        return self.__is_admin
    
    def set_is_admin(self, is_admin):
        self.__is_admin = is_admin

class Allow_to:

    def __init__(self, temp_hum = False, volt_int = False, smoke = False):
        self.temp_hum = temp_hum
        self.volt_int = volt_int
        self.smoke = smoke
        
"""start creating app"""

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = escape(request.form['username'])
        useremail = escape(request.form['useremail'])
        password = escape(request.form['password'])
        modules = request.form.getlist('option')
        temp_hum = False
        volt_int = False
        smoke = False
        # token = str(uuid.uuid1())
        error = None

        if not username:
            error = 'Username is required.'
        elif not useremail:
            error = 'Useremail is required.'
        elif not password:
            error = 'Password is required.'
        
        if error is None:
            user = User(username, useremail, password)

             # verification des modules choisis
            if 'temp_hum' in modules:
                temp_hum = True
            if 'volt_int' in modules:
                volt_int = True
            if 'smoke' in modules:
                smoke = True
            allow_to = Allow_to(temp_hum, volt_int, smoke)

            # insertion des informations dans la base de donnée
            try:
                db = get_db()
                exc = db.cursor()

                exc.execute(
                    'INSERT INTO "users" (username, useremail, password, token) VALUES (%s, %s, %s, %s)',
                    (user.username, user.useremail, generate_password_hash(user.password), user.token,)
                    )

                exc.execute(
                    'INSERT INTO "allow_to" (temp_hum, volt_int, smoke, token) VALUES (%s, %s, %s, %s)',
                    (allow_to.temp_hum, allow_to.volt_int, allow_to.smoke, user.token,)
                    )
                
                db.commit()
                db.close()
            except IntegrityError :
                error  =  'already registered'
            except Exception as e:
                print(e)
                error = "Veuillez vérifier votre connexion et reéssayez !"
                return render_template('auth/register.html')
            else:
                flash(f'mettre ce token dans le microcontroleur {user.token}')
                return redirect(url_for("auth.login"))
            
        flash(error)
    return render_template('auth/register.html')

@bp.route('/login', methods = ('GET', 'POST'))
def login():
    if request.method == 'POST':
        useremail = escape(request.form['useremail'])
        password = escape(request.form['password'])
        
        error = None
        try:
            db = get_db()
            exc = db.cursor(cursor_factory=DictCursor)
            exc.execute('SELECT * FROM "users" WHERE useremail = %s', (useremail,))
            user = exc.fetchone()
        except Exception as e:
            print(e)
            flash('Veuillez vérifier votre connexion et reessayez !')
            return render_template('auth/login.html')
        
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

    if user_token is None:
        g.user = None
    else:
        try:
            db = get_db()
            exc = db.cursor(cursor_factory=DictCursor)
            exc.execute('SELECT u.*, temp_hum, volt_int, smoke FROM users u INNER JOIN allow_to l ON l.token = u.token WHERE u.token = %s', (user_token,))
            g.user = exc.fetchone()
        except Exception as e:
            print(e)
            message = flash('Veuillez vérifier votre connexion et reessayez !')
            return redirect(url_for('auth.login'), message)


@bp.route('/logout')
def logout():
    try:
        session.clear()
        return redirect(url_for('index'))
    except:
        flash('Veillez vérifier votre connexion et reéssayez !')
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