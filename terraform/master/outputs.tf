output "internal_ip" {
  value = "${azure_instance.master.ip}"
}

output "external_ip" {
  value = "${azure_instance.master.vip}"
}

output "internal_dns" {
  value = "${dnsimple_record.internal.hostname}"
}

output "external_dns" {
  value = "${dnsimple_record.external.hostname}"
}
