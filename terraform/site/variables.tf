### Variables set from main.tf
variable "prefix_name" {}
variable "location" {}


### Storage
# See: https://www.terraform.io/docs/providers/azure/r/storage_service.html
# NOTE: We add an prefix to this name in storage.tf
variable "storage_name" {
  description = "The name of the Azure storage service"
  default = "storage"
}

variable "storage_type" {
  description = "The type of storage service to be used"
  default = "Standard_GRS"
}


### Network
# See: https://www.terraform.io/docs/providers/azure/r/virtual_network.html
variable "network_name" {
  description = "The name of the Azure virtual network"
  default = "network"
}

variable "public_subnet_name" {
  description = "The name of public subnet in the virtual network"
  default = "public"
}

variable "private_subnet_name" {
  description = "The name of private subnet in the virtual network"
  default = "private"
}


### Security groups and rules
# See: https://www.terraform.io/docs/providers/azure/r/security_group.html
variable "public_security_group" {
  description = "The name of public security group"
  default = "public"
}

variable "private_security_group" {
  description = "The name of private security group"
  default = "private"
}
