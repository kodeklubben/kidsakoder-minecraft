# Installs OpenJDK 7 for running Minecraft
install-openjdk:
  pkg.installed:
    - name: openjdk-7-jdk

# Ensures that there is an Minecraft user which will be used for permissions.
minecraft-user:
  user.present:
    - name: {{ pillar['minecraft']['server']['user'] }}
    - home: {{ pillar['minecraft']['server']['path'] }}

# Downloads the Minecraft Forge installer .jar file.
minecraft-forge-installer:
  file.managed:
    - name: {{ pillar['minecraft']['server']['path'] }}/forge-installer.jar
    - source: {{ pillar['minecraft']['server']['forge']['installer']['link'] }}
    - source_hash: {{ pillar['minecraft']['server']['forge']['installer']['checksum'] }}
    - user: {{ pillar['minecraft']['server']['user'] }}
    - group: {{ pillar['minecraft']['server']['group'] }}
    - mode: 755

# Installs Minecraft Forge server using the installer.
# This takes a short while as it downloads other dependencies and sets up directories.
install-minecraft-forge:
  cmd.wait:
    - name: "java -jar forge-installer.jar --installServer"
    - cwd: /opt/minecraft
    - user: {{ pillar['minecraft']['server']['user'] }}
    - group: {{ pillar['minecraft']['server']['group'] }}
    - watch:
      - file: minecraft-forge-installer

# Install ComputerCraft mod 
install-computercraft-mod:
  file.managed:
    - name: {{ pillar['minecraft']['server']['mods_path'] }}/{{ pillar['minecraft']['mods']['computercraft']['jar_name'] }}
    - source: {{ pillar['minecraft']['mods']['computercraft']['link'] }}
    - source_hash: {{ pillar['minecraft']['mods']['computercraft']['checksum'] }}
    - user: {{ pillar['minecraft']['server']['user'] }}
    - group: {{ pillar['minecraft']['server']['group'] }}
    - mode: 755

# Add EULA file required for Minecraft server to run.
minecraft-eula:
  file.managed:
    - name: /opt/minecraft/eula.txt
    - source: salt://minecraft/files/eula.txt
    - user: {{ pillar['minecraft']['server']['user'] }}
    - group: {{ pillar['minecraft']['server']['group'] }}

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
    - require:
      - file: minecraft-upstart
