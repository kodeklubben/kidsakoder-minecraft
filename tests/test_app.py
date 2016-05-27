# -*- coding: utf-8 -*-
"""
Unittests with test client
"""
import pytest
from flask_app import app, user_datastore
from flask_app.models import User, World, Meeting
from flask_app.database import db, create_db
from celery import current_app
from datetime import datetime, timedelta


EMAIL = ''
PASSWORD = ''


# A new test client is created for each test case. The database is reset
# each time, and one user is added. This user has no initial role.
@pytest.fixture
def client(request):
    """ Creates the test client """
    client = app.test_client()
    app.config.from_pyfile('config/testing.py')

    # Update celery app config for testing
    current_app.conf.update(app.config)

    # Add email and password as globals for easy ref.
    global EMAIL
    EMAIL = app.config['TEST_EMAIL']
    global PASSWORD
    PASSWORD = app.config['TEST_PASSWORD']

    # Initialize db and add a test user
    create_db()
    user_datastore.create_user(email=EMAIL, password=PASSWORD)
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


def add_testworld(client):
    """ Add a mock world for use in testing. Returns the world id """
    world = World()
    world.store()
    return world.id

def add_testmeeting(client, title, world_id, start_time, end_time):
    """ Add a meeting through the client """
    return client.post('/', data=dict(
        title=title,
        start_time=start_time,
        end_time=end_time,
        participant_count=10,
        world_id=world_id
    ), follow_redirects=True)


def test_front_page(client):
    """ Make sure we resieve an HTML page """
    rv = client.get('/', follow_redirects=True)
    assert rv.status == '200 OK'


def test_login_logout(client):
    """ Make sure login and logout works as intended """

    # Make sure login works with correct credentials
    rv = login(client, EMAIL, PASSWORD)
    print rv.data
    assert 'Velg verden' in rv.data

    # Make sure logout redirects to the login view
    rv = logout(client)
    assert app.config['SECURITY_MSG_LOGIN'][0].encode('utf-8') in rv.data

    # Make sure we are denied access using incorrect email
    rv = login(client, EMAIL + 'x', PASSWORD)
    assert app.config['SECURITY_MSG_USER_DOES_NOT_EXIST'][0] in rv.data

    # Make sure we are denied access using incorrect password
    rv = login(client, EMAIL, PASSWORD + 'x')
    assert app.config['SECURITY_MSG_INVALID_PASSWORD'][0] in rv.data


def test_access_before_after_login(client):
    """ Make sure we need to log inn to get access to the site """

    # Make sure we do not have access before login
    rv = client.get('/kontakt', follow_redirects=True)
    assert 'Kode-Kidza' not in rv.data
    assert app.config['SECURITY_MSG_LOGIN'][0].encode('utf-8') in rv.data

    # Make sure we do have access after login
    login(client, EMAIL, PASSWORD)
    rv = client.get('/kontakt', follow_redirects=True)
    assert 'Kode-Kidza' in rv.data


def test_admin_access(client):
    """ Make sure an admin has access to the admin functionality, while others do not """

    # Make sure we do not have access to admin while not admin
    login(client, EMAIL, PASSWORD)
    rv = client.get('/admin/user', follow_redirects=True)
    assert rv.status == '403 FORBIDDEN'
    rv = client.get('/admin/meeting', follow_redirects=True)
    assert rv.status == '403 FORBIDDEN'
    rv = client.get('/admin/world', follow_redirects=True)
    assert rv.status == '403 FORBIDDEN'

    # Login as admin
    logout(client)
    user_datastore.add_role_to_user(EMAIL, 'admin')
    login(client, EMAIL, PASSWORD)

    # Make sure we get access as admin
    rv = client.get('/admin/user', follow_redirects=True)
    assert rv.status == '200 OK'
    rv = client.get('/admin/meeting', follow_redirects=True)
    assert rv.status == '200 OK'
    rv = client.get('/admin/world', follow_redirects=True)
    assert rv.status == '200 OK'


def test_fme_url(client):
    """ Test that it does not accept invalid url """
    import json
    login(client, EMAIL, PASSWORD)
    url = 'http://www.skummel.no/farlig.exe'
    rv = client.post('/mc_world_url', data=dict(
        url=url,
        description=''
    ))
    result_json = json.loads(rv.data)
    assert result_json['message'] == u'Ugyldig <a href="' + url + u'">URL</a>'


def test_add_meeting(client):
    """ Make sure we are able to add meetings """

    login(client, EMAIL, PASSWORD)

    # Add a testworld to the db
    world_id = add_testworld(client)

    # Meeting starts one hour from now, and ends one hour later
    start_time = '{:%d.%m.%Y %H:%M}'.format(datetime.now() + timedelta(hours=1))
    end_time = '{:%d.%m.%Y %H:%M}'.format(datetime.now() + timedelta(hours=2))

    # Make sure we are able to add a meeting
    title = 'Testmeeting-1'
    rv = add_testmeeting(client, title, world_id, start_time, end_time)
    assert 'Nytt møte lagt til' in rv.data
    assert 'Testmeeting-1' in rv.data

    # Make sure we find the meeting in the database
    assert 'Testmeeting-1' in Meeting.get_meeting_by_id(1).title

    # Make sure we can not add meeting with non-existing world
    title = 'Testmeeting-2'
    world_id_fail = 10000
    rv = add_testmeeting(client, title, world_id_fail, start_time, end_time)
    assert 'Nytt møte lagt til' not in rv.data
    assert 'Den valgte Minecraft verdenen eksisterer ikke' in rv.data
