# The prefix of the storage service and hosted service for the master machine
# The value must only contain lowercase letters and digits
variable "prefix_name" {
  description = "The prefix of the services in the Azure infrastructure."
  default = "kidsakoder"
}


# The regions available in Azure
# See: https://azure.microsoft.com/en-us/regions/#services
variable "location" {
  description = "The location of the Azure infrastructure"
  default = "North Europe"
}


# The VM images available in Azure
# See: https://azure.microsoft.com/en-us/documentation/articles/virtual-machines-linux-cli-ps-findimage/
variable "vm_image" {
  description = "The name of the virtual machine image to be used"
  default = "Ubuntu Server 14.04 LTS"
}


# The definition of the different sizes of machines in Azure
# See: https://azure.microsoft.com/en-us/documentation/articles/virtual-machines-windows-sizes/
variable "vm_sizes" {
  description = "The size of the virtual machines to be used"
  default = {
    "0" = "Standard_DS1_v2"
    "1" = "Standard_DS2_v2"
    "2" = "Standard_DS3_v2"
  }
}
