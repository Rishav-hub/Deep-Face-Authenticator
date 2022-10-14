resource "azurerm_service_plan" "faceapp_service_plan" {
  name                = var.webapp_service_plan_name
  resource_group_name = module.resource_group.faceapp_resource_group_name
  location            = module.resource_group.faceapp_resource_group_location
  os_type             = var.webapp_os_type
  sku_name            = var.webapp_sku_name
}
