# -*- coding: utf-8 -*-
"""
flask_app.files
~~~~~~~~~~~~~~~

File storage controller
"""
import StringIO
import urllib2
import os
from zipfile import ZipFile
from flask_security import current_user
from flask import send_file, jsonify, safe_join
from icalendar import Calendar, Event
from pytz import timezone
from jinja2 import escape
from models import Meeting, World
from flask_app import app
from werkzeug.datastructures import FileStorage


def safe_join_all(root, *arg):
    """ Splits unix-style paths, and joins all paths to a single safe path."""
    path = root  # sets first as root
    # SPLIT
    paths = []
    for a in arg:
        p = a.split('/')
        paths += p

    paths.reverse()  # reverse, so we go left to right.
    # JOIN
    while paths:
        path = safe_join(path, paths.pop()) # join all paths, one by one

    return path


def super_safe_join(directory, filename):
    """
    Allow slashes in `filename` and safely join `directory` and `filename`

    :param directory: the base directory.
    :param filename: the untrusted path relative to that directory.
    """
    path_list = filename.split('/')
    for path in path_list:
        directory = safe_join(directory, path)
    return directory


def search_for_file(path, filename):
    """
    Searches top down for a filename and returns the path to the folder of the file if found, False if not found

    :param path: path to start looking from.
    :param filename: file to look for.
    """
    for root, dirs, files in os.walk(path): 
        for file in files:
            if file == filename:
                return root

    return False


def save_world_from_fme(url=None, description=""):
    """ Save generated Minecraft world from FME cloud """
    # Link example:
    # https://mc-sweco.fmecloud.com:443/fmedatadownload/results/FME_2E257068_1457457321707_15896.zip
    if url is None:
        return '<p>Ingen URL mottatt</p>'
    split_url = url.strip().split('/')
    sane_url = '/'.join(split_url[0:5]) == 'https://mc-sweco.fmecloud.com:443/fmedatadownload/results'
    if not sane_url:
        return jsonify(message=u'Ugyldig <a href="' + escape(url) + u'">URL</a>')
    response = urllib2.urlopen(url)

    world = save_world(response, description)
    return jsonify(
        message=u'Verden overført',
        world_id=str(world.id)
    )


def save_world(file_data=None, description=""):
    """ Save file from form data or download """
    world = World(user_id=current_user.id)
    # Construct file name with world ID and user ID for reference. End with arbitrary string and zip extension
    # Example: 7_3_mc_world.zip
    file_name = str(world.id) + '_' + str(current_user.id) + '_' + 'mc_world.zip'
    file_path = safe_join_all(app.root_path, app.config['WORLD_UPLOAD_PATH'], file_name)

    # Check if file data comes from a form submission
    if isinstance(file_data, FileStorage):
        file_data.save(file_path)
    else:  # Else assume it has read() function
        with open(file_path, 'wb') as world_file:
            world_file.write(file_data.read())

    world.file_ref = file_name
    world.description = description
    world.store()
    return world


def generate_world_preview(world_ref):
    from tasks import generate_preview_task
    # create file path
    zip_path = safe_join_all(app.root_path, app.config['WORLD_UPLOAD_PATH'], world_ref)
    # open file:
    # TODO Use proper temp folder: tempfile.gettempdir()
    unzip_path = safe_join_all(app.root_path, 'tmp', world_ref)
    print('unzipping')
    with ZipFile(zip_path, 'r') as world_zip:
        # unzip file
        world_zip.extractall(unzip_path)

    print('finding')
    # Find minecraft world inside unzipped directory.
    # TODO locate level.dat file. For user uploaded worlds file structure probably does not contain entire saves dir

    world_path = search_for_file(unzip_path, 'level.dat')
    # path to put preview
    preview_path = safe_join_all(app.root_path, app.config['PREVIEW_STORAGE_PATH'], world_ref)

    texturepack_path = safe_join_all(app.root_path, app.config['TEXTUREPACK_PATH'])

    config_path = safe_join_all(app.root_path, 'tmp', 'overviewer_config_%s' % world_ref)

    # Create config file
    with open(config_path, 'w+') as cfile:
        cfile.writelines(
            ['worlds["world"] = "%s" \n \n' % world_path,
            'renders["normalrender"] = { \n',
            '   "world": "world", \n',
            '   "title": "Kart over din Minecraft-verden", \n',
            '} \n \n', 'outputdir = "%s" \n' % preview_path,
            'texturepath = "%s" \n' % texturepack_path,
            'defaultzoom = 12 \n'
            ])
    # Call overviewer to generate
    result = generate_preview_task.apply_async((config_path,), task_id=world_ref) # Note: singleton arg tuple needs a trailing comma
    # subprocess.call(["overviewer.py", "--config=%s" % config_path])
    # TODO Clean up tmp files

    return '<p> Verden generert tror jeg </p>'


def export_calendar_for_user(cal_user_id=None, filename="export"):
    """Create and export iCalendar file with the meetings of the chosen user"""
    if cal_user_id is None:
        # Defaults to current user
        cal_user_id = current_user.id

    meeting_list = Meeting.get_user_meetings(cal_user_id)
    tz = timezone('Europe/Oslo')
    c = Calendar()
    for meeting in meeting_list:
        e = Event()
        e.add('summary', meeting.title)
        e.add('dtstart', tz.localize(meeting.start_time))
        e.add('dtend', tz.localize(meeting.end_time))
        e.add('description',
              u'Møte generert av %s. Antall deltakere: %s. ' % (app.config['APP_NAME'], meeting.participant_count))
        c.add_component(e)

    export = StringIO.StringIO()
    export.writelines(c.to_ical())
    export.seek(0)
    return send_file(export,
                     attachment_filename=filename + '.ics',
                     as_attachment=True)


def show_preview(world_ref):
    preview_path = safe_join_all(app.root_path, app.config['PREVIEW_STORAGE_PATH'], world_ref, 'index.html')
    return preview_path


def delete_world_file(file_ref):
    file_path = safe_join_all(app.root_path, app.config['WORLD_UPLOAD_PATH'], file_ref)
    try:
        os.remove(file_path)
    except OSError:
        app.logger.warning('Could not remove: ' + file_path)


def delete_world_preview(file_ref):
    from tasks import delete_preview_task
    dir_path = safe_join_all(app.root_path, app.config['PREVIEW_STORAGE_PATH'], file_ref)
    result = delete_preview_task.delay(dir_path)
    return result
