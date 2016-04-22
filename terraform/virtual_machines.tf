### Salt Master 
## Hosted Service for the master
resource "azure_hosted_service" "hs-master" {
    name = "kidsakoder-hs-master"
    location = "${var.location}"
    ephemeral_contents = false
}

## Virtual machine instance for the master
resource "azure_instance" "master" {
    name = "master"
    image = "${var.image_name}"
    size = "${var.vm_size}"
    location = "${var.location}"

    hosted_service_name = "${azure_hosted_service.hs-master.name}"
    storage_service_name = "${azure_storage_service.storage.name}"
    virtual_network = "${azure_virtual_network.network.name}"
    subnet = "${var.public_subnet}"
    username = "${var.ssh.username}"
    password = "${var.ssh.password}"

    endpoint {
        name = "SSH"
        protocol = "tcp"
        public_port = 22
        private_port = 22
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
        user = "${var.ssh.username}"
        password = "${var.ssh.password}"
    }

    # Copy saltstack dir with config, states and pillar
    provisioner "file" {
        source = "../saltstack"
        destination = "/tmp/saltstack"
    }

    # Copy provisioning script
    provisioner "file" {
        source = "install_salt_master.sh"
        destination = "/tmp/install_salt_master.sh"
    }

    # Run provisioning script as sudo
    provisioner "remote-exec" {
        inline = [
          "chmod +x /tmp/install_salt_master.sh",
          "cat /tmp/install_salt_master.sh | sudo -E sh -s",
        ]
    }
}


### Web Server 
## Hosted Service for the webserver
resource "azure_hosted_service" "hs-webserver" {
    name = "kidsakoder-hs-webserver"
    location = "${var.location}"
    ephemeral_contents = false
}

## Virtual machine instance for the webserver
resource "azure_instance" "webserver" {
    name = "webserver"
    image = "${var.image_name}"
    size = "${var.vm_size}"
    location = "${var.location}"

    hosted_service_name = "${azure_hosted_service.hs-webserver.name}"
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
        name = "HTTP"
        protocol = "tcp"
        public_port = 80
        private_port = 80
    }

    connection {
        user = "${var.ssh.username}"
        password = "${var.ssh.password}"
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

