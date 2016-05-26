"""
flask_app.tasks
~~~~~~~~~~~~~~~

Celery tasks controller
"""

from celery import Celery
from celery.utils.log import get_task_logger
from flask_app import app
import subprocess
import shutil
import os

# Need to import and setup logger, otherwise Salt overrides it
# See http://stackoverflow.com/questions/28041539/importing-salt-causes-flask-to-output-nothing-in-the-terminal
import sys
import logging
logging.basicConfig(stream=sys.stdout, level=logging.DEBUG, format="%(message)s")
import salt.client


def make_celery(app):
    """ Create celery instance that runs tasks in an app context """
    celery = Celery(app.import_name, broker=app.config['CELERY_BROKER_URL'])
    celery.conf.update(app.config)
    TaskBase = celery.Task

    class ContextTask(TaskBase):
        abstract = True

        def __call__(self, *args, **kwargs):
            with app.app_context():
                return TaskBase.__call__(self, *args, **kwargs)
    celery.Task = ContextTask
    return celery

celery = make_celery(app)
celery_logger = get_task_logger(__name__)


@celery.task(name='tasks.generate_preview_task', bind=True)
def generate_preview_task(self, config_path, unzip_path):
    """ Celery task to generate Minecraft world preview """
    task_id = self.request.id  # Get own id
    backend = self.backend
    backend.store_result(task_id, None, "SENT")  # Set own status to SENT
    subprocess.call(["overviewer.py", "--config=%s" % config_path])

    # Clean up temp files
    try:
        # Remove config file
        os.remove(config_path)
    except OSError:
        celery_logger.warning('Could not remove: ' + config_path)
    try:
        # Remove unzip directory
        shutil.rmtree(unzip_path)
    except OSError:
        celery_logger.warning('Could not remove: ' + unzip_path)
    
    return "Preview complete."


@celery.task(name='tasks.delete_preview_task')
def delete_preview_task(dir_path):
    """ Celery task to delete Minecraft world preview """
    try:
        shutil.rmtree(dir_path)
        return True
    except OSError:
        celery_logger.warning('Could not remove: ' + dir_path)
        return False


@celery.task(name='tasks.meeting_test')
def meeting_test():
    """ Test task for meeting """
    print "Meeting started"


# SALT CLOUD
############
# Note: We are calling the Salt Cloud module (NOT Salt Cloud) from the LocalClient API.
# See https://docs.saltstack.com/en/latest/ref/clients/#localclient for docs on Salt LocalClient API
# See: https://docs.saltstack.com/en/latest/ref/modules/all/salt.modules.cloud.html for more info on the Cloud module


def _async(fun, arg=[]):
    """
    Helper method for asynchronous Salt calls
    """
    client = salt.client.LocalClient()
    client.cmd_async(tgt='master', fun=fun, arg=arg,
                     username=app.config['SALT_CLOUD_USERNAME'],
                     password=app.config['SALT_CLOUD_PASSWORD'],
                     eauth='pam')


def _sync(fun, arg=[]):
    """
    Helper method for synchronous Salt calls
    """
    client = salt.client.LocalClient()
    return client.cmd(tgt='master', fun=fun, arg=arg,
                      username=app.config['SALT_CLOUD_USERNAME'],
                      password=app.config['SALT_CLOUD_PASSWORD'],
                      eauth='pam')


def _action(action, host):
    """
    Helper method for sending cloud actions
    """
    # Allowed actions
    actions = ['start', 'stop', 'reboot']
    if action not in actions:
        pass
    _async(fun='cloud.action', arg=[action, 'instance=%s' % host])


@celery.task(name='tasks.create_machines')
def create_machines(hostnames, profile):
    """
    Creates a number of virtual machines from a list of hostnames.
    Note: Hostnames must be unique in Azure.
    Profiles can be found in saltstack/salt/cloud/cloud.profiles/azure.conf
    """
    # Go through hostnames and create async jobs for each of them
    for host in hostnames:
        _async(fun='cloud.profile', arg=[profile, host])


def create_machines_with_options(hostnames, options):
    """
    WIP

    Creates a number of virtual machines from a list of hostnames.
    Similar to regular create_machine method, however here you need to
    specifiy all your own options.
    """
    # Go through hostnames and create async jobs for each of them
    for host in hostnames:
        _async(fun='cloud.profile', arg=[profile, host])


@celery.task(name='tasks.destroy_machines')
def destroy_machines(hostnames):
    """
    Destroys a number of virtual machines from a list of hostnames.
    """
    for host in hostnames:
        _async(fun='cloud.destroy', arg=[host])


def list_machines():
    """
    List information about all active machines synchronous.
    """
    return _sync(fun='cloud.query')


@celery.task(name='tasks.start_machines')
def start_machines(hostnames):
    """
    Start virtual machines from a list of hostnames as strings.
    """
    for host in hostnames:
        _action('start', host)


@celery.task(name='tasks.stop_machines')
def stop_machines(hostnames):
    """
    Stop virtual machines from a list of hostnames as strings.
    """
    for host in hostnames:
        _action('stop', host)


@celery.task(name='tasks.restart_machines')
def restart_machines(hostnames):
    """
    Restart virtual machines from a list of hostnames as strings.
    """
    for host in hostnames:
        _action('reboot', host)
