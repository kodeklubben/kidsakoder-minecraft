### Hosted Service
resource "azure_hosted_service" "web_hosted_service" {
    name = "kidsakoder-hs-test"
    location = "North Europe"
    ephemeral_contents = false
    description = ""
    label = "kidsakoder-hs-test"
}

### Instance
resource "azure_instance" "webserver" {
    name = "kidsakoder-instance-webserver"
    image = "Ubuntu Server 14.04 LTS"
    size = "Basic_A1"
    location = "North Europe"

    hosted_service_name = "${azure_hosted_service.web_hosted_service.name}"
    storage_service_name = "${azure_storage_service.storage.name}"
    virtual_network = "${azure_virtual_network.azure_test_network.id}"

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

    # Copy saltstack dir with config, states and pillar
    provisioner "file" {
        source = "../saltstack"
        destination = "/tmp/saltstack"
    }

    # Copy provisioning script
    provisioner "file" {
        source = "provision.sh"
        destination = "/tmp/provision.sh"
    }

    # Run provisioning script as sudo
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
    value = "${azure_instance.webserver.vip_address}"
    type = "A"
    ttl = 360

    depends_on = ["azure_instance.webserver"]
}
