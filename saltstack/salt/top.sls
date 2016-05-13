base:
  '*':
    - common
    - users

  # Salt master states
  'master':
    - cloud
    - webserver
    - celery
    - overviewer

  # Minecraft server states
  '*mc*':
    - minecraft
