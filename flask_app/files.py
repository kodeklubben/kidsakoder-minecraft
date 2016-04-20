# -*- coding: utf-8 -*-
"""
File storage controller
"""
import StringIO
import urllib2

from flask_security import current_user

from flask import send_file
from icalendar import Calendar, Event
from pytz import timezone
from jinja2 import escape
from models import Meeting, World
from flask import url_for, safe_join, session
from flask_app import app
import json


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
    file_path = safe_join(app.root_path, app.config['WORLD_UPLOAD_PATH'])
    file_path = safe_join(file_path, file_name)
    with open(file_path, 'wb') as world_file:
        world_file.write(response.read())
        world.file_ref = file_name
        world.description = description
        world.store()
        return_message = {
            'message': '<p>Verden overført</p>',
            'world_id': str(world.id)
        }
        return json.dumps(return_message)

    return '<p>Noe gikk galt!</p>'


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
        e.add('description', u'Møte generert av %s. Antall deltakere: %s. ' % (app.config['APP_NAME'], meeting['participant_count']))
        c.add_component(e)

    export = StringIO.StringIO()
    export.writelines(c.to_ical())
    export.seek(0)
    return send_file(export,
                     attachment_filename=filename + '.ics',
                     as_attachment=True)
