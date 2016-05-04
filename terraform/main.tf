### PROVIDERS ###
# Azure Provider
provider "azure" {
  publish_settings = "${file("secret.publishsettings")}"
}

# DNSimple Provider
provider "dnsimple" {
  token = "${var.dnsimple.token}"
  email = "${var.dnsimple.email}"
}

### MODULES ###
# Site module sets up all the shared resources necessary such as storage and network
module "site" {
  source = "./site"

  # Set the location of the resources
  location = "${var.location}"
}


# Master module sets up the Salt master server
module "master" {
  source = "./master"

  # Set the location of the server
  location = "${var.location}"

  # Set the VM image and size
  vm_image = "${var.vm_image}"
  vm_size = "${var.vm_sizes.2}"

  # Get the shared resources necessary from the site module
  network_name = "${module.site.network_name}"
  storage_name = "${module.site.storage_name}"
  subnet_name = "${module.site.public_subnet_name}"

  # SSH credentials for provisioning the server with Terraform
  ssh_username = "${var.ssh.username}"
  ssh_password = "${var.ssh.password}"

  # Which domain to use for the DNS records
  domain = "${var.domain}"
}


### OUTPUTS ###
output "azure_storage_primary_key" {
  value = "${module.site.storage_primary_key}"
}

output "salt_master_address" {
  value = "${module.master.external_dns}"
}
