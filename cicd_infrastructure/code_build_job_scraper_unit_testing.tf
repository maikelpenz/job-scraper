# terraform import aws_iam_role.codebuild-job-scraper-unit-testing codebuild-job-scraper-unit-testing-service-role
resource "aws_iam_role" "codebuild-job-scraper-unit-testing" {
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
  name                  = "codebuild-job-scraper-unit-testing"
  path                  = "/service-role/"
}

resource "aws_iam_policy" "codebuild-job-scraper-unit-testing" {
  description = "Policy used in trust relationship with CodeBuild"
  name        = "codebuild-job-scraper-unit-testing"
  path        = "/service-role/"
  policy = jsonencode(
    {
      Statement = [
        {
          "Effect" : "Allow",
          "Action" : [
            "s3:PutObject",
            "s3:GetObject",
            "codebuild:CreateReportGroup",
            "codebuild:CreateReport",
            "logs:CreateLogStream",
            "codebuild:UpdateReport",
            "s3:GetBucketAcl",
            "logs:PutLogEvents",
            "s3:GetBucketLocation",
            "codebuild:BatchPutTestCases",
            "s3:GetObjectVersion"
          ],
          "Resource" : [
            "*"
          ]
        },
        {
          "Sid" : "VisualEditor1",
          "Effect" : "Allow",
          "Action" : [
            "secretsmanager:GetRandomPassword",
            "secretsmanager:GetResourcePolicy",
            "secretsmanager:GetSecretValue",
            "secretsmanager:DescribeSecret",
            "secretsmanager:ListSecretVersionIds",
            "secretsmanager:ListSecrets"
          ],
          "Resource" : "*"
        },
        {
          "Sid" : "VisualEditor2",
          "Effect" : "Allow",
          "Action" : "logs:CreateLogGroup",
          "Resource" : [
            "*"
          ]
        }
      ]
      Version = "2012-10-17"
    }
  )
}

resource "aws_iam_role_policy_attachment" "codebuild-job-scraper-unit-testing" {
  role       = aws_iam_role.codebuild-job-scraper-unit-testing.name
  policy_arn = aws_iam_policy.codebuild-job-scraper-unit-testing.arn
}

resource "aws_codebuild_project" "job-scraper-unit-testing" {
  name          = "job-scraper-unit-testing"
  description   = "Unit testing phase"
  build_timeout = "60"
  service_role  = aws_iam_role.codebuild-job-scraper-unit-testing.arn

  artifacts {
    type = "CODEPIPELINE"
  }

  source {
    buildspec           = "buildspec-unittests.yml"
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

