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
  '*mc*':
    - minecraft

  # Forge Server version
  {% set forge_version = salt['grains.get']('forge_version', '') %}
  {% if forge_version %}
  'forge_version:{{ forge_version }}':
    - match: grain
    - minecraft.forge.{{ forge_version }}
  {% endif %}

  # Minecraft instance sizes
  {% set size = salt['grains.get']('size', '') %}
  {% if size %}
  'size:{{ size }}':
    - match: grain
    - minecraft.sizes.{{ size }}
  {% endif %}
