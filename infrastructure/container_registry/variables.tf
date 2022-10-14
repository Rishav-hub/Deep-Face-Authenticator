variable "my_acr_name" {
  default = "scaniaACR"
  type    = string
}

variable "my_resource_group_name" {
  default = "myRG"
  type    = string
}

variable "my_resource_group_location" {
  default = "eastus"
  type    = string
}

variable "my_acr_sku" {
  default = "Standard"
  type    = string
}

variable "my_acr_admin_enabled" {
  default = true
  type    = bool
}
