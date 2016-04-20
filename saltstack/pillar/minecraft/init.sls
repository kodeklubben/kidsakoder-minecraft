minecraft:
  server:
    user: minecraft
    group: minecraft
    port: 25565
    path: /opt/minecraft
    mods_path: /opt/minecraft/mods
    max_mem: 512M
    min_mem: 512M

    forge:
      jar_name: forge-1.8.9-11.15.1.1722-universal.jar
      installer:
        link: http://files.minecraftforge.net/maven/net/minecraftforge/forge/1.8.9-11.15.1.1722/forge-1.8.9-11.15.1.1722-installer.jar
        checksum: sha1=49e4e6a9509e77c8649c95c01b29e8e120db3c70

  mods:
    computercraft:
      jar_name: ComputerCraft1.79.jar
      link: http://minecraft.curseforge.com/projects/computercraft/files/2291384/download
      checksum: sha1=045e5843e95276ec19c1876de5bce851fba0233b
