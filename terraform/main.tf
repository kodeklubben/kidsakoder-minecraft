### PROVIDERS ###
# Azure Provider
provider "azure" {
  publish_settings = "${file("secret.publishsettings")}"
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
  vm_size = "${var.vm_sizes.0}"

  # Get the shared resources necessary from the site module
  network_name = "${module.site.network_name}"
  storage_name = "${module.site.storage_name}"
  subnet_name = "${module.site.public_subnet_name}"

  # Use random password for bootstrapping/provisioning the server with Terraform
  ssh_password = "${uuid()}"
}

# Display the address of the master server
output "master_server_address" {
  value = "${module.master.hosted_service_url}"
}
