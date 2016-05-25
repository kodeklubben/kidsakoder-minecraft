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

  # Ignore password field as Terraform detects is a change
  lifecycle {
    ignore_changes = ["password"]
  }

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

  # Enable endpoints/ports for Salt
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

  # SSH connection details for Terraform provisioner
  connection {
    user = "${var.ssh_username}"
    password = "${var.ssh_password}"
  }

  # Copy Saltstack directory containing config, states, pillars and etc.
  provisioner "file" {
    source = "${path.root}/../saltstack"
    destination = "/tmp/saltstack"
  }

  # Copy Salt bootstrap/provisioning script
  provisioner "file" {
    source = "${path.module}/bootstrap.sh"
    destination = "/tmp/bootstrap.sh"
  }

  provisioner "remote-exec" {
    inline = [
      "echo '${azure_instance.master.ip_address}' > /tmp/testip"
    ]
  }

  # Run the Salt bootstrap/provisioning script as sudo
  provisioner "remote-exec" {
    inline = [
      "chmod +x /tmp/bootstrap.sh",
      "cat /tmp/bootstrap.sh | sudo -E sh -s",
    ]
  }
}
