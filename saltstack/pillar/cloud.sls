salt:
  master: 'master.kode-kidza.no'

azure:
  subscription_id: '9b4a61df-e91a-4cfd-98a5-9cc2f0273859'
  certificate_path: '/etc/salt/kidsakoder.pem'
  vm_image: 'b39f27a8b8c64d52b05eac6a62ebad85__Ubuntu-14_04_4-LTS-amd64-server-20160222-en-us-30GB'
  vm_size: 'Basic_A0'
  location: 'North Europe'
  storage: 'https://kidsakoderstorage.blob.core.windows.net/vhds'
  network: 'network'
  subnet: 'public'
  slot: 'production'
  ssh_username: 'terraform'
  ssh_password: 'Terraform123'
