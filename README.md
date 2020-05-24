# Job Scraper

This project collects new Job Listings from this [website](https://www.seek.co.nz/) and notify via slack.

The [Architecture](#architecture) section explains how it works and the [Deployment](#deployment) section walks you through how to deploy this project to AWS.

<a name="architecture"/>
## Architecture

This repository is split into two parts:
* The Scraper code: `job_scraper` folder.
* The CI/CD pipeline: responsible for deploying the scraper and pushing changes to the code, which lives inside `cicd_infrastructure`.

![ArchitectureImage](images/architecture.jpeg)


&nbsp;<a name="deployment"/>
## Deployment

