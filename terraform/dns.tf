### DNSimple Provider
provider "dnsimple" {
    token = "${var.dnsimple.token}"
    email = "${var.dnsimple.email}"
}

### DNS Records
## Webserver
# Internal record for webserver
resource "dnsimple_record" "webserver_internal" {
    domain = "${var.dnsimple_domain}"
    name = "${var.dns_webserver_internal}"
    value = "${azure_instance.webserver.ip_address}"
    type = "A"
    ttl = 360
    depends_on = ["azure_instance.webserver"]
}

# External record for webserver
resource "dnsimple_record" "webserver_external" {
    domain = "${var.dnsimple_domain}"
    name = "${var.dns_webserver_external}"
    value = "${azure_instance.webserver.vip_address}"
    type = "A"
    ttl = 360
    depends_on = ["azure_instance.webserver"]
}

# Demo record for webserver
resource "dnsimple_record" "webserver_demo" {
    domain = "${var.dnsimple_domain}"
    name = "${var.dns_webserver_demo}"
    value = "${azure_instance.webserver.vip_address}"
    type = "A"
    ttl = 360
    depends_on = ["azure_instance.webserver"]
}

## Master server
# Internal record for master server
resource "dnsimple_record" "master_internal" {
    domain = "${var.dnsimple_domain}"
    name = "${var.dns_master_internal}"
    value = "${azure_instance.master.ip_address}"
    type = "A"
    ttl = 360
    depends_on = ["azure_instance.master"]
}

# External record for master server
resource "dnsimple_record" "master_external" {
    domain = "${var.dnsimple_domain}"
    name = "${var.dns_master_external}"
    value = "${azure_instance.master.vip_address}"
    type = "A"
    ttl = 360
    depends_on = ["azure_instance.master"]
}
