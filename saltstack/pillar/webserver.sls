flask:
  git_repo: https://github.com/szeestraten/kidsakoder-minecraft
  git_branch: master
  srv_dir: /srv/flask_app
  venv_dir: /srv/flask_app/venv

celery:
  app: flask_app.tasks:celery
  proj_dir: /opt/kidsakoder-minecraft/
