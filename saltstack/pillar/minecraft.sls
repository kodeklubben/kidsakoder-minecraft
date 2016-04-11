minecraft:
  server:
    user: minecraft
    group: minecraft
    port: 25565
    path: /opt/minecraft
    max_mem: 512M
    min_mem: 512M
    forge:
      jar_name: forge-1.8.9-11.15.1.1722-universal.jar
      installer:
        link: http://files.minecraftforge.net/maven/net/minecraftforge/forge/1.8.9-11.15.1.1722/forge-1.8.9-11.15.1.1722-installer.jar
        checksum: sha1=49e4e6a9509e77c8649c95c01b29e8e120db3c70
