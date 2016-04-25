# Virtual machine instance for the webserver
resource "azure_instance" "mc" {
    count = "${var.count}"

    name = "mc-${lookup(var.sizes, count.index)}"
    image = "${var.image_name}"
    size = "${lookup(var.vm_sizes, count.index)}"
    location = "${var.location}"

    storage_service_name = "${azure_storage_service.storage.name}"
    virtual_network = "${azure_virtual_network.network.name}"
    subnet = "${var.public_subnet}"
    username = "${var.ssh.username}"
    password = "${var.ssh.password}"

    depends_on = ["azure_instance.master"]

    endpoint {
        name = "SSH"
        protocol = "tcp"
        public_port = 22
        private_port = 22
    }
    endpoint {
        name = "MINECRAFT"
        protocol = "tcp"
        public_port = 25565
        private_port = 25565
    }

    connection {
        user = "${var.ssh.username}"
        password = "${var.ssh.password}"
    }

    # Set which Minecraft mod and size should be used
    provisioner "remote-exec" {
        inline = [
          "sudo mkdir /etc/salt/",
          "sudo echo 'forge_version: 1.8.8' > /etc/salt/grains",
          "sudo echo 'mod: raspberryjam' >> /etc/salt/grains",
          "sudo echo 'raspberryjam_version: 0.52' >> /etc/salt/grains",
          "sudo echo 'size: ${lookup(var.sizes, count.index)}' >> /etc/salt/grains"
        ]
    }

    # Copy saltstack dir with config, states and pillar
    provisioner "file" {
        source = "../saltstack"
        destination = "/tmp/saltstack"
    }

    # Copy provisioning script
    provisioner "file" {
        source = "install_web_server.sh"
        destination = "/tmp/install_web_server.sh"
    }

    # Run provisioning script as sudo
    provisioner "remote-exec" {
        inline = [
          "chmod +x /tmp/install_web_server.sh",
          "cat /tmp/install_web_server.sh | sudo -E sh -s",
        ]
    }
}

# DNS for Minecraft servers
resource "dnsimple_record" "mc" {
    count = "${var.count}"
    domain = "${var.dnsimple_domain}"
    name = "${concat("mc0", count.index + 1)}"
    value = "${element(azure_instance.mc.*.vip_address, count.index)}"
    type = "A"
    ttl = 360

    depends_on = ["azure_instance.mc"]
}
