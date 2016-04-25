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

  # Minecraft server states
  '*mc*':
    - minecraft
