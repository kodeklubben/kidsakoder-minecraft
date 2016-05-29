# Pillar for things related to the Minecraft server

minecraft:
  server:
    # The user and group account that owns and runs Minecraft
    user: minecraft
    group: minecraft

    # The path where we install and run Minecraft
    path: /opt/minecraft

    # The path to the Minecraft mods for Forge
    mods_path: /opt/minecraft/mods

    # Default Minecraft Java process memory sizes
    # These values should be overwritten by the other sizes in sizes/ directory
    max_mem: 512M
    min_mem: 256M

    # The location of the error logs for the Java process
    java_log: /opt/minecraft/log/hs_err_pid%p.log


  # The pillar data for the different versions of Forge is located in the forge directory
  forge:
    # The name of the executable Forge server jar
    # We symlink the actual jar file to this as it has a lot of versioning info
    jar_symlink_name: forge-universal.jar


  # Minecraft server properties and settings
  # See http://minecraft.gamepedia.com/Server.properties for more information
  properties:
    # The port to be used for Minecraft
    port: 25565
    ip: ""

    # Game rules
    gamemode: 1
    force_gamemode: true
    allow_flight: true
    allow_nether: false
    difficulty: 1
    hardcore: false
    pvp: true

    # World specifics
    level_name: world
    level_seed: ""
    level_type: DEFAULT
    max_world_size: 1000
    max_build_height: 256
    generator_settings: ""
    generate_structures: true

    # Spawn entities
    spawn_npcs: true
    spawn_animals: true
    spawn_monsters: true

    # Server specifics
    max_players: 20
    max_tick_time: 60000
    network_compression_threshold: 256
    view_distance: 10
    motd: Kidsakoder.no
    white_list: false
    announce_player_achievements: false
    player_idle_timeout: 0
    op_permission_level: 4

    # Other
    enable_query: false
    enable_rcon: false
    enable_command_block: false
    snooper_enabled: false
    online_mode: true
    resource_pack: ""
    resource_pack_sha1: ""
