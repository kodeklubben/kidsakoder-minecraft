"""
File storage controller
"""
import urllib2


def save_world_from_fme(url=None):
    # Link example:
    # https://mc-sweco.fmecloud.com:443/fmedatadownload/results/FME_2E257068_1457457321707_15896.zip
    if url is None:
        return 'Ingen URL mottatt'
    split_url = url.strip().split('/')
    sane_url = '/'.join(split_url[0:5]) == 'https://mc-sweco.fmecloud.com:443/fmedatadownload/results'
    if not sane_url:
        return '<p>Ugyldig <a href="' + url + '">URL</a></p>'
    response = urllib2.urlopen(url)
    # TODO use a proper file name
    with open('mc_world.zip', 'wb') as world_file:
        # TODO save in a relevant place
        # TODO store world ref in db
        world_file.write(response.read())
        return u'<p>Verden overført</p>'
    return '<p>Noe gikk galt!</p>'
