# -*- coding: utf-8 -*-
"""
Routes and views for the flask application.
"""

from datetime import datetime
from flask import render_template, request, session, redirect, url_for, g, flash
from sqlalchemy import select

from flask.ext.app.database import engine
from flask.ext.app.schema import meetings
from flask_app import app
from functools import wraps


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' in session:
            return f(*args, **kwargs)
        session['redirect_page'] = request.url
        return redirect(url_for('login'))

    return decorated_function


@app.route('/')
@app.route('/hjem')
@app.route('/home')
@app.route('/indeks')
@app.route('/index')
@login_required
def home():
    """Renders the home page."""
    return render_template(
        'index.html',
        title='Hjem',
        year=datetime.now().year,
        app_name=app.config['APP_NAME']
    )


@app.route('/kontakt')
@app.route('/contact')
@login_required
def contact():
    """Renders the contact page."""
    return render_template(
        'contact.html',
        title='Kontakt',
        year=datetime.now().year,
        message='Your contact page.',
        app_name=app.config['APP_NAME']
    )


@app.route('/logg_inn', methods=['GET', 'POST'])
@app.route('/logginn', methods=['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'])
def login():
    """ Login page """
    if 'username' in session:
        # If user is already logged in, redirect to home
        return redirect(url_for('home'))

    if request.method == 'POST':
        # processLogin()
        session['username'] = request.form.get('username', None)
        return redirect(session.pop('redirect_page', url_for('home')))

    return render_template(
        'login.html',
        title='Logg inn',
        year=datetime.now().year,
        app_name=app.config['APP_NAME']
    )

@app.route('/logg_ut')
@app.route('/loggut')
@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))


@app.route('/database', methods=['GET', 'POST'])
@login_required
def database():
    """ Test page for database """
    selection = select([meetings])
    result = g.db.execute(selection)
    output = [dict(title=row[meetings.c.title], time=row[meetings.c.time], participants=row[meetings.c.participants])
              for row in result.fetchall()]
    return render_template('database.html',
                           meetings=output,
                           title='Database test',
                           year=datetime.now().year,
                           app_name=app.config['APP_NAME']
                           )

@app.route('/nytt_mote', methods=['GET', 'POST'])
@app.route('/nyttmote', methods=['GET', 'POST'])
@app.route('/newmeeting', methods=['GET', 'POST'])
@app.route('/new_meeting', methods=['GET', 'POST'])
@login_required
def new_meeting():
    """Renders the meeting creation page"""
    return render_template(
        'new_meeting.html',
        title = 'New Meeting',
        year = datetime.now().year,
        app_name = app.config['APP_NAME']
    )

@app.route('/legg_til_mote', methods=['POST'])
@app.route('/leggtilmote', methods=['POST'])
@app.route('/add_meeting', methods=['POST'])
@app.route('/addmeeting', methods=['POST'])
@login_required
def add_meeting():
    insert = meetings.insert().values(creator_id='1', title=request.form['title'], time=request.form['time'],
                                      participants=request.form['participants'], map_id=request.form['map_id'])
    g.db.execute(insert)
    flash('Nytt mote lagt til!')
    return redirect(url_for('database'))

@app.errorhandler(401)
def custom_401(error):
    return render_template(
    '401.html',
    title = '401',
    year = datetime.now().year,
    app_name = app.config['APP_NAME']
    ), 401    

@app.errorhandler(404)
def page_not_found(error):
    return render_template(
    '404.html',
    title = '404',
    year = datetime.now().year,
    app_name = app.config['APP_NAME']
    ), 404
    
