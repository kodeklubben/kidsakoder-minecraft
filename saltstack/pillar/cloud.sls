# Pillar for Salt Cloud
# See https://docs.saltstack.com/en/latest/topics/cloud/azure.html#configuration

cloud:
  # Salt Cloud profiles
  profiles:
    # Small Azure VM profile
    small:
      provider: azure-config
      size: Standard_DS1_v2
      script_args: stable 2015.8
      grains:
        role: minecraft
        minecraft_size: small
        forge_version: 189
        computercraft_version: 179

    # Medium Azure VM profile
    medium:
      provider: azure-config
      size: Standard_DS2_v2
      script_args: stable 2015.8
      grains:
        role: minecraft
        minecraft_size: medium
        forge_version: 189
        computercraft_version: 179

    # EXAMPLE PROFILE
    # Add more profiles here if necessary
    example-profile:
      # Which provider this profile belongs to
      provider: azure-config
      # The size of the Azure virtual machine
      size: Standard_DS1_v2
      # The Salt bootstrap arguments to be used when Salt Cloud creates a new minion
      # Here we specify that we wish to install the stable version of 2015.8 release of Salt
      script_args: stable 2015.8
      # Specify the Salt grains for all minions created with this profile
      # These grains will be set in /etc/salt/grains on the minions
      # See salt/top.sls and pillar/top.sls for how we match on the grain level
      grains:
        # This determines the role of the minion and which states apply to it
        role: minecraft
        # Determines the how much memory the Minecraft Java process will use
        minecraft_size: small
        # Determines the version of Minecraft Forge
        forge_version: 188
        # Determines the version of the ComputerCraft
        computercraft_version: 178


  # Salt Cloud provider definition
  providers:
    azure-config:
      # The name of the Salt Cloud driver to be used.
      driver: azure

      # NOTE: CHANGE ME
      # The Azure subscription ID to be used.
      subscription_id: 'd8a5f553-66ae-46a1-a5f4-c599cc2bb502'

      # NOTE: CHANGE ME
      # The name of the storage service in Azure to be used for the VMs.
      media_link: https://kidsakoderstorage.blob.core.windows.net/vhds

      # The name of the location of where to create VMs.
      # This much match the name of the storage service defined and created in Terraform.
      location: 'North Europe'

      # Virtual network name
      # This must match the network defined and created in Terraform.
      virtual_network_name: network

      # The VM image SKU in Azure to be used.
      # These can be found by running salt-cloud --list-images=azure
      # More information https://azure.microsoft.com/en-us/documentation/articles/virtual-machines-linux-cli-ps-findimage/
      image: 'b39f27a8b8c64d52b05eac6a62ebad85__Ubuntu-14_04_4-LTS-amd64-server-20160222-en-us-30GB'

      # The path of the certificate used to access Azure.
      # See the wiki for more information on how to create this certificate.
      # Or see https://docs.saltstack.com/en/latest/topics/cloud/azure.html#configuration
      certificate_path: '/etc/salt/azure.pem'

      # Specifices which slot to use in the Azure Hosted Service (Specific for Azure Service management API)
      slot: production

      # SSH credentials used for temporary access when creating VM with Salt Cloud.
      # This is account will be removed after the Salt state is run.
      ssh_username: salt-bootstrap
      ssh_password: BootstrapPassword123

      # Cleanup Azure disk, vhd and service when deleting minions
      cleanup_disks: True
      cleanup_vhds: True
      cleanup_services: True

      # Minion configuration for new minions created with this provider
      minion:
        # Set the location of the Salt master
        # FIXME: This is hardcoded to the first IP in the Azure public subnet
        master: 10.0.4.4
