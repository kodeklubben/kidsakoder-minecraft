# Variables set when using module
variable "location" {}
variable "storage_name" {}
variable "network_name" {}
variable "subnet_name" {}
variable "vm_image" {}
variable "vm_size" {}
variable "ssh_username" {}
variable "ssh_password" {}
variable "domain" {}

# DNS Records
variable "dns_webserver_internal" {
  description = "DNS A record pointing to the internal IP of the webserver"
  default = "webserver"
}

variable "dns_webserver_external" {
  description = "DNS A record pointing to the external IP of the webserver"
  default = "webserver-ext"
}
