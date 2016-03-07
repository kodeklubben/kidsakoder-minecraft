# Configure Azure provider
provider "azure" {
    publish_settings = "${file("secret.publishsettings")}"
}
