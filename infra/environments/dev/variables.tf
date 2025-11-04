variable "app_name" {
  description = "The name of the application."
  type        = string
}

variable "environment" {
  description = "The deployment environment."
  type        = string
  default     = "dev"
}
