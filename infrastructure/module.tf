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

module "web_app" {
  source = "./web_app"
}
