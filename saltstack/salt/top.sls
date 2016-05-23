# See the Salt Top file docs for more information on how this file works
# https://docs.saltstack.com/en/latest/ref/states/top.html

base:
  # Common packages and users for all minions
  '*':
    - common
    - users

  # Salt master states
  'master':
    - cloud
    - webserver
    - celery
    - overviewer

  # Minecraft server states determined by grain.
  'role:minecraft':
    - match: grain
    - minecraft
