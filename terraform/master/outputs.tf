output "internal_ip" {
  value = "${azure_instance.master.ip}"
}

output "external_ip" {
  value = "${azure_instance.master.vip}"
}
