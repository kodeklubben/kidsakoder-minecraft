overviewer:
  pkgrepo.managed:
    - name: deb http://overviewer.org/debian ./
    - gpgcheck: 1
    - key_url: http://overviewer.org/debian/overviewer.gpg.asc
  pkg.installed:
    - name: minecraft-overviewer
   
rabbitmq-server:
  pkg.installed:
    - name: rabbitmq-server

minecraft-required-for-overviewer:
  file.managed:
    - name: /tmp/minecraft/1.9.jar
    - source: https://s3.amazonaws.com/Minecraft.Download/versions/1.9/1.9.jar
    - source_hash: sha1=2f67dfe8953299440d1902f9124f0f2c3a2c940f
    - makedirs: True
    - mode: 0644
