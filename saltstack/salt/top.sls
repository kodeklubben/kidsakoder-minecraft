base:
  '*':
    - common
    - users

  # Salt master states
  'master*':
    - cloud

  # Web server states
  'web*':
    - webserver
    - overviewer

  # Minecraft server states
  '*mc*':
    - minecraft
