terraform {
  backend "azurerm" {
    resource_group_name  = "tfstate"
    storage_account_name = "tfstate28099"
    container_name       = "tfstate"
    key                  = "ws.tfstate"
  }
}
