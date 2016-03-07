### Hosted Service
resource "azure_hosted_service" "web_hosted_service" {
    name = "kidsakoder-hs-test"
    location = "North Europe"
    ephemeral_contents = false
    description = ""
    label = "kidsakoder-hs-test"
}

### Instance
resource "azure_instance" "nat" {
    name = "${azure_virtual_network.network.id}-nat"
    image = "Ubuntu Server 14.04 LTS"
    size = "Basic_A1"
    location = "North Europe"

    hosted_service_name = "${azure_hosted_service.web_hosted_service.name}"
    storage_service_name = "${azure_storage_service.storage.name}"
    virtual_network = "${azure_virtual_network.network.id}"

    subnet = "public"
    username = "${var.ssh_username}"
    password = "${var.ssh_user_password}"
    security_group = "${azure_security_group.public_ssh.name}"

    endpoint {
        name = "SSH"
        protocol = "tcp"
        public_port = 22
        private_port = 22
    }
    endpoint {
        name = "HTTP"
        protocol = "tcp"
        public_port = 80
        private_port = 80
    }

    connection {
        user = "${var.ssh_username}"
        password = "${var.ssh_user_password}"
    }

    # Copy salt-master config
    provisioner "file" {
        source = "../saltstack/etc/minion.conf"
        destination = "/etc/salt/minion"
    }

    # Copy salt-master pillars
    provisioner "file" {
        source = "../saltstack/pillar"
        destination = "/srv/pillar"
    }

    # Copy salt-master states
    provisioner "file" {
        source = "../saltstack/salt"
        destination = "/srv/salt"
    }

    provisioner "file" {
        source = "provision.sh"
        destination = "/tmp/provision.sh"
    }

    provisioner "remote-exec" {
        inline = [
          "chmod +x /tmp/provision.sh",
          "cat /tmp/provision.sh | sudo -E sh -s",
        ]
    }
}

### DNS
resource "dnsimple_record" "webserver_a_record" {
    domain = "${var.dnsimple_domain}"
    name = "${var.webserver_a_record}"
    value = "${azure_instance.nat.vip_address}"
    type = "A"
    ttl = 360
}
