terraform {
  backend "azurerm" {
    resource_group_name  = "<your_app_name>tfstate"
    storage_account_name = "<your_app_name>tfstate"
    container_name       = "tfstate"
    key                  = "prod.terraform.tfstate"
  }
}

provider "azurerm" {
  features {}
}

module "web_app" {
  source = "./web_app"
}
