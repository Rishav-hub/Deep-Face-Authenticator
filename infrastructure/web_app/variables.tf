variable "web_app_name" {
  default = "scaniadockerapp"
  type    = string
}

variable "resource_group_name" {
  default = "myRG"
  type    = string
}

variable "resource_group_location" {
  default = "eastus"
  type    = string
}

variable "web_app_settings_storage" {
  default = false
  type    = bool
}

variable "web_app_settings_port" {
  default = 8080
  type    = number
}

variable "web_app_start_time_limit" {
  default = 20
  type    = number
}

variable "container_registry_name" {
  default = "mywebappacr"
  type    = string
}

variable "container_registry_admin_enabled" {
  default = true
  type    = bool
}

variable "container_registry_sku" {
  default = "Standard"
  type    = string
}

variable "webapp_service_plan_name" {
  default = "my-service-plan"
  type    = string
}

variable "webapp_os_type" {
  default = "Linux"
  type    = string
}

variable "webapp_sku_name" {
  default = "P1v2"
  type    = string
}

variable "docker_image_name" {
  default = "faceapp"
  type    = string
}
