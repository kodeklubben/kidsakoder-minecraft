base:
  '*':
    - common

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
  {% if grains['size'] %}
  'size:{{ grains['size'] }}':
    - match: grain
    - minecraft.sizes.{{ grains['size'] }}
  {% endif %}
