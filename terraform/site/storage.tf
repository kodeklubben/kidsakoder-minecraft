### Storage Service
resource "azure_storage_service" "default" {
  name = "${var.prefix_name}${var.storage_name}"
  location = "${var.location}"
  account_type = "${var.storage_type}"
}
