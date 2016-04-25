base:
  '*':
    - common
  'master*':
    - cloud
  'web*':
    - webserver
    - cloud
  'mc*':
    - minecraft
  'mc-small*':
    - minecraft.small
  'mc-medium*':
    - minecraft.medium
  'mc-large*':
    - minecraft.large
  'mc-mega*':
    - minecraft.mega
