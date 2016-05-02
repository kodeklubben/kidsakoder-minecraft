# Install Raspberryjam mod 
{% if grains['mod'] == 'raspberryjam' %}

{% if salt['grains.get']('raspberryjam_version', '') == '0.52' %}
download-raspberryjam-mod-old:
  file.managed:
    - name: {{ server.mods_path }}/{{ mods.raspberryjam.052.jar_name }}
    - source: {{ mods.raspberryjam.052.link }}
    - source_hash: {{ mods.raspberryjam.052.checksum }}
    - user: {{ server.user }}
    - group: {{ server.group }}
    - makedirs: True
    - mode: 755
    - watch:
      - cmd: install-minecraft-forge

{% else %}

download-raspberryjam-mod:
  archive.extracted:
    - name: {{ server.mods_path }}
    - source: {{ mods.raspberryjam.065.link }}
    - source_hash: {{ mods.raspberryjam.065.checksum }}
    - if_missing: {{ server.mods_path }}
    - archive_format: zip
    - user: {{ server.user }}
    - group: {{ server.group }}
    - watch:
      - cmd: install-minecraft-forge
{% endif %}

download-raspberryjam-mcpipy:
  archive.extracted:
    - name: {{ server.path }}
    - source: {{ mods.raspberryjam.052.mcpipy_link }}
    - source_hash: {{ mods.raspberryjam.052.mcpipy_checksum }}
    - if_missing: {{ server.path }}/mcpipy/
    - archive_format: zip
    - user: {{ server.user }}
    - group: {{ server.group }}
    - require:
      - archive: download-raspberryjam-mod
{% endif %}

