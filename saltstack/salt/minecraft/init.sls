{% set server = pillar['minecraft']['server'] %}
{% set forge = pillar['minecraft']['forge'] %}
{% set mods = pillar['minecraft']['mods'] %}

# Installs OpenJDK 7 for running Minecraft
install-openjdk:
  pkg.installed:
    - name: openjdk-7-jdk


# Ensures that there is an Minecraft user which will be used for permissions.
minecraft-user:
  user.present:
    - name: {{ server.user }}
    - home: {{ server.path }}


# Downloads the Minecraft Forge installer .jar file.
minecraft-forge-installer:
  file.managed:
    - name: {{ server.path }}/forge_installer.jar
    - source: {{ forge.link }}
    - source_hash: {{ forge.checksum }}
    - user: {{ server.user }}
    - group: {{ server.group }}
    - mode: 755


# Installs Minecraft Forge server using the installer.
# This takes a short while as it downloads other dependencies and sets up directories.
install-minecraft-forge:
  cmd.wait:
    - name: "java -jar forge_installer.jar --installServer"
    - cwd: {{ server.path }}
    - user: {{ server.user }}
    - group: {{ server.group }}
    - watch:
      - file: minecraft-forge-installer


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


# Install Raspberryjam mod 
{% if grains['mod'] == 'raspberryjam' %}
download-raspberryjam-mod:
  archive.extracted:
    - name: {{ server.mods_path }}
    - source: {{ mods.raspberryjam.link }}
    - source_hash: {{ mods.raspberryjam.checksum }}
    - if_missing: {{ server.mods_path }}
    - archive_format: zip
    - user: {{ server.user }}
    - group: {{ server.group }}
    - watch:
      - cmd: install-minecraft-forge

download-raspberryjam-mcpipy:
  archive.extracted:
    - name: {{ server.path }}
    - source: {{ mods.raspberryjam.mcpipy_link }}
    - source_hash: {{ mods.raspberryjam.mcpipy_checksum }}
    - if_missing: {{ server.path }}/mcpipy/
    - archive_format: zip
    - user: {{ server.user }}
    - group: {{ server.group }}
    - require:
      - archive: download-raspberryjam-mod
{% endif %}


# Add EULA file required for Minecraft server to run.
minecraft-eula:
  file.managed:
    - name: {{ server.path }}/eula.txt
    - source: salt://minecraft/files/eula.txt
    - user: {{ server.user }}
    - group: {{ server.group }}


# Add Minecraft server properties
minecraft-server-properties:
  file.managed:
    - name: {{ server.path }}/server.properties
    - source: salt://minecraft/files/server.properties.j2
    - user: {{ server.user }}
    - group: {{ server.group }}
    - template: jinja
    - watch:
      - cmd: install-minecraft-forge


# Create Upstart file for managing the Minecraft service.
# The Upstart file has variables for which port, memory and etc the Minecraft instance should use.
# The service can then be managed by Salt or via commands like 'service minecraft restart'.
minecraft-upstart:
  file.managed:
    - name: /etc/init/minecraft.conf
    - user: root
    - group: root
    - mode: 644
    - source: salt://minecraft/files/minecraft-upstart.conf.j2
    - template: jinja


# Ensures that the Minecraft service is running.
minecraft-service:
  service.running:
    - name: minecraft
    - enable: True
    - restart: True
    - init_delay: 10
    - require:
      - file: minecraft-upstart
    - watch:
      - file: minecraft-server-properties
