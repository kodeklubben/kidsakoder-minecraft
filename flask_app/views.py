# -*- coding: utf-8 -*-
"""
Routes and views for the flask application.
"""

from datetime import datetime
from functools import wraps

from flask import render_template, request, session, redirect, url_for, flash

from flask_app.models import Meeting
from flask.ext.app.database import db_session

from flask_app import app


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
    all_meetings = Meeting.query.all()
    output = [dict(title=meeting.title, time=meeting.time, participants=meeting.participants)
              for meeting in all_meetings]
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
        title='New Meeting',
        year=datetime.now().year,
        app_name=app.config['APP_NAME']
    )

@app.route('/legg_til_mote', methods=['POST'])
@app.route('/leggtilmote', methods=['POST'])
@app.route('/add_meeting', methods=['POST'])
@app.route('/addmeeting', methods=['POST'])
@login_required
def add_meeting():
    meeting = Meeting(creator_id='1', title=request.form['title'], time=request.form['time'],
                      participants=request.form['participants'], world_id=request.form['map_id'])
    db_session.add(meeting)
    db_session.commit()
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
