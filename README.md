# Job Scraper

This project collects new Job Listings from this [website](https://www.seek.co.nz/) and notify about them via slack.

## Table of Contents  
[Architecture](#architecture)  
[Deployment](#deployment)  
<a name="architecture"/>
## Architecture

![ArchitectureImage](images/architecture.jpg)

The Slack message:

![JobSamples](images/job-samples.jpg)

&nbsp;<a name="deployment"/>
## Deployment

This repository is split into two parts:
* The Scraper code: `job_scraper` folder.
* The CI/CD pipeline: responsible for deploying the scraper and pushing changes to the code, which lives inside `cicd_infrastructure`.

### Prerequisites:
You need the following to deploy the project:
* [Terraform](https://www.terraform.io/downloads.html)
* [AWS account](https://aws.amazon.com/premiumsupport/knowledge-center/create-and-activate-aws-account/) 
* [AWS Cli](https://docs.aws.amazon.com/cli/latest/userguide/install-cliv2.html)
* [AWS Profile](https://docs.aws.amazon.com/cli/latest/userguide/cli-chap-configure.html#cli-quick-configuration)
    This creates a profile with keys to access the AWS account
* [Slack Workspace](https://slack.com/create#email) 
* [Slack App](https://api.slack.com/apps?new_app=1)

### Steps:

1 - Slack

* [Create a slack channel to receive jobs notifications](https://slack.com/intl/en-nz/help/articles/201402297-Create-a-channel)
* [Create a slack webhook from your Slack App](https://api.slack.com/apps/AV4KE26U9/incoming-webhooks?)
    Save the generated webhook url somewhere as you will need to use it later

2 - AWS

* [Create bucket to store deployment artifacts](https://docs.aws.amazon.com/AmazonS3/latest/gsg/CreatingABucket.html)
* [Store slack webhook on secrets manager](https://docs.aws.amazon.com/secretsmanager/latest/userguide/tutorials_basic.html#tutorial-basic-step1)
    I create a "Other type of secrets" and put the name of the secret and the Secret key the same.
    E.g:
        Secret Name: mpenz-ws-slack-webhook
        Secret Key: mpenz-ws-slack-webhook
        Secret Value: https://hooks.slack.com/services/....


3 - Github

* [Clone the Repository](https://help.github.com/en/github/creating-cloning-and-archiving-repositories/cloning-a-repository)
* [Create personal Access Token](https://docs.aws.amazon.com/codepipeline/latest/userguide/GitHub-create-personal-token-CLI.html)
    This is needed to allow your AWS account to connect with your clone github repo.
    Follow from step 1 to 6.
    Make sure you save it somewhere safe but with quick access.

4 - Configure cloned repository

important: wherever it asks you to set the bucket use the one created on section (2 - AWS)

* Update terraform variables accordingly
    files: 
        cicd_infrastructure\terraform-backend.tfvars
        cicd_infrastructure\terraform-deployment.tfvars

        important: bucket and 

* Update serverless file
    file:
        serverless.yml

    variables:
        deploymentBucket: set the bucket name for serverless artifacts