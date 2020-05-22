provider "aws" {
  region  = var.aws_region
  profile = var.aws_profile
}

terraform {
  backend "s3" {
    key = "job-scraper/terraform.tfstate"
  }
}
