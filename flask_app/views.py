# -*- coding: utf-8 -*-
"""
Routes and views for the flask application.
"""
from flask import render_template, request, redirect, url_for, flash, send_from_directory, safe_join, session
from flask_app import app
from models import Meeting, World
from flask_security import login_required, current_user, roles_required
import forms
import files


@app.route('/', methods=['GET', 'POST'])
@login_required
def home():
    """ Renders the home page. """
    form = forms.MeetingForm(request.form)
    meeting_list = Meeting.get_user_meetings_as_dict(current_user.id)
    world = None
    set_tab = 0
    # TODO check if world_id exists
    if form.validate_on_submit():
        # TODO render form on partial form and set tab set_tab=1
        meeting = Meeting(user_id=current_user.id)
        form.populate_obj(meeting)
        meeting.store()
        flash(u'Nytt møte lagt til!')
        return redirect(url_for('home'))

    # TODO flash(u'Feil i skjema!')
    return render_template(
        'index.html',
        set_tab=set_tab,
        title='Hjem',
        meetings=meeting_list,
        form=form,
        world=world,
        action=url_for('home')
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
    all_worlds = World.get_all_as_dict()
    return render_template(
        'database.html',
        title='Database test',
        meetings=all_meetings,
        worlds=all_worlds
    )


@app.route('/nytt_mote', methods=['POST'])
@login_required
def new_meeting():
    """ Renders the meeting creation page """

    # TODO integrate in 'home' and remove

    form = forms.WorldForm(request.form)
    meeting_form = forms.MeetingForm()
    world = None
    if form.validate_on_submit():
        try:
            world_id = int(form.world_id.data)
            description = form.description.data
            world = World.get_by_id(world_id)
            if world.description != description:
                world.description = description
                world.store()
            meeting_form.world_id.process_data(str(world_id))

        except ValueError:
            flash(u'world_id ValueError')

    return redirect(url_for('home', form=meeting_form, world=world))


@app.route('/edit_meeting/<int:meeting_id>', methods=['GET', 'POST'])
@login_required
def edit_meeting(meeting_id):
    # TODO check user id
    if request.method == 'GET':
        meeting = Meeting.get_meeting_by_id(meeting_id)
        form = forms.MeetingForm(obj=meeting)

        return render_template(
            'edit_meeting.html',
            set_tab=1,
            form=form,
            action=url_for('edit_meeting', meeting_id=meeting_id)
        )
    else:
        form = forms.MeetingForm(request.form)
        if form.validate_on_submit():
            meeting = Meeting.get_meeting_by_id(meeting_id)
            form.populate_obj(meeting)
            meeting.update()
            flash(u'Møte endret!')
        return redirect(url_for('home'))


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
    description = request.form['description']
    return files.save_world_from_fme(url=url, description=description)


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


@app.route('/export_calendar', methods=['GET'])
def export_calendar():
    return files.export_calendar_for_user()


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
