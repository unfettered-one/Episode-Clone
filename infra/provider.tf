terraform {
  backend "s3" {
  }
}


provider "aws" {
  region = var.region

  default_tags {
    tags = {
      ManagedBy   = "UnfetteredOne"
      Environment = var.stage
      Service     = "auth-service"
    }
  }
}
