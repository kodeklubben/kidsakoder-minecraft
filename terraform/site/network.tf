### Virtual Network
resource "azure_virtual_network" "default" {
  name = "${var.network_name}"
  location = "${var.location}"
  address_space = ["10.0.0.0/16"]

  subnet {
    name = "${var.public_subnet_name}"
    address_prefix = "10.0.4.0/22"
    security_group = "${azure_security_group.public.name}"
  }

  subnet {
    name = "${var.private_subnet_name}"
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

resource "azure_security_group_rule" "public_http_access" {
  name = "public-http-access-rule"
  security_group_names = ["${azure_security_group.public.name}"]
  type = "Inbound"
  action = "Allow"
  priority = 201
  source_address_prefix = "*"
  source_port_range = "*"
  destination_address_prefix = "10.0.4.0/22"
  destination_port_range = "80"
  protocol = "TCP"
}

resource "azure_security_group_rule" "public_minecraft_access" {
  name = "public-minecraft-access-rule"
  security_group_names = ["${azure_security_group.public.name}"]
  type = "Inbound"
  action = "Allow"
  priority = 202
  source_address_prefix = "*"
  source_port_range = "*"
  destination_address_prefix = "10.0.4.0/22"
  destination_port_range = "25565"
  protocol = "TCP"
}

resource "azure_security_group_rule" "private_ssh_access" {
  name = "private-ssh-access-rule"
  security_group_names = ["${azure_security_group.private.name}"]
  type = "Inbound"
  action = "Allow"
  priority = 203
  source_address_prefix = "10.0.4.0/22"
  source_port_range = "*"
  destination_address_prefix = "10.0.0.0/22"
  destination_port_range = "22"
  protocol = "TCP"
}
