# -*- coding: utf-8 -*-
"""
Routes and views for the flask application.
"""

from flask import render_template, request, redirect, url_for, flash, send_from_directory
from flask_app import app
from models import Meeting, World
from flask_security import login_required, current_user, roles_required
import forms
import files


@app.route('/index')
@app.route('/home')
@app.route('/hjem')
@app.route('/')
@login_required
def home():
    """ Renders the home page. """
    meeting_list = Meeting.get_user_meetings_as_dict(current_user.id)
    return render_template(
        'index.html',
        title='Hjem',
        meetings=meeting_list
    )


@app.route('/contact')
@app.route('/kontakt')
@login_required
def contact():
    """ Renders the contact page. """
    return render_template(
        'contact.html',
        title='Kontakt oss'
    )


@app.route('/database')
@login_required
@roles_required('admin')
def database():
    """ Test page for database """
    all_meetings = Meeting.get_all_as_dict()
    return render_template(
        'database.html',
        title='Database test',
        meetings=all_meetings
    )


@app.route('/newmeeting')
@app.route('/new_meeting')
@app.route('/nyttmote')
@app.route('/nytt_mote')
@login_required
def new_meeting():
    """ Renders the meeting creation page """
    form = forms.MeetingForm()
    return render_template(
        'new_meeting.html',
        title='New Meeting',
        form=form
    )


@app.route('/storemeeting', methods=['POST'])
@app.route('/store_meeting', methods=['POST'])
@app.route('/lagremote', methods=['POST'])
@app.route('/lagre_mote', methods=['POST'])
@login_required
def store_meeting():
    """ Store meeting POST form handler """
    form = forms.MeetingForm(request.form)
    if form.validate():
        meeting = Meeting(user_id=current_user.id,
                          title=form.title.data,
                          start_time=form.start_time.data,
                          end_time=form.end_time.data,
                          participant_count=form.participant_count.data
                          )
        meeting.store()
        flash(u'Nytt møte lagt til!')
        return redirect(url_for('home'))
    flash('Feil i skjema!')
    return render_template(
        'new_meeting.html',
        title='New Meeting',
        form=form
    )


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
    url = str(request.form['url'])
    world = World(user_id=current_user.id)
    print url
    return files.save_world_from_fme(url=url, world=world)


@app.route('/get_world/<file_name>')
@login_required
def get_world(file_name):
    return send_from_directory('world_storage', file_name, as_attachment=True)


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
