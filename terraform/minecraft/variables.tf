# Variables set when using module
variable "location" {}
variable "storage_name" {}
variable "network_name" {}
variable "subnet_name" {}
variable "vm_image" {}
variable "ssh_username" {}
variable "ssh_password" {}
variable "domain" {}
variable "count" {}

variable "vm_sizes" {
  description = "The size of the virtual machines to be used"
  default = {
    "0" = "Basic_A0"
    "1" = "Basic_A1"
    "2" = "Standard_DS1_v2"
    "3" = "Standard_DS2_v2"
  }
}

variable "sizes" {
  description = "Helper variable for the different sizes of Minecraft servers"
  default = {
    "0" = "small"
    "1" = "medium"
    "2" = "large"
    "3" = "mega"
  }
}
