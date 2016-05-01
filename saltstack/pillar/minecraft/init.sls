minecraft:
  server:
    user: minecraft
    group: minecraft
    path: /opt/minecraft
    mods_path: /opt/minecraft/mods
    ip: ""
    port: 25565
    max_mem: 512M
    min_mem: 512M
    java_log: /opt/minecraft/log/hs_err_pid%p.log


  # Minecraft Server Properties
  properties:
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
