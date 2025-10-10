resource "aws_dynamodb_table" "users" {
  name         = "${var.app_name}-${terraform.workspace}-users"
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "user_id"

  attribute {
    name = "user_id"
    type = "S"
  }

  attribute {
    name = "email"
    type = "S"
  }

  global_secondary_index {
    name            = "${var.app_name}-${terraform.workspace}-users-by-email"
    hash_key        = "email"
    projection_type = "ALL"
  }
}
