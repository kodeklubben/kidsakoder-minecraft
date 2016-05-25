flask:
  # The user that Flask/wsgi will be run as
  user: flask
  group: flask

  # The name of the project directory
  proj_dir: /opt/kidsakoder-minecraft
  # Location of Flask logs
  log_dir: /var/log/flask

  # The name of the Flask app
  app_name: flask_app
  # The name of the wsgi file
  wsgi_name: flask_app.wsgi

  # Celery app instance
  celery_app: flask_app.tasks:celery

  # Git
  git_repo: https://github.com/szeestraten/kidsakoder-minecraft
  git_branch: master
