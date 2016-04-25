base:
  '*':
    - common
    - users

  # Salt master configuration
  'master*':
    - cloud

  # Web server configuration
  'web*':
    - webserver
    - cloud

  # Minecraft base configuration
  'mc*':
    - minecraft

  # Minecraft sizes
  {% set size = salt['grains.get']('size', '') %}
  {% if size %}
  'size:{{ size }}':
    - match: grain
    - minecraft.sizes.{{ size }}
  {% endif %}
