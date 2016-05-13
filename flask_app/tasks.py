from celery import Celery, current_app
from celery.signals import after_task_publish

from flask_app import app

import subprocess
import shutil


celery = Celery('tasks', broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)


@celery.task(name='tasks.generate_preview_task', bind=True)
def generate_preview_task(self, config_path):
    # Call overviewer to generate
    # WINDOWS
    # subprocess.call(["C:\users\Andreas\overviewer\overviewer.exe", world_path, preview_path])
    # Linux
    task_id = self.request.id # Get own id
    backend = self.backend
    backend.store_result(task_id, None, "SENT") # Set own status to SENT
    subprocess.call(["overviewer.py", "--config=%s" % config_path])
    return "Preview complete."


@celery.task(name='tasks.delete_preview_task')
def delete_preview_task(dir_path):
    try:
        shutil.rmtree(dir_path)
    except OSError:
        pass


@celery.task(name='tasks.meeting_test')
def meeting_test():
    print "Meeting started"
