base:
  '*':
    - common
  'master*':
    - cloud
  'web*':
    - webserver
    - cloud
  '*mc*':
    - minecraft
