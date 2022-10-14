resource "azurerm_container_registry" "my_acr" {
  name                = var.my_acr_name
  resource_group_name = var.my_resource_group_name
  location            = var.my_resource_group_location
  admin_enabled       = var.my_acr_admin_enabled
  sku                 = var.my_acr_sku
}

output "my_acr_login_server" {
  value = azurerm_container_registry.my_acr.login_server
}

output "my_acr_admin_username" {
  value = azurerm_container_registry.my_acr.admin_username
}

output "my_acr_admin_password" {
  value = azurerm_container_registry.my_acr.admin_password
}