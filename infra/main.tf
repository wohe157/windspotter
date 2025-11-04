module "dev" {
  source = "./environments/dev"

  app_name    = var.app_name
  environment = "dev"
}
