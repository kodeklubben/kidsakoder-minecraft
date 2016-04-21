### Azure Provider
provider "azure" {
    publish_settings = "${file("secret.publishsettings")}"
}
