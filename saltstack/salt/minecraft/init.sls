# Salt state for the base requirements needed to run Minecraft/Forge
# Here we make sure Java is install and that there is a user for the Minecraft instance 

{% set server = pillar['minecraft']['server'] %}

# Installs OpenJDK 7 for running Minecraft
install-openjdk:
  pkg.installed:
    - name: openjdk-7-jdk


# Setup a user who will own all the Minecraft files and be able to run the Minecraft instance
minecraft-user:
  user.present:
    - name: {{ server.user }}
    - home: {{ server.path }}

