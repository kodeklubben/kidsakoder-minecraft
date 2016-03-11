# -*- coding: utf-8 -*-
"""
File storage controller
"""
import urllib2
from flask_security import current_user
from flask import url_for, safe_join
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
        return '<p>Verden overført<br><a href="' + url_for('get_world', file_name=file_name) + '">Link</a></p>'
    return '<p>Noe gikk galt!</p>'
