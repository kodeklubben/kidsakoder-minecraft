### SECRETS PULLED FROM THE FILE secret.tfvars ###
################### DO NOT EDIT #################
# SSH options for instance
variable "ssh_username" { description = "Username for SSH User" }
variable "ssh_user_password" { description = "Password for SSH User" }

# DNSimple authentication 
variable "dnsimple_email" { description = "DNSimple account email" }
variable "dnsimple_token" { description = "DNSimple account API token" }

### AZURE VARIABLES ###
variable "env" {
    description = "The environment Terraform will build (appends prod or dev to names of services)"
    default = "dev"
}

variable "location" {
    description = "The location of the Azure infrastructure"
    default = "North Europe"
}

### DOMAIN SETTINGS ###
variable "dnsimple_domain" { 
    description = "The DNSimple domain to be managed" 
    default = "kode-kidza.no"
}

variable "dns_www" {
    description = "The A record that points to the webserver"
    default = "demo"
}

variable "dns_salt_master" {
    description = "The A record that points to the Salt master"
    default = "master"
}

