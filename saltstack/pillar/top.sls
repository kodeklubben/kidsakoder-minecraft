base:
  '*':
    - common
  'master*':
    - cloud
  'webserver*':
    - web
    - cloud
  '*mc*':
    - minecraft
