# -*- coding: utf-8 -*-
"""
Routes and views for the flask application.
"""

from flask import render_template, request, redirect, url_for, flash, send_from_directory, safe_join, session
from flask_app import app, user_datastore
from models import Meeting, World, User
from flask_security import login_required, current_user, roles_required
from flask_security.forms import RegisterForm

from flask_sqlalchemy import SQLAlchemy

import forms
import files

db = SQLAlchemy(app)

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
    all_users = User.get_all_as_dict()
    return render_template(
        'database.html',
        title='Database test',
        meetings=all_meetings,
        users=all_users
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
        title='New meeting',
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
    flash(u'Feil i skjema!')
    return render_template(
        'new_meeting.html',
        title='New meeting',
        form=form
    )

@app.route('/storeuser', methods=['POST'])
@app.route('/store_user', methods=['POST'])
@app.route('/lagrebruker', methods=['POST'])
@app.route('/lagre_bruker', methods=['POST'])
@login_required
def store_user():
    
    """ Store user POST form handler """
    form = forms.RegisterForm(request.form)
    if form.validate():
        
        #Adds new user to database, based on the info from the form filled in on admin_page
        user_datastore.create_user(email=form.email.data, password=form.password.data)
        user_datastore.add_role_to_user(form.email.data, form.roles.data)
        db.session.commit()
        
        #Takes the user back to admin_page, while displaying a message confirming creation of a user
        flash(u'Ny bruker lagt til!')
        return redirect(url_for('admin_page'))
        
    flash(u'Feil i skjema!')
    return render_template(
        'admin_page.html',
        title='Adminside - Registrer nye brukere',
        form=form
    )
    
@app.route('/register', methods=['GET'])
@login_required
@roles_required('admin')
def register_user():
    """Her er en kul kommentar"""
    return render_template(
        'security/register_user.html'
    )
    
@app.route('/adminpage', methods=['GET', 'POST'])
@login_required
@roles_required('admin')
def admin_page():
    """ Enables admins to register new users """
    form=forms.RegisterForm()
    return render_template(
        'admin_page.html',
        title='Adminside - Registrer nye brukere',
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
    """
    Download Minecraft world
    :param file_name:
    :return:
    """
    directory = safe_join(app.root_path, app.config['WORLD_UPLOAD_PATH'])
    return send_from_directory(directory, file_name, as_attachment=True, attachment_filename=file_name)


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
