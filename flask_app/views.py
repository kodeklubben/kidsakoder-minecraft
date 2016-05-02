# -*- coding: utf-8 -*-
"""
Routes and views for the flask application.
"""

from flask import render_template, request, redirect, url_for, flash, send_from_directory, safe_join, jsonify
from flask_app import app
from models import Meeting, World, User
from flask_security import login_required, current_user, roles_required, utils
import forms
import files
import urllib2
import locale


@app.route('/', methods=['GET', 'POST'])
@login_required
def home():
    """ Renders the home page. """
    meeting_list = Meeting.get_user_meetings_as_dict(current_user.id)
    world = None
    set_tab = 0

    if request.method == 'POST':
        world_form = forms.WorldForm(request.form)
        if world_form.validate():
            set_tab = 1
            form = forms.MeetingForm()
            try:
                world_id = int(world_form.world_id.data)
                description = world_form.description.data
                world = World.get_by_id(world_id)
                if world.description != description:
                    world.description = description
                    world.store()
                form.world_id.process_data(str(world_id))

            except ValueError:
                flash(u'world_id ValueError')

            return render_template(
                'index.html',
                set_tab=set_tab,
                title=u'Hjem',
                meetings=meeting_list,
                form=form,
                world=world,
                action=url_for('home'),
                locale=locale.getpreferredencoding()
            )

        form = forms.MeetingForm(request.form)
        if form.validate():
            # TODO Check if world actually exists
            meeting = Meeting(user_id=current_user.id)
            form.populate_obj(meeting)
            meeting.store()
            flash(u'Nytt møte lagt til!')
            return redirect(url_for('home'))

        flash(u'Feil i skjema!')
        set_tab = 1
        return render_template(
            'index.html',
            set_tab=set_tab,
            title=u'Hjem',
            meetings=meeting_list,
            form=form,
            world=world,
            action=url_for('home'),
            locale=locale.getpreferredencoding()
        )

    # else GET blank frontpage
    form = forms.MeetingForm()
    return render_template(
        'index.html',
        set_tab=set_tab,
        title=u'Hjem',
        meetings=meeting_list,
        form=form,
        world=world,
        action=url_for('home'),
        locale=locale.getpreferredencoding()
    )


@app.route('/contact')
@app.route('/kontakt')
@login_required
def contact():
    """ Renders the contact page. """
    return render_template(
        'contact.html',
        title=u'Kontakt oss'
    )


@app.route('/database')
@login_required
@roles_required('admin')
def database():
    """ Test page for database """
    all_meetings = Meeting.get_all_as_dict()
    all_users = User.get_all_as_dict()
    all_worlds = World.get_all_as_dict()
    return render_template(
        'database.html',
        title=u'Database test',
        meetings=all_meetings,
        users=all_users,
        worlds=all_worlds
    )


@app.route('/admin', methods=['GET', 'POST'])  # Need post?
@login_required
@roles_required('admin')
def admin():
    # TODO: Unsure about what (if anything) is still necessary here.
    # This is mostly here to try and make sure non-admins can not access the admin panel.
    """ Enables admins to register new users """
    return render_template(
        'admin/admin.html',
        title=u'Adminside - Registrer nye brukere',
    )


@app.route('/bruker')
@login_required
def user():
    return render_template(
        'user/user.html',
        title=u'Instillinger'
    )


@app.route('/bruker/endre_epost', methods=['GET', 'POST'])
@login_required
def change_email():
    form = forms.ChangeEmail(request.form)
    if form.validate_on_submit():
        if utils.verify_password(form.password.data, current_user.password):
            current_user.email = form.new_email.data
            current_user.store()
            flash(u'E-post adressen ble oppdatert')
            return redirect(url_for('user'))
        form.password.errors.append(u'Feil passord')

    return render_template(
        'user/change_email.html',
        title=u'Endre e-post',
        form=form,
        action=url_for('change_email')
    )


@app.route('/bruker/endre_navn', methods=['GET', 'POST'])
@login_required
def change_name():
    form = forms.ChangeName(request.form)
    if form.validate_on_submit():
        current_user.name = form.new_name.data
        current_user.store()
        flash(u'Navn ble oppdatert')
        return redirect(url_for('user'))

    form.new_name.process_data(current_user.name)
    return render_template(
        'user/change_name.html',
        title=u'Endre navn',
        form=form,
        action=url_for('change_name')
    )


@app.route('/bruker/endre_passord', methods=['GET', 'POST'])
@login_required
def change_password():
    form = forms.ChangePassword(request.form)
    if form.validate_on_submit():
        if utils.verify_password(form.old_password.data, current_user.password):
            current_user.password = utils.encrypt_password(form.new_password.data)
            current_user.store()
            flash(u'Passordet ble endret')
            return redirect(url_for('user'))
        form.old_password.errors.append(u'Feil passord')

    return render_template(
        'user/change_password.html',
        title=u'Endre passord',
        form=form,
        action=url_for('change_password')
    )


