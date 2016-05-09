cloud:
  ### Salt specific configurations
  salt:
    # Set the location of the Salt master
    master: master.kode-kidza.no

  ### Azure configuration
  azure:
    # The Azure subscription ID to be used
    # This can be found in the Azure portal
    # https://portal.azure.com/#blade/Microsoft_Azure_Billing/SubscriptionsBlade
    subscription_id: '2ac9ba3f-cdb8-4ad9-8575-9c0ea4d15fdf'

    # The path of the certificate used to access Azure
    # See README.md for more information on how to create this certificate
    # Or see https://docs.saltstack.com/en/latest/topics/cloud/azure.html#configuration
    certificate_path: '/etc/salt/kidsakoder.pem'

    # SSH credentials used for creating VMs with Salt Cloud
    ssh:
      username: terraform
      password: Terraform123

    ### Virtual Machine settings
    # The VM image SKU in Azure to be used.
    # These can be found by running salt-cloud --list-images=azure
    # More information https://azure.microsoft.com/en-us/documentation/articles/virtual-machines-linux-cli-ps-findimage/
    vm_image: 'b39f27a8b8c64d52b05eac6a62ebad85__Ubuntu-14_04_4-LTS-amd64-server-20160222-en-us-30GB'

    # The name of the location of where to create VMs
    # NOTE: This much match the name of the storage service defined and created in Terraform
    # See terraform/variables.tf for more details
    location: 'North Europe'

    # The name of the storage service in Azure to be used for the VMs
    # NOTE: This much match the name of the storage service defined and created in Terraform
    # See terraform/site/variables.tf for more details
    storage_name: kidsakoderstorage

    # NOT WORKING
    network_name: network
    subnet_name: public

    # Specifices which slot to use in the Azure Hosted Service (Specific for Azure Service management API)
    slot: production

    # The size/profile of the VM to be used in Azure
    # See https://azure.microsoft.com/en-us/pricing/details/virtual-machines/ for more details
    vm_size:
      small: 'Standard_DS1_v2'
      medium: 'Standard_DS2_v2'
