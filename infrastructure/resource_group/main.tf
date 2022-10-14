resource "azurerm_resource_group" "faceapp_resource_group" {
  name     = var.faceapp_resource_group_name
  location = var.faceapp_resource_group_location
}

output "faceapp_resource_group_name" {
  value = azurerm_resource_group.faceapp_resource_group.name
}

output "faceapp_resource_group_location" {
  value = azurerm_resource_group.faceapp_resource_group.location
}
