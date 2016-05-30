# Variables set from main.tf
variable "location" {}
variable "prefix_name" {}
variable "storage_name" {}
variable "network_name" {}
variable "subnet_name" {}
variable "security_group_name" {}
variable "vm_image" {}
variable "vm_size" {}
variable "ssh_password" {}


# The username of the account used to provision with Terraform
variable "ssh_username" {
  description = "The username of the user account to be used for provisioning with Terraform."
  default = "salt-bootstrap"
}
