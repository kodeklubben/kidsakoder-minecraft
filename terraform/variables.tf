### SECRETS PULLED FROM THE FILE secret.tfvars ###
###################### START ####################
variable "ssh" {
  description = "The SSH username and password user for provisioning"
  default = {
    username = ""
    password = ""
  }
}

variable "dnsimple" {
  description = "The email and token for accessing DNSimple"
  default = {
    email = ""
    token = ""
  }
}
###################### STOP #####################

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
    "0" = "Basic_A0"
    "1" = "Basic_A1"
    "2" = "Standard_DS1_v2"
    "3" = "Standard_DS2_v2"
  }
}


### DOMAIN SETTINGS ###
variable "domain" {
  description = "The domain to be managed in DNSimple"
  default = "kode-kidza.no"
}
