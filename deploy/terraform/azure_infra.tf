### Provider
provider "azure" {
    publish_settings = "${file("secret.publishsettings")}"
}

### Storage
resource "azure_storage_service" "storage" {
    name = "kidsakoderstor${var.env}"
    location = "${var.location}"
    account_type = "Standard_GRS"
}

### Hosted Service
resource "azure_hosted_service" "hosted_service" {
    name = "kidsakoder-hs-${var.env}"
    location = "${var.location}"
    ephemeral_contents = false
}

### Virtual Network
resource "azure_virtual_network" "network" {
    name = "kidsakoder-network-${var.env}"
    address_space = ["10.128.0.0/16"]
    location = "${var.location}"

    subnet {
        name = "private"
        address_prefix = "10.128.1.0/24"
    }
    subnet {
        name = "public"
        address_prefix = "10.128.2.0/24"
    }
}

### Security Groups
resource "azure_security_group" "public_ssh" {
    name = "public-ssh-${var.env}"
    location = "${var.location}"
}

resource "azure_security_group" "private_ssh" {
    name = "private-ssh-${var.env}"
    location = "${var.location}"
}

resource "azure_security_group_rule" "public_ssh_access" {
    name = "public-ssh-access-rule-${var.env}"
    security_group_names = ["${azure_security_group.public_ssh.name}"]
    type = "Inbound"
    action = "Allow"
    priority = 200
    source_address_prefix = "*"
    source_port_range = "*"
    destination_address_prefix = "10.128.2.0/24"
    destination_port_range = "22"
    protocol = "TCP"
}

resource "azure_security_group_rule" "private_ssh_access" {
    name = "private-ssh-access-rule-${var.env}"
    security_group_names = ["${azure_security_group.private_ssh.name}"]
    type = "Inbound"
    action = "Allow"
    priority = 200
    source_address_prefix = "10.128.2.0/24"
    source_port_range = "*"
    destination_address_prefix = "10.128.1.0/24"
    destination_port_range = "22"
    protocol = "TCP"

