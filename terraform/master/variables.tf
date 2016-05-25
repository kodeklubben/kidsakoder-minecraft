# Variables set when using module
variable "location" {}
variable "storage_name" {}
variable "network_name" {}
variable "subnet_name" {}
variable "vm_image" {}
variable "vm_size" {}
variable "domain" {}
variable "ssh_password" {}

variable "ssh_username" {
  description = "The username of the user account to be used for provisioning with Terraform."
  default = "salt-bootstrap"
}
