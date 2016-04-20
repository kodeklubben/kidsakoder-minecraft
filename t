[1mdiff --git a/saltstack/pillar/minecraft/init.sls b/saltstack/pillar/minecraft/init.sls[m
[1mindex d9417b6..890c77d 100644[m
[1m--- a/saltstack/pillar/minecraft/init.sls[m
[1m+++ b/saltstack/pillar/minecraft/init.sls[m
[36m@@ -2,20 +2,64 @@[m [mminecraft:[m
   server:[m
     user: minecraft[m
     group: minecraft[m
[31m-    port: 25565[m
     path: /opt/minecraft[m
     mods_path: /opt/minecraft/mods[m
[32m+[m[32m    ip: ""[m
[32m+[m[32m    port: 25565[m
     max_mem: 512M[m
     min_mem: 512M[m
 [m
[31m-    forge:[m
[31m-      jar_name: forge-1.8.9-11.15.1.1722-universal.jar[m
[31m-      installer:[m
[31m-        link: http://files.minecraftforge.net/maven/net/minecraftforge/forge/1.8.9-11.15.1.1722/forge-1.8.9-11.15.1.1722-installer.jar[m
[31m-        checksum: sha1=49e4e6a9509e77c8649c95c01b29e8e120db3c70[m
[32m+[m[32m  forge:[m
[32m+[m[32m    jar_name: forge-1.8.9-11.15.1.1722-universal.jar[m
[32m+[m[32m    link: http://files.minecraftforge.net/maven/net/minecraftforge/forge/1.8.9-11.15.1.1722/forge-1.8.9-11.15.1.1722-installer.jar[m
[32m+[m[32m    checksum: sha1=49e4e6a9509e77c8649c95c01b29e8e120db3c70[m
 [m
   mods:[m
     computercraft:[m
       jar_name: ComputerCraft1.79.jar[m
       link: http://minecraft.curseforge.com/projects/computercraft/files/2291384/download[m
       checksum: sha1=045e5843e95276ec19c1876de5bce851fba0233b[m
[32m+[m
[32m+[m[32m  properties:[m
[32m+[m[32m    # Game rules[m
[32m+[m[32m    gamemode: 1 # Creative mode[m
[32m+[m[32m    force_gamemode: true[m
[32m+[m[32m    allow_flight: true[m
[32m+[m[32m    allow_nether: false[m
[32m+[m[32m    difficulty: 1[m
[32m+[m[32m    hardcore: false[m
[32m+[m[32m    pvp: true[m
[32m+[m
[32m+[m[32m    # World specifics[m
[32m+[m[32m    level_name: world[m
[32m+[m[32m    level_seed: ""[m
[32m+[m[32m    level_type: DEFAULT[m
[32m+[m[32m    max_world_size: 1000[m
[32m+[m[32m    max_build_height: 256[m
[32m+[m[32m    generator_settings: ""[m
[32m+[m[32m    generate_structures: true[m
[32m+[m
[32m+[m[32m    # Spawn entities[m
[32m+[m[32m    spawn_npcs: true[m
[32m+[m[32m    spawn_animals: true[m
[32m+[m[32m    spawn_monsters: true[m
[32m+[m
[32m+[m[32m    # Server specifics[m
[32m+[m[32m    max_players: 20[m
[32m+[m[32m    max_tick_time: 60000[m
[32m+[m[32m    network_compression_threshold: 256[m
[32m+[m[32m    view_distance: 10[m
[32m+[m[32m    motd: Kidsakoder.no[m
[32m+[m[32m    white_list: false[m
[32m+[m[32m    announce_player_achievements: false[m
[32m+[m[32m    player_idle_timeout: 0[m
[32m+[m[32m    op_permission_level: 4[m
[32m+[m
[32m+[m[32m    # Other[m
[32m+[m[32m    enable_query: false[m
[32m+[m[32m    enable_rcon: false[m
[32m+[m[32m    enable_command_block: false[m
[32m+[m[32m    snooper_enabled: false[m
[32m+[m[32m    online_mode: true[m
[32m+[m[32m    resource_pack: ""[m
[32m+[m[32m    resource_pack_sha1: ""[m
[1mdiff --git a/saltstack/salt/minecraft/files/minecraft-upstart.conf.j2 b/saltstack/salt/minecraft/files/minecraft-upstart.conf.j2[m
[1mindex 0235d75..6e044dc 100644[m
[1m--- a/saltstack/salt/minecraft/files/minecraft-upstart.conf.j2[m
[1m+++ b/saltstack/salt/minecraft/files/minecraft-upstart.conf.j2[m
[36m@@ -1,4 +1,6 @@[m
 # Upstart script for Minecraft Forge server[m
[32m+[m[32m{% set server = pillar['minecraft']['server'] %}[m
[32m+[m[32m{% set forge = pillar['minecraft']['forge'] %}[m
 [m
 description "minecraft forge server"[m
 [m
[36m@@ -8,14 +10,14 @@[m [mstop on runlevel [!2345][m
 respawn[m
 respawn limit 10 5[m
 [m
[31m-setuid {{ pillar['minecraft']['server']['user'] }}[m
[31m-setgid {{ pillar['minecraft']['server']['group'] }}[m
[32m+[m[32msetuid {{ server.user }}[m
[32m+[m[32msetgid {{ server.group }}[m
 [m
[31m-env JAR={{ pillar['minecraft']['server']['forge']['jar_name'] }}[m
[31m-env CWD={{ pillar['minecraft']['server']['path'] }}[m
[31m-env PORT={{ pillar['minecraft']['server']['port'] }}[m
[31m-env MAX_MEM={{ pillar['minecraft']['server']['max_mem'] }}[m
[31m-env MIN_MEM={{ pillar['minecraft']['server']['min_mem'] }}[m
[32m+[m[32menv CWD={{ server.path }}[m
[32m+[m[32menv JAR={{ forge.jar_name }}[m
[32m+[m[32menv PORT={{ server.port }}[m
[32m+[m[32menv MAX_MEM={{ server.max_mem }}[m
[32m+[m[32menv MIN_MEM={{ server.min_mem }}[m
 [m
 script [m
   cd $CWD[m
[1mdiff --git a/saltstack/salt/minecraft/init.sls b/saltstack/salt/minecraft/init.sls[m
[1mindex 5f2dee3..a97bd22 100644[m
[1m--- a/saltstack/salt/minecraft/init.sls[m
[1m+++ b/saltstack/salt/minecraft/init.sls[m
[36m@@ -1,52 +1,74 @@[m
[32m+[m[32m{% set server = pillar['minecraft']['server'] %}[m
[32m+[m[32m{% set forge = pillar['minecraft']['forge'] %}[m
[32m+[m[32m{% set mods = pillar['minecraft']['mods'] %}[m
[32m+[m
 # Installs OpenJDK 7 for running Minecraft[m
 install-openjdk:[m
   pkg.installed:[m
     - name: openjdk-7-jdk[m
 [m
[32m+[m
 # Ensures that there is an Minecraft user which will be used for permissions.[m
 minecraft-user:[m
   user.present:[m
[31m-    - name: {{ pillar['minecraft']['server']['user'] }}[m
[31m-    - home: {{ pillar['minecraft']['server']['path'] }}[m
[32m+[m[32m    - name: {{ server.user }}[m
[32m+[m[32m    - home: {{ server.path }}[m
[32m+[m
 [m
 # Downloads the Minecraft Forge installer .jar file.[m
 minecraft-forge-installer:[m
   file.managed:[m
[31m-    - name: {{ pillar['minecraft']['server']['path'] }}/forge-installer.jar[m
[31m-    - source: {{ pillar['minecraft']['server']['forge']['installer']['link'] }}[m
[31m-    - source_hash: {{ pillar['minecraft']['server']['forge']['installer']['checksum'] }}[m
[31m-    - user: {{ pillar['minecraft']['server']['user'] }}[m
[31m-    - group: {{ pillar['minecraft']['server']['group'] }}[m
[32m+[m[32m    - name: {{ server.path }}/forge_installer.jar[m
[32m+[m[32m    - source: {{ forge.link }}[m
[32m+[m[32m    - source_hash: {{ forge.checksum }}[m
[32m+[m[32m    - user: {{ server.user }}[m
[32m+[m[32m    - group: {{ server.group }}[m
     - mode: 755[m
 [m
[32m+[m
 # Installs Minecraft Forge server using the installer.[m
 # This takes a short while as it downloads other dependencies and sets up directories.[m
 install-minecraft-forge:[m
   cmd.wait:[m
[31m-    - name: "java -jar forge-installer.jar --installServer"[m
[31m-    - cwd: /opt/minecraft[m
[31m-    - user: {{ pillar['minecraft']['server']['user'] }}[m
[31m-    - group: {{ pillar['minecraft']['server']['group'] }}[m
[32m+[m[32m    - name: "java -jar forge_installer.jar --installServer"[m
[32m+[m[32m    - cwd: {{ server.path }}[m
[32m+[m[32m    - user: {{ server.user }}[m
[32m+[m[32m    - group: {{ server.group }}[m
     - watch:[m
       - file: minecraft-forge-installer[m
 [m
 # Install ComputerCraft mod [m
 install-computercraft-mod:[m
   file.managed:[m
[31m-    - name: {{ pillar['minecraft']['server']['mods_path'] }}/{{ pillar['minecraft']['mods']['computercraft']['jar_name'] }}[m
[31m-    - source: {{ pillar['minecraft']['mods']['computercraft']['link'] }}[m
[31m-    - source_hash: {{ pillar['minecraft']['mods']['computercraft']['checksum'] }}[m
[31m-    - user: {{ pillar['minecraft']['server']['user'] }}[m
[31m-    - group: {{ pillar['minecraft']['server']['group'] }}[m
[32m+[m[32m    - name: {{ server.mods_path }}/{{ mods.computercraft.jar_name }}[m
[32m+[m[32m    - source: {{ mods.computercraft.link }}[m
[32m+[m[32m    - source_hash: {{ mods.computercraft.checksum }}[m
[32m+[m[32m    - user: {{ server.user }}[m
[32m+[m[32m    - group: {{ server.group }}[m
[32m+[m[32m    - makedirs: True[m
     - mode: 755[m
[32m+[m[32m    - watch:[m
[32m+[m[32m      - cmd: install-minecraft-forge[m
[32m+[m
 [m
 # Add EULA file required for Minecraft server to run.[m
 minecraft-eula:[m
   file.managed:[m
[31m-    - name: /opt/minecraft/eula.txt[m
[32m+[m[32m    - name: {{ server.path }}/eula.txt[m
     - source: salt://minecraft/files/eula.txt[m
[31m-    - user: {{ pillar['minecraft']['server']['user'] }}[m
[31m-    - group: {{ pillar['minecraft']['server']['group'] }}[m
[32m+[m[32m    - user: {{ server.user }}[m
[32m+[m[32m    - group: {{ server.group }}[m
[32m+[m
[32m+[m
[32m+[m[32m# Add Minecraft server properties[m
[32m+[m[32mminecraft-server-properties:[m
[32m+[m[32m  file.managed:[m
[32m+[m[32m    - name: {{ server.path }}/server.properties[m
[32m+[m[32m    - source: salt://minecraft/files/server.properties.j2[m
[32m+[m[32m    - user: {{ server.user }}[m
[32m+[m[32m    - group: {{ server.group }}[m
[32m+[m[32m    - template: jinja[m
[32m+[m
 [m
 # Create Upstart file for managing the Minecraft service.[m
 # The Upstart file has variables for which port, memory and etc the Minecraft instance should use.[m
[36m@@ -60,10 +82,15 @@[m [mminecraft-upstart:[m
     - source: salt://minecraft/files/minecraft-upstart.conf.j2[m
     - template: jinja[m
 [m
[32m+[m
 # Ensures that the Minecraft service is running.[m
 minecraft-service:[m
   service.running:[m
     - name: minecraft[m
     - enable: True[m
[32m+[m[32m    - restart: True[m
[32m+[m[32m    - init_delay: 10[m
     - require:[m
       - file: minecraft-upstart[m
[32m+[m[32m    - watch:[m
[32m+[m[32m      - file: minecraft-server-properties[m
