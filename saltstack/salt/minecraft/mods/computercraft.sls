# Install ComputerCraft mod 
{% if grains['mod'] == 'computercraft' %}
install-computercraft-mod:
  file.managed:
    - name: {{ server.mods_path }}/{{ mods.computercraft.jar_name }}
    - source: {{ mods.computercraft.link }}
    - source_hash: {{ mods.computercraft.checksum }}
    - user: {{ server.user }}
    - group: {{ server.group }}
    - makedirs: True
    - mode: 755
    - watch:
      - cmd: install-minecraft-forge
{% endif %}
