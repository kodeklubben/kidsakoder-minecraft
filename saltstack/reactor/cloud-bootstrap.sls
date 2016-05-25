# This is a startup state to be run when minions have been created by Salt Cloud

# We need to add an endpoint to the VM in Azure in order to open ports for Minecraft
# As we're not using CloudClient, we've hacked this together so the Salt master runs
# a salt-cloud command specifically for Azure to add an endpoint for Minecraft
add_azure_endpoint:
  local.cmd.run:
    - tgt: 'master'
    - arg:
      - salt-cloud -f add_input_endpoint azure-config service={{ data['name'] }} deployment={{ data['name'] }} role={{ data['name'] }} name=MINECRAFT local_port=25565 port=25565 protocol=tcp

# After the minion has been created by Salt Cloud, it needs to run highstate
# to pull down its configuration
run_highstate:
  cmd.state.apply:
    - tgt: {{ data['name'] }}
