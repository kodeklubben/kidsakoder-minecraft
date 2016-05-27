#################
### CHANGE ME ###
variable "prefix_name" {
  description = "The prefix of the services in the Azure infrastructure."
  default = "kidsakoder"
}
#################

### AZURE VARIABLES ###
variable "location" {
  description = "The location of the Azure infrastructure"
  default = "North Europe"
}

variable "vm_image" {
  description = "The name of the virtual machine image to be used"
  default = "Ubuntu Server 14.04 LTS"
}

variable "vm_sizes" {
  description = "The size of the virtual machines to be used"
  default = {
    "0" = "Standard_DS1_v2"
    "1" = "Standard_DS2_v2"
  }
}
