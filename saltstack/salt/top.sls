base:
  '*':
    - common
    - users

  # Salt master states
  'master':
    - cloud
    - webserver
    - overviewer

  # Minecraft server states
  '*mc*':
    - minecraft
