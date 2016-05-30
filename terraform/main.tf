### NOTE ###
# We are using the Azure (Service Management) provider in Terraform,
# not the newer AzureRM (Resource Manager) provider.
# See https://www.terraform.io/docs/providers/azure/index.html for more info.
############

### PROVIDERS ###
# Azure Provider
provider "azure" {
  # Looks for the publish settings file in the same directory.
  publish_settings = "${file("secret.publishsettings")}"
}

### MODULES ###
# Site module sets up all the shared resources such as storage and network.
module "site" {
  source = "./site"

  # Add an prefix to the Azure storage service as it needs to be unique
  prefix_name = "${var.prefix_name}"

  # Set the location of the resources
  location = "${var.location}"
}


# Master module sets up the Salt master server
module "master" {
  source = "./master"

  # We add an prefix to the Azure hosted
  prefix_name = "${var.prefix_name}"

  # Set the location of the server
  location = "${var.location}"

  # Set the VM image and size
  vm_image = "${var.vm_image}"
  vm_size = "${var.vm_sizes.0}"

  # Get the shared resources necessary from the site module
  network_name = "${module.site.network_name}"
  storage_name = "${module.site.storage_name}"
  subnet_name = "${module.site.public_subnet_name}"
  security_group_name = "${module.site.public_security_group_name}"

  # Use random password for bootstrapping/provisioning the server with Terraform
  ssh_password = "${uuid()}"
}
