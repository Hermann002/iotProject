import pytest
from flask import g, session
from API.db import get_db
from psycopg2.extras import DictCursor


def test_register(client, app):
    assert client.get('/auth/register').status_code == 200
    response = client.post(
        '/auth/register', data={'username': 'a', 'useremail': 'test', 'password': 'testa', 'option': ['temp_hum', 'volt_int']}
    )
    assert response.headers["Location"] == "/auth/login"

    with app.app_context():
        assert get_db().cursor(cursor_factory=DictCursor).execute(
            "SELECT * FROM user WHERE username = 'a'",
        ).fetchone() is not None


@pytest.mark.parametrize(('username', 'useremail', 'password', 'option', 'message'), (
    ('', '', '', [], b'Username is required.'),
    ('a', '', '', [], b'Useremail is required.'),
    ('a', 'a', '', [], b'password is required.'),
    ('test', 'test', 'test', [], b'already registered'),
))

def test_register_validate_input(client, username, useremail, password, option, message):
    response = client.post(
        '/auth/register',
        data={'username': username,'useremail': useremail, 'password': password, 'option': option}
    )

    assert message in response.data

def test_login(client, auth):
    assert client.get('/auth/login').status_code == 200
    response = auth.login()
    assert response.headers["Location"] == "/"

    with client:
        client.get('/')
        assert session['user_id'] == 1
        assert g.user['useremail'] == 'test'


@pytest.mark.parametrize(('useremail', 'password', 'message'), (
    ('a', 'test', b'Incorrect useremail.'),
    ('test', 'a', b'Incorrect password.'),
))
def test_login_validate_input(auth, useremail, password, message):
    response = auth.login(useremail, password)
    assert message in response.data

def test_logout(client, auth):
    auth.login()

    with client:
        auth.logout()
        assert 'user_id' not in session