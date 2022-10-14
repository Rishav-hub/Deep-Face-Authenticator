variable "web_app_name" {
  default = "faceappsethu"
  type    = string
}

variable "web_app_settings_storage" {
  default = false
  type    = bool
}

variable "web_app_settings_port" {
  default = 8000
  type    = number
}

variable "web_app_start_time_limit" {
  default = 20
  type    = number
}

variable "webapp_service_plan_name" {
  default = "faceapp-service-plan"
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

variable "docker_image_tag" {
  default = "latest"
  type    = string
}
