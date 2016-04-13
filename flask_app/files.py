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

from flask import send_file
from icalendar import Calendar, Event
from pytz import timezone

from models import Meeting
from flask import url_for, safe_join, session
from flask_app import app


def save_world_from_fme(url=None, world=None):
    """ Save generated Minecraft world from FME cloud """
    # Link example:
    # https://mc-sweco.fmecloud.com:443/fmedatadownload/results/FME_2E257068_1457457321707_15896.zip
    if url is None:
        return 'Ingen URL mottatt'
    split_url = url.strip().split('/')
    sane_url = '/'.join(split_url[0:5]) == 'https://mc-sweco.fmecloud.com:443/fmedatadownload/results'
    if not sane_url:
        return '<p>Ugyldig <a href="' + url + '">URL</a></p>'
    response = urllib2.urlopen(url)

    file_name = str(world.id) + '_' + str(current_user.id) + '_' + 'mc_world.zip'
    file_path = safe_join(app.root_path, app.config['WORLD_UPLOAD_PATH'])
    file_path = safe_join(file_path, file_name)
    with open(file_path, 'wb') as world_file:
        world_file.write(response.read())
        world.file_ref = file_name
        world.store()
        session['last_world_ref'] = file_name
        return '<p>Verden overført<br><a href="' + url_for('get_world', file_name=file_name) + '">Link</a></p>'
    return '<p>Noe gikk galt!</p>'


def generate_world_preview(world_ref):
    # create file path
    zip_path = safe_join(app.root_path, app.config['WORLD_UPLOAD_PATH'])
    zip_path = safe_join(zip_path, world_ref)
    # open file:
    unzip_path = safe_join(app.root_path, 'tmp')
    unzip_path = safe_join(unzip_path, world_ref)
    print('unzipping')
    with ZipFile(zip_path, 'r') as world_zip:
        # unzip file
        world_zip.extractall(unzip_path)

    print('finding')
    # TODO find name of mc world:
    world_path = safe_join(unzip_path, 'saves')
    world_path = safe_join(world_path, 'Kodeklubben')
    # path to put preview
    preview_path = safe_join(app.root_path, 'static')
    preview_path = safe_join(preview_path, app.config['PREVIEW_STORAGE_PATH'])
    preview_path = safe_join(preview_path, world_ref)

    # Call overviewer to generate

    subprocess.call(["C:\users\Andreas\overviewer\overviewer.exe", world_path, preview_path])
    # UNIX: subprocess.call(["overviewer.py", world_path, preview_path])
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
    preview_path = safe_join(app.root_path, app.config['PREVIEW_STORAGE_PATH'])
    preview_path = safe_join(preview_path, world_ref)
    preview_path = safe_join(preview_path, 'index.html')
    return preview_path
