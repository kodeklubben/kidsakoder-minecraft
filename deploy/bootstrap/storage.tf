resource "azure_storage_service" "storage" {
    name = "kidsakoderstor1"
    location = "North Europe"
    account_type = "Standard_LRS"
}
