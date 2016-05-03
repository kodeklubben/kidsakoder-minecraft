import pytest
import os

from flask_app import app

@pytest.fixture
def client(request):
    app.config['TESTING'] = True
    client = app.test_client()

    return client

def login(client, username, password):
    return client.post('/login', data=dict(
        username=username,
        password=password
    ), follow_redirects=True)


def logout(client):
    return client.get('/logout', follow_redirects=True)


def test_front_page(client):
    """Make sure we resieve an HTML page"""
    rv = client.get('/', follow_redirects=True)
    assert rv.status == '200 OK'
