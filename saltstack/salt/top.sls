base:
  '*':
    - common
  'master*':
    - cloud
  'web*':
    - webserver
    - overviewer
  '*mc*':
    - minecraft
