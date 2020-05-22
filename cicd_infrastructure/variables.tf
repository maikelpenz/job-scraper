variable "aws_region" {
  description = "AWS region we are building on"
}

variable "aws_profile" {
  description = "AWS profile to connect to the AWS account"
}

variable "artifacts_bucket" {
  description = "AWS bucket to store terraform deployment artifacts"
}

variable "github_repository_owner" {
  description = "Owner of cloned repository"
}

variable "github_repository_name" {
  description = "Name of cloned repository"
}

variable "github_oauth_token" {
  description = "Github token to connect to source repository"
}
