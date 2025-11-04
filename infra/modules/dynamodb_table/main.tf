resource "aws_dynamodb_table" "this" {
  name         = var.table_name
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = var.hash_key_name

  attribute {
    name = var.hash_key_name
    type = var.hash_key_type
  }

  dynamic "attribute" {
    for_each = var.global_secondary_indices
    content {
      name = attribute.value.hash_key_name
      type = attribute.value.hash_key_type
    }
  }

  dynamic "global_secondary_index" {
    for_each = var.global_secondary_indices
    content {
      name            = global_secondary_index.value.name
      hash_key        = global_secondary_index.value.hash_key_name
      projection_type = global_secondary_index.value.projection_type
    }
  }

  dynamic "ttl" {
    for_each = var.ttl_attibute_name != "" ? [1] : []
    content {
      attribute_name = var.ttl_attibute_name
      enabled        = true
    }
  }

  tags = var.tags
}
