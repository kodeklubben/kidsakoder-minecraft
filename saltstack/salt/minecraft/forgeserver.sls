# Salt state for setting up Minecraft Forge server

{% set server = pillar['minecraft']['server'] %}
{% set forge = pillar['minecraft']['forge'] %}
{% set mods = pillar['minecraft']['mods'] %}


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


# Creates an symlink for the runnable jar for Forge to something simpler
setup-minecraft-forge-symlink:
  file.symlink:
    - name: {{ server.path }}/forge-universal.jar
    - target: {{ server.path }}/{{ forge.jar_name }}
    - watch:
      - cmd: install-minecraft-forge


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