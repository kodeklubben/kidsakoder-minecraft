# -*- coding: utf-8 -*-
"""
Routes and views for the flask application.
"""

from flask import render_template, request, redirect, url_for, flash
from flask_app import app
from models import Meeting
from database import db
from flask_security import login_required


@app.route('/index')
@app.route('/home')
@app.route('/hjem')
@app.route('/')
@login_required
def home():
    """ Renders the home page. """
    return render_template(
        'index.html',
        title='Hjem',
    )


@app.route('/contact')
@app.route('/kontakt')
@login_required
def contact():
    """ Renders the contact page. """
    return render_template(
        'contact.html',
        title='Kontakt oss',
    )


@app.route('/database')
@login_required
def database():
    """ Test page for database """
    all_meetings = Meeting.query.all()
    output = [dict(title=meeting.title, time=meeting.time, participants=meeting.participants)
              for meeting in all_meetings]
    return render_template(
        'database.html',
        meetings=output,
        title='Database test'
    )


@app.route('/newmeeting')
@app.route('/new_meeting')
@app.route('/nyttmote')
@app.route('/nytt_mote')
@login_required
def new_meeting():
    """ Renders the meeting creation page """
    return render_template(
        'new_meeting.html',
        title='New Meeting'
    )


@app.route('/addmeeting', methods=['POST'])
@app.route('/add_meeting', methods=['POST'])
@app.route('/leggtilmote', methods=['POST'])
@app.route('/legg_til_mote', methods=['POST'])
@login_required
def add_meeting():
    """ Add meeting POST form handler """
    meeting = Meeting(user_id='1', title=request.form['title'], time=request.form['time'],
                      participants=request.form['participants'], world_id=request.form['map_id'])
    db.session.add(meeting)
    db.session.commit()
    flash('Nytt mote lagt til!')
    return redirect(url_for('database'))


@app.route('/fra_kart')
@login_required
def from_map():
    """ Renders the map area selection page """
    return render_template(
        'map/minecraft_kartverket.html',
        title='Kart'
    )


@app.errorhandler(401)
def custom_401(error):
    return render_template(
        '401.html',
        title='401'
    ), 401


@app.errorhandler(404)
def page_not_found(error):
    return render_template(
        '404.html',
        title='404'
    ), 404
