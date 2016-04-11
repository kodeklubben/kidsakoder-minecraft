install-openjdk:
  pkg.installed:
    - name: openjdk-7-jdk

minecraft-user:
  user.present:
    - name: {{ pillar['minecraft']['server']['user'] }}
    - home: {{ pillar['minecraft']['server']['path'] }}

minecraft-forge-installer:
  file.managed:
    - name: {{ pillar['minecraft']['server']['path'] }}/forge-installer.jar
    - source: {{ pillar['minecraft']['server']['forge']['installer']['link'] }}
    - source_hash: {{ pillar['minecraft']['server']['forge']['installer']['checksum'] }}
    - user: {{ pillar['minecraft']['server']['user'] }}
    - group: {{ pillar['minecraft']['server']['group'] }}
    - mode: 755

install-minecraft-forge:
  cmd.wait:
    - name: "java -jar forge-installer.jar --installServer"
    - cwd: /opt/minecraft
    - user: {{ pillar['minecraft']['server']['user'] }}
    - group: {{ pillar['minecraft']['server']['group'] }}
    - watch:
      - file: minecraft-forge-installer

minecraft-eula:
  file.managed:
    - name: /opt/minecraft/eula.txt
    - source: salt://minecraft/files/eula.txt
    - user: {{ pillar['minecraft']['server']['user'] }}
    - group: {{ pillar['minecraft']['server']['group'] }}

minecraft-upstart:
  file.managed:
    - name: /etc/init/minecraft.conf
    - user: root
    - group: root
    - mode: 644
    - source: salt://minecraft/minecraft.conf
    - template: jinja

minecraft-service:
  service.running:
    - name: minecraft
    - enable: True
    - require:
      - file: minecraft-upstart
