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
# The location of the Azure infrastructure
variable "location" { default = "North Europe" }

# The name of the virtual machine image to be used
variable "image_name" { default = "Ubuntu Server 14.04 LTS" }

# The size of the virtual machine to be used
variable "vm_size" { default = "Basic_A0" }

# The name of the Azure storage service
variable "storage_name" { default = "kidsakoderstorage" }

# The name of the Azure virtual network
variable "network_name" { default = "network" }

# The name of public subnet in the virtual network
variable "public_subnet" { default = "public" }

# The name of private subnet in the virtual network
variable "private_subnet" { default = "private" }

# The name of public security group
variable "public_security_group" { default = "public" }

# The name of private security group 
variable "private_security_group" { default = "private" }


### DOMAIN SETTINGS ###
# The DNSimple domain to be managed
variable "dnsimple_domain" { default = "kode-kidza.no" }

## DNS A Records
variable "dns_webserver_demo" { default = "demo" }
variable "dns_webserver_internal" { default = "webserver" }
variable "dns_webserver_external" { default = "webserver-ext" }
variable "dns_master_internal" { default = "master" }
variable "dns_master_external" { default = "master-ext" }
