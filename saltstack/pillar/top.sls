# See the Salt Top file docs for more information on how this file works
# https://docs.saltstack.com/en/latest/ref/states/top.html

base:
  # Common pillar data for all minions
  '*':
    - common

  # Salt master pillar data
  'master':
    - cloud
    - webserver

  # Minecraft server pillar determined by the role grain.
  'role:minecraft':
    - match: grain
    - minecraft

  # NOTE: The following section uses grains to determine what pillar data
  # This allows us to map grain values to pillar individual files
  # For exmaple, when writing states, we can simply use the pillar data
  # which is determined by the pillar file which is mapped by the grain value

  # Forge Server version
  # See pillar/minecraft/forge/ for the versions available
  {% set forge_version = salt['grains.get']('forge_version', '') %}
  {% if forge_version %}
  'forge_version:{{ forge_version }}':
    - match: grain
    - minecraft.forge.{{ forge_version }}
  {% endif %}

  # ComputerCraft version
  # See pillar/minecraft/mods/computercraft/ for the versions available
  {% set computercraft_version = salt['grains.get']('computercraft_version', '') %}
  {% if computercraft_version %}
  'computercraft_version:{{ computercraft_version }}':
    - match: grain
    - minecraft.mods.computercraft.{{ computercraft_version }}
  {% endif %}

  # Minecraft instance sizes
  # See pillar/minecraft/sizes/ for the sizes available
  {% set size = salt['grains.get']('minecraft_size', '') %}
  {% if size %}
  'minecraft_size:{{ size }}':
    - match: grain
    - minecraft.sizes.{{ size }}
  {% endif %}
