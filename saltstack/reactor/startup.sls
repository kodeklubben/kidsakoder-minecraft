startup:
  local.cmd.run:
    - tgt: 'master'
    - arg:
      - salt-cloud -f add_input_endpoint azure-config service={{ data['name'] }} deployment={{ data['name'] }} role={{ data['name'] }} name=MINECRAFT local_port=25565 port=25565 protocol=tcp

test:
  local.cmd.run:
    - tgt: 'master'
    - arg:
      - touch /tmp/{{ data['name'] }}
