# Job Scraper

This project collects new Job Listings from this [website](https://www.seek.co.nz/) and notify about them via slack.

## Table of Contents  
[Architecture](#architecture)  
[Deployment](#deployment)  
<a name="architecture"/>
## Architecture

![ArchitectureImage](images/architecture.jpg)

The output on Slack:

![JobSamples](images/job-samples.jpg)

&nbsp;<a name="deployment"/>
## Deployment

This repository is split into two parts:
* The Scraper code: `job_scraper` folder.
* The CI/CD pipeline: responsible for deploying the scraper and pushing changes to the code, which lives inside `cicd_infrastructure`.

