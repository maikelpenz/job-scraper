data "aws_s3_bucket" "artifacts_bucket" {
  bucket = var.artifacts_bucket
}

# resource "aws_s3_bucket" "job-scraper-artifacts" {
#   arn           = "arn:aws:s3:::${var.artifacts_bucket}"
#   bucket        = var.artifacts_bucket
#   region        = var.aws_region
#   request_payer = "BucketOwner"

#   versioning {
#     enabled    = false
#     mfa_delete = false
#   }
# }
