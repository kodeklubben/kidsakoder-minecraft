cloud:
  ### Salt specific configurations
  salt:
    # The hostname of the Salt master
    master: 'master.kode-kidza.no'

  ### Azure configuration
  azure:
    # The Azure subscription ID to be used
    subscription_id: '2ac9ba3f-cdb8-4ad9-8575-9c0ea4d15fdf'
    # The path of the certificate used to access Azure
    certificate_path: '/etc/salt/kidsakoder.pem'
    # SSH credentials used for provisioning VMs with Salt Cloud
    ssh_username: 'terraform'
    ssh_password: 'Terraform123'

    ### Virtual Machine settings
    # The VM image used
    vm_image: 'b39f27a8b8c64d52b05eac6a62ebad85__Ubuntu-14_04_4-LTS-amd64-server-20160222-en-us-30GB'
    # The location of where to create VMs
    location: 'North Europe'
    # Specifices which slot to use in the Azure Hosted Service (Specific for Azure Service Managemtn API)
    slot: 'production'
    # The name of the storage service in Azure to be used for the VMs
    storage_name: 'kidsakoderstorage'

    # NOT WORKING
    network: 'network'
    subnet: 'public'

    ### VM profiles
    vm_size_small: 'Standard_DS1_v2'
    vm_size_medium: 'Standard_DS1_v2'
    vm_size_large: 'Standard_DS2_v2'
