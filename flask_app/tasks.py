from celery import Celery, current_app
from celery.signals import after_task_publish
import subprocess

app = Celery('tasks', broker='amqp://guest@master//')
app.conf.update(
    CELERY_RESULT_BACKEND='rpc://',
    CELERY_TRACK_STARTED=True,
)

@app.task(name='tasks.generate_preview_task', bind=True)
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

