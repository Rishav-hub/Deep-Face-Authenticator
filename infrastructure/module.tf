terraform {
  backend "azurerm" {
    resource_group_name  = "faceapptfstate"
    storage_account_name = "faceapptfstate"
    container_name       = "tfstate"
    key                  = "prod.terraform.tfstate"
  }
}

provider "azurerm" {
  features {}
}

module "container_registry" {
  source = "./container_registry"
}

module "web_app" {
  source = "./web_app"
  depends_on = [
    module.container_registry
  ]
}


