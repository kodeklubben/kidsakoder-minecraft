output "storage_name" {
  value = "${azure_storage_service.default.name}"
}

output "network_name" {
  value = "${azure_virtual_network.default.name}"
}

output "public_subnet_name" {
  value = "${var.public_subnet_name}"
}

output "private_subnet_name" {
  value = "${var.private_subnet_name}"
}

output "public_security_group_name" {
  value = "${azure_security_group.public.name}"
}
