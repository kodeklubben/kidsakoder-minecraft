### SECRETS PULLED FROM THE FILE secret.tfvars ###
# SSH options for instance
variable "ssh_username" { description = "Username for SSH User" }
variable "ssh_user_password" { description = "Password for SSH User" }

# DNSimple authentication 
variable "dnsimple_email" { description = "DNSimple account email" }
variable "dnsimple_token" { description = "DNSimple account API token" }


### DOMAIN SETTINGS ###
# DNSimple domain
variable "dnsimple_domain" { 
    description = "DNSimple domain" 
    default = "kode-kidza.no"
}

variable "webserver_a_record" {
    description = "The A record that points to the webserver"
    default = "demo"
}
