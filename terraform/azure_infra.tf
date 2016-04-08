### Cloud Provider
provider "azure" {
    publish_settings = "${file("secret.publishsettings")}"
}


### Storage Service
resource "azure_storage_service" "storage" {
    name = "${var.storage_name}"
    location = "${var.location}"
    account_type = "Standard_GRS"
}


### Virtual Network
resource "azure_virtual_network" "network" {
    name = "${var.network_name}"
    address_space = ["10.0.0.0/16"]
    location = "${var.location}"
    subnet {
        name = "${var.public_subnet}"
        address_prefix = "10.0.4.0/22"
        security_group = "${azure_security_group.public.name}"
    }
    subnet {
        name = "${var.private_subnet}"
        address_prefix = "10.0.0.0/22"
        security_group = "${azure_security_group.private.name}"
    }
}


### Security Groups
resource "azure_security_group" "public" {
    name = "${var.public_security_group}"
    location = "${var.location}"
}

resource "azure_security_group" "private" {
    name = "${var.private_security_group}"
    location = "${var.location}"
}


### Security Groups Rules
resource "azure_security_group_rule" "public_ssh_access" {
    name = "public-ssh-access-rule"
    security_group_names = ["${azure_security_group.public.name}"]
    type = "Inbound"
    action = "Allow"
    priority = 200
    source_address_prefix = "*"
    source_port_range = "*"
    destination_address_prefix = "10.0.4.0/22"
    destination_port_range = "22"
    protocol = "TCP"
}

resource "azure_security_group_rule" "private_ssh_access" {
    name = "private-ssh-access-rule"
    security_group_names = ["${azure_security_group.private.name}"]
    type = "Inbound"
    action = "Allow"
    priority = 200
    source_address_prefix = "10.0.4.0/22"
    source_port_range = "*"
    destination_address_prefix = "10.0.0.0/22"
    destination_port_range = "22"
    protocol = "TCP"
}
