# -*- coding: utf-8 -*-
"""
Routes and views for the flask application.
"""

from flask import render_template, request, redirect, url_for, flash
from flask.ext.login import current_user

from flask_app import app
from models import Meeting
from database import db
from flask_security import login_required
import urllib2
from flask_wtf import Form
from wtforms import TextField, validators


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
    meetings = Meeting.query.filter_by(user_id=current_user.id)
    output = [dict(title=meeting.title, time=meeting.time, participants=meeting.participants)
              for meeting in meetings]
    return render_template(
        'database.html',
        meetings=output,
        title='Database test'
    )


@app.route('/newmeeting', methods=['GET', 'POST'])
@app.route('/new_meeting', methods=['GET', 'POST'])
@app.route('/nyttmote', methods=['GET', 'POST'])
@app.route('/nytt_mote', methods=['GET', 'POST'])
@login_required
def new_meeting():
    """ Renders the meeting creation page """
    form = MeetingForm(request.form)
    if request.method == 'POST' and form.validate():
        """ Temporary redirect to contact """
        return redirect(url_for('contact'))

    return render_template(
        'new_meeting.html',
        title='New Meeting',
        form=form
    )


class MeetingForm(Form):
    name = TextField('Navn', [validators.Length(min=4, max=25)])
    startTime = TextField('Start Tidspunkt')
    endTime = TextField('Slutt Tidspunkt')
    participants = TextField('Medlemmer')


@app.route('/addmeeting', methods=['POST'])
@app.route('/add_meeting', methods=['POST'])
@app.route('/leggtilmote', methods=['POST'])
@app.route('/legg_til_mote', methods=['POST'])
@login_required
def add_meeting():
    """ Add meeting POST form handler """
    user_id = current_user.id

    meeting = Meeting(user_id=user_id, title=request.form['title'], time=request.form['time'],
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


@app.route('/mc_world_url', methods=['POST'])
@login_required
def mc_world_url():
    """ Pass MC world url to server """
    # Link example:
    # https://mc-sweco.fmecloud.com:443/fmedatadownload/results/FME_2E257068_1457457321707_15896.zip
    url = str(request.form['url'])
    print url
    split_url = url.strip().split('/')
    sane_url = '/'.join(split_url[0:5]) == 'https://mc-sweco.fmecloud.com:443/fmedatadownload/results'
    if not sane_url:
        return '<p>Ugyldig <a href="' + url + '">URL</a></p>'
    response = urllib2.urlopen(url)
    with open('mc_world.zip', 'wb') as world_file:
        # TODO save in a relevant place
        world_file.write(response.read())
        return '<p>Verden overført</p>'
    return '<p>Noe gikk galt!</p>'


@app.route('/test_cloud', methods=['GET', 'POST'])
def test_cloud():
    if request.method == 'POST':
        # TODO test code here
        server_list = [{'name': 'Test server', 'location': 1234},
                       {'name': 'Dead server', 'location': 5678}]
        return render_template(
            'test_cloud.html',
            title='Test cloud',
            server_list=server_list
        )

    return render_template(
        'test_cloud.html',
        title='Test cloud',
        server_list=[]
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