@app.route('/bruker/endre_spillernavn', methods=['GET', 'POST'])
@login_required
def change_playername():
    form = forms.ChangePlayername(request.form)
    if form.validate_on_submit():
        if utils.verify_password(form.password.data, current_user.password):
            current_user.mojang_playername = form.playername.data
            current_user.mojang_uuid = form.uuid.data
            current_user.store()
            flash(u'Minecraft spillernavnet ble oppdatert')
            return redirect(url_for('user'))
        form.password.errors.append(u'Feil passord')

    else:
        form.playername.process_data(current_user.mojang_playername)
        form.uuid.process_data(current_user.mojang_uuid)

    return render_template(
        'user/change_playername.html',
        title=u'Endre Minecraft spillernavn',
        form=form,
        action=url_for('change_playername')
    )


@app.route('/bruker/hent_mojang_uuid_proxy/<playername>')
@login_required
def get_mojang_uuid_proxy(playername):
    response = urllib2.urlopen('https://api.mojang.com/users/profiles/minecraft/' + playername)
    return app.response_class(response.read(), mimetype='application/json')


@app.route('/edit_meeting/<int:meeting_id>', methods=['GET', 'POST'])
@login_required
def edit_meeting(meeting_id):
    meeting = Meeting.get_meeting_by_id(meeting_id)
    if meeting.user_id != current_user.id:
        flash(u'Du har ikke tilgang til å endre dette møtet!')
        return redirect(url_for('home'))

    if request.method == 'GET':
        form = forms.MeetingForm(obj=meeting)
        return render_template(
            'edit_meeting.html',
            set_tab=1,
            form=form,
            action=url_for('edit_meeting', meeting_id=meeting_id)
        )

    form = forms.MeetingForm(request.form)
    if form.validate_on_submit():
        form.populate_obj(meeting)
        meeting.store()
        flash(u'Møtet ble endret!')
    return redirect(url_for('home'))


@app.route('/delete_meeting/<int:meeting_id>')
@login_required
def delete_meeting(meeting_id):
    meeting = Meeting.get_meeting_by_id(meeting_id)
    if meeting.user_id == current_user.id:
        # TODO remove world from world list if loaded
        meeting.delete()
        return jsonify(
            success=True,
            message=u'Møtet ble slettet'
        )
    return jsonify(
        success=False,
        message=u'Du har ikke tilgang til å slette dette møtet!'
    )


@app.route('/delete_world/', defaults={'world_id': None})
@app.route('/delete_world/<int:world_id>')
@login_required
def delete_world(world_id):
    if not world_id:
        return jsonify(
            success=False,
            message=u'Ingen verden ID mottatt'
        )

    world = World.get_by_id(world_id)
    if world.user_id == current_user.id:
        if world.delete():
            return jsonify(
                success=True,
                message=u'Verdenen ble slettet'
            )
        return jsonify(
            success=False,
            message=u'Denne verdenen er registrert brukt i et møte'
        )

    return jsonify(
        success=False,
        message=u'Du har ikke tilgang til å slette denne verdenen!'
    )


@app.route('/fra_kart')
@login_required
def from_map():
    """ Renders the map area selection page """
    form = forms.WorldForm()
    return render_template(
        'map/minecraft_kartverket.html',
        title=u'Kart',
        form=form,
        action=url_for('home')
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


@app.route('/dine_verdener')
@login_required
def browse_worlds():
    world_list = World.get_user_worlds(current_user.id)
    return render_template(
        'browse_worlds.html',
        world_list=world_list
    )


@app.route('/generer_test_verdener')
@login_required
@roles_required('admin')
def generate_test_worlds():
    # Generate some test worlds
    world = World(
        user_id=current_user.id,
        description=''
    )
    world.file_ref = str(world.id) + '_1_mc_world.zip'
    world.store()
    for i in range(0, 5):
        world = World(
            user_id=current_user.id,
            description='Verden' + str(i)
        )
        world.file_ref = str(world.id) + '_1_mc_world.zip'
        world.store()
    # End test worlds code
    return 'Success'


@app.route('/veksle_favoritt/', defaults={'world_id': None})
@app.route('/veksle_favoritt/<int:world_id>')
@login_required
def toggle_favourite(world_id):
    if not world_id:
        return jsonify(
            success=False,
            message=u'Ingen verden ID mottatt'
        )
    world = World.get_by_id(world_id)
    if current_user.id == world.user_id:
        world.favourite = not world.favourite
        world.store()

        return jsonify(
            success=True,
            message=u'Lagret som favoritt' if world.favourite else u'Favoritt fjernet',
            favourite=world.favourite
        )

    return jsonify(
        success=False,
        message=u'Du har ikke tilgang til å lagre denne verdenen som favoritt'
    )


@app.route('/test_cloud', methods=['GET', 'POST'])
@login_required
def test_cloud():
    if request.method == 'POST':
        # TODO test code here
        server_list = [{'name': 'Test server', 'location': 1234},
                       {'name': 'Dead server', 'location': 5678}]
        return render_template(
            'test_cloud.html',
            title=u'Test cloud',
            server_list=server_list
        )

    return render_template(
        'test_cloud.html',
        title=u'Test cloud',
        server_list=[]
    )


@app.route('/export_calendar', methods=['GET'])
@login_required
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
