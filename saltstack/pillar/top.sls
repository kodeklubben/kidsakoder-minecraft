base:
  '*':
    - common
    - users

  # Salt master configuration
  'master':
    - cloud
    - webserver

  # Minecraft configuration
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
  {% set size = salt['grains.get']('minecraft_size', '') %}
  {% if size %}
  'minecraft_size:{{ size }}':
    - match: grain
    - minecraft.sizes.{{ size }}
  {% endif %}
