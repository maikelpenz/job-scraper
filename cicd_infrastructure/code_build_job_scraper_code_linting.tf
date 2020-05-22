# terraform import aws_iam_role.codebuild-job-scraper-code-linting codebuild-job-scraper-code-linting-service-role
resource "aws_iam_role" "codebuild-job-scraper-code-linting" {
  assume_role_policy = jsonencode(
    {
      Statement = [
        {
          Action = "sts:AssumeRole"
          Effect = "Allow"
          Principal = {
            Service = "codebuild.amazonaws.com"
          }
        },
      ]
      Version = "2012-10-17"
    }
  )
  force_detach_policies = false
  max_session_duration  = 3600
  name                  = "codebuild-job-scraper-code-linting"
  path                  = "/service-role/"
}

# terraform import aws_iam_policy.codebuild-job-scraper-code-linting arn:aws:iam::844814218183:policy/service-role/CodeBuildBasePolicy-job-scraper- build-us-east-1
resource "aws_iam_policy" "codebuild-job-scraper-code-linting" {
  description = "Policy used in trust relationship with CodeBuild"
  name        = "codebuild-job-scraper-code-linting"
  path        = "/service-role/"
  policy = jsonencode(
    {
      Statement = [
        {
          "Effect" : "Allow",
          "Resource" : [
            "arn:aws:logs:us-east-1:844814218183:log-group:/aws/codebuild/job-scraper-code-linting",
            "arn:aws:logs:us-east-1:844814218183:log-group:/aws/codebuild/job-scraper-code-linting:*"
          ],
          "Action" : [
            "logs:CreateLogGroup",
            "logs:CreateLogStream",
            "logs:PutLogEvents"
          ]
        },
        {
          "Effect" : "Allow",
          "Resource" : [
            "arn:aws:s3:::codepipeline-us-east-1-*",
            "arn:aws:s3:::job-scraper-artifacts*"
          ],
          "Action" : [
            "s3:PutObject",
            "s3:GetObject",
            "s3:GetObjectVersion",
            "s3:GetBucketAcl",
            "s3:GetBucketLocation"
          ]
        },
        {
          "Effect" : "Allow",
          "Action" : [
            "codebuild:CreateReportGroup",
            "codebuild:CreateReport",
            "codebuild:UpdateReport",
            "codebuild:BatchPutTestCases"
          ],
          "Resource" : [
            "arn:aws:codebuild:us-east-1:844814218183:report-group/job-scraper-code-linting-*"
          ]
        }
      ]
      Version = "2012-10-17"
    }
  )
}

# terraform import aws_iam_role_policy_attachment.codebuild-job-scraper-code-linting codebuild-job-scraper-code-linting-service-role/arn:aws:iam::844814218183:policy/service-role/CodeBuildBasePolicy-job-scraper-build-us-east-1
resource "aws_iam_role_policy_attachment" "codebuild-job-scraper-code-linting" {
  role       = aws_iam_role.codebuild-job-scraper-code-linting.name
  policy_arn = aws_iam_policy.codebuild-job-scraper-code-linting.arn
}

resource "aws_codebuild_project" "job-scraper-code-linting" {
  name          = "job-scraper-code-linting"
  description   = "Code Linting phase"
  build_timeout = "60"
  service_role  = aws_iam_role.codebuild-job-scraper-code-linting.arn

  artifacts {
    type = "CODEPIPELINE"
  }

  source {
    buildspec           = "buildspec-linting.yml"
    git_clone_depth     = 0
    insecure_ssl        = false
    report_build_status = false
    type                = "CODEPIPELINE"
  }

  environment {
    compute_type                = "BUILD_GENERAL1_SMALL"
    image                       = "aws/codebuild/standard:4.0"
    image_pull_credentials_type = "CODEBUILD"
    privileged_mode             = false
    type                        = "LINUX_CONTAINER"
  }
}

