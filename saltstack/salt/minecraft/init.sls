# Salt state for the base requirements needed to run Minecraft/Forge

{% set server = pillar['minecraft']['server'] %}
{% set forge = pillar['minecraft']['forge'] %}
{% set mods = pillar['minecraft']['mods'] %}

# Setup a user who will own all the Minecraft files and be able to run the Minecraft instance
minecraft-user:
  user.present:
    - name: {{ server.user }}
    - home: {{ server.path }}


# Installs OpenJDK 7 for running Minecraft
install-openjdk:
  pkg.installed:
    - name: openjdk-7-jdk


# Downloads the Minecraft Forge installer .jar file.
download-minecraft-forge:
  file.managed:
    - name: {{ server.path }}/forge_installer.jar
    - source: {{ forge.link }}
    - source_hash: {{ forge.checksum }}
    - user: {{ server.user }}
    - group: {{ server.group }}
    - mode: 755
    - require:
      - pkg: install-openjdk


# Installs Minecraft Forge server using the installer.
# This takes a short while as it downloads other dependencies and sets up directories.
# See http://www.minecraftforge.net/wiki/Installation/Universal for more information
install-minecraft-forge:
  cmd.run:
    - name: "java -jar forge_installer.jar --installServer"
    - cwd: {{ server.path }}
    - user: {{ server.user }}
    - group: {{ server.group }}
    - require:
      - pkg: install-openjdk
    - onchanges:
      - file: download-minecraft-forge


# Creates an symlink for the runnable jar for Forge to something simpler.
# The jar created by the forge installer has a lot of versioning info in the filename.
setup-minecraft-forge-symlink:
  file.symlink:
    - name: {{ server.path }}/{{ forge.jar_symlink_name }}
    - target: {{ server.path }}/{{ forge.jar_name }}
    - user: {{ server.user }}
    - group: {{ server.group }}
    - onchanges:
      - cmd: install-minecraft-forge


# Install ComputerCraft mod for Forge
install-computercraft-mod:
  file.managed:
    - name: {{ server.mods_path }}/{{ mods.computercraft.jar_name }}
    - source: {{ mods.computercraft.link }}
    - source_hash: {{ mods.computercraft.checksum }}
    - user: {{ server.user }}
    - group: {{ server.group }}
    - makedirs: True
    - mode: 755
    - onchanges:
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
    - replace: False


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
    - onchanges:
      - cmd: install-minecraft-forge
    - order: last
