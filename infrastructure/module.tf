terraform {
  backend "azurerm" {
    resource_group_name  = "mytfstate"
    storage_account_name = "scaniatfstate"
    container_name       = "tfstate"
    key                  = "prod.terraform.tfstate"
  }
}

provider "azurerm" {
  features {}
}

module "resource_group" {
  source = "./resource_group"
}

module "container_registry" {
  source = "./container_registry"
  depends_on = [
    module.resource_group
  ]
}

module "web_app" {
  source = "./web_app"
  depends_on = [
    module.resource_group
  ]
}