import pytest

from flask_app import app, user_datastore
from flask_app.models import User
from flask_app.database import db, init_db


@pytest.fixture
def client(request):
    """ Creates the test client """
    client = app.test_client()
    app.config.from_pyfile('config/testing.py')

    """ Initialize db and add a test user """
    init_db()
    user_datastore.create_user(email=app.config['TEST_EMAIL'], password=app.config['TEST_PASSWORD'])
    user_datastore.add_role_to_user(app.config['TEST_EMAIL'], 'admin')
    db.session.commit()

    return client

def login(client, email, password):
    """ Login to the test client """
    return client.post('/login', data=dict(
        email=email,
        password=password
    ), follow_redirects=True)


def logout(client):
    """ Logout of the test client """
    return client.get('/logout', follow_redirects=True)



def test_front_page(client):
    """ Make sure we resieve an HTML page """
    rv = client.get('/', follow_redirects=True)
    assert rv.status == '200 OK'


def test_login_logout(client):
    """Make sure login works and logout works """
    rv = login(client, app.config['TEST_EMAIL'], app.config['TEST_PASSWORD'])
    assert 'Velg verden' in rv.data

    rv = logout(client)
    assert app.config['SECURITY_MSG_LOGIN'][0].encode('utf-8') in rv.data

    """ Make sure we are denied access using incorrect credentials """
    rv = login(client, app.config['TEST_EMAIL'] + 'x', app.config['TEST_PASSWORD'])
    assert app.config['SECURITY_MSG_USER_DOES_NOT_EXIST'][0] in rv.data

    rv = login(client, app.config['TEST_EMAIL'], app.config['TEST_PASSWORD'] + 'x')
    assert app.config['SECURITY_MSG_INVALID_PASSWORD'][0] in rv.data


def test_access_before_after_login(client):
    """ Make sure we do not have access before login """
    rv = client.get('/kontakt', follow_redirects=True)
    assert 'Kode-Kidza' not in rv.data
    assert app.config['SECURITY_MSG_LOGIN'][0].encode('utf-8') in rv.data

    """ Make sure we do have access after login """
    login(client, app.config['TEST_EMAIL'], app.config['TEST_PASSWORD'])
    rv = client.get('/kontakt', follow_redirects=True)
    assert 'Kode-Kidza' in rv.data
