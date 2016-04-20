### SECRETS PULLED FROM THE FILE secret.tfvars ###
###################### START ####################
## SSH username and password used by Terraform to provision 
variable "ssh_username" {}
variable "ssh_user_password" {}

# DNSimple authentication 
variable "dnsimple_email" {}
variable "dnsimple_token" {}
###################### STOP #####################

### AZURE VARIABLES ###
variable "location" { 
  description = "The location of the Azure infrastructure"
  default = "North Europe" 
}

variable "image_name" { 
  description = "The name of the virtual machine image to be used"
  default = "Ubuntu Server 14.04 LTS" 
}

variable "vm_size" { 
  description = "The size of the virtual machine to be used"
  default = "Basic_A0" 
}

variable "vm_sizes" {
  description = "The size of the virtual machines to be used"
  default = {
    "0" = "Basic_A0"
    "1" = "Basic_A1"
    "2" = "Standard_DS1_v2"
  }
}

variable "storage_name" { 
  description = "The name of the Azure storage service"
  default = "kidsakoderstorage"
}

variable "network_name" { 
  description = "The name of the Azure virtual network"
  default = "network"
}

variable "public_subnet" { 
  description = "The name of public subnet in the virtual network"
  default = "public"
}

variable "private_subnet" { 
  description = "The name of private subnet in the virtual network"
  default = "private" 
}

variable "public_security_group" { 
  description = "The name of public security group"
  default = "public" 
}

variable "private_security_group" { 
  description = "The name of private security group"
  default = "private" 
}

variable "count" { 
  description = "The amount of Minecraft servers to spin up"
  default = 3 
}

variable "sizes" {
  description = "Helper variable for the different sizes of Minecraft servers"
  default = {
    "0" = "small"
    "1" = "medium"
    "2" = "large"
  }
}


### DOMAIN SETTINGS ###
# The DNSimple domain to be managed
variable "dnsimple_domain" { default = "kode-kidza.no" }

## DNS A Records
variable "dns_webserver_demo" { default = "demo" }
variable "dns_webserver_internal" { default = "webserver" }
variable "dns_webserver_external" { default = "webserver-ext" }
variable "dns_master_internal" { default = "master" }
variable "dns_master_external" { default = "master-ext" }
