resource "azurerm_service_plan" "my_service_plan" {
  name                = "my-service-plan"
  resource_group_name = var.resource_group_name
  location            = var.resource_group_location
  os_type             = var.webapp_os_type
  sku_name            = var.webapp_sku_name
}



