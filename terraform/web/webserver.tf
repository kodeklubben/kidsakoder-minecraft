# Hosted service required in order to create virtual machine
resource "azure_hosted_service" "webserver" {
  name = "kidsakoder-hs-webserver"
  location = "${var.location}"
  ephemeral_contents = false
}

# Virtual machine instance for webserver
resource "azure_instance" "webserver" {
  # Hostname of instance
  name = "webserver"

  # VM image and size
  image = "${var.vm_image}"
  size = "${var.vm_size}"

  # Azure resources
  hosted_service_name = "${azure_hosted_service.webserver.name}"
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

  # Enable HTTP endpoint
  endpoint {
    name = "HTTP"
    protocol = "tcp"
    public_port = 80
    private_port = 80
  }

  # Connection details for Terraform provisioner
  connection {
    user = "${var.ssh_username}"
    password = "${var.ssh_password}"
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


# A record for internal IP of the webserver
resource "dnsimple_record" "internal" {
    domain = "${var.domain}"
    name = "${var.dns_webserver_internal}"
    value = "${azure_instance.webserver.ip_address}"
    type = "A"
    ttl = 360
}

# A record for external IP of the webserver
resource "dnsimple_record" "external" {
    domain = "${var.domain}"
    name = "${var.dns_webserver_external}"
    value = "${azure_instance.webserver.vip_address}"
    type = "A"
    ttl = 360
}
