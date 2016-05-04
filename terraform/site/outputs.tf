output "storage_name" {
  value = "${azure_storage_service.default.name}"
}

output "storage_primary_key" {
  value = "${azure_storage_service.default.primary_key}"
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
