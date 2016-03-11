### DNSimple provider
provider "dnsimple" {
    token = "${var.dnsimple_token}"
    email = "${var.dnsimple_email}"
}

### DNS
# Domain record for www
resource "dnsimple_record" "www_record" {
    domain = "${var.dnsimple_domain}"
    name = "${var.dns_www}"
    value = "${azure_instance.webserver.vip_address}"
    type = "A"
    ttl = 360

    depends_on = ["azure_instance.webserver"]
}

# Domain record for master
resource "dnsimple_record" "salt_master_record" {
    domain = "${var.dnsimple_domain}"
    name = "${var.dns_salt_master}"
    value = "${azure_instance.webserver.ip_address}"
    type = "A"
    ttl = 360

    depends_on = ["azure_instance.webserver"]
}
