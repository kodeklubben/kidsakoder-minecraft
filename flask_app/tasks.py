from celery import Celery
import subprocess

app = Celery('tasks', broker='amqp://guest@web//')
app.conf.update(
    CELERY_RESULT_BACKEND='rpc://'
)

@app.task(name='tasks.generate_preview_task')
def generate_preview_task(config_path):
    # Call overviewer to generate
    # WINDOWS
    # subprocess.call(["C:\users\Andreas\overviewer\overviewer.exe", world_path, preview_path])
    # Linux
    subprocess.call(["overviewer.py", "--config=%s" % config_path])
    return "Preview complete."
