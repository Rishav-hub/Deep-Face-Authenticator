resource "random_id" "random_string_for_web_app_service_plan" {
  byte_length = 8
}

resource "azurerm_service_plan" "faceapp_service_plan" {
  name                = "${random_id.random_string_for_web_app_service_plan.dec}-${var.webapp_service_plan_name}"
  resource_group_name = module.container_registry.faceapp_resource_group_name
  location            = module.container_registry.faceapp_resource_group_location
  os_type             = var.webapp_os_type
  sku_name            = var.webapp_sku_name
}
