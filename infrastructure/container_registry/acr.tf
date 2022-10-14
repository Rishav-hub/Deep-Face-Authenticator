module "resource_group" {
  source = "../resource_group"
}

resource "random_id" "random_string_for_acr" {
  byte_length = 8
}

resource "azurerm_container_registry" "faceappacr" {
  name                = "${random_id.random_string_for_acr.dec}${var.faceapp_acr_name}"
  resource_group_name = module.resource_group.faceapp_resource_group_name
  location            = module.resource_group.faceapp_resource_group_location
  admin_enabled       = var.faceapp_acr_admin_enabled
  sku                 = var.faceapp_acr_sku
}

output "faceappacr_login_server" {
  value = azurerm_container_registry.faceappacr.login_server
}

output "faceappacr_admin_username" {
  value = azurerm_container_registry.faceappacr.admin_username
}

output "faceappacr_admin_password" {
  value = azurerm_container_registry.faceappacr.admin_password
}

output "faceapp_resource_group_name" {
  value = module.resource_group.faceapp_resource_group_name
}

output "faceapp_resource_group_location" {
  value = module.resource_group.faceapp_resource_group_location
}