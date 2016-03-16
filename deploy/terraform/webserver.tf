### Instance
resource "azure_instance" "webserver" {
    name = "webserver-${var.env}"
    image = "Ubuntu Server 14.04 LTS"
    size = "Basic_A0"
    location = "${var.location}"

    hosted_service_name = "${azure_hosted_service.hosted_service.name}"
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
    endpoint {
        name = "SALT1"
        protocol = "tcp"
        public_port = 4505
        private_port = 4505
    }
    endpoint {
        name = "SALT2"
        protocol = "tcp"
        public_port = 4506
        private_port = 4506
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
