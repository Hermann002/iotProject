import pytest
from API.db import get_db


def test_index(client, auth):
    response = client.get('/')
    assert b"Login" in response.data
    assert b"Register" in response.data

    auth.login()
    response = client.get('/')
    assert b'Log Out' in response.data
    assert b'Graph' in response.data

def test_add_message(client, api):
    api.add_message()
    assert client.post('/add_message/', data={'temperature': 1, 'humidity': 3, 'token': 'a'})