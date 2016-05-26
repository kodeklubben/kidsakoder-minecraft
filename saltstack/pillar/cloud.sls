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


  # Salt Cloud provider definition
  providers:
    azure-config:
      # The name of the Salt Cloud driver to be used.
      driver: azure

      # NOTE: Must be filled out.
      # The Azure subscription ID to be used. This can be found in the Azure portal
      # https://portal.azure.com/#blade/Microsoft_Azure_Billing/SubscriptionsBlade
      subscription_id: 'd8a5f553-66ae-46a1-a5f4-c599cc2bb502'

      # NOTE: Must be filled out.
      # The name of the storage service in Azure to be used for the VMs.
      # This much match the name of the storage service defined and created in Terraform.
      # See terraform/site/variables.tf for more details
      media_link: https://kidsakoderstorage.blob.core.windows.net/vhds

      # The name of the location of where to create VMs.
      # This much match the name of the storage service defined and created in Terraform.
      # See terraform/variables.tf for more details.
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

      # Minion specific settings
      minion:
        # Set the location of the Salt master
        # FIXME: This is hardcoded to the first IP in the Azure public subnet
        master: 10.0.4.4
