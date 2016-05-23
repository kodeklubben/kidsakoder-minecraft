# See the Salt Top file docs for more information on how this file works
# https://docs.saltstack.com/en/latest/ref/states/top.html

base:
  # COMMON
  # Pillar data that should be available for all minions
  '*':
    - common
    - users

  # MASTER
  # Salt master configuration
  'master':
    - cloud
    - webserver

  # MINECRAFT
  # Minecraft server states determined by grain.
  'role:minecraft':
    - match: grain
    - minecraft

  # Forge Server version determined by Salt grain.
  # See minecraft/forge/ directory for the versions available
  {% set forge_version = salt['grains.get']('forge_version', '') %}
  {% if forge_version %}
  'forge_version:{{ forge_version }}':
    - match: grain
    - minecraft.forge.{{ forge_version }}
  {% endif %}

  # ComputerCraft version determined by Salt grain.
  # See minecraft/mods/computercraft/ directory for the versions available.
  {% set computercraft_version = salt['grains.get']('computercraft_version', '') %}
  {% if computercraft_version %}
  'computercraft_version:{{ computercraft_version }}':
    - match: grain
    - minecraft.mods.computercraft.{{ computercraft_version }}
  {% endif %}

  # Minecraft instance sizes determined by Salt grain.
  # See minecraft/sizes/ directory for the sizes available.
  {% set size = salt['grains.get']('minecraft_size', '') %}
  {% if size %}
  'minecraft_size:{{ size }}':
    - match: grain
    - minecraft.sizes.{{ size }}
  {% endif %}
