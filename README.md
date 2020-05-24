# Job Scraper

This project collects new Job Listings from this [website](https://www.seek.co.nz/) and notify via slack.

## Table of Contents  
[Architecture](#architecture)  
[Deployment](#deployment)  
<a name="architecture"/>
## Architecture

This repository is split into two parts:
* The Scraper code: `job_scraper` folder.
* The CI/CD pipeline: responsible for deploying the scraper and pushing changes to the code, which lives inside `cicd_infrastructure`.

The [Deployment](#deployment) section below gives you information about how to deploy this project to AWS.

![ArchitectureImage](images/architecture.jpeg)


&nbsp;<a name="deployment"/>
## Deployment

