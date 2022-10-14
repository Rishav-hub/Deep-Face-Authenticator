resource "random_id" "random_string_for_rg" {
  byte_length = 8
}

resource "azurerm_resource_group" "faceapp_resource_group" {
  name     = "${random_id.random_string_for_rg.dec}-${var.faceapp_resource_group_name}"
  location = var.faceapp_resource_group_location
}

output "faceapp_resource_group_name" {
  value = azurerm_resource_group.faceapp_resource_group.name
}

output "faceapp_resource_group_location" {
  value = azurerm_resource_group.faceapp_resource_group.location
}
