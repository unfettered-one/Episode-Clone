variable "stage" {
  default     = "development"
  description = "The environment stage (e.g., dev, prod)"
  type        = string
}
variable "region" {
  default     = "ap-south-1"
  description = "The AWS region to deploy resources in"
  type        = string
}

variable "service_name" {
  type    = string
  default = "episode"
}

variable "lock_table" {
  type        = string
  description = "name of the state lock dynamodb table"
}

variable "lock_bucket" {
  type        = string
  description = "name of the state lock s3 bucket"
}
variable "lambda_image_uri" {
  description = "Docker image URI for Lambda function"
  type        = string
  default     = ""
}

