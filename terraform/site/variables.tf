### Variables set from main.tf
variable "prefix_name" {}
variable "location" {}


### Storage
variable "storage_name" {
  description = "The name of the Azure storage service. Must be unique on Azure so we add an prefix in storage.tf"
  default = "storage"
}

variable "storage_type" {
  description = "The type of storage service to be used"
  default = "Standard_GRS"
}


### Network
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
variable "public_security_group" {
  description = "The name of public security group"
  default = "public"
}

variable "private_security_group" {
  description = "The name of private security group"
  default = "private"
}
