# -*- coding: utf-8 -*-
"""
File storage controller
"""
import StringIO
import urllib2
import os
import subprocess
from zipfile import ZipFile

from flask_security import current_user
from flask import send_file, jsonify
from icalendar import Calendar, Event
from pytz import timezone
from jinja2 import escape
from models import Meeting, World
from flask import safe_join
from flask_app import app
import os

def safe_join_all(root, *arg):
    """ Splits unix-style paths, and joins all paths to a single safe path."""
    path = root # sets first as root
    # SPLIT
    paths = []
    for a in arg:
        p = a.split('/')
        paths += p

    paths.reverse() # reverse, so we go left to right.
    # JOIN
    while paths:
        path = safe_join(path, paths.pop()) # join all paths, one by one

    return path



def save_world_from_fme(url=None, description=""):
    """ Save generated Minecraft world from FME cloud """
    # Link example:
    # https://mc-sweco.fmecloud.com:443/fmedatadownload/results/FME_2E257068_1457457321707_15896.zip
    if url is None:
        return '<p>Ingen URL mottatt</p>'
    split_url = url.strip().split('/')
    sane_url = '/'.join(split_url[0:5]) == 'https://mc-sweco.fmecloud.com:443/fmedatadownload/results'
    if not sane_url:

        return '<p>Ugyldig <a href="' + escape(url) + '">URL</a></p>'
    response = urllib2.urlopen(url)

    world = World(user_id=current_user.id)
    file_name = str(world.id) + '_' + str(current_user.id) + '_' + 'mc_world.zip'
    file_path = safe_join_all(app.root_path, app.config['WORLD_UPLOAD_PATH'], file_name)
    with open(file_path, 'wb') as world_file:
        world_file.write(response.read())
        world.file_ref = file_name
        world.description = description
        world.store()
        return jsonify(
            message=u'Verden overført',
            world_id=str(world.id)
        )

    return '<p>Noe gikk galt!</p>'


def generate_world_preview(world_ref):
    from tasks import generate_preview_task
    # create file path
    zip_path = safe_join_all(app.root_path, app.config['WORLD_UPLOAD_PATH'], world_ref)
    # open file:
    unzip_path = safe_join_all(app.root_path, 'tmp', world_ref)
    print('unzipping')
    with ZipFile(zip_path, 'r') as world_zip:
        # unzip file
        world_zip.extractall(unzip_path)

    print('finding')
    # Find minecraft world inside unzipped directory.
    world_path = safe_join_all(unzip_path, 'saves')
    # We assume there is only one minecraft world, so we pick the first subdir:
    world_path = safe_join_all(world_path, os.listdir(world_path)[0])
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
    result = generate_preview_task.delay(config_path=config_path, world_ref=world_ref)
    # subprocess.call(["overviewer.py", "--config=%s" % config_path])
    # TODO Clean up tmp files

    return '<p> Verden generert tror jeg </p>'


def export_calendar_for_user(cal_user_id=None, filename="export"):
    """Create and export iCalendar file with the meetings of the chosen user"""
    if cal_user_id is None:
        # Defaults to current user
        cal_user_id = current_user.id

    meeting_list = Meeting.get_user_meetings_as_dict(cal_user_id)
    tz = timezone('Europe/Oslo')
    c = Calendar()
    for meeting in meeting_list:
        e = Event()
        e.add('summary', meeting['title'])
        e.add('dtstart', tz.localize(meeting['start_time']))
        e.add('dtend', tz.localize(meeting['end_time']))
        e.add('description',
              u'Møte generert av %s. Antall deltakere: %s. ' % (app.config['APP_NAME'], meeting['participant_count']))
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
        pass


def delete_world_preview(file_ref):
    # TODO Delete generated world preview
    pass
