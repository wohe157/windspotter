variable "table_name" {
  description = "The name of the DynamoDB table."
  type        = string
}

variable "hash_key_name" {
  description = "The name of the hash key of the DynamoDB table."
  type        = string
}

variable "hash_key_type" {
  description = "The type of the hash key of the DynamoDB table."
  type        = string
  default     = "S"
}

variable "global_secondary_indices" {
  description = "A list of global secondary indices for the DynamoDB table."
  type = list(object({
    name            = string
    hash_key_name   = string
    hash_key_type   = string
    projection_type = string
  }))
  default = []
}

variable "ttl_attibute_name" {
  description = "The name of the TTL attribute for the DynamoDB table (optional)."
  type        = string
  default     = ""
}

variable "tags" {
  description = "A map of tags to assign to the DynamoDB table."
  type        = map(string)
  default     = {}
}