import pytest
import os

from flask_app import app


@pytest.fixture
def client(request):
    client = app.test_client()
    app.config['WTF_CSRF_ENABLED'] = False
    return client

def login(client, email, password):
    return client.post('/login', data=dict(
        email=email,
        password=password
    ), follow_redirects=True)


def logout(client):
    return client.get('/logout', follow_redirects=True)



def test_front_page(client):
    """Make sure we resieve an HTML page"""
    rv = client.get('/', follow_redirects=True)
    assert rv.status == '200 OK'


def test_login_logout(client):
    """Make sure login and logout works"""
    rv = login(client, 'admin@mail.com', 'adminpass123')
    assert 'Velg verden' in rv.data
    rv = logout(client)
    assert 'Venligst logg inn' in rv.data
    rv = login(client, 'admin@mail.com' + 'x', 'adminpass123')
    assert 'Feil brukernavn og / eller passord' in rv.data
    rv = login(client, 'admin@mail.com', 'adminpass123' + 'x')
    assert 'Feil brukernavn og / eller passord' in rv.data
