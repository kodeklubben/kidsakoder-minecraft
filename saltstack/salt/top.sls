# See the Salt Top file docs for more information on how this file works
# https://docs.saltstack.com/en/latest/ref/states/top.html

base:
  # Common states for all minions
  '*':
    - common.packages
    - common.locale
    - common.users

  # Salt master states
  'master':
    - cloud
    - webserver
    - webserver.celery
    - webserver.apache
    - overviewer

  # Minecraft server states determined by the role grain
  'role:minecraft':
    - match: grain
    - minecraft

  # Development states used in when in the Vagrant development environment
  'role:development':
    - match: grain
    - development
    - development.testing
