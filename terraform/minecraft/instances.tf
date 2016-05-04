# Virtual machine instance for the webserver
resource "azure_instance" "mc" {
    # The amount of instances to create
    count = "${var.count}"

    # Hostname of instance
    name = "mc-${lookup(var.sizes, count.index)}"

    # VM image and size
    image = "${var.vm_image}"
    size = "${lookup(var.vm_sizes, count.index)}"

    # Azure resources
    storage_service_name = "${var.storage_name}"
    virtual_network = "${var.network_name}"
    subnet = "${var.subnet_name}"
    location = "${var.location}"

    # Create account with the following credentials
    username = "${var.ssh_username}"
    password = "${var.ssh_password}"

    # Enable SSH endpoint
    endpoint {
        name = "SSH"
        protocol = "tcp"
        public_port = 22
        private_port = 22
    }

    # Enable Minecraft endpoint
    endpoint {
        name = "MINECRAFT"
        protocol = "tcp"
        public_port = 25565
        private_port = 25565
    }

    # Connection details for Terraform provisioner
    connection {
        user = "${var.ssh_username}"
        password = "${var.ssh_password}"
    }

    # Set Salt grains
    provisioner "remote-exec" {
        inline = [
          "echo 'forge_version: 1.8.8' > /tmp/grains",
          "echo 'mod: raspberryjam' >> /tmp/grains",
          "echo 'raspberryjam_version: 0.52' >> /tmp/grains",
          "echo 'size: ${lookup(var.sizes, count.index)}' >> /tmp/grains"
        ]
    }

    # Copy saltstack dir with config, states and pillar
    provisioner "file" {
        source = "${path.root}/../saltstack"
        destination = "/tmp/saltstack"
    }

    # Copy provisioning script
    provisioner "file" {
        source = "${path.module}/install_minion.sh"
        destination = "/tmp/install_minion.sh"
    }

    # Run provisioning script as sudo
    provisioner "remote-exec" {
        inline = [
          "chmod +x /tmp/install_minion.sh",
          "cat /tmp/install_minion.sh | sudo -E sh -s",
        ]
    }
}

# DNS for Minecraft servers
resource "dnsimple_record" "mc" {
    count = "${var.count}"
    domain = "${var.domain}"
    name = "${concat("mc0", count.index + 1)}"
    value = "${element(azure_instance.mc.*.vip_address, count.index)}"
    type = "A"
    ttl = 360

    depends_on = ["azure_instance.mc"]
}
