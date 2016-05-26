output "hosted_service_url" {
  value = "${azure_hosted_service.master.url}"
}

output "internal_ip" {
  value = "${azure_instance.master.ip}"
}

output "external_ip" {
  value = "${azure_instance.master.vip}"
}
