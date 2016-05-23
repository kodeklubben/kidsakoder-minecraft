# Pillar for Salt Cloud
# See https://docs.saltstack.com/en/latest/topics/cloud/azure.html#configuration
cloud:
  # Salt Cloud profiles
  profiles:
    # Small Azure VM profile
    small:
      provider: azure-config
      size: Standard_DS1_v2
      grains:
        minecraft_size: small
        forge_version: 189
        computercraft_version: 179

    # Medium Azure VM profile
    medium:
      provider: azure-config
      size: Standard_DS2_v2
      grains:
        minecraft_size: medium
        forge_version: 189
        computercraft_version: 179


  # Salt Cloud provider definition
  providers:
    azure-config:
      # Specify the driver of the providers
      driver: azure

      # The Azure subscription ID to be used
      # This can be found in the Azure portal
      # https://portal.azure.com/#blade/Microsoft_Azure_Billing/SubscriptionsBlade
      subscription_id: 'd8a5f553-66ae-46a1-a5f4-c599cc2bb502'

      # The path of the certificate used to access Azure
      # See README.md for more information on how to create this certificate
      # Or see https://docs.saltstack.com/en/latest/topics/cloud/azure.html#configuration
      certificate_path: '/etc/salt/azure.pem'

      # Cleanup disk, vhd and service when deleting minions
      cleanup_disks: True
      cleanup_vhds: True
      cleanup_services: True

      # SSH credentials used for creating VMs with Salt Cloud
      ssh_username: terraform
      ssh_password: Terraform123

      ### Virtual Machine settings
      # The VM image SKU in Azure to be used.
      # These can be found by running salt-cloud --list-images=azure
      # More information https://azure.microsoft.com/en-us/documentation/articles/virtual-machines-linux-cli-ps-findimage/
      image: 'b39f27a8b8c64d52b05eac6a62ebad85__Ubuntu-14_04_4-LTS-amd64-server-20160222-en-us-30GB'

      # The name of the location of where to create VMs
      # NOTE: This much match the name of the storage service defined and created in Terraform
      # See terraform/variables.tf for more details
      location: 'North Europe'

      # The name of the storage service in Azure to be used for the VMs
      # NOTE: This much match the name of the storage service defined and created in Terraform
      # See terraform/site/variables.tf for more details
      media_link: https://kidsakoderstorage.blob.core.windows.net/vhds

      # Network name
      virtual_network_name: network

      # Specifices which slot to use in the Azure Hosted Service (Specific for Azure Service management API)
      slot: production

      # Minion specific settings
      minion:
        # Set the location of the Salt master
        master: master.kode-kidza.no
