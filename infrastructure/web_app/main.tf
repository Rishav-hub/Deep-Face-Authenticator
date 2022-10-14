module "container_registry" {
  source = "../container_registry"
}

resource "azurerm_linux_web_app" "mydockerapp" {
  name                = var.web_app_name
  resource_group_name = var.resource_group_name
  location            = var.resource_group_location
  service_plan_id     = azurerm_service_plan.my_service_plan.id

  app_settings = {
    WEBSITES_ENABLE_APP_SERVICE_STORAGE = var.web_app_settings_storage
    WEBSITES_PORT                       = var.web_app_settings_port
    WEBSITES_CONTAINER_START_TIME_LIMIT = var.web_app_start_time_limit
    DOCKER_REGISTRY_SERVER_URL          = module.container_registry.my_acr_login_server
    DOCKER_REGISTRY_SERVER_USERNAME     = module.container_registry.my_acr_admin_username
    DOCKER_REGISTRY_SERVER_PASSWORD     = module.container_registry.my_acr_admin_password
  }

  site_config {
    application_stack {
      docker_image     = "${module.container_registry.my_acr_login_server}/${var.docker_image_name}"
    }
  }
}


