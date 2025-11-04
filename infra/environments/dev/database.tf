module "revoked_refresh_tokens_table" {
  source = "../../modules/dynamodb_table"

  table_name    = "${var.app_name}-${var.environment}-revoked-refresh-tokens"
  hash_key_name = "token"

  tags = {
    app = var.app_name
    env = var.environment
  }
}

module "users_table" {
  source = "../../modules/dynamodb_table"

  table_name    = "${var.app_name}-${var.environment}-users"
  hash_key_name = "user_id"

  global_secondary_indices = [
    {
      name            = "${var.app_name}-${var.environment}-users-by-email"
      hash_key_name   = "email"
      hash_key_type   = "S"
      projection_type = "ALL"
    }
  ]

  ttl_attibute_name = "expires_at"

  tags = {
    app = var.app_name
    env = var.environment
  }
}
