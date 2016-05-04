# Hosted service required in order to create virtual machine
resource "azure_hosted_service" "master" {
  name = "kidsakoder-hs-master"
  location = "${var.location}"
  ephemeral_contents = false
}


# Virtual machine instance for master server
resource "azure_instance" "master" {
  # Hostname of instance
  name = "master"

  # VM image and size
  image = "${var.vm_image}"
  size = "${var.vm_size}"

  # Azure resources
  hosted_service_name = "${azure_hosted_service.master.name}"
  storage_service_name = "${var.storage_name}"
  location = "${var.location}"
  virtual_network = "${var.network_name}"
  subnet = "${var.subnet_name}"

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

  # Enable endpoints for Salt
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
    source = "${path.module}/install_master.sh"
    destination = "/tmp/install_master.sh"
  }

  # Run provisioning script as sudo
  provisioner "remote-exec" {
    inline = [
      "chmod +x /tmp/install_master.sh",
      "cat /tmp/install_master.sh | sudo -E sh -s",
    ]
  }
}


# A record for internal IP of master server
resource "dnsimple_record" "internal" {
  domain = "${var.domain}"
  name = "${var.dns_master_internal}"
  value = "${azure_instance.master.ip_address}"
  type = "A"
  ttl = 360
}

# A record for external IP of master server
resource "dnsimple_record" "external" {
  domain = "${var.domain}"
  name = "${var.dns_master_external}"
  value = "${azure_instance.master.vip_address}"
  type = "A"
  ttl = 360
}
