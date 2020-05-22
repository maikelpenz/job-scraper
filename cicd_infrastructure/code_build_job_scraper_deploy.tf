# terraform import aws_iam_role.codebuild-job-scraper-deploy codebuild-job-scraper-deploy-service-role
resource "aws_iam_role" "codebuild-job-scraper-deploy" {
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
  name                  = "codebuild-job-scraper-deploy"
  path                  = "/service-role/"
}

# terraform import aws_iam_policy.codebuild-job-scraper-deploy arn:aws:iam::844814218183:policy/service-role/CodeBuildBasePolicy-job-scraper-deploy-us-east-1
resource "aws_iam_policy" "codebuild-job-scraper-deploy" {
  description = "Policy used in trust relationship with CodeBuild"
  name        = "codebuild-job-scraper-deploy"
  path        = "/service-role/"
  policy = jsonencode(
    {
      Statement = [
        {
          "Sid" : "VisualEditor0",
          "Effect" : "Allow",
          "Action" : [
            "codebuild:CreateReportGroup",
            "codebuild:CreateReport",
            "logs:CreateLogStream",
            "codebuild:UpdateReport",
            "logs:PutLogEvents",
            "codebuild:BatchPutTestCases"
          ],
          "Resource" : [
            "arn:aws:logs:us-east-1:844814218183:log-group:/aws/codebuild/job-scraper-deploy",
            "arn:aws:logs:us-east-1:844814218183:log-group:/aws/codebuild/job-scraper-deploy:*",
            "arn:aws:codebuild:us-east-1:844814218183:report-group/job-scraper-deploy-*"
          ]
        },
        {
          "Sid" : "VisualEditor1",
          "Effect" : "Allow",
          "Action" : [
            "iam:*",
            "s3:*",
            "logs:*",
            "lambda:*",
            "cloudformation:*",
            "events:*"
          ],
          "Resource" : "*"
        },
        {
          "Sid" : "VisualEditor2",
          "Effect" : "Allow",
          "Action" : "logs:CreateLogGroup",
          "Resource" : [
            "arn:aws:logs:us-east-1:844814218183:log-group:/aws/codebuild/job-scraper-deploy",
            "arn:aws:logs:us-east-1:844814218183:log-group:/aws/codebuild/job-scraper-deploy:*"
          ]
        }
      ]
      Version = "2012-10-17"
    }
  )
}

# terraform import aws_iam_role_policy_attachment.codebuild-job-scraper-deploy codebuild-job-scraper-deploy-service-role/arn:aws:iam::844814218183:policy/service-role/CodeBuildBasePolicy-job-scraper-build-us-east-1
resource "aws_iam_role_policy_attachment" "codebuild-job-scraper-deploy" {
  role       = aws_iam_role.codebuild-job-scraper-deploy.name
  policy_arn = aws_iam_policy.codebuild-job-scraper-deploy.arn
}

resource "aws_codebuild_project" "job-scraper-deploy" {
  name          = "job-scraper-deploy"
  description   = "Deploy phase"
  build_timeout = "60"
  service_role  = aws_iam_role.codebuild-job-scraper-deploy.arn

  artifacts {
    type = "CODEPIPELINE"
  }

  source {
    buildspec           = "buildspec-deploy.yml"
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

    environment_variable {
      name  = "env"
      type  = "PLAINTEXT"
      value = "stg"
    }
  }
}

